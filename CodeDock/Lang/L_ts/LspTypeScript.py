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

class TypeScriptCompletionWorker(QRunnable):
    """Worker to send LSP requests safely using a mutex for TypeScript completion."""
    def __init__(self, ts_server:"TypeScriptLsp", file_path, line, char_pos, signal, ver):
        super().__init__() 
        self.ts_server = ts_server  # Store the TypeScriptLsp instance
        self.line = line
        self.char_pos = char_pos
        self.signal = signal  # Use signal instead of callback
        self.ver = ver
        print("ok")
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

        self.ts_server.req_version += 1  
        request_id = self.ver
        self.ts_server.send_lsp_request("textDocument/completion", params, request_id)
        response = self.ts_server.read_lsp_response(request_id)
        print("responce :",response)
        if response and 'result' in response:
            suggestions = []
            items = response.get("result", {})
            
            # Handle both dict with 'items' key and direct list
            if isinstance(items, dict) and 'items' in items:
                items = items['items']
            elif items is None:
                items = []
                
            self.signal.emit(items)


class TypeScriptLsp(QObject):
    completions_ready = pyqtSignal(list)
    hover_ready = pyqtSignal(object)
    definition_ready = pyqtSignal(object)
    type_definition_ready = pyqtSignal(object)
    implementation_ready = pyqtSignal(object)
    references_ready = pyqtSignal(object, tuple)
    signature_help_ready = pyqtSignal(object)
    formatting_ready = pyqtSignal(object)
    code_action_ready = pyqtSignal(object)
    document_symbols_ready = pyqtSignal(object)
    workspace_symbols_ready = pyqtSignal(object)
    diagnostics_ready = pyqtSignal(object)
    rename_ready = pyqtSignal(object)
    organize_imports_ready = pyqtSignal(object)
    quick_fix_ready = pyqtSignal(object)

    def __init__(self, workspace_path=None, use_typescript_server=True):
        super().__init__()
        self.pause = False
        self.workspace_path = workspace_path or os.getcwd()
        self.use_typescript_server = use_typescript_server
        
        self.req_version = 1
        
        # Start TypeScript language server process
        try:
            if use_typescript_server:
                # Use typescript-language-server (requires: npm install -g typescript-language-server typescript)
                cmd = ['typescript-language-server', '--stdio']
            else:
                # Alternative: Use Pyright (requires: npm install -g pyright)
                cmd = ['pyright-langserver', '--stdio']
                
            self.ts_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,  # Keep as binary for JsonRpcStreamWriter
                bufsize=0,
                cwd=self.workspace_path
            )
            print(f"TypeScript language server started: {' '.join(cmd)}")

            # Initialize JSON-RPC streams
            self.writer = JsonRpcStreamWriter(self.ts_process.stdin)

        except Exception as e:
            print(f"Failed to start TypeScript language server: {e}")
            print("Make sure you have installed: npm install -g typescript-language-server typescript")
            self.ts_process = None
            self.writer = None

        self.mutex = QMutex()
        self.thread_pool = QThreadPool.globalInstance()
        self.pending_requests = {}  # Track pending requests by ID
        
        if self.ts_process:
            self.initialize_typescript_server()

    def send_lsp_request(self, method, params, request_id=1):
        """Send LSP request to TypeScript server using JsonRpcStreamWriter"""
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
        """Read a single LSP message from TypeScript server manually"""
        if not self.ts_process:
            return None
            
        try:
            # Read headers line by line
            headers = {}
            while True:
                line = self.ts_process.stdout.readline().decode('utf-8')
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
                content = self.ts_process.stdout.read(content_length).decode('utf-8')
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
                    elif method == 'window/logMessage':
                        # Handle log messages from the server
                        print(f"TS Server Log: {message.get('params', {}).get('message', '')}")
                    else:
                        print(f"Received notification: {method}")
                        
            except Exception as e:
                print(f"Error in read_lsp_response: {e}")
                break
                
        # Clean up expired request
        self.pending_requests.pop(request_id, None)
        return None
    
    def initialize_typescript_server(self):
        """Initialize TypeScript server with LSP initialize request"""
        init_params = {
            "processId": os.getpid(),
            "clientInfo": {"name": "typescript-lsp-tester", "version": "1.0"},
            "rootUri": f"file://{self.workspace_path}",
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
                    "typeDefinition": {
                        "linkSupport": True
                    },
                    "implementation": {
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
                    "onTypeFormatting": {
                        "firstTriggerCharacter": ";",
                        "moreTriggerCharacter": [",", "}"]
                    },
                    "codeAction": {
                        "codeActionLiteralSupport": {
                            "codeActionKind": {
                                "valueSet": [
                                    "quickfix",
                                    "refactor",
                                    "refactor.extract",
                                    "refactor.inline",
                                    "refactor.rewrite",
                                    "source.organizeImports"
                                ]
                            }
                        }
                    },
                    "documentSymbol": {
                        "hierarchicalDocumentSymbolSupport": True
                    },
                    "rename": {
                        "prepareSupport": True
                    }
                },
                "workspace": {
                    "workspaceFolders": True,
                    "symbol": {},
                    "configuration": True,
                    "didChangeConfiguration": {
                        "dynamicRegistration": True
                    },
                    "executeCommand": {
                        "dynamicRegistration": True
                    }
                }
            },
            "initializationOptions": {
                "preferences": {
                    "includeCompletionsForModuleExports": True,
                    "includeCompletionsWithInsertText": True,
                    "allowIncompleteCompletions": True,
                    "importModuleSpecifier": "relative"
                },
                "suggest": {
                    "autoImports": True
                }
            }
        }
        
        print("Initializing TypeScript language server...")
        if self.send_lsp_request("initialize", init_params, 1):
            response = self.read_lsp_response(1)
            if response and 'result' in response:
                print("TypeScript language server initialized successfully")
                # Send initialized notification (no id for notifications)
                self.send_notification("initialized", {})
                return True
            else:
                print(f"Failed to initialize TypeScript server: {response}")
                return False
        return False
        
    def send_notification(self, method, params):
        """Send LSP notification to TypeScript server (no response expected)"""
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
        """Open the document in TypeScript server"""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path),
                "languageId": self._get_language_id(file_path),
                "version": self.req_version,
                "text": content
            }
        }
        
        self.req_version += 1

        print("Opening document in TypeScript server...")
        return self.send_notification("textDocument/didOpen", params)
    
    def did_change_full(self, file_path):
        """Update the entire document content"""
        with open(file_path, "r", encoding='utf-8') as f:
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
        """Send incremental document changes to TypeScript server"""
        params = {
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
        self.req_version += 1
        
        return self.send_notification("textDocument/didChange", params)

    def did_save(self, file_path):
        """Notify TypeScript server that a document was saved."""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path)
            }
        }
        
        return self.send_notification("textDocument/didSave", params)

    def did_close(self, file_path):
        """Notify TypeScript server that a document was closed."""
        params = {
            "textDocument": {
                "uri": pathToURL(file_path)
            }
        }
        return self.send_notification("textDocument/didClose", params)

    def _get_language_id(self, file_path):
        """Determine language ID based on file extension."""
        ext = pathlib.Path(file_path).suffix.lower()
        if ext == '.ts':
            return 'typescript'
        elif ext == '.tsx':
            return 'typescriptreact'
        elif ext == '.js':
            return 'javascript'
        elif ext == '.jsx':
            return 'javascriptreact'
        elif ext == '.json':
            return 'json'
        elif ext == '.vue':
            return 'vue'
        else:
            return 'typescript'  # Default to TypeScript

    def stop(self):
        """Shut down TypeScript server properly."""
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
            if self.ts_process:
                self.ts_process.terminate()
                
        except Exception as e:
            print(f"Error during shutdown: {e}")
            if self.ts_process:
                self.ts_process.kill()

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
            worker = TypeScriptCompletionWorker(self, file_path, line, column, self.completions_ready, self.req_version)
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

    def request_type_definition(self, file_path, line, column):
        """Request go to type definition"""
        self._start_worker("textDocument/typeDefinition", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column}
        }, self.type_definition_ready)

    def request_implementation(self, file_path, line, column):
        """Request go to implementation"""
        self._start_worker("textDocument/implementation", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column}
        }, self.implementation_ready)

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
            "options": {
                "tabSize": 2,
                "insertSpaces": True,
                "trimTrailingWhitespace": True,
                "insertFinalNewline": True
            }
        }, self.formatting_ready)

    def request_range_formatting(self, file_path, start_line, start_char, end_line, end_char):
        """Request range formatting"""
        self._start_worker("textDocument/rangeFormatting", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": start_line, "character": start_char},
                "end": {"line": end_line, "character": end_char}
            },
            "options": {
                "tabSize": 2,
                "insertSpaces": True
            }
        }, self.formatting_ready)

    def request_code_action(self, file_path, start_line, start_char, end_line, end_char, diagnostics=None):
        """Request code actions"""
        if diagnostics is None:
            diagnostics = []
            
        self._start_worker("textDocument/codeAction", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": start_line, "character": start_char},
                "end": {"line": end_line, "character": end_char}
            },
            "context": {
                "diagnostics": diagnostics,
                "only": ["quickfix", "refactor", "source.organizeImports"]
            }
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

    def request_rename(self, file_path, line, column, new_name):
        """Request rename symbol"""
        self._start_worker("textDocument/rename", {
            "textDocument": {"uri": pathToURL(file_path)},
            "position": {"line": line, "character": column},
            "newName": new_name
        }, self.rename_ready)

    def request_organize_imports(self, file_path):
        """Request organize imports - TypeScript specific"""
        self._start_worker("textDocument/codeAction", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 0}
            },
            "context": {
                "diagnostics": [],
                "only": ["source.organizeImports"]
            }
        }, self.organize_imports_ready)

    def request_quick_fix(self, file_path, line, column, diagnostics):
        """Request quick fixes for specific diagnostics"""
        self._start_worker("textDocument/codeAction", {
            "textDocument": {"uri": pathToURL(file_path)},
            "range": {
                "start": {"line": line, "character": column},
                "end": {"line": line, "character": column + 1}
            },
            "context": {
                "diagnostics": diagnostics,
                "only": ["quickfix"]
            }
        }, self.quick_fix_ready)

    def _start_worker(self, method, params, signal, *other):
        """Start a worker thread for LSP request"""
        self.thread_pool.start(TypeScriptLspWorker(self, method, params, signal, *other))


