#!/usr/bin/env python3

import subprocess
import json
import pathlib
import os
import time

class SimpleTsLspTest:
    def __init__(self, workspace_root):
        self.workspace_root = workspace_root
        self.process = None
        self.request_id = 1
        
    def start_lsp(self):
        """Start the TypeScript Language Server."""
        commands = [
            ["npx", "typescript-language-server", "--stdio"],
            ["typescript-language-server", "--stdio"]
        ]
        
        for cmd in commands:
            try:
                print(f"Trying: {' '.join(cmd)}")
                self.process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    cwd=self.workspace_root
                )
                
                # Test if it started
                time.sleep(0.5)
                if self.process.poll() is None:
                    print(f"✅ Started: {' '.join(cmd)}")
                    return True
                else:
                    print(f"❌ Exited immediately: {' '.join(cmd)}")
                    
            except Exception as e:
                print(f"❌ Failed: {e}")
                continue
                
        return False
    
    def send_message(self, message):
        """Send a message to the LSP server."""
        if not self.process:
            return None
            
        try:
            message_json = json.dumps(message)
            content = f"Content-Length: {len(message_json)}\r\n\r\n{message_json}"
            
            print(f"Sending: {message.get('method', 'response')}")
            self.process.stdin.write(content)
            self.process.stdin.flush()
            
            # If it's a request (has id), wait for response
            if 'id' in message:
                return self.read_response()
                
        except Exception as e:
            print(f"Send error: {e}")
            return None
    
    def read_response(self):
        """Read response from LSP server."""
        try:
            while True:
                # Read headers
                headers = {}
                while True:
                    line = self.process.stdout.readline().strip()
                    if not line:
                        break
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        headers[key] = value
                
                if "Content-Length" not in headers:
                    print("No Content-Length header")
                    return None
                
                # Read content
                length = int(headers["Content-Length"])
                content = self.process.stdout.read(length)
                
                if content:
                    response = json.loads(content)
                    
                    # Skip notifications
                    if 'method' in response:
                        method = response['method']
                        print(f"Received notification: {method}")
                        if method in ['window/logMessage', '$/typescriptVersion']:
                            continue
                            
                    # Return actual responses
                    if 'id' in response:
                        return response
                        
        except Exception as e:
            print(f"Read error: {e}")
            return None
    
    def initialize(self):
        """Initialize the LSP server."""
        workspace_uri = pathlib.Path(self.workspace_root).resolve().as_uri()
        
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "processId": os.getpid(),
                "rootUri": workspace_uri,
                "capabilities": {
                    "textDocument": {
                        "completion": {"completionItem": {"snippetSupport": True}},
                        "hover": {"contentFormat": ["markdown", "plaintext"]},
                    }
                }
            }
        }
        
        self.request_id += 1
        response = self.send_message(init_request)
        
        if response:
            print("✅ Initialized successfully")
            # Send initialized notification
            self.send_message({
                "jsonrpc": "2.0",
                "method": "initialized",
                "params": {}
            })
            return True
        else:
            print("❌ Initialization failed")
            return False
    
    def open_document(self, file_path, content):
        """Open a document."""
        uri = str(pathlib.Path(file_path).resolve().as_uri())
        
        notification = {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": uri,
                    "languageId": "typescript",
                    "version": 1,
                    "text": content
                }
            }
        }
        
        self.send_message(notification)
        print(f"✅ Opened document: {file_path}")
    
    def request_completions(self, file_path, line, column):
        """Request completions."""
        uri = str(pathlib.Path(file_path).resolve().as_uri())
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": column}
            }
        }
        
        self.request_id += 1
        response = self.send_message(request)
        
        if response and 'result' in response:
            items = response['result'].get('items', [])
            print(f"✅ Got {len(items)} completions:")
            for item in items[:10]:  # Show first 10
                label = item.get('label', 'Unknown')
                kind = item.get('kind', 'Unknown')
                print(f"  - {label} (kind: {kind})")
        else:
            print("❌ No completions received")
            print(f"Response: {response}")
    
    def stop(self):
        """Stop the LSP server."""
        if self.process:
            try:
                # Send shutdown
                self.send_message({
                    "jsonrpc": "2.0",
                    "id": self.request_id,
                    "method": "shutdown",
                    "params": None
                })
                
                # Send exit
                self.send_message({
                    "jsonrpc": "2.0",
                    "method": "exit",
                    "params": None
                })
                
                self.process.terminate()
                print("✅ LSP stopped")
            except:
                pass


def main():
    # Create test directory and file
    test_dir = "/tmp/ts_simple_test"
    os.makedirs(test_dir, exist_ok=True)
    
    test_file = os.path.join(test_dir, "test.ts")
    test_content = """imp
interface User {
    id: number;
    name: string;
}
class User{}
class Omkumar{}
const s=new Omkumar();
class UserService {
    getUser(): User {
        return { id: 1, name: "test" };
    }
    
    getAllUsers(): User[] {
        return [];
    }
}

const service = new UserService();
service."""
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    print(f"Created test file: {test_file}")
    
    # Test LSP
    lsp = SimpleTsLspTest(test_dir)
    
    try:
        if not lsp.start_lsp():
            print("❌ Failed to start LSP")
            return
            
        time.sleep(1)  # Give it time to start
        
        if not lsp.initialize():
            print("❌ Failed to initialize")
            return
            
        time.sleep(1)  # Give it time to initialize
        
        lsp.open_document(test_file, test_content)
        time.sleep(2)  # Give it time to process the document
        
        # Request completions at the end of 'service.'
        print("\n=== Requesting completions ===")
        lsp.request_completions(test_file, line=0, column=2)  # After 'service.'
        
    finally:
        lsp.stop()


if __name__ == "__main__":
    main()