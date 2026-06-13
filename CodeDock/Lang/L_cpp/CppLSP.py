import os
import json
import subprocess
import pathlib
import time
import uuid
from pylsp_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter
from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool, QMutex, QMutexLocker


def pathToURL(path) -> str:
    return pathlib.Path(path).resolve().as_uri()

class ClangdCompletionWorker(QRunnable):
    """Worker to send LSP requests safely using a mutex for C++ completion."""
    def __init__(self, clangd:"ClangdLsp", file_path, line, char_pos, signal, ver):
        super().__init__() 
        self.clangd = clangd  # Store the ClangdLsp instance
        self.line = line
        self.char_pos = char_pos
        self.signal = signal  # Use signal instead of callback
        self.ver = ver
        try:
            self.file_path = pathToURL(file_path)
        except:
            self.file_path = file_path

    def run(self):
        """Runs in a thread pool worker and sends the request safely."""
        params = {
            "textDocument": {
                "uri": f"{self.file_path}"
            },
            "position": {
                "line": self.line,
                "character": self.char_pos
            },
            "context": {
                "triggerKind": 1,
            }

        }

        self.clangd.req_version+=1  
        request_id = self.ver
        if self.clangd.send_lsp_request("textDocument/completion", params, request_id):
            response = self.clangd.read_lsp_response(request_id)
            if response and 'result' in response:
                suggestions = []
                items = response.get("result", {})
                
                # Handle both dict with 'items' key and direct list
                if isinstance(items, dict) and 'items' in items:
                    items = items['items']
                elif items is None:
                    items = []
                    
                """for item in items:
                    suggestions.append((item.get("label"), item.get("kind")))       
                """
                self.signal.emit(items,"cpp")