class TypeScriptLspWorker(QRunnable):
    def __init__(self, ts_server, method, params, signal, *other):
        super().__init__()
        self.ts_server = ts_server
        self.method = method
        self.params = params
        self.signal = signal
        self.other = other

    def run(self):
        request_id = id(self)
        if self.ts_server.send_lsp_request(self.method, self.params, request_id):
            result = self.ts_server.read_lsp_response(request_id)
            
            if self.other:
                self.signal.emit(result, self.other)
            else:
                self.signal.emit(result)


# Utility functions for TypeScript projects
def find_package_json(start_path):
    """Find the nearest package.json file by walking up the directory tree"""
    current = pathlib.Path(start_path).resolve()
    
    while current != current.parent:
        package_json = current / "package.json"
        if package_json.exists():
            return current
        current = current.parent
    
    return None

def find_tsconfig_json(start_path):
    """Find the nearest tsconfig.json file by walking up the directory tree"""
    current = pathlib.Path(start_path).resolve()
    
    while current != current.parent:
        tsconfig = current / "tsconfig.json"
        if tsconfig.exists():
            return current
        current = current.parent
    
    return None

def create_typescript_project_structure(project_path, project_name=None, use_react=False):
    """
    Create a basic TypeScript project structure if it doesn't exist
    
    Args:
        project_path: Path to create the project
        project_name: Name of the project (defaults to directory name)
        use_react: Whether to include React types and setup
    """
    project_path = pathlib.Path(project_path)
    project_path.mkdir(exist_ok=True)
    
    if project_name is None:
        project_name = project_path.name
    
    # Create package.json if it doesn't exist
    package_json = project_path / "package.json"
    if not package_json.exists():
        dependencies = {
            "typescript": "^5.0.0",
            "@types/node": "^20.0.0"
        }
        
        if use_react:
            dependencies.update({
                "react": "^18.0.0",
                "react-dom": "^18.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0"
            })
        
        package_content = {
            "name": project_name,
            "version": "1.0.0",
            "main": "dist/index.js",
            "scripts": {
                "build": "tsc",
                "dev": "tsc --watch",
                "start": "node dist/index.js"
            },
            "devDependencies": dependencies
        }
        
        with open(package_json, 'w') as f:
            json.dump(package_content, f, indent=2)
    
    # Create tsconfig.json if it doesn't exist
    tsconfig_json = project_path / "tsconfig.json"
    if not tsconfig_json.exists():
        compiler_options = {
            "target": "ES2022",
            "module": "commonjs",
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        }
        
        if use_react:
            compiler_options.update({
                "jsx": "react-jsx",
                "lib": ["ES2022", "DOM", "DOM.Iterable"]
            })
        else:
            compiler_options["lib"] = ["ES2022"]
        
        tsconfig_content = {
            "compilerOptions": compiler_options,
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist"]
        }
        
        with open(tsconfig_json, 'w') as f:
            json.dump(tsconfig_content, f, indent=2)
    
    # Create src directory and index.ts
    src_dir = project_path / "src"
    src_dir.mkdir(exist_ok=True)
    
    index_ts = src_dir / "index.ts"
    if not index_ts.exists():
        if use_react:
            index_content = """import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return <h1>Hello, TypeScript + React!</h1>;
}

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(<App />);
"""
        else:
            index_content = """function greet(name: string): string {
    return `Hello, ${name}!`;
}

console.log(greet("TypeScript"));
"""
        
        with open(index_ts, 'w') as f:
            f.write(index_content)
    
    return project_path

