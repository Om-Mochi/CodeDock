from CodeDock.src.controllers.PathHandler import Dir_Scanner
from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool, QMutex, QMutexLocker
import subprocess
import json
import pathlib


class PylspComplitionWorker(QRunnable):
    """Worker to send LSP requests safely using a mutex."""
    def __init__(self, pylsp, file_path, line, char_pos, signal):
        super().__init__() 
        self.pylsp = pylsp  # Store the PyLsp instance
        self.line = line
        self.char_pos = char_pos
        self.signal = signal  # Use signal instead of callback
        try:
            self.file_path = str(pathlib.Path(file_path).resolve().as_uri())
        except:
            self.file_path = file_path

    def run(self):
        """Runs in a thread pool worker and sends the request safely."""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": self.file_path},
                "position": {"line": self.line, "character": self.char_pos}
            }
        }
        response = self.pylsp.send_request(request)
        if response and 'result' in response:
            items = response.get("result", {})
            # Handle both dict with 'items' key and direct list
            if isinstance(items, dict) and 'items' in items:
                items = items['items']
            elif isinstance(items, list):  # PyLSP might return direct list
                pass  # items is already the list
            elif items is None:
                items = []
            else:
                items = []  # fallback for unexpected formats
        
        self.signal.emit(items,"py")

class PyLsp(QObject):
    completions_ready = pyqtSignal(list,str)
    hover_ready = pyqtSignal(object)
    definition_ready = pyqtSignal(object)
    references_ready = pyqtSignal(object,tuple)
    signature_help_ready = pyqtSignal(object)
    formatting_ready = pyqtSignal(object)
    code_action_ready = pyqtSignal(object)
    document_symbols_ready = pyqtSignal(object)
    workspace_symbols_ready = pyqtSignal(object)
    diagnostics_ready = pyqtSignal(object)
    def __init__(self,workspace_path=None):
        super().__init__()
        self.pause=False
        self.process = subprocess.Popen(
            ["python3", "-m", "pylsp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )


        if workspace_path:
            self.workspace_path = workspace_path or pathlib.Path.cwd()
            self.workspace_path = f"file://{self.workspace_path}"
        else:
            self.workspace_path = None


        self.mutex = QMutex()
        self.thread_pool = QThreadPool.globalInstance()
        self._initialize()

    def _initialize(self):
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "processId": None,
                "rootUri": self.workspace_path,
                "capabilities": {
                    "textDocument": {
                        "documentSymbol": {
                            "hierarchicalDocumentSymbolSupport": False
                        }
                    }
                }
            }
        }
        self.send_request(init_request)

    def send_request(self, request):
        with QMutexLocker(self.mutex):
            try:
                if self.process.poll() is not None:
                    return None
                request_json = json.dumps(request)
                content = f"Content-Length: {len(request_json)}\r\n\r\n{request_json}"
                self.process.stdin.write(content)
                self.process.stdin.flush()

                response_headers = {}
                while True:
                    line = self.process.stdout.readline().strip()
                    if not line:
                        break
                    key, value = line.split(": ", 1)
                    response_headers[key] = value

                if "Content-Length" not in response_headers:
                    return None

                content_length = int(response_headers["Content-Length"])
                response_text = self.process.stdout.read(content_length)
                return json.loads(response_text)

            except Exception as e:
                print(f"Error: {e}")
                return None

    def stop(self):
        """Shut down pylsp properly."""
        exit_request = {"jsonrpc": "2.0", "id": 3, "method": "shutdown", "params": None}
        self.send_request(exit_request)
        self.process.terminate()

    def did_open(self,*arg):pass
    def did_change(self,*arg):pass
    
    def request_completions(self, file_path, line, column):
        """Run a completion request in a worker threadpool."""
        if self.pause!=True:
            worker = PylspComplitionWorker(self, file_path, line, column, self.completions_ready)
            self.thread_pool.start(worker)

    def request_hover(self, file_path, line, column):
        self._start_worker("textDocument/hover", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())},
            "position": {"line": line, "character": column}
        }, self.hover_ready)

    def request_definition(self, file_path, line, column):
        self._start_worker("textDocument/definition", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())},
            "position": {"line": line, "character": column}
        }, self.definition_ready)

    def request_references(self,word,file_path, line, column):
        self._start_worker("textDocument/references", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())},
            "position": {"line": line, "character": column},
            "context": {"includeDeclaration": True}
        }, self.references_ready,word)

    def request_signature_help(self, file_path, line, column):
        self._start_worker("textDocument/signatureHelp", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())},
            "position": {"line": line, "character": column}
        }, self.signature_help_ready)

    def request_formatting(self, file_path):
        self._start_worker("textDocument/formatting", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())},
            "options": {"tabSize": 4, "insertSpaces": True}
        }, self.formatting_ready)

    def request_code_action(self, file_path, line, column):
        self._start_worker("textDocument/codeAction", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())},
            "range": {
                "start": {"line": line, "character": column},
                "end": {"line": line, "character": column + 1}
            },
            "context": {"diagnostics": []}
        }, self.code_action_ready)

    def request_document_symbols(self, file_path):
        print("sended")
        self._start_worker("textDocument/documentSymbol", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())}
        }, self.document_symbols_ready)

    def request_workspace_symbols(self, query):
        self._start_worker("workspace/symbol", {"query": query}, self.workspace_symbols_ready)

    def request_diagnostics(self, file_path):
        self._start_worker("textDocument/publishDiagnostics", {
            "textDocument": {"uri": str(pathlib.Path(file_path).resolve().as_uri())}
        }, self.diagnostics_ready)

    def _start_worker(self, method, params, signal,*other):
        self.thread_pool.start(LspWorker(self, method, params, signal,*other))

