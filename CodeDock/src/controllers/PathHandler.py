import os
import pathlib 
from PyQt6 import QtGui 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR=BASE_DIR[:BASE_DIR.find('src')-1]
SUPPORTED_IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
SUPPORTED_FILE_FORMATS = ('folder', '.txt','.py', '.pyc', '.pyi','.cpp', '.hpp', '.c', '.h', '.rs', '.ts')

class Path_Handler:
    def __init__(self):

        self.LANG_THEME="white" 
        self.TOOLS_THEME="white"
        
        self.HOME_USER_PATH=os.path.expanduser("~")

        #LANG_DIR=os.path.join(BASE_DIR,"Lang")
        self.TEMP_FILE=os.path.join(BASE_DIR, "cd_temps")
        self.TAB_IMAGE_DIRPATH=os.path.join(BASE_DIR,"tab_image")
        
        self.updateIcon()   
        self.base_dir=BASE_DIR
    
    def updateIcon(self):
        ICONS_DIR=os.path.join(BASE_DIR,"icons")

        USR=os.path.join(BASE_DIR,"usr")

        INCDICATOR_ICONS_DIR=os.path.join(ICONS_DIR,"indicators")

        #ICONS_DIR=os.path.join(BASE_DIR, "icons")
        TOOLS_ICON_DIR=os.path.join(ICONS_DIR,f"{self.TOOLS_THEME}/tools")
        LANG_ICON_DIR=os.path.join(ICONS_DIR,f"{self.LANG_THEME}/coding_lang")
        OTHER_ICON_DIR=os.path.join(ICONS_DIR,f"{self.LANG_THEME}/other")
        KIND_ICON_DIR=os.path.join(ICONS_DIR,f"{self.TOOLS_THEME}/kinds")
        LANG_CONFIG_DIR=os.path.join(BASE_DIR,"Lang")


        self.CODEDOCK_ICON=os.path.join(ICONS_DIR,f"{self.LANG_THEME}/CD_ICON.png")
        self.CODEDOCK_SPLASH_SVG=os.path.join(ICONS_DIR, "cd_icon.svg")
        self.CODEDOCK_SPLASH=os.path.join(ICONS_DIR, "codedock_splash6.png")
        self.CODEBOOK_ICON=os.path.join(ICONS_DIR, "codebook_icon.png")
        
        #self.TEMP_FILE=os.path.join(TEMP_FILE, "tempFilePy.py")
        self.OPEN_FILE_ICON=os.path.join(TOOLS_ICON_DIR, "file_open.png")
        self.SAVE_FILE_ICON=os.path.join(TOOLS_ICON_DIR, "file_save.png")
        self.SETTINGS_ICON=os.path.join(TOOLS_ICON_DIR, "settings.png")
        self.PARAMETER_ICON=os.path.join(TOOLS_ICON_DIR, "stack.png")
        self.COLOR_DIALOG_ICON=os.path.join(TOOLS_ICON_DIR, "paint_tool.png")
        self.LONG_VIEW_CODE=os.path.join(TOOLS_ICON_DIR,"long_view.png")
        self.ZOOM_IN_ICON=os.path.join(TOOLS_ICON_DIR,"zoom_in")
        self.ZOOM_OUT_ICON=os.path.join(TOOLS_ICON_DIR,"zoom_out")
        self.UP_ARROW_ICON=os.path.join(TOOLS_ICON_DIR,"up_arrow")
        self.DOWN_ARROW_ICON=os.path.join(TOOLS_ICON_DIR,"down_arrow")
        self.ADD_SUBWINDOW_ICON=os.path.join(TOOLS_ICON_DIR,"add_window")
        self.AUTO_WINDOW_ARRANGE_ICON=os.path.join(TOOLS_ICON_DIR,"multi_window")
        self.CASCADE_WINDOW_ICON=os.path.join(TOOLS_ICON_DIR,"window")
        self.PAINT_DIALOG_ICON=os.path.join(TOOLS_ICON_DIR,"color_brush")
        self.WEB_BROWSER_ICON=os.path.join(TOOLS_ICON_DIR,"browser.png")

        self.THEME_SDT=os.path.join(USR,"theme_sdt.txt")

        self.CLOSE_RIGHT_ICON=os.path.join(TOOLS_ICON_DIR,"close_right.png")
        self.OPEN_DOWN_ICON=os.path.join(TOOLS_ICON_DIR,"open_down.png")

        self.KEYBOARD_ICON=os.path.join(KIND_ICON_DIR,"keyboard1")
        
        #32X32
        self.ADD_FILE_ICON=os.path.join(KIND_ICON_DIR,"add_file.png")
        self.ADD_FOLDER_ICON=os.path.join(KIND_ICON_DIR,"add_folder.png")
        self.CLOSE_PANEL_ICON=os.path.join(KIND_ICON_DIR,"close_panel.png")
        self.COLLAPS_ICON=os.path.join(KIND_ICON_DIR,"collaps.png")
        self.EXPAND_ICON=os.path.join(KIND_ICON_DIR,"expand.png")
        self.FILTER_ICON=os.path.join(KIND_ICON_DIR,"filter.png")
        self.FOLDER_TREE_ICON=os.path.join(KIND_ICON_DIR,"folder_tree.png")
        self.SYMBOL_TREE_ICON=os.path.join(KIND_ICON_DIR,"symbol_tree.png")

        #lang icons
        self.IMAGE_EXT_ICON=os.path.join(OTHER_ICON_DIR,"image_icn.png")
        self.FOLDER_ICON=os.path.join(OTHER_ICON_DIR,"folder")
        self.TXT_E=os.path.join(OTHER_ICON_DIR,"txt_file.png")
        self.PY_E=os.path.join(LANG_ICON_DIR,"py_icon.png")
        self.C_E=os.path.join(LANG_ICON_DIR,"c_icon.png")
        self.CPP_E=os.path.join(LANG_ICON_DIR,"cpp_icon.png")
        self.CS_E=os.path.join(LANG_ICON_DIR,"csharp_icon.png")
        self.RS_E=os.path.join(LANG_ICON_DIR,"rust_icon.png")
        self.TS_E=os.path.join(LANG_ICON_DIR,"ts_icon.png")

        #kind icons
        #self.CLASS_KIND_ICON=os.path.join(KIND_ICON_DIR,"class")    
        self.CUBE_3_METHOD_KIND_ICON=os.path.join(KIND_ICON_DIR,"3cube.png")
        self.CLASS_KIND_ICON=os.path.join(KIND_ICON_DIR,"class_kind.png")
        self.CUBE_CLASS_KIND_ICON=os.path.join(KIND_ICON_DIR,"cube.png")
        self.FUNCTION_KING_ICON=os.path.join(KIND_ICON_DIR,"function_kind.png")
        self.CONSTRUCTER_KIND_ICON=os.path.join(KIND_ICON_DIR,"construct.png")
        self.FX_FUNCTION_KIND_ICON=os.path.join(KIND_ICON_DIR,"fx_function.png")
        self.METHOD_KIND_ICON=os.path.join(KIND_ICON_DIR,"method.png")
        self.PI_CONSTANT_KIND_ICON=os.path.join(KIND_ICON_DIR,"pi_constant.png")
        self.X_VARIABLE_KIND_ICON=os.path.join(KIND_ICON_DIR,"x_variable.png")
        self.TEXT_KIND_ICON=os.path.join(KIND_ICON_DIR,"keyboard.png")
        
        #others
        self.SYMBOL_REFERENCE_CHAIN_ICON=os.path.join(OTHER_ICON_DIR,"link_chain.png")
        self.SYMBOL_CONNECTION_CHAIN_ICON=os.path.join(OTHER_ICON_DIR,"connection.png")
        
        self.CLOSE_ICON=os.path.join(OTHER_ICON_DIR,"close.png")
        self.MINIMIZE_ICON=os.path.join(OTHER_ICON_DIR,"minimize.png")
        self.MAXIMIZE_ICON=os.path.join(OTHER_ICON_DIR,"maximize.png")

        self.BREAKPOINT_ICON=os.path.join(INCDICATOR_ICONS_DIR,"breakpoint.png")
        self.WARNING_ICON=os.path.join(INCDICATOR_ICONS_DIR,"warning.png")

        self.SYNTAX_HIGHLIGHTER_DIR=os.path.join(LANG_CONFIG_DIR,"Syntax_Themes")
        self.CD_THEMELIST_DIR=os.path.join(LANG_CONFIG_DIR,"CD_Themes")


        self.lang_icons_dict={
            ".jpg":self.IMAGE_EXT_ICON,
            ".jpeg":self.IMAGE_EXT_ICON,
            ".png":self.IMAGE_EXT_ICON,
            ".webep":self.IMAGE_EXT_ICON,
            ".gif":self.IMAGE_EXT_ICON,
            ".bmp":self.IMAGE_EXT_ICON,
    
            "folder":self.FOLDER_ICON,
            ".txt":self.KEYBOARD_ICON,
            ".py":self.PY_E,
            ".pyi":self.PY_E,
            ".pyc":self.PY_E,
            ".c":self.C_E,
            ".cpp":self.CPP_E,
            ".cs":self.CS_E,
            ".rs":self.RS_E,
            ".ts":self.TS_E,
            }

        #self._E=os.path.join(LANG_DIR,"py_icon.png")
        self.COMPLITION_KIND_INCONS_LIST={
            0:QtGui.QIcon(self.KEYBOARD_ICON), 
            3:QtGui.QIcon(self.FUNCTION_KING_ICON),
            6:QtGui.QIcon(self.X_VARIABLE_KIND_ICON),
            7:QtGui.QIcon(self.CLASS_KIND_ICON)
        }
        
        self.SYMBOL_KIND_ICONS_LIST={
            0:QtGui.QIcon(self.TEXT_KIND_ICON),
            5:QtGui.QIcon(self.CUBE_CLASS_KIND_ICON),
            6:QtGui.QIcon(self.METHOD_KIND_ICON),
            9:QtGui.QIcon(self.CONSTRUCTER_KIND_ICON),
            12:QtGui.QIcon(self.FX_FUNCTION_KIND_ICON),
            13:QtGui.QIcon(self.X_VARIABLE_KIND_ICON),
            14:QtGui.QIcon(self.PI_CONSTANT_KIND_ICON),
            8:QtGui.QIcon(self.X_VARIABLE_KIND_ICON),
        }
        
        self.SYMBOL_KIND_NAMES = {
            1: "File",
            2: "Module",
            3: "Namespace",
            4: "Package",
            5: "Class",
            6: "Method",
            7: "Property",
            8: "Field",
            9: "Constructor",
            10: "Enum",
            11: "Interface",
            12: "Function",
            13: "Variable",
            14: "Constant",
            15: "String",
            16: "Number",
            17: "Boolean",
            18: "Array",
            19: "Object",
            20: "Key",
            21: "Null",
            22: "EnumMember",
            23: "Struct",
            24: "Event",
            25: "Operator",
            26: "TypeParameter",
        }



    class CodeDock:
        CONFIG=os.path.join(BASE_DIR,"config")

        WORKSPACE=os.path.join(CONFIG,"workspace/workspace_details.txt")
        WINDOW_TITLEBAR_S=os.path.join(CONFIG,"window_titlebar.txt")
        VIRTUAL_CD_WIDGET_S=os.path.join(CONFIG,"virtual_widget_cd.txt")
        VIRTUAL_CD_TABBAR_S=os.path.join(CONFIG,"virtual_tabbar_cd.txt")
        PREVIEW_TAB_SWITCHER=os.path.join(CONFIG,"preview_tab_switcher.txt")
        
    class Dock:
        CONFIG=os.path.join(BASE_DIR,"Dock/config")
        OTHER=os.path.join(CONFIG,"other.txt")
        PFILE_TREE_S=os.path.join(CONFIG,"file_tree.txt")
        PMAP_TREE_S=os.path.join(CONFIG,"map_tree.txt")
        TABBAR_S=os.path.join(CONFIG,"tabbar.txt")
        TOOLBOX_S=os.path.join(CONFIG,"toolbox.txt")
        TOOL_CONTAINER_S=os.path.join(CONFIG,"tool_container.txt")
        TOOLBUTTON_S=os.path.join(CONFIG,"tool_button.txt")

    class Code:
        CONFIG=os.path.join(BASE_DIR,"Code/config")
        EDITOR_S=os.path.join(CONFIG,"editor.txt")
        EDITOR_NUMPAD_S=os.path.join(CONFIG,"editor_numpad.txt")
        TABBAR_S=os.path.join(CONFIG,"tabbar.txt")
        TOOLBOX_S=os.path.join(CONFIG,"toolbox.txt")
        TOOLBUTTON_S=os.path.join(CONFIG,"tool_button.txt")
        TOOL_CONTAINER_S=os.path.join(CONFIG,"tool_container.txt")
        MDI_S=os.path.join(CONFIG,"mdi.txt")
        MINIMAP_S=os.path.join(CONFIG,"mini_map.txt")
        COMPLITER_S=os.path.join(CONFIG,"compliter.txt")
        CUSTOM_COLOR_THEME=os.path.join(CONFIG,"custom_color_theme.txt")
        SELECTED_SYNTAX_THEME=os.path.join(CONFIG,"selected_themes.txt")
        SELECTED_CD_THEME=os.path.join(CONFIG,"selected_themes.txt")
        DEFAULT_CD_THEME=os.path.join(BASE_DIR,"Lang","CD_Themes","CodeDock Dark")

    def convertPathIntoSystemFormat(self,path:str)->str:
        return str(pathlib.Path(path))
    def getHighlighterColorsFile(self,file_ext:str):
        ...


    def isSupportImgExt(self,f_name):
        
        f_name=f_name[f_name.rfind("."):]
        if f_name in SUPPORTED_IMAGE_FORMATS:
            return True
    
        else: return False
    

    def isSupportFileExt(self,f_name):
        f_name=f_name[f_name.rfind("."):]
        if f_name in SUPPORTED_FILE_FORMATS:
            return True
        else: return False
        
    def getExtensionIcon(self,path,is_full_path=True):
        
        if is_full_path:
            f_str=self.filePathToFileName(path)
        else:
            f_str=path

        extension=f_str[f_str.rfind("."):]
        if extension in self.lang_icons_dict:
            return self.lang_icons_dict[extension]
        else:return None
    
    def filePathToFileName(self,file_path):
        if not file_path:
            return None
        return os.path.basename(file_path)

    def createDummyFile(self,file_path,code):

        with open(f'{self.TEMP_FILE}/{self.filePathToFileName(file_path)}','w')as file:
            file.write(code)
            file.close()
            return f'{self.TEMP_FILE}/{self.filePathToFileName(file_path)}'
        
    def pathJoin(self,path,join_path):
        return os.path.join(path,join_path)    
    

class Dir_Scanner:
    def child_deep_scan(parent_dir):
        child_paths=[]
        for root,_,files in os.walk(parent_dir):
            for file in files:
                child_paths.append(os.path.join(root, file))
        return child_paths
    def child_scan(parent_dir):
        return os.listdir(parent_dir)
    