from PyQt6 import QtWidgets,QtGui
from PyQt6.QtCore import pyqtSignal,QObject
from CodeDock.Lang.L_py.PyLsp import PyLsp
from CodeDock.Lang.L_cpp.CppLSP import ClangdLsp
from CodeDock.Lang.L_rs.RustLsp import RustAnalyzerLsp
from CodeDock.Lang.L_ts.LspTypeScript import TypeScriptLsp
from CodeDock.src.controllers.PathHandler import Path_Handler
from CodeDock.C_Widgets.Custom import Custom
from CodeDock.Code.src.controllers.CodePadHighlighter import CppHighlighter,PythonHighlighter,RustHighlighter

#from CodeDock.Lang.ProjectDetector import getProjectRootsAndProjectDirs
import typing
import dataclasses
import os


# Ignore junk/cache/IDE dirs
IGNORE_DIRS = {
    "build", "dist", "out", "bin", "obj", "target", "Debug", "Release",
    ".cache", ".gradle", ".cargo", ".venv", "env", 
    "CMakeFiles", "cmake-build-debug", "cmake-build-release",
    "coverage", "htmlcov", ".pytest_cache", ".tox", ".mypy_cache", ".ruff_cache",
    ".git", ".svn", ".hg", ".idea", ".vscode", ".vs", ".DS_Store",
    "__pycache__", "node_modules", "jspm_packages", "bower_components",
    ".nuget", "Packages", "Pods", "DerivedData", ".next", ".svelte-kit",
    ".angular", "typings", ".docusaurus", ".yarn", ".pnp",
    "vendor", "classes", "logs",
}

# Strong project markers
PROJECT_MARKERS = {
    ".cpp": ["CMakeLists.txt", "compile_commands.json"],
    ".py": ["pyproject.toml", "requirements.txt", "setup.py"],
    ".rs": ["Cargo.toml"],
    ".ts": ["tsconfig.json", "package.json"],
    ".js": ["package.json"],
    ".java": ["pom.xml", "build.gradle"],
    ".cs": [".csproj", ".sln"],
}

GET_HIGHLIGHTERS={
    
    ".cpp":CppHighlighter,
    ".hpp":CppHighlighter,
    ".c":CppHighlighter,
    ".h":CppHighlighter,
    ".py":PythonHighlighter,
    ".pyi":PythonHighlighter,
    ".rs":RustHighlighter,
    ".ts":None,
}

"""
@dataclasses.dataclass
class HighLighters:
    
"""




@dataclasses.dataclass
class LspServiceConfig:
    file_ext:str
    lsp_object:typing.Union[None,PyLsp,ClangdLsp,RustAnalyzerLsp]
    lsp_is_active:bool

@dataclasses.dataclass
class EditorServiceConfig:
    file_ext:str
    project_root:typing.Union[str,None]
    highlighter_object:typing.Union[None,CppHighlighter,PythonHighlighter]


@dataclasses.dataclass
class UserProjecs:
    #project_root:str
    lsp:LspServiceConfig

GET_LSPS={
    ".py":PyLsp,
    ".cpp":ClangdLsp,
    ".hpp":ClangdLsp,
    ".c":ClangdLsp,
    ".h":ClangdLsp,
    ".rs":RustAnalyzerLsp,
    ".ts":TypeScriptLsp
}


def getProjectRootsAndProjectDirs(base_path:str) -> dict:
    """Detect project roots in a folder tree"""

    lang_service_configs:dict[str,LspServiceConfig]={}
    project_dirs = {} 

    previous_project_root=None
    for root, dirs, files in os.walk(base_path):
        # --- Skip ignored dirs ---
        clean_dirs = []
        for d in dirs:
            
            if d not in IGNORE_DIRS:
                clean_dirs.append(d)
        dirs[:] = clean_dirs  
              
        #splited_root,splited_dir=os.path.split(root)

        
        """else:
            project_dirs[root]=None 
        """    

        files_set = set(files)


        for lang_ext, markers in PROJECT_MARKERS.items():
            for marker in markers:
                if marker in files_set:
                    try:
                        project_dirs[root]
                        del project_dirs[root]
                        project_dirs[root]=root
                    except KeyError:
                        print("check out pproject scanner.... if print more than one")
                        project_dirs[root]=root

                    if dirs:
                        for dir in dirs:
                            project_dirs[os.path.join(root,dir)]=root 

                    lang_service_configs[root]=LspServiceConfig(file_ext=lang_ext,lsp_object=GET_LSPS[lang_ext],lsp_is_active=False)
                    
                    #deep dir scan
                    #dirs.clear()
                    break
                
                else:
                    if dirs:
                        splited_path,_=os.path.split(root)
                        try:
                            root_path=project_dirs[splited_path]

                            for dir in dirs:
                                project_dirs[os.path.join(root,dir)]=root_path 
                        
                        except KeyError:pass

            if root in lang_service_configs:    
                print("\n\n....breaked....")
                break
            """        
        if previous_project_root :
            print(previous_project_root,"--->>",root)"""

    return lang_service_configs,project_dirs