def get_typescript_project_info(workspace_path):
    """Get information about the TypeScript project"""
    workspace_path = pathlib.Path(workspace_path)
    package_json = workspace_path / "package.json"
    tsconfig_json = workspace_path / "tsconfig.json"
    
    info = {"workspace_path": workspace_path}
    
    # Parse package.json
    if package_json.exists():
        try:
            with open(package_json, 'r') as f:
                package_data = json.load(f)
            
            info.update({
                "name": package_data.get("name"),
                "version": package_data.get("version"),
                "dependencies": package_data.get("dependencies", {}),
                "devDependencies": package_data.get("devDependencies", {}),
                "scripts": package_data.get("scripts", {})
            })
        except Exception as e:
            print(f"Error parsing package.json: {e}")
    
    # Parse tsconfig.json
    if tsconfig_json.exists():
        try:
            with open(tsconfig_json, 'r') as f:
                tsconfig_data = json.load(f)
            
            info.update({
                "compilerOptions": tsconfig_data.get("compilerOptions", {}),
                "include": tsconfig_data.get("include", []),
                "exclude": tsconfig_data.get("exclude", [])
            })
        except Exception as e:
            print(f"Error parsing tsconfig.json: {e}")
    
    return info

def create_eslint_config(project_path, use_react=False):
    """Create a basic ESLint configuration for TypeScript"""
    project_path = pathlib.Path(project_path)
    eslint_config = project_path / ".eslintrc.json"
    
    if not eslint_config.exists():
        config = {
            "env": {
                "es2022": True,
                "node": True
            },
            "extends": [
                "@typescript-eslint/recommended"
            ],
            "parser": "@typescript-eslint/parser",
            "parserOptions": {
                "ecmaVersion": 2022,
                "sourceType": "module"
            },
            "plugins": [
                "@typescript-eslint"
            ],
            "rules": {}
        }
        
        if use_react:
            config["env"]["browser"] = True
            config["extends"].extend([
                "plugin:react/recommended",
                "plugin:react-hooks/recommended"
            ])
            config["plugins"].extend(["react", "react-hooks"])
            config["settings"] = {
                "react": {
                    "version": "detect"
                }
            }
        
        with open(eslint_config, 'w') as f:
            json.dump(config, f, indent=2)
    
    return eslint_config

