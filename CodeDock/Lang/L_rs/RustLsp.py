import os
import json
import subprocess
import pathlib
import time
import uuid
from pylsp_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter
from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool, QMutex, QMutexLocker
from CodeDock.Debuger import Debug


def pathToURL(path) -> str:
    return pathlib.Path(path).resolve().as_uri()

class RustAnalyzerCompletionWorker(QRunnable):
    """Worker to send LSP requests safely using a mutex for Rust completion."""
    def __init__(self, rust_analyzer:"RustAnalyzerLsp", file_path, line, char_pos, signal, ver):
        super().__init__() 
        self.rust_analyzer = rust_analyzer  # Store the RustAnalyzerLsp instance
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
        Debug.success(self.file_path)

        self.rust_analyzer.req_version += 1  
        request_id = self.ver
        if self.rust_analyzer.send_lsp_request("textDocument/completion", params, request_id):
            response = self.rust_analyzer.read_lsp_response(request_id)
            if response and 'result' in response:
                suggestions = []
                items = response.get("result", {})
                
                # Handle both dict with 'items' key and direct list
                if isinstance(items, dict) and 'items' in items:
                    items = items['items']
                elif items is None:
                    items = []
                    
                self.signal.emit(items,"rs")


class RustAnalyzerLsp(QObject):
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
    inlay_hints_ready = pyqtSignal(object)
    runnables_ready = pyqtSignal(object)

    def __init__(self, workspace_path=None):
        super().__init__()
        self.pause = False
        
        if workspace_path:
            self.workspace_path = workspace_path or os.getcwd()
            self.workspace_path = f"file://{self.workspace_path}"
        else:
            self.workspace_path = None
        Debug.yellow(workspace_path)
        self.req_version = 1
        
        # Start rust-analyzer process
        try:
            self.process = subprocess.Popen(
                ['rust-analyzer'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,  # Keep as binary for JsonRpcStreamWriter
                bufsize=0
            )
            print("rust-analyzer process started")

            # Initialize JSON-RPC streams
            self.writer = JsonRpcStreamWriter(self.process.stdin)

        except Exception as e:
            print(f"Failed to start rust-analyzer: {e}")
            self.process = None
            self.writer = None

        self.mutex = QMutex()
        self.thread_pool = QThreadPool.globalInstance()
        self.pending_requests = {}  # Track pending requests by ID
        
        if self.process:
            self.initialize_rust_analyzer()

    def send_lsp_request(self, method, params, request_id=1):
        """Send LSP request to rust-analyzer using JsonRpcStreamWriter"""
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
        """Read a single LSP message from rust-analyzer manually"""
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
                        self.diagnostics_ready.emit(message)
                    elif method == 'rust-analyzer/inlayHints':
                        self.inlay_hints_ready.emit(message)
                    else:
                        print(f"Received notification: {method}")
                        
            except Exception as e:
                print(f"Error in read_lsp_response: {e}")
                break
                
        # Clean up expired request
        self.pending_requests.pop(request_id, None)
        return None
    
    def initialize_rust_analyzer(self):
        """Initialize rust-analyzer with LSP initialize request"""
        init_params = {
            "processId": os.getpid(),
            "clientInfo": {"name": "rust-analyzer-tester", "version": "1.0"},
            "rootUri": self.workspace_path,
            "capabilities": {
                "textDocument": {
                    "completion": {
                        "completionItem": {
                            "snippetSupport": True,
                            "commitCharactersSupport": True,
                            "documentationFormat": ["markdown", "plaintext"],
                            "resolveSupport": {
                                "properties": ["documentation", "detail", "additionalTextEdits"]
                            }
                        },
                        "contextSupport": True
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
                            "documentationFormat": ["markdown", "plaintext"],
                            "parameterInformation": {
                                "labelOffsetSupport": True
                            }
                        }
                    },
                    "formatting": {},
                    "rangeFormatting": {},
                    "codeAction": {
                        "codeActionLiteralSupport": {
                            "codeActionKind": {
                                "valueSet": [
                                    "quickfix",
                                    "refactor",
                                    "refactor.extract",
                                    "refactor.inline",
                                    "refactor.rewrite"
                                ]
                            }
                        }
                    },
                    "documentSymbol": {
                        "hierarchicalDocumentSymbolSupport": True
                    },
                    "inlayHint": {
                        "dynamicRegistration": True
                    }
                },
                "workspace": {
                    "workspaceFolders": True,
                    "symbol": {},
                    "configuration": True,
                    "didChangeConfiguration": {
                        "dynamicRegistration": True
                    }
                },
                "experimental": {
                    "hoverActions": True,
                    "commands": {
                        "commands": [
                            "rust-analyzer.runSingle",
                            "rust-analyzer.debug",
                            "rust-analyzer.gotoLocation"
                        ]
                    }
                }
            },
            "initializationOptions": {
                "cargo": {
                    "buildScripts": {
                        "enable": True
                    }
                },
                "procMacro": {
                    "enable": True
                },
                "diagnostics": {
                    "enable": True
                },
                "inlayHints": {
                    "typeHints": {
                        "enable": True
                    },
                    "parameterHints": {
                        "enable": True
                    },
                    "chainingHints": {
                        "enable": True
                    }
                }
            }
        }
        
        print("Initializing rust-analyzer...")
        if self.send_lsp_request("initialize", init_params, 1):
            response = self.read_lsp_response(1)
            if response and 'result' in response:
                print("rust-analyzer initialized successfully")
                # Send initialized notification (no id for notifications)
                self.send_notification("initialized", {})
                return True
            else:
                print(f"Failed to initialize rust-analyzer: {response}")
                return False
        return False
        
    def send_notification(self, method, params):
        """Send LSP notification to rust-analyzer (no response expected)"""
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
        Debug.blue(pathToURL(file_path))
        """Open the document in rust-analyzer"""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path),
                "languageId": self._get_language_id(file_path),
                "version": self.req_version,
                "text": content
            }
        }
        
        self.req_version += 1

        print("Opening document in rust-analyzer...")
        return self.send_notification("textDocument/didOpen", params)
    
    def did_change_full(self, file_path):
        """Update the entire document content"""
        with open(file_path, "r") as f:
            dt = f.read()

        params = {
            "textDocument": {
                "uri": pathToURL(file_path),
                "version": self.req_version
            },
            "contentChanges": [{"text": dt}]
        }
        self.req_version += 1
        return self.send_notification("textDocument/didChange", params)

    def did_change(self, file_path, start_line, start_char, end_line, end_char, new_text):
        """Send incremental document changes to rust-analyzer"""
        """        params = {
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
        self.req_version += 1"""
    
        #return self.send_notification("textDocument/didChange", params)
        print(file_path)
        self.did_change_full(file_path)
    def did_save(self, file_path):
        """Notify rust-analyzer that a document was saved."""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path)
            }
        }
        
        return self.send_notification("textDocument/didSave", params)

    def did_close(self, file_path):
        """Notify rust-analyzer that a document was closed."""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path)
            }
        }
        return self.send_notification("textDocument/didClose", params)

    def _get_language_id(self, file_path):
        """Determine language ID based on file extension."""
        ext = pathlib.Path(file_path).suffix.lower()
        if ext == '.rs':
            return 'rust'
        else:
            return 'rust'  # Default to rust for unknown extensions in Rust projects

    def stop(self):
        """Shut down rust-analyzer properly."""
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
            worker = RustAnalyzerCompletionWorker(self, file_path, line, column, self.completions_ready, self.req_version)
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

    def request_range_formatting(self, file_path, start_line, start_char, end_line, end_char):
        """Request range formatting"""
        self._start_worker("textDocument/rangeFormatting", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": start_line, "character": start_char},
                "end": {"line": end_line, "character": end_char}
            },
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
        """Request document symbols"""
        print("Document symbols request sent")
        self._start_worker("textDocument/documentSymbol", {
            "textDocument": {"uri": pathToURL(file_path)}
        }, self.document_symbols_ready)

    def request_workspace_symbols(self, query):
        """Request workspace symbols"""
        self._start_worker("workspace/symbol", {"query": query}, self.workspace_symbols_ready)

    def request_inlay_hints(self, file_path, start_line=0, end_line=1000):
        """Request inlay hints (type annotations, parameter names, etc.)"""
        self._start_worker("textDocument/inlayHint", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": start_line, "character": 0},
                "end": {"line": end_line, "character": 0}
            }
        }, self.inlay_hints_ready)

    def request_runnables(self, file_path):
        """Request runnables (tests, main functions, examples) - rust-analyzer specific"""
        self._start_worker("experimental/runnables", {
            "textDocument": {"uri": pathToURL(file_path)}
        }, self.runnables_ready)

    def request_expand_macro(self, file_path, line, column):
        """Request macro expansion - rust-analyzer specific"""
        return self._start_worker("rust-analyzer/expandMacro", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column}
        }, self.hover_ready)  # Reuse hover_ready for macro expansion

    def request_parent_module(self, file_path):
        """Request parent module - rust-analyzer specific"""
        return self._start_worker("experimental/parentModule", {
            "textDocument": {"uri": pathToURL(file_path)}
        }, self.definition_ready)  # Reuse definition_ready

    def _start_worker(self, method, params, signal, *other):
        """Start a worker thread for LSP request"""
        self.thread_pool.start(RustAnalyzerLspWorker(self, method, params, signal, *other))