class LspWorker(QRunnable):
    def __init__(self, pylsp, method, params, signal,*other):
        super().__init__()
        self.pylsp = pylsp
        self.method = method
        self.params = params
        self.signal = signal
        self.other=other
        #print(method)
    def run(self):
        request = {
            "jsonrpc": "2.0",
            "id": id(self),
            "method": self.method,
            "params": self.params
        }
        result = self.pylsp.send_request(request)
        #print("type : ",type(result))
        if self.other:
            self.signal.emit(result,self.other)
        else:self.signal.emit(result)



"""
class PyLSP:
	def __init__(self):

		self.tags=[]
		self.completions=[]
		self.current_block=0
		self.imports=[]

		self.setProjectDir()
	def setProjectDir(self,dir_path="/"):
		self.project_dir_path=dir_path
		self.project_dirs=Dir_Scanner.child_deep_scan(dir_path)
		
	def tagsGenerator(self,codefile_path,path_h):
		tagfile_path=path_h.CustomTags.py()
		command=["ctags","-R","-f","-",f"--options={tagfile_path}",codefile_path]
		result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
		lines=[]
		for line in result.stdout.splitlines():
			if line.startswith("!"):
				continue

			parts = line.split("\t")
			
			if len(parts)>=5:
				if len(parts)==4:
					name,pattern,types,line_no,member=parts[0],parts[2],parts[3],parts[4],parts[5]
				else:name,pattern,types,line_no,member=parts[0],parts[2],parts[3],parts[4],None
				#tags.append({"name": tag_name, "pattern": pattern, "line":,"def": components_name})
				
				
				
				pattern=pattern.replace("/^","",1)
				pattern=pattern.replace('$/;"',"")
				line_no=line_no.replace("line:","")

				total_block=0
				if pattern.startswith('    ')==True:
					total_block=pattern.count('    ')
				
				#replace std tabs to html tabs
				pattern=pattern.replace(total_block*'    ',total_block*'')
				#pattern=f"{line_no} {pattern}"
				#lines.append(line_no)

				if types=='c':
					pattern=f"<span style='color: green;'>class</span> {name}"
				if types=='m':
					pattern=f"<span style='color: yellow;'>def</span> {name}"
				if types=='f':
					pattern=f"<span style='color: pink;'>def</span> {name}"

				self.imports.append(pattern)
				self.tags.append([int(line_no),int(total_block),types,name,pattern,member])
		return sorted(self.tags,key=lambda x: x[0])

	def getTags(self,file_path,path_h, flag_d="-v"):
		self.tags.clear()
		#self.completions.clear()

		pytags=self.tagsGenerator(file_path,path_h)
		filtered_pytags=[]
		for tag in pytags:
			if tag[2] == 'v' or tag[2]=='i' or tag[2]=='r':...
				#self.completions.append(tag[3])
			else:
				filtered_pytags.append(tag)
				#self.completions.append(tag[3]) 
		return filtered_pytags
	



	def getCompletions(self,parent_completion=None):
		return self.getImportsCompletions(parent_completion="CodeDock")
		if parent_completion==None:
			completion_list=[]
			for i,tag in enumerate(self.tags):
				if self.current_block>=tag[1]:
					completion_list.append(tag[3])
			return completion_list
		elif parent_completion!=None:pass

	def getImportsCompletions(self,parent_completion=None):
		if parent_completion==None:
			return Dir_Scanner.child_scan(self.project_dir_path)

		elif parent_completion!=None:
			return Dir_Scanner.child_scan(f"{self.project_dir_path}/{parent_completion}")

	
		


"""