def create_prettier_config(project_path):
    """Create a Prettier configuration for code formatting"""
    project_path = pathlib.Path(project_path)
    prettier_config = project_path / ".prettierrc.json"
    
    if not prettier_config.exists():
        config = {
            "semi": True,
            "trailingComma": "es5",
            "singleQuote": True,
            "printWidth": 80,
            "tabWidth": 2,
            "useTabs": False
        }
        
        with open(prettier_config, 'w') as f:
            json.dump(config, f, indent=2)
    
    return prettier_config


# Example usage
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Example workspace setup
    workspace = "/path/to/your/typescript/project"  # Change this to your TypeScript project path
    
    # Create LSP instance
    ts_lsp = TypeScriptLsp(workspace)
    
    # Connect signals to handle responses
    def on_completions(items):
        print(f"Received {len(items)} completions:")
        for item in items[:10]:  # Show first 10
            label = item.get('label', '')
            kind = item.get('kind', '')
            detail = item.get('detail', '')
            print(f"  - {label} ({kind}): {detail}")
    
    def on_hover(result):
        if result and 'result' in result:
            hover_info = result['result']
            if hover_info and 'contents' in hover_info:
                contents = hover_info['contents']
                if isinstance(contents, dict):
                    print(f"Hover: {contents.get('value', '')}")
                elif isinstance(contents, list) and contents:
                    print(f"Hover: {contents[0].get('value', contents[0])}")
                else:
                    print(f"Hover: {contents}")
    
    def on_diagnostics(result):
        if result and 'params' in result:
            diagnostics = result['params'].get('diagnostics', [])
            if diagnostics:
                print(f"Diagnostics for {result['params'].get('uri', '')}:")
                for diag in diagnostics:
                    severity = ['Error', 'Warning', 'Information', 'Hint'][diag.get('severity', 1) - 1]
                    message = diag.get('message', '')
                    line = diag.get('range', {}).get('start', {}).get('line', 0)
                    print(f"  {severity} at line {line + 1}: {message}")
    
    def on_definition(result):
        if result and 'result' in result:
            definitions = result['result']
            if definitions:
                print("Definitions found:")
                for defn in definitions[:3]:  # Show first 3
                    uri = defn.get('uri', '')
                    line = defn.get('range', {}).get('start', {}).get('line', 0)
                    print(f"  - {uri}:{line + 1}")
    
    def on_document_symbols(result):
        if result and 'result' in result:
            symbols = result['result']
            print(f"Found {len(symbols)} symbols:")
            for symbol in symbols[:10]:  # Show first 10
                name = symbol.get('name', '')
                kind = symbol.get('kind', '')
                print(f"  - {name} ({kind})")
    
    # Connect signals
    ts_lsp.completions_ready.connect(on_completions)
    ts_lsp.hover_ready.connect(on_hover)
    ts_lsp.diagnostics_ready.connect(on_diagnostics)
    ts_lsp.definition_ready.connect(on_definition)
    ts_lsp.document_symbols_ready.connect(on_document_symbols)
    
    # Example: Open a file and request various LSP features
    test_file = workspace + "/src/index.ts"
    if os.path.exists(test_file):
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Opening file: {test_file}")
        ts_lsp.did_open(test_file, content)
        time.sleep(2)  # Give TypeScript server time to process
        
        # Request completions at a specific position
        print("Requesting completions...")
        ts_lsp.request_completions(test_file, 0, 0)
        
        # Request hover information
        print("Requesting hover info...")
        ts_lsp.request_hover(test_file, 0, 8)  # Hover over function name
        
        # Request document symbols
        print("Requesting document symbols...")
        ts_lsp.request_document_symbols(test_file)
        
        # Request definition
        print("Requesting definition...")
        ts_lsp.request_definition(test_file, 0, 8)
    
    else:
        print(f"Test file not found: {test_file}")
        print("Creating sample TypeScript project...")
        
        # Create a sample project structure
        sample_project = create_typescript_project_structure(workspace, "sample-ts-project")
        print(f"Created sample project at: {sample_project}")
        
        # Try again with the created project
        test_file = sample_project / "src" / "index.ts"
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ts_lsp.did_open(str(test_file), content)
        time.sleep(2)
        
        ts_lsp.request_completions(str(test_file), 0, 0)
    
    # Keep the application running briefly to see results
    print("Processing events...")
    for i in range(50):  # Process events for 5 seconds
        app.processEvents()
        time.sleep(0.1)
    
    print("Shutting down...")
    ts_lsp.stop()
    app.quit()