"""
getProjectRootsAndProjectDirs("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/")
"""
class Lsp_Handler(QObject):

    completionsReady = pyqtSignal(list,str)
    hoverReady = pyqtSignal(object)
    definitionReady = pyqtSignal(object)
    referencesReady = pyqtSignal(object)
    signatureHelpReady = pyqtSignal(object)
    formattingReady = pyqtSignal(object)
    codeActionReady = pyqtSignal(object)
    documentSymbolsReady = pyqtSignal(object)
    workspaceSymbolsReady = pyqtSignal(object)
    diagnosticsReady = pyqtSignal(object)


    def __init__(self):
        super().__init__()
        
        self.pylsp=PyLsp()

        self.running_highlighters:dict[str,list]={
            ".py":[],
            ".pyi":[],
            ".cpp":[],
            ".rs":[],
            ".ts":[]
        }

        self.temp_lsps:dict[str,typing.Union[PyLsp,ClangdLsp,RustAnalyzerLsp,None]]={
            ".py":None,
            ".pyi":None,
            ".cpp":None,
            ".rs":None,
            ".ts":None
        }

        

        self.selected_highlighters={
            ".cpp":None,
            ".py":None,
            ".pyi":None,
            ".rs":None,
            ".ts":None,
            }


        self.editor_services_buffer:dict[Custom.TextEditor,EditorServiceConfig]={}
        self.activated_lsp:typing.Union[ClangdLsp,PyLsp,RustAnalyzerLsp,None]=None
        self.active_project=None
        self.path_h:Path_Handler=None
        
        self.current_minimap_highlighter:typing.Union[None,CppHighlighter,PythonHighlighter]=None
        self.current_minimap_type:str=None
        #user_project:UserProjecs=UserProjecs(project_root=str,lsps=list[Lsp(str,object,bool)])
        #self.user_projects_buffer:dict[UserProjecs]={}
    
    def updateSelectedSntxThemeInConfigs(self,h_ext:str,theme_path:str):

        if os.path.exists(theme_path):
                
            with open(theme_path,"r")as f:
                data:str=f.read()
                #print("ssss dta",data)
                colors=eval(data.splitlines()[0])
            #print(self.selected_highlighters)
            try:
                self.selected_highlighters[colors['language']]=colors
            except:pass

    def saveSelectedSyntxTheme(self,lst):
        with open(lst[0],"w")as f:
            f.write(f"{lst[2].colors}")

        self.selected_highlighters[lst[1]]=lst[2].colors
        self.saveSelectedSyntxThemeAllCongigs()

    def saveSelectedSyntxThemeAllCongigs(self):
        with open(self.path_h.Code.SELECTED_SYNTAX_THEME,"w")as f:
            #f.write(f"{self.selected_highlighters}")
            pass

    
    #def updateSelectedHighlighterDict
    def manageMiniMapHighlighter(self,minimap:Custom.TextEditMinimap,text_editor:Custom.TextEditor,f_ext:str):
        if self.current_minimap_type:
            
            if self.current_minimap_type==f_ext:
                pass

            else:
                self.current_minimap_highlighter.deleteLater()
                print("deletedd past and new hhhh minimap created ")
                self.current_minimap_highlighter=GET_HIGHLIGHTERS[f_ext](minimap.document())
                self.current_minimap_type=f_ext
        
        else:
            print("....new hhhh minimap created ....")

            self.current_minimap_highlighter=GET_HIGHLIGHTERS[f_ext](minimap.document())
            self.current_minimap_type=f_ext
    

    def onOpenProject(self,root:str):
        #self.user_projects_buffer[root]={}
        self.lang_services_config,self.project_dirs=getProjectRootsAndProjectDirs(root)

        self.lang_services_config:dict[str,LspServiceConfig]

        """for k,dir in self.project_dirs.items():
            print(k,"------",dir)
        """

    def onOpenCodeFile(self,file_path,text_editor:Custom.TextEditor,minimap:Custom.TextEditMinimap):
        def single_file():
            print("single file.....")
            project_root=None
            try:
                lsp_process=self.temp_lsps[file_ext]
            except:return
            if lsp_process==None:
                lsp=GET_LSPS[file_ext]
                lsp_process=self.startLsp(lsp,None)
                self.temp_lsps[file_ext]=lsp_process

            self.activated_lsp=lsp_process
       
        splited_path,_=os.path.split(file_path)
        file_ext=file_path[file_path.rfind("."):]
        try:
            project_root=self.project_dirs[splited_path]
            lang_services=self.lang_services_config[project_root]
            project_ext=lang_services.file_ext

            if project_ext==file_ext:    
                if not lang_services.lsp_is_active:

                    lsp_process=self.startLsp(lang_services.lsp_object,project_root)
                    lang_services.lsp_object=lsp_process
                    self.activated_lsp=lsp_process
                    lang_services.lsp_is_active=True
            else:
                single_file()
        
        except KeyError:
            single_file()
        
        #create new highlighter
        print(text_editor.toPlainText())
        highlighter=GET_HIGHLIGHTERS[file_ext](text_editor.document())
        self.running_highlighters[file_ext].append(highlighter)
        self.manageMiniMapHighlighter(minimap,text_editor,file_ext)

        h_colors=self.selected_highlighters[file_ext]
        if h_colors:
            print("changing colors...")
            highlighter.colors=h_colors
            highlighter.setColors()
            highlighter.rehighlight()

        self.editor_services_buffer[text_editor]=EditorServiceConfig(file_ext,project_root,highlighter)

    def onSwitchCodeFile(self,file_path:str,text_editor:Custom.TextEditor,minimap:Custom.TextEditMinimap):
        editor_services=self.editor_services_buffer[text_editor]
        if editor_services.project_root!=None:
            lsp_services=self.lang_services_config[editor_services.project_root]

            #switch lsp        
            self.activated_lsp=lsp_services.lsp_object
        
        else:
            self.activated_lsp=self.temp_lsps[editor_services.file_ext]

        self.manageMiniMapHighlighter(minimap,text_editor,editor_services.file_ext)


        ####################
        """colors=highlighter.colors
        highlighter.deleteLater()

        del highlighter

        highlighter=PythonHighlighter(text_editor.document())
        highlighter.colors=colors
        highlighter.setColors()
        lang_services.highlighter_object=highlighter"""

    def startLsp(self,lsp,root=None):

        lsp_process=lsp(root)

        lsp_process.completions_ready.connect(lambda c,l:self.completionsReady.emit(c,l))
        lsp_process.hover_ready.connect(lambda *arg:self.hoverReady.emit(arg))
        lsp_process.definition_ready.connect(lambda *arg:self.definitionReady.emit(arg))
        lsp_process.references_ready.connect(lambda *arg:self.referencesReady.emit(arg))
        lsp_process.signature_help_ready.connect(lambda *arg:self.signatureHelpReady.emit(arg))
        lsp_process.document_symbols_ready.connect(lambda *arg:self.documentSymbolsReady.emit(arg))
        lsp_process.code_action_ready.connect(lambda *arg:self.codeActionReady.emit(arg))
        lsp_process.diagnostics_ready.connect(lambda msg:print("diagno.. : ",msg))
        
        return lsp_process
    
    def restartLsp(self,file_path):
        splited_path,_=os.path.split(file_path)

        project_root=self.project_dirs[splited_path]
        print("restarted......")
        lsp=self.lang_services_config[project_root]
        print(lsp.lsp_object.process.poll(), " -:poll")

        lsp.lsp_object.process.kill()
        print(lsp.lsp_object.process.poll(), " -:poll")
        
        del lsp.lsp_object

        lsp.lsp_object=GET_LSPS[lsp.file_ext](project_root)
        self.activated_lsp=lsp.lsp_object
        
        self.activated_lsp.completions_ready.connect(lambda c,t:self.completionsReady.emit(c,t))
        self.activated_lsp.hover_ready.connect(lambda *arg:self.hoverReady.emit(arg))
        self.activated_lsp.definition_ready.connect(lambda *arg:self.definitionReady.emit(arg))
        self.activated_lsp.references_ready.connect(lambda *arg:self.referencesReady.emit(arg))
        self.activated_lsp.signature_help_ready.connect(lambda *arg:self.signatureHelpReady.emit(arg))
        self.activated_lsp.document_symbols_ready.connect(lambda *arg:self.documentSymbolsReady.emit(arg))
        self.activated_lsp.code_action_ready.connect(lambda *arg:self.codeActionReady.emit(arg))
        

            
        with open(file_path,"r")as fs:
            text=fs.read()
        self.activated_lsp.did_open(file_path,text)


    def closeProject(self,root:str):pass
    def switchLsp():pass
    def closeLsp():pass



    def didOpen(self,file_path,text):
        self.activated_lsp.did_open(file_path,text)

    def didChange(self, file_path, start_line, start_char, end_line, end_char, new_text):
        self.activated_lsp.did_change(file_path, start_line, start_char, end_line, end_char, new_text)
    
    def requestCompletions(self, file_path, line, column):
        self.activated_lsp.request_completions(file_path, line, column)
    
    def requestHover(self, file_path, line, column):
        self.activated_lsp.request_hover(file_path, line, column)

    def requestDefinition(self, file_path, line, column):
        self.activated_lsp.request_definition(file_path, line, column)
        
    def requestReferences(self, word, file_path, line, column):
        self.activated_lsp.request_references( word, file_path, line, column)

    def requestSignatureHelp(self, file_path, line, column):
        self.activated_lsp.request_signature_help( file_path, line, column)

    def requestFormatting(self, file_path):
        self.activated_lsp.formatting_ready(file_path)

    def requestCodeAction(self, file_path, line, column):
        self.activated_lsp.code_action_ready(file_path, line, column)

    def requestDocumentSymbols(self, file_path):
        
        self.activated_lsp.request_document_symbols(file_path)

    def requestWorkspaceSymbols(self,query):
        self.activated_lsp.request_workspace_symbols(query)





















































