class RustAnalyzerLspWorker(QRunnable):
    def __init__(self, rust_analyzer, method, params, signal, *other):
        super().__init__()
        self.rust_analyzer = rust_analyzer
        self.method = method
        self.params = params
        self.signal = signal
        self.other = other

    def run(self):
        request_id = id(self)
        if self.rust_analyzer.send_lsp_request(self.method, self.params, request_id):
            result = self.rust_analyzer.read_lsp_response(request_id)
            
            if self.other:
                self.signal.emit(result, self.other)
            else:
                self.signal.emit(result)


# Utility functions for Rust projects
def find_cargo_toml(start_path):
    """Find the nearest Cargo.toml file by walking up the directory tree"""
    current = pathlib.Path(start_path).resolve()
    
    while current != current.parent:
        cargo_toml = current / "Cargo.toml"
        if cargo_toml.exists():
            return current
        current = current.parent
    
    return None

def create_rust_project_structure(project_path, project_name=None):
    """
    Create a basic Rust project structure if it doesn't exist
    
    Args:
        project_path: Path to create the project
        project_name: Name of the project (defaults to directory name)
    """
    project_path = pathlib.Path(project_path)
    project_path.mkdir(exist_ok=True)
    
    if project_name is None:
        project_name = project_path.name
    
    # Create Cargo.toml if it doesn't exist
    cargo_toml = project_path / "Cargo.toml"
    if not cargo_toml.exists():
        cargo_content = f"""[package]
name = "{project_name}"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
        with open(cargo_toml, 'w') as f:
            f.write(cargo_content)
    
    # Create src directory and main.rs
    src_dir = project_path / "src"
    src_dir.mkdir(exist_ok=True)
    
    main_rs = src_dir / "main.rs"
    if not main_rs.exists():
        main_content = """fn main() {
    println!("Hello, world!");
}
"""
        with open(main_rs, 'w') as f:
            f.write(main_content)
    
    return project_path

def get_rust_project_info(workspace_path):
    """Get information about the Rust project"""
    workspace_path = pathlib.Path(workspace_path)
    cargo_toml = workspace_path / "Cargo.toml"
    
    if not cargo_toml.exists():
        return None
    
    try:
        import toml
        with open(cargo_toml, 'r') as f:
            cargo_data = toml.load(f)
        
        return {
            "name": cargo_data.get("package", {}).get("name"),
            "version": cargo_data.get("package", {}).get("version"),
            "edition": cargo_data.get("package", {}).get("edition"),
            "dependencies": cargo_data.get("dependencies", {}),
            "workspace_path": workspace_path
        }
    except ImportError:
        print("toml package not available, parsing Cargo.toml manually")
        # Basic manual parsing as fallback
        with open(cargo_toml, 'r') as f:
            content = f.read()
        
        info = {"workspace_path": workspace_path}
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('name ='):
                info["name"] = line.split('=')[1].strip().strip('"')
            elif line.startswith('version ='):
                info["version"] = line.split('=')[1].strip().strip('"')
            elif line.startswith('edition ='):
                info["edition"] = line.split('=')[1].strip().strip('"')
        
        return info
    except Exception as e:
        print(f"Error parsing Cargo.toml: {e}")
        return None


# Example usage
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Example workspace setup
    workspace = "/path/to/your/rust/project"  # Change this to your Rust project path
    
    # Create LSP instance
    rust_lsp = RustAnalyzerLsp(workspace)
    
    # Connect signals to handle responses
    def on_completions(items):
        print(f"Received {len(items)} completions:")
        for item in items[:5]:  # Show first 5
            print(f"  - {item.get('label')}: {item.get('detail', '')}")
    
    def on_hover(result):
        if result and 'result' in result:
            hover_info = result['result']
            if hover_info and 'contents' in hover_info:
                print(f"Hover: {hover_info['contents']}")
    
    rust_lsp.completions_ready.connect(on_completions)
    rust_lsp.hover_ready.connect(on_hover)
    
    # Example: Open a file and request completions
    test_file = workspace + "/src/main.rs"
    if os.path.exists(test_file):
        with open(test_file, 'r') as f:
            content = f.read()
        
        rust_lsp.did_open(test_file, content)
        time.sleep(1)  # Give rust-analyzer time to process
        
        # Request completions at a specific position
        rust_lsp.request_completions(test_file, 0, 0)
    
    # Keep the application running briefly to see results
    app.processEvents()
    time.sleep(2)
    
    rust_lsp.stop()
    app.quit()