# Additional TypeScript-specific utility functions
def install_typescript_dependencies(project_path):
    """Install TypeScript and related dependencies via npm"""
    project_path = pathlib.Path(project_path)
    
    try:
        # Install TypeScript language server globally if not present
        subprocess.run(['npm', 'install', '-g', 'typescript-language-server', 'typescript'], 
                      cwd=project_path, check=True)
        print("Global TypeScript tools installed successfully")
        
        # Install project dependencies if package.json exists
        package_json = project_path / "package.json"
        if package_json.exists():
            subprocess.run(['npm', 'install'], cwd=project_path, check=True)
            print("Project dependencies installed successfully")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("npm not found. Please install Node.js and npm first.")
        return False

def check_typescript_setup(workspace_path):
    """Check if TypeScript environment is properly set up"""
    checks = {
        "typescript_server": False,
        "typescript_compiler": False,
        "package_json": False,
        "tsconfig_json": False
    }
    
    # Check for typescript-language-server
    try:
        subprocess.run(['typescript-language-server', '--version'], 
                      capture_output=True, check=True)
        checks["typescript_server"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Check for TypeScript compiler
    try:
        subprocess.run(['tsc', '--version'], 
                      capture_output=True, check=True)
        checks["typescript_compiler"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    workspace_path = pathlib.Path(workspace_path)
    
    # Check for package.json
    if (workspace_path / "package.json").exists():
        checks["package_json"] = True
    
    # Check for tsconfig.json
    if (workspace_path / "tsconfig.json").exists():
        checks["tsconfig_json"] = True
    
    return checks

def get_typescript_file_list(workspace_path):
    """Get all TypeScript files in the workspace"""
    workspace_path = pathlib.Path(workspace_path)
    
    ts_files = []
    ts_files.extend(list(workspace_path.rglob("*.ts")))
    ts_files.extend(list(workspace_path.rglob("*.tsx")))
    ts_files.extend(list(workspace_path.rglob("*.js")))
    ts_files.extend(list(workspace_path.rglob("*.jsx")))
    
    # Filter out node_modules and other common ignore patterns
    ignore_patterns = ['node_modules', 'dist', 'build', '.git', '.vscode']
    filtered_files = []
    
    for file in ts_files:
        if not any(pattern in str(file) for pattern in ignore_patterns):
            filtered_files.append(file)
    
    return filtered_files