class ClangdLsp(QObject):
    completions_ready = pyqtSignal(list,str)
    hover_ready = pyqtSignal(object)
    definition_ready = pyqtSignal(object)
    references_ready = pyqtSignal(object, tuple)
    signature_help_ready = pyqtSignal(object)
    formatting_ready = pyqtSignal(object)
    code_action_ready = pyqtSignal(object)
    document_symbols_ready = pyqtSignal(object)
    workspace_symbols_ready = pyqtSignal(object)
    diagnostics_ready = pyqtSignal(object)

    def __init__(self, workspace_path=None):
        super().__init__()
        self.pause = False

        if workspace_path:
            self.workspace_path = workspace_path or os.getcwd()
            self.workspace_path = f"file://{self.workspace_path}"
        else:
            self.workspace_path = None

        self.req_version=1
        
        self.lsp_name='clangd'
        # Start clangd process
        try:
            self.process = subprocess.Popen(
                [self.lsp_name, '--log=error'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,  # Keep as binary for JsonRpcStreamWriter
                bufsize=0
            )
            
            print("Clangd process started")

            # Initialize JSON-RPC streams
            self.writer = JsonRpcStreamWriter(self.process.stdin)
            # Note: We'll handle reading manually since JsonRpcStreamReader 
            # is designed for async/callback patterns

        except Exception as e:
            print(f"Failed to start clangd: {e}")
            self.process = None
            self.writer = None

        self.mutex = QMutex()
        self.thread_pool = QThreadPool.globalInstance()
        self.pending_requests = {}  # Track pending requests by ID
        
        if self.process:
            self.initialize_clangd()

    def send_lsp_request(self, method, params, request_id=1):
        """Send LSP request to clangd using JsonRpcStreamWriter"""
        with QMutexLocker(self.mutex):
            if not self.writer:
                return False
                
            request = {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params
            }
            
            try:
                self.writer.write(request)
                self.pending_requests[request_id] = time.time()
                return True
            except Exception as e:
                print(f"Error sending request: {e}")
                return False
        
    def read_lsp_message(self):
        """Read a single LSP message from clangd manually"""
        if not self.process:
            return None
            
        try:
            # Read headers line by line
            headers = {}
            while True:
                line = self.process.stdout.readline().decode('utf-8')
                if not line:
                    return None
                line = line.strip()
                if not line:  # Empty line indicates end of headers
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
            
            # Read content
            content_length = int(headers.get('Content-Length', 0))
            if content_length > 0:
                content = self.process.stdout.read(content_length).decode('utf-8')
                return json.loads(content)
                
        except Exception as e:
            print(f"Error reading message: {e}")
            
        return None
    
    def read_lsp_response(self, request_id, timeout=5):
        """Read LSP response for a specific request ID"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                message = self.read_lsp_message()
                if not message:
                    time.sleep(0.01)  # Small delay to prevent busy waiting
                    continue

                # Handle response messages (have 'id')
                if 'id' in message:
                    msg_id = message['id']
                    if msg_id == request_id:
                        # Clean up pending request
                        self.pending_requests.pop(request_id, None)
                        return message
                    else:
                        # This is a response for a different request
                        print(f"Received response for different request ID: {msg_id}")

                # Handle notification messages (have 'method' but no 'id')
                elif 'method' in message:
                    method = message['method']
                    if method == 'textDocument/publishDiagnostics':
                        print("diagno.. : ",message)
                        self.diagnostics_ready.emit(message)
                    else:
                        print(f"Received notification: {method}")
                        
            except Exception as e:
                print(f"Error in read_lsp_response: {e}")
                break
                
        # Clean up expired request
        self.pending_requests.pop(request_id, None)
        return None
        
    def initialize_clangd(self):
        """Initialize clangd with LSP initialize request"""
        init_params = {
            "processId": os.getpid(),
            "clientInfo": {"name": "clangd-tester", "version": "1.0"},
            "rootUri": self.workspace_path,
            "capabilities": {
                "textDocument": {
                    "completion": {
                        "completionItem": {
                            "snippetSupport": True,
                            "commitCharactersSupport": True,
                            "documentationFormat": ["markdown", "plaintext"]
                        },
                        "contextSupport": True
                    },

                    "documentSymbol": {
                        "hierarchicalDocumentSymbolSupport": True
                    },
                    "hover": {
                        "contentFormat": ["markdown", "plaintext"]
                    },
                    "definition": {
                        "linkSupport": True
                    },
                    "references": {},
                    "signatureHelp": {
                        "signatureInformation": {
                            "documentationFormat": ["markdown", "plaintext"]
                        }
                    },
                    "formatting": {},
                    "codeAction": {},
                    
                },
                "workspace": {
                    "workspaceFolders": True,
                    "symbol": {}
                }
            }
        }
        
        print("Initializing clangd...")
        if self.send_lsp_request("initialize", init_params, 1):
            response = self.read_lsp_response(1)
            if response and 'result' in response:
                print("Clangd initialized successfully")
                # Send initialized notification (no id for notifications)
                self.send_notification("initialized", {})
                return True
            else:
                print(f"Failed to initialize clangd: {response}")
                return False
        return False
        
    def send_notification(self, method, params):
        """Send LSP notification to clangd (no response expected)"""
        with QMutexLocker(self.mutex):
            if not self.writer:
                return False
                
            notification = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params
            }
            
            try:
                self.writer.write(notification)
                return True
            except Exception as e:
                print(f"Error sending notification: {e}")
                return False

    def did_open(self, file_path, content):
        """Open the document in clangd"""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path),
                "languageId": self._get_language_id(file_path),
                "version": self.req_version,
                "text": content
            }
        }
        
        self.req_version+=1

        print("Opening document in clangd...")
        return self.send_notification("textDocument/didOpen", params)
    
    
    def did_change_full(self,file_path):
        with open(file_path,"r")as f:
            dt=f.read()
        print(file_path)
        params = {
            "textDocument": {
                "uri": pathToURL(file_path),
                "version": self.req_version
            },
            "contentChanges": [{"text": dt}]
        }
        self.req_version+=1
        return self.send_notification("textDocument/didChange", params)

    def did_change(self, file_path, start_line, start_char, end_line, end_char, new_text):
        self.did_change_full(file_path)
        """params = {
            "textDocument": {
                "uri": pathToURL(file_path),
                "version": self.req_version
            },
            "contentChanges": [{
                "range": {
                    "start": {"line": start_line, "character": start_char},
                    "end": {"line": end_line, "character": end_char}
                },
                "text": new_text
            }]
        }
        self.req_version+=1
        
        return self.send_notification("textDocument/didChange", params)
"""
        
    def did_save(self, file_path):
        """Notify clangd that a document was saved."""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path)
            }
        }
        
        return self.send_notification("textDocument/didSave", params)

    def did_close(self, file_path):
        """Notify clangd that a document was closed."""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path)
            }
        }
        return self.send_notification("textDocument/didClose", params)

    def _get_language_id(self, file_path):
        """Determine language ID based on file extension."""
        ext = pathlib.Path(file_path).suffix.lower()
        if ext in ['.cpp', '.cxx', '.cc', '.c++']:
            return 'cpp'
        elif ext in ['.c']:
            return 'c'
        elif ext in ['.h', '.hpp', '.hxx', '.h++']:
            return 'cpp'  # Treat headers as C++ by default
        else:
            return 'cpp'

    def stop(self):
        """Shut down clangd properly."""
        try:
            # Send shutdown request
            if self.send_lsp_request("shutdown", {}, 999):
                self.read_lsp_response(999, timeout=2)
            
            # Send exit notification
            self.send_notification("exit", {})
            
            # Close streams
            if self.writer:
                try:
                    self.writer.close()
                except:
                    pass
                
            # Terminate process
            if self.process:
                self.process.terminate()
                
        except Exception as e:
            print(f"Error during shutdown: {e}")
            if self.process:
                self.process.kill()

    def send_request(self, request):
        """Compatibility method for generic LSP requests"""
        return self.send_lsp_request(
            request["method"], 
            request["params"], 
            request["id"]
        )

    def request_completions(self, file_path, line, column):
        """Run a completion request in a worker threadpool."""
        if not self.pause:
            worker = ClangdCompletionWorker(self, file_path, line, column, self.completions_ready, self.req_version)
            self.thread_pool.start(worker)

    def request_hover(self, file_path, line, column):
        """Request hover information"""
        self._start_worker("textDocument/hover", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column}
        }, self.hover_ready)

    def request_definition(self, file_path, line, column):
        """Request go to definition"""
        self._start_worker("textDocument/definition", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column}
        }, self.definition_ready)

    def request_references(self, word, file_path, line, column):
        """Request find references"""
        self._start_worker("textDocument/references", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column},
            "context": {"includeDeclaration": True}
        }, self.references_ready, word)

    def request_signature_help(self, file_path, line, column):
        """Request signature help"""
        self._start_worker("textDocument/signatureHelp", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column}
        }, self.signature_help_ready)

    def request_formatting(self, file_path):
        """Request document formatting"""
        self._start_worker("textDocument/formatting", {
            "textDocument": {"uri": pathToURL(file_path)},
            "options": {"tabSize": 4, "insertSpaces": True}
        }, self.formatting_ready)

    def request_code_action(self, file_path, line, column):
        """Request code actions"""
        self._start_worker("textDocument/codeAction", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": line, "character": column},
                "end": {"line": line, "character": column + 1}
            },
            "context": {"diagnostics": []}
        }, self.code_action_ready)

    def request_document_symbols(self, file_path):
        #print("Document symbols request sent")
        self._start_worker(
            "textDocument/documentSymbol",
            {"textDocument": {"uri": pathToURL(file_path)}},
            self.document_symbols_ready
        )

    def request_workspace_symbols(self, query):
        """Request workspace symbols"""
        self._start_worker("workspace/symbol", {"query": query}, self.workspace_symbols_ready)

    def _start_worker(self, method, params, signal, *other):
        """Start a worker thread for LSP request"""
        self.thread_pool.start(ClangdLspWorker(self, method, params, signal, *other))


class ClangdLspWorker(QRunnable):
    def __init__(self, clangd, method, params, signal, *other):
        super().__init__()
        self.clangd = clangd
        self.method = method
        self.params = params
        self.signal = signal
        self.other = other

    def run(self):
        request_id = id(self)
        if self.clangd.send_lsp_request(self.method, self.params, request_id):
            result = self.clangd.read_lsp_response(request_id)
            """
            if self.other:
                self
                
                .signal.emit(result, self.other)
            else:"""


            print(result,"\n\n\n\n\nn\n\n\n\n\n\n\n\n\n\n\n\n\n")
            self.signal.emit(result)


# Example usage and utility functions
def create_compile_commands(project_path, cpp_files=None, compiler="clang++", flags=None):
    """
    Create compile_commands.json for better clangd analysis
    
    Args:
        project_path: Path to the project root
        cpp_files: List of cpp files (if None, finds all .cpp/.cc files)
        compiler: Compiler to use (default: clang++)
        flags: Additional compiler flags
    """
    if flags is None:
        flags = ["-std=c++17"]
    
    if cpp_files is None:
        project_path = pathlib.Path(project_path)
        cpp_files = list(project_path.rglob("*.cpp")) + list(project_path.rglob("*.cc"))
    
    compile_commands = []
    for cpp_file in cpp_files:
        compile_commands.append({
            "directory": str(project_path),
            "command": f"{compiler} {' '.join(flags)} {cpp_file}",
            "file": str(cpp_file)
        })
    
    compile_commands_file = pathlib.Path(project_path) / "compile_commands.json"
    with open(compile_commands_file, 'w') as f:
        json.dump(compile_commands, f, indent=2)
    
    return compile_commands_file