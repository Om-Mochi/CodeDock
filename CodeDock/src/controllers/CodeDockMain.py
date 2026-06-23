from PyQt6 import QtCore, QtGui, QtWidgets

from CodeDock.C_Widgets.Custom import Custom

from CodeDock.Code.src.controllers.CodeMain import Code_Main
from CodeDock.Code.src.controllers.CodePadHighlighter import PythonHighlighter,SignatureHighlighter
from CodeDock.Dock.src.controllers.DockMain import Dock_Main
from CodeDock.DockingSystem.core.SettingsManager import DockWidgetStyle

from CodeDock.src.controllers.CodeDockSettings import Code_Dock_Settings
from CodeDock.src.controllers.CodeDockKeysHandler import Code_Dock_Key_Handler
from CodeDock.src.controllers.PathHandler import Path_Handler,Dir_Scanner
from CodeDock.src.controllers.SettingDialogWidgets import Setting_Dialog_Widgets
from CodeDock.src.controllers.CDLoader import CDLoader

from CodeDock.src.views.ThemeListUiDialog import ThemeListerWidget

from CodeDock.DockingSystem import DockingSystem

from CodeDock.Lang.LspHandler import Lsp_Handler
from CodeDock.Lang.L_py.PyTags import PyLsp
from CodeDock.Lang.L_cpp.CppLSP import ClangdLsp
from CodeDock.src.controllers.TabSwitcher import Tab_V_Switcher,Ui_Tab_Switcher,BasicTabSwitcher

#from CodeDock.Lang.L_rs.RustLsp import RustLsp
#from CodeDock.Lang.L_ts.LspTypeScript import TsLsp

import time
import os

class Code_Dock_Main(Code_Dock_Settings):
    def __init__(self,app):

        from CodeDock.src.controllers.WorkSpaceHandler import WorkSpace_Handler

        Code_Dock_Settings.__init__(self)
        
        self.MainWindow.setStyleSheet("background-color:black;")
        self.app=app


        self.get_loader={
            "syntax_theme":self.loadSyntaxThemes,
            "completer":self.loadCompleterSettings,
            "editor_textedit":self.loadTextEditorSettings,
            "minimap":self.loadMiniMapSettings,
            "dock_widgets":self.loadDockWidgetSettings,
            "tabbar":self.loadCodeTabbar,
            "main_window_titlebar":self.loadWindowTitleBarSettings,
            "file_tree":self.loadPanelFileTreeSettings,
            "symbol_tree":self.loadPaneSymbolTreeSettings,
            "tool_box":self.loadToolBoxWindgetSsttings,
            "tool_button":self.loadToolButtonSettings,
        }

        #self.lsp_handler=Lsp_Handler()
        
        
        #self.tslsp=TsLsp(os.path.dirname("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/test_ts/"))
        
        #self.clangd=ClangdLsp("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tmp3jou25k_/")
        
        #self.rust_lsp=RustLsp()

        self.worker=None
        #self.MainWindow.show()
        
        self.workspace_buffer=[]

        self.virtual_desk_list=[]

        self.Path_h = Path_Handler()        
        self.windowSplash()
        
        
        #self.Code = Code_Main(self.app)
        #self.Dock = Dock_Main()
        #self.lsp_handler=None


        self.MainWindow.titlebar.close_button.setIcon(QtGui.QIcon(self.Path_h.CLOSE_ICON))
        self.MainWindow.titlebar.maximize_button.setIcon(QtGui.QIcon(self.Path_h.MAXIMIZE_ICON))
        self.MainWindow.titlebar.minimize_button.setIcon(QtGui.QIcon(self.Path_h.MINIMIZE_ICON))
        
        self.virtual_CD.tab_add_btn.setIcon(QtGui.QIcon(self.Path_h.ADD_SUBWINDOW_ICON))
        self.virtual_CD.whenVirtualTabAdd.connect(self.createVirtualSpace)
        self.virtual_CD.whenVirtualTabChange.connect(self.VirtualDeskChange)


        self.virtual_session_handler=WorkSpace_Handler.Store.VirtualSpace()
    
        self.virtual_session_handler.setStorageDir(self.Path_h.CodeDock.WORKSPACE)
        self.virtual_running_index=0

        self.basic_tab_switcher=BasicTabSwitcher()        
        self.basic_tab_switcher.set_current_change=True
        self.basic_tab_switcher.whenTabSelectedText.connect(self.onCDThemeSelected)
        self.ver=1

        #self.virtual_session_buffer=self.virtual_session_handler.createNewVirtualStorageBuffer()
        #self.virtual_session_buffer=self.virtual_session_handler.getBuffer()
        #self.Code.lsp_server=self.pylsp


        #self.Code.whenSubWindowEditorAdded.connect(self.onSubWindowEditorAdded)
        #self.Code.whenSubWindowSwitch.connect(self.onSubWindowSwitche)
        ##################################\\\\\\\\\\\\\\\\\\
        
        #self.virtual_desk_list.append([self.main_widget,self.Dock,self.Code,self.lang_handler,self.virtual_session_buffer])
        #self.MainWindow.titlebar.add_virtual_desk_btn.clicked.connect(self.VirtualStart)
        #self.MainWindow.titlebar.connect_virtual_button=self.VirtualDeskChange
        
        self.MainWindow.titlebar.h_layout.insertWidget(1,self.virtual_CD)
        
        
        #self.Dock.main_frame.setParent(self.splitter)
        #self.Code.main_frame.setParent(self.splitter)

        # self.Dock.Panel.Fpaths=self.Path
        # self.Code.Fpaths=self.Path
        
        #self.Dock.Panel.setIconsInFileMode()
        #self.Dock.file_open_btn.clicked.connect(self.sendDocumentSymbolsRequest)
        # self.file_open_btn.clicked.connect(lambda:self.openCodeFile(True))
        # self.settings_btn.clicked.connect(self.openSettingsUi)
        # self.color_widget_btn.clicked.connect(self.openColorDilaogLive)
        # self.color_dialog_open.clicked.connect(self.openColorDialog)

        #self.Code.auto_subwindow_arrange_btn.clicked.connect(self.Code.mdi_area.tileSubWindows)
        #self.MainWindow.whenResize.connect(lambda x:self.Code.mdi_area.tileSubWindows())
        #self.Dock.settings_btn.clicked.connect(self.openSettingWidget)
        #self.Dock.color_dialog_open.clicked.connect(self.openThemeWidget)
        # self.zoom_in_btn.clicked.connect(self.zoomInEditor)
        # self.zoom_out_btn.clicked.connect(self.code.zoomOutEditor)


        # call this method when enterkey clicked in editor.
        #self.Dock.Panel.on_double_click_file_tree=lambda flag,f_path:(self.Code.openUrlSubwindow(f_path))
        #self.Dock.connect_map_items=lambda line_no:(self.Code.jumpTagsInEditor(line_no),print(line_no))
        
        #self.Code.whenKeyEnterPressedInTextEdit.connect(self.sendDocumentSymbolsRequest)
        #self.tslsp.completions_ready.connect(self.setComplitionsList)
        #self.clangd.completions_ready.connect(self.setComplitionsList)
        #self.clangd.completion_ready.connect(self.setComplitionsList)
        #self.rust_lsp.completions_ready.connect(self.setComplitionsList)
        self.loadWindowTitleBarSettings()
        
        #WorkSpace_Handler.ReStore.ReStoreWorkSpace.loadAll(self)
        self.virtual_CD.tab_add_btn.click()

        

                
        #self.createVirtualSpace()
        self.loadPreviewTabSwitcher()


        #self.clangd.completions_ready.connect(self.setComplitionsList)
        #self.pylsp.completions_ready.connect(self.setComplitionsList)
        #self.Code.zoom_in_btn.clicked.connect(lambda:Setting_Dialog_Widgets().openFontDialog(self.Code.textedit_code_editor,self.Code.configCodeEditor))
        #self.Code.up_arrow_btn.clicked.connect(lambda:(self.virtual_session_handler.storeIt()))
        #self.loadPanelTreeS()
        #self.loadToolBoxS()
        #self.loadCodeTabbar()
        #self.loadDockTabbar()
        
        #sub=self.Code.openUrlSubwindow("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py")
        
        #sub.showMaximized()
        
        self.main_splitter.setSizes([100,700])
        #self.loadEditorSettings()
        #self.MainWindow.installEventFilter(self)  # Install event filter
        #def VirtualOpen(self,index):
        self.hover_pop_pos=None
        
        #self.pylsp.hover_ready.connect(lambda x:print(x))
        


        #self.pylsp.request_document_symbols("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py")
        #self.pylsp.request_hover("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15,1)
        #self.pylsp.request_definition("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15, 7)
        
        #self.pylsp.request_references("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15, 7)
        #self.pylsp.request_signature_help("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15, 1)
        #self.pylsp.code_action_ready("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 0, 19)
        
        self.hover_popup_highlighter=PythonHighlighter(self.hover_popup.popup_text_edit.document())

        self.signature_popup=Custom.PopupSignature()
        #self.Code.linkCodeThemeOther(o_highlighter=self.signature_popup.highlighter)
        self.disable_document_symbol_kind=[2]
        #parent_list=[]        
        #same index(len) every list
        self.document_symbols_l=[]
        self.symbol_start_lineno=[]
        self.symbol_end_lineno=[]

        #self.Dock.Panel.setStyleSheet(self.Code.tabbar_editor.styleSheet())
        

        self.last_cusror=None
        self.inputBar()
        self.findInputBar()


        #self.MainWindow.when_Ctrl_pressed.connect(lambda :self.Code.running_subwindow.titlebar.setSmoothDrag(False))
        #self.MainWindow.when_Ctrl_release.connect(lambda :self.Code.running_subwindow.titlebar.setSmoothDrag(True))
        self.MainWindow.when_Ctrl_f_pressed.connect(self.showFindInputBar)
        self.MainWindow.when_Ctrl_g_pressed.connect(self.showGoToInputBar)
        self.MainWindow.when_Esc_pressed.connect(self.hideGoToInputBar)
        self.MainWindow.when_Ctrl_l_pressed.connect(lambda:(self.lsp_handler.restartLsp(self.Code.codefile_path)))

        self.MainWindow.when_Ctrl_w_pressed.connect(lambda:self.Code.subWinWebBrowser())
        self.MainWindow.when_Ctrl_n_pressed.connect(lambda:self.Code.add_subwindow_btn.click())
        self.MainWindow.when_Ctrl_t_pressed.connect(lambda:self.popUpTabSwitcher())

        self.cd_icon_as_loader=CDLoader.ThreadedFadeColorSVGLoader(34,20)
        self.cd_icon_as_loader.setSvgAndInit(self.Path_h.CODEDOCK_SPLASH_SVG)
        self.MainWindow.titlebar.h_layout.insertWidget(0,self.cd_icon_as_loader)
        self.Code.up_arrow_btn.clicked.connect(self.testLoadThreadStart)
        self.MainWindow.titlebar.h_layout.insertWidget(4,self.Dock.frame_toolbox)



        #self.MainWindow.titlebar.grid_layout.setColumnStretch(0,0)
        
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(1,5)
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(2,10)
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(3,20)
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(4,20)
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(5,1)
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(6,1)
        #self.MainWindow.titlebar.grid_layout.setColumnStretch(7,1)
            
        #self.Code.mini_map.setReadOnly(False)
        #self.onCDThemeSelected()

    def popupSignature(self,sig):
        # Assume this is called when you receive signatureHelp response from LSP
        print(sig)
        self.signature_popup.setSignature(sig, self.Code.running_textedit_editor)
        pass

    def onOnlyAplphaNemuricKeyPressed(self,charecter):
        print("char - ",charecter)
        self.workerRequestComplition(charecter)
        
        #self.Code.startMiniMapDeboucingTimer()

    def testLoadThreadStart(self):
        #self.test_wtread=CDLoader.LongTaskTestThread()
        #self.test_wtread.start_loader.connect(self.cd_icon_as_loader.start_animation())
        #self.test_wtread.stop_loader.connect(self.cd_icon_as_loader.stop_animation())
        self.cd_icon_as_loader.start_animation()

    def onProjectRootSetedInFileModel(self,root):
        self.lsp_handler.onOpenProject(root)

    def onSubWindowEditorAdded(self):
        #self.loadTextEditorSettings()
        #self.loadDockWidgetSettings()
        self.Code.style_editor.applyStyle(self.Code.textedit_code_editor)
        self.Code.textedit_code_editor.update()
        
        self.Code.textedit_code_editor.notifyOnKeyStrock.connect(self.Code.autoSaveCodeFile)
        
        self.Code.subwindow_session_handler.setObjects(self.virtual_session_buffer,self.Code.subwindow_index_id,self.Code,self.Code.subwindow,self.Code.textedit_code_editor,self.Path_h)
        self.Code.subwindow_session_handler.storeBuf()
        
        if self.Code.codefile_path:
        
            self.Code.textedit_code_editor.whenOnlyAplphaNemuricKeyPressed.connect(self.onOnlyAplphaNemuricKeyPressed)
            self.Code.textedit_code_editor.whenGoToDefinitionRequest.connect(
                lambda w,l,c,p:(
                self.lsp_handler.requestDefinition(self.Code.codefile_path,l,c))
            )
            #self.Code.textedit_code_editor.whenLinePosChangeGetLineNo.connect(lambda x:self.Code.running_subwindow.titlebar.block_path_navigation_bar.setBlockSymbols((self.getSymbolsParentBlocksName(x))))
            
            self.Code.textedit_code_editor.whenMouseCursorTextMatch.connect(self.sendHoverRequest)
            self.Code.textedit_code_editor.whenMouseCursorNoTextMatch.connect(lambda:self.hover_popup.hide())
            
            self.Code.textedit_code_editor.whenMouseCursorLeaveHover.connect(self.whenCursorLeaveHover)
            
            self.Code.textedit_code_editor.when_Key_SHIFT_F12_Pressed.connect(self.sendReferenceRequest)        
                
            self.lsp_handler.onOpenCodeFile(self.Code.codefile_path,self.Code.textedit_code_editor,self.Code.mini_map)

            #self.sendDocumentSymbolsRequest()

            with open(self.Code.codefile_path,"r")as fs:
                text=fs.read()
            self.lsp_handler.didOpen(self.Code.codefile_path,text)

            self.Code.textedit_code_editor.whenCompletionInsert.connect(self.onCompletionInserted)
            self.Code.textedit_code_editor.when_Key_Ctrl_BackSpace_Pressed_V2.connect(self.onCompletionInserted)
            self.Code.textedit_code_editor.whenAutoPair.connect(self.onCompletionInserted)
            self.Code.textedit_code_editor.when_Key_Enter_Pressed_V2.connect(self.onCompletionInserted)
        
        self.loadCompleterSettings()
        #print(self.virtual_session_buffer)

    def onCompletionInserted(self,s_line,start_col,e_line,end_col,completion):
        print("....complition....inserted....")
        line_text = self.Code.running_textedit_editor.document().findBlockByNumber(
            s_line
        ).text()

        print("LINE:", repr(line_text))

        print("|sline : ",s_line,"|scol :",start_col,"|eline : ",e_line,"|e_col : ",end_col,"|com : ",completion)

        self.lsp_handler.didChange(self.Code.codefile_path,s_line,start_col,e_line,end_col,completion)

    def sendReferenceRequest(self):
        word,line,column,pos=self.Code.running_textedit_editor.getWordUnderCursorDetail()
        self.lsp_handler.activated_lsp.request_references(word,self.Code.codefile_path,line,column)
        
    def goToRefranceWindow(self,refrence):
            print(refrence)
            self.Code.refrenceDisplaySubWindow("test-0000")
            result=refrence[0]["result"]
            last_path=None
            textedit=QtWidgets.QPlainTextEdit()
            doc=textedit.document()
            final_refrence_buffer=[]
            for refrence_data in result:

                file_path=refrence_data["uri"]
                file_path=file_path.replace("file://","")
                line_column=refrence_data["range"]["start"]
            
                if file_path!=last_path:

                    if final_refrence_buffer:
                        #print(final_refrence_buffer)

                        self.Code.addRefrenceGroup(final_refrence_buffer)
                    final_refrence_buffer.clear()
                    
                    with open(file_path,"r")as file:
                        file_text=file.read()
                        file.close()

                    textedit.setPlainText(file_text)    
                    last_path=file_path
                    final_refrence_buffer.append(self.Path_h.filePathToFileName(file_path))
                    final_refrence_buffer.append(file_path)

                    
                block=doc.findBlockByNumber(line_column["line"])
                if block.isValid():
                    line_text=block.text()
                    line_text=line_text.lstrip()

                
                final_refrence_buffer.append([line_text,line_column["line"],line_column["character"]])
                
            if final_refrence_buffer:
                #print(final_refrence_buffer)
                self.Code.addRefrenceGroup(final_refrence_buffer)


    def goToDefinition(self,definition_result):
        print(definition_result)
        results=definition_result[0]['result']
        total_result=len(results)
        
        #print(results)

        if total_result==1:
            d_path=results[0]["uri"]
            d_range=results[0]["range"]
            d_line=d_range["start"]["line"]
            d_column=d_range["start"]["character"]
            
            d_path=d_path.replace("file://","")
            
            if d_path==self.Code.codefile_path:
                self.Code.running_textedit_editor.set_cursor_position(d_line,d_column,True)
            else:    

                if self.Code.isSubWindowHere(d_path):
                    
                    self.Code.setSubWindowActiveViaPath(d_path)
                    self.Code.running_textedit_editor.set_cursor_position(d_line,d_column,True)
                    #print("okokokokok",self.Code.running_textedit_editor.windowTitle())
                
                else:
                    self.Code.openUrlSubwindow(d_path)
                    self.Code.running_textedit_editor.set_cursor_position(d_line,d_column,True)
                

    def whenFindInputBarTextReturn(self):
        text=self.find_inp_bar.find_input_box.text()
        #self.cursor_list=self.Code.textedit_code_editor.highlight_matching_words(text)
        #self.c_index=0
        self.Code.running_textedit_editor.on_find_text_changed(text)

    def whenFindInputBarEntreReturn(self):
        """if 0<len(self.cursor_list):    
            cursor = self.Code.running_textedit_editor.textCursor()
            f_cursor=self.cursor_list[self.c_index]
            cursor.setPosition(f_cursor.position())
            self.Code.running_textedit_editor.setTextCursor(cursor)
            self.Code.textedit_code_editor.highlight_cursor(f_cursor)
            self.c_index+=1
"""     
        text=self.find_inp_bar.find_input_box.text()
        print(text)
        if text:
            try:
                finded_index,total_words=self.Code.running_textedit_editor.find_word_and_focus(text)
            except:
                self.Code.running_textedit_editor.clear_highlighted_words()
                total_words=None
                pass
        else:total_words=None
        if total_words!=None:    
            self.find_inp_bar.spin_box.setValue(finded_index)
            self.find_inp_bar.spin_box.setRange(1,total_words)
            self.find_inp_bar.out_of_label.setText(f"of {total_words}")
        else:total_words=None
        
    def hideGoToInputBar(self,set_cursor_last_pos=False):

        if set_cursor_last_pos==False:
            self.input_box.hide()
        else:        
            cursor=self.Code.running_textedit_editor.textCursor()
            cursor.setPosition(self.last_cusror)
            self.Code.running_textedit_editor.setTextCursor(cursor)
            self.Code.running_textedit_editor.setFocus()
            self.input_box.hide()

    def showGoToInputBar(self):
        self.last_cusror=self.Code.running_textedit_editor.textCursor().position()
        #print("save: ",self.last_cusror)
        self.input_box.show()
        self.input_box.clear()
        self.input_box.setFocus()
        
    def showFindInputBar(self):
        self.find_inp_bar.show()
        self.find_inp_bar.find_input_box.setFocus()
    
        
    def inputBar(self):
        self.input_box=Custom.GoToInputBar()
        self.input_box.setPlaceholderText("Go To")
        self.input_box.setFixedWidth(100)

        self.MainWindow.titlebar.bars_layout.addWidget(self.input_box)
        self.input_box.hide()
        
        self.input_box.returnPressed.connect(lambda:self.whenGoToInputBoxReturn(True))
        self.input_box.textChanged.connect(lambda:(self.whenGoToInputBoxReturn(),self.input_box.setFocus))
        self.input_box.returnPressed.connect(lambda:self.input_box.hide())
        self.input_box.when_Esc_KeyPressed.connect(lambda:self.hideGoToInputBar(set_cursor_last_pos=True))
    

    
    def findInputBar(self):
        self.find_inp_bar=Custom.FindInputBar(self.MainWindow.titlebar)
        self.find_inp_bar.spin_box.setValue(0)
        self.find_inp_bar.spin_box.setRange(0,0)
        self.find_inp_bar.out_of_label.setText("of 0")

        self.find_inp_bar.hide()
        self.MainWindow.titlebar.bars_layout.addWidget(self.find_inp_bar)
        self.find_inp_bar.find_input_box.returnPressed.connect(self.whenFindInputBarEntreReturn)
        self.find_inp_bar.find_input_box.textChanged.connect(self.whenFindInputBarTextReturn)
        self.find_inp_bar.find_input_box.textChanged.connect(self.whenFindInputBarEntreReturn)
        


    def whenGoToInputBoxReturn(self,set_cursor=False):
        
        try:
            line_no=int(self.input_box.text())
            if line_no.is_integer():
                self.Code.running_textedit_editor.goToLine(line_no,set_cursor)
        except:pass

    def whenCursorLeaveHover(self):    
        self.hover_popup.hide()
    
    def sendDocumentSymbolsRequest(self):
        #print(self.Code.dummy_codefile_path)
        self.lsp_handler.requestDocumentSymbols(self.Code.codefile_path)
    

    
    def getSymbolsParentBlocksName(self,line_no):
        
        low=0
        high=len(self.symbol_start_lineno)-1
        last_line=0
        block_symbol_list=[]
        final_inedx=None

        while low<=high:
            mid_i=(high+low)//2
            final_lineno=None

            is_end_passed=bool

            final_inedx=None
            #rev_i=high-low
            if line_no==self.symbol_start_lineno[mid_i]:
                
                final_inedx=mid_i
                break
            elif line_no > self.symbol_start_lineno[mid_i]:
                low=mid_i+1
                
                if self.symbol_end_lineno[mid_i]>=self.symbol_end_lineno[mid_i]:
                    is_end_passed=False
                else:is_end_passed=True

                final_lineno=self.symbol_start_lineno[mid_i]
                final_inedx=mid_i
                #last_line=self.symbol_line_no_l[mid_i]

            elif line_no < self.symbol_start_lineno[mid_i]:
                high=mid_i-1
                
                if self.symbol_end_lineno[mid_i]>=self.symbol_end_lineno[mid_i]:
                    is_end_passed=False
                else:is_end_passed=True
                
                final_lineno=self.symbol_start_lineno[mid_i-1]   
                #last_line=self.symbol_line_no_l[mid_i]
                final_inedx=mid_i-1


        #final_i done
        if final_inedx!=None:
                
            for i in range(10):
                
                symbol_list=self.document_symbols_l[final_inedx]

                #print(symbol_list)
                if symbol_list[2]==None:
                    #print("parent : ",symbol_list[0])
                
                    
                    block_symbol_list.append([symbol_list[0],self.Path_h.SYMBOL_KIND_ICONS_LIST[symbol_list[3]]])
                    break

                else:
                    #print(symbol_list[0], symbol_list[1])
                    #print("index ",symbol_list[2])

                    if not is_end_passed:
                        block_symbol_list.append([symbol_list[0],self.Path_h.SYMBOL_KIND_ICONS_LIST[symbol_list[3]]])
                    final_inedx=symbol_list[2]

            return block_symbol_list
  

    def setDocumentSymbol(self,symbols):
        
        self.Dock.Panel.map_model.clear()

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n.............................")
        print(symbols)

        symbols=symbols[0]['result']
        print(symbols,"........")
        parent_list=[]
        #parent_list.append([item,name,container_name,line_no,index])
        #print("lenth ",len(symbols))
        #same index(len) every list
        item_l=[] #[[item,index],....n]]
        name_l=[]
        container_name_l=[]
        line_no_l=[]
        parent_index=0
        self.document_symbols_l.clear()
        self.symbol_start_lineno.clear()
        self.symbol_end_lineno.clear()

        for index,symbol in enumerate(symbols):
            print(symbol)
            name=symbol['name']
            container_name=symbol['containerName']
            starting_line_no=symbol['location']['range']['start']['line']
            ending_line_no=symbol['location']['range']['end']['line']
            #print(name,container_name ,":.......name")
            
            kind=symbol['kind']

            len_name_l=len(name_l)-1
        
            """if name==self.last_name_l[index] and container_name==self.last_container_name_l[index]:
                continue"""

            
            if kind in self.disable_document_symbol_kind:
                continue
        
            #print(symbol)
            #print(symbol,"\n\n")

            #print(f"{name}-->{container_name}  kind:{kind}")
            
            if container_name==None:
                #print(name)
                item=QtGui.QStandardItem()
                item.setIcon(self.Path_h.SYMBOL_KIND_ICONS_LIST[kind])
                item.setText(name)
                item.setEditable(False)
                self.Dock.Panel.map_model.appendRow(item)
                #parent_list.append([item,name,container_name,line_no,index])
                

                item_l.clear()
                name_l.clear()
                
                if kind in [5,6,12]:     
                    self.symbol_start_lineno.append(starting_line_no)
                    self.symbol_end_lineno.append(ending_line_no)
                    
                    self.document_symbols_l.append([name,container_name,None,kind])
                    item_l.append([item,parent_index])
                    name_l.append(name)
                    line_no_l.append(starting_line_no)
                    parent_index+=1
                #container_name_l.append(container_name)
                continue

            for i,parent_name in enumerate(name_l[::-1]):
                
                rev_i=(len_name_l)-i
                if container_name==parent_name:
                    item=QtGui.QStandardItem()
                    item.setIcon(self.Path_h.SYMBOL_KIND_ICONS_LIST[kind])
                    item.setText(name)
                    item.setEditable(False)
                    
                    item_l[rev_i][0].appendRow(item)
                    
                    if kind in [5,6,12]:    
                        parent_index+=1
                        item_l.append([item,parent_index])
                        name_l.append(name)
                        line_no_l.append(starting_line_no)
                        
                        self.symbol_start_lineno.append(starting_line_no)
                        self.symbol_end_lineno.append(ending_line_no)
                        #[ name, contaimer_name, container index]
                        self.document_symbols_l.append([name,container_name,item_l[rev_i][1],kind])

                    if container_name not in container_name_l:
                        container_name_l.append(container_name)
                
                else:
                    pass
                    #print("pop -------------------- : ",name_l[rev_i])
                    #item_l.pop(rev_i)
                    #name_l.pop(rev_i)


    def sendGoToDefinitionRequest(self):pass
    


    def sendHoverRequest(self,word,line,col,pos):
        self.hover_pop_pos=pos
        #self.lsp_handler.activated_lsp.request_hover(self.Code.codefile_path,line,col)

    
    def popupHover(self,hover_data):
        print("hover data ",hover_data)
        result=hover_data[0]['result']
        #print(result)
        if  result['contents']=='':
            self.hover_popup.hide()
            return
        
        value=result['contents']['value']
        if value=='':
            self.hover_popup.hide()
            return
        
        value=value.replace("```python","")
        value=value.replace("```","")
        #print("vavavav ",value)
        self.hover_popup.show_popup(value,self.hover_pop_pos)
        
                

    
    def VirtualDeskChange(self,index):
        self.virtual_running_index=index
        self.main_widget.hide()
        self.gridLayout_centralw.removeWidget(self.main_widget)
        self.main_widget=self.virtual_desk_list[index][0]
        self.lsp_handler=self.virtual_desk_list[index][3]
        self.Dock=self.virtual_desk_list[index][1]
        self.Code=self.virtual_desk_list[index][2]
        self.virtual_session_buffer=self.virtual_desk_list[index][4]
        self.dock_session_handler=self.virtual_desk_list[index][5]
        self.main_splitter=self.virtual_desk_list[index][6]
        
        #self.settingDialogUpdateObj()
        self.gridLayout_centralw.addWidget(self.main_widget,0,0)
        
        self.main_widget.show()

    def createVirtualSpace(self):
        from CodeDock.src.controllers.WorkSpaceHandler import WorkSpace_Handler
        self.main_widget.hide()
        self.gridLayout_centralw.removeWidget(self.main_widget)
        
        self.main_widget = QtWidgets.QWidget()
        #self.main_widget.setObjectName("main_widget")
        self.gridLayout_mainw = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout_mainw.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_mainw.setSpacing(0)
        self.gridLayout_mainw.setObjectName("gridLayout_3")
        
        self.main_splitter = Custom.Splitter(parent=self.main_widget)
        
        #self.splitter.setStyleSheet("background-color:black;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_splitter.sizePolicy().hasHeightForWidth())
        self.main_splitter.setSizePolicy(sizePolicy)
        self.main_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.main_splitter.setObjectName("splitter")
        self.main_splitter.setSizes([100, 700])
        self.main_splitter.setContentsMargins(0,0,0,0)

        #self.splitter.setStyleSheet("background-color:white;")
    
        self.main_splitter.setStyleSheet("""

            
            Splitter::handle {
                background-color: #4d5e5a;   /* Dark color */
                
            }
            QSplitter::handle:horizontal {
                width: 2px;               /* Thicker horizontally */
            }
            QSplitter::handle:vertical {
                height: 3px;              /* Thicker vertically */
            }
                            

            QSplitter::handle:hover {
                background-color:  #699595;   /* Dark color */
                   /* Outline */
            }
	    
	        QSplitter::handle:pressed{
                background-color:  #b4ffff;   /* Dark color */
                   /* Outline */
            }
	    
        
        """)

        self.gridLayout_centralw.setSpacing(0)
        self.gridLayout_mainw.setSpacing(0)



        self.gridLayout_mainw.addWidget(self.main_splitter, 0, 0, 1, 1)
        self.gridLayout_centralw.addWidget(self.main_widget, 0, 0, 1, 1)
        
        
        
        self.lsp_handler=Lsp_Handler()
        self.lsp_handler.path_h=self.Path_h
        self.lsp_handler.completionsReady.connect(self.setComplitionsList)

        self.lsp_handler.hoverReady.connect(self.popupHover)
        self.lsp_handler.definitionReady.connect(self.goToDefinition)
        self.lsp_handler.referencesReady.connect(self.goToRefranceWindow)
        self.lsp_handler.signatureHelpReady.connect(self.popupSignature)
        self.lsp_handler.documentSymbolsReady.connect(lambda x:self.setDocumentSymbol(x))
        self.lsp_handler.codeActionReady.connect(lambda x: print(f"Hover: {x}"))
        


        self.Code = Code_Main(self.app)
        self.Dock = Dock_Main()

        #self.Code.subWinWidgets(DockingSystem.MainWindow(),"Test Docking")
        #self.Dock.frame_toolbox.addToolButton(self.Code.zoom_in_btn)
        #self.Dock.frame_toolbox.addToolButton(self.Code.zoom_out_btn)
        #self.Dock.frame_toolbox.addToolButton(self.Code.up_arrow_btn)
        #self.Dock.frame_toolbox.addToolButton(self.Code.down_arrow_btn)
        self.Dock.frame_toolbox.addToolButton(self.Code.add_subwindow_btn)
        self.Dock.frame_toolbox.addToolButton(self.Code.web_browser_btn)
        self.Dock.frame_toolbox.addToolButton(self.Code.auto_subwindow_arrange_btn)

        self.Dock.frame_toolbox.setParent(None)
        
        self.Dock.Panel.whenProjectRootSetedInFileModel.connect(self.onProjectRootSetedInFileModel)


        self.Dock.Panel.setPathUrlInFileModel(self.Path_h.base_dir)

        
        self.Code.frame_toolbox.hide()

        DockWidgetStyle.textEditThemeUpdate.whenUpdateDock.connect(self.loadTextEditorSettingsByObj)
        #self.Path_h = Path_Handler()
        self.virtual_session_buffer=self.virtual_session_handler.createNewVirtualStorageBuffer()
        #self.virtual_session_buffer=self.virtual_session_handler.getBuffer()
        self.dock_session_handler=WorkSpace_Handler.Store.DockViews()
        
        self.dock_session_handler.addBuffer(self.virtual_session_buffer)
        #self.dock_session_handler.getBuffer()
        self.dock_session_handler.storeIt(self)
        
        self.main_splitter.splitterMoved.connect(lambda _:self.dock_session_handler.storeIt(self))
        
        self.virtual_desk_list.append([self.main_widget,self.Dock,self.Code,self.lsp_handler,self.virtual_session_buffer,self.dock_session_handler,self.main_splitter])
        
        self.Code.lsp_server=self.lsp_handler

        self.Dock.main_frame.setParent(self.main_splitter)
        self.Code.main_frame.setParent(self.main_splitter)
        
        self.Code.whenMiniMapRefresh.connect(lambda:(self.loadSyntaxThemes()))
        self.Code.whenSubWindowEditorAdded.connect(self.onSubWindowEditorAdded)
        self.Code.whenSubWindowSwitch.connect(self.onSubWindowSwitche)
        # self.Dock.Panel.Fpaths=self.Path
         # self.Code.Fpaths=self.Path
        self.Dock.Panel.setIconsInFileMode()
    
        # self.file_open_btn.clicked.connect(lambda:self.openCodeFile(True))
        # self.settings_btn.clicked.connect(self.openSettingsUi)
        # self.color_widget_btn.clicked.connect(self.openColorDilaogLive)
        # self.color_dialog_open.clicked.connect(self.openColorDialog)
        
        self.Code.add_subwindow_btn.clicked.connect(lambda: self.Code.addSubWindowEditor())

        self.Code.auto_subwindow_arrange_btn.clicked.connect(self.Code.mdi_area.tileSubWindows)
        #self.MainWindow.whenResize.connect(lambda x:self.Code.mdi_area.tileSubWindows())
        self.Dock.settings_btn.clicked.connect(self.openSettingWidget)
        #self.Dock.color_dialog_open.clicked.connect(self.openThemeWidget)
        # self.zoom_in_btn.clicked.connect(self.zoomInEditor)
        # self.zoom_out_btn.clicked.connect(self.code.zoomOutEditor)

        # call this method when enterkey clicked in editor.
        self.Dock.Panel.on_double_click_file_tree=lambda flag,f_path:(self.Code.dock_zone.onPathUrlDropped(f_path))
        self.Dock.connect_map_items=lambda line_no:(lambda:print("jump symbols"))
        self.Code.onEnterKeyEditor = self.onEnterKeyInEditor
        
        #self.Code.onTypeInEditor=self.workerRequestComplition
        
        self.Code.up_arrow_btn.clicked.connect(lambda:(self.virtual_session_handler.storeIt()))

        self.Code.down_arrow_btn.clicked.connect(lambda:(self.lsp_handler.restartLsp(self.Code.codefile_path)))

        #self.clangd.completions_ready.connect(self.setComplitionsList)
        #self.pylsp.completions_ready.connect(self.setComplitionsList)
        self.Code.zoom_in_btn.clicked.connect(lambda:self.Setting_D.openFontDialog(self.Code.textedit_code_editor.font(),self.Code.configCodeEditor))
        #self.Dock.file_open_btn.clicked.connect(self.sendDocumentSymbolsRequest)
        self.Code.web_browser_btn.clicked.connect(self.Code.subWinWebBrowser)

        self.loadToolButtonSettings()
        self.loadPanelFileTreeSettings()
        self.loadPaneSymbolTreeSettings()
        self.loadToolBoxWindgetSsttings()
        #self.loadVirtualCDWidget()
        self.loadVirtualCDTabbarSettings()
        self.loadToolBoxContainerSettings()
        self.loadCodeTabbar()
        self.loadPreviewTabSwitcher()
        #self.loadSyntaxThemes()
        #print("=========++++........",open(open(self.Path_h.Code.SELECTED_CD_THEME,"r").read(),'r').read())

        try :
            self.loadFullCDTheme(open(open(self.Path_h.Code.SELECTED_CD_THEME,"r").read(),'r').read())
        except:
            self.loadFullCDTheme(open(self.Path_h.Code.DEFAULT_CD_THEME,'r').read())
            with open(self.Path_h.Code.SELECTED_CD_THEME,"w")as f:
                f.write(self.Path_h.Code.DEFAULT_CD_THEME)
        self.Code.add_subwindow_btn.click()
        #sub=self.Code.openUrlSubwindow("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py")
        #sub.showMaximized()
        #self.Dock.settings_btn.click()
        self.main_splitter.setSizes([100,700])  

        self.hover_pop_pos=None
        
        #self.pylsp.hover_ready.connect(lambda x:print(x))

        #self.pylsp.hover_ready.connect(self.popupHover)
        #self.pylsp.definition_ready.connect(self.goToDefinition)
        #self.pylsp.references_ready.connect(self.goToRefranceWindow)
        #self.pylsp.signature_help_ready.connect(lambda x: print(f"Hover: {x}"))
        #self.pylsp.document_symbols_ready.connect(lambda x:self.setDocumentSymbol(x))
        #self.pylsp.code_action_ready.connect(lambda x: print(f"Hover: {x}"))
        
        #self.pylsp.request_document_symbols("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py")
        #self.pylsp.request_hover("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15,1)
        #self.pylsp.request_definition("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15, 7)
        
        #self.pylsp.request_references("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15, 7)
        #self.pylsp.request_signature_help("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 15, 1)
        #self.pylsp.code_action_ready("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/tempN/test.py", 0, 19)
        
        #self.project_desk=Custom.ProjectDesktop(self.Code.mdi_area)
        
        #self.project_desk.connect_desk_projects=lambda x:print(x)

        #self.project_desk.project_list=[["CodeDock","/home/omx/file_o.png","/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock"],
         #                               ["test1","/home/omx/file_o.png","sp1"],
          #                              ["test2","/home/omx/file_o.png","sp2"],
           #                             ["test3","/home/omx/file_o.png","sp3"]]
    
        #self.project_desk.refreshProjectDesk()
        self.hover_popup=Custom.PopupHover()
        #self.hover_popup_highlighter=PythonHighlighter(self.hover_popup.popup_text_edit.document())

        #self.Code.textedit_code_editor.whenMouseCursorHover.connect(self.sendHoverRequest)
        #self.Code.textedit_code_editor.whenMouseCursorLeaveHover.connect(self.whenCursorLeaveHover)
        
        
        self.disable_document_symbol_kind=[2]
        self.last_symbols=[]
        #parent_list=[]        
        #same index(len) every list
        self.last_item_l=[] #[[item,index],....n]]
        self.last_name_l=[]
        self.document_symbols_l=[]
        self.symbol_start_lineno=[]
        self.symbol_end_lineno=[]

        self.Dock.Panel.setStyleSheet(self.Code.tabbar_editor.styleSheet())
        
        self.last_cusror=None
        
        self.Code.mini_map.setReadOnly(False)
        
    def projectOpenCall(self,path):
        self.Dock.Panel.setPathUrlInFileModel(path)

    def workerRequestComplition(self, character):
        cur, l, c = self.Code.running_textedit_editor.getCurrentLineOrColumnPos()
        
        line_text = self.Code.running_textedit_editor.document().findBlockByNumber(
            l
        ).text()

        print("LINE:", repr(line_text))

        print("charecter :- ",character)
        print("line : ",l,"col : ",c)

        self.lsp_handler.didChange(
            self.Code.codefile_path,
            l, c, l, c,
            character
        )

        # Get current word
        word = self.Code.running_textedit_editor.textCursor().block().text()

        if not word.strip():
            return
        QtCore.QTimer.singleShot(
            10,
            lambda: self.lsp_handler.requestCompletions(
                self.Code.codefile_path,
                l,
                c + 1
            )
        )

        #self.clangd.did_save(self.Code.codefile_path)
        #self.tslsp.did_open_document("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/test_ts/src/main.ts",self.Code.running_textedit_editor.toPlainText())
        #self.tslsp.request_completions("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/test_ts/src/main.ts",l,c)
        
        #self.clangd.di(self.Code.dummy_codefile_path)
        #self.Code.running_textedit_editor.onTextChanged()
        #self.rust_lsp.did_open(self.Code.dummy_codefile_path,self.Code.running_textedit_editor.toPlainText())
        #self.rust_lsp.request_completions(self.Code.dummy_codefile_path,l,c)
        #print(self.Code.dummy_codefile_path)
        #self.pylsp.request_signature_help(self.Code.dummy_codefile_path,l,c)
    
    def workerRequestHover(self,l,c):
        self.lsp_handler.requestHover(self.Code.dummy_codefile_path,l,c)
    
    def setComplitionsList(self,c,t):
        #self.c=self.lang_handler.getCompletions(self.Code.dummy_codefile_path,l,c)
        #print("sendede...........")

        #print("\n\n\n\n.....type : ",t)
        self.Code.running_textedit_editor.onTextChanged(len(c))
        self.Code.running_textedit_editor.setCompletions(c,t)
        
            
        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_N and event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
                
                print("pressed")
                return True
        return super().eventFilter(obj, event)  
    
    def windowSplash(self):
        # Frameless splash container
        self.container_test = QtWidgets.QWidget()
        self.container_test.setWindowFlags( 
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.container_test.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.container_test.resize(800, 465)

        # Background pixmap label
        splash_pix = QtGui.QPixmap(self.Path_h.CODEDOCK_SPLASH)
        splash_pix = splash_pix.scaled(800, 465,
                                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                    QtCore.Qt.TransformationMode.SmoothTransformation)

        bg_label = QtWidgets.QLabel(self.container_test)
        bg_label.setPixmap(splash_pix)
        bg_label.setGeometry(0, 0, 800, 465)  # full size

        # Loader widget OVER pixmap
        self.loader_splash_test = CDLoader.ThreadedFadeColorSVGLoader(340,220, self.container_test)
        self.loader_splash_test.setSvgAndInit(self.Path_h.CODEDOCK_SPLASH_SVG)
        #self.loader_splash_test.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.loader_splash_test.setStyleSheet("background: transparent;")

        # Position loader (center of splash)
        loader_w, loader_h = 340, 220
        x = (800 - loader_w) // 2
        y = (465 - loader_h) // 2
        self.loader_splash_test.setGeometry(x, y-100, loader_w, loader_h)

        # Show splash
        self.container_test.show()
        self.loader_splash_test.start_animation()

        # Auto close splash after 10s and show main window
        QtCore.QTimer.singleShot(5000, lambda: (
            self.container_test.close(),
            self.loader_splash_test.stop_animation(),
            self.MainWindow.show()
        ))


    def onEnterKeyInEditor(self):
        #self.Dock.Panel.map_model.clear()
        #self.lang_handler.setLangPath(self.Code.dummyCodeFilePath())
        #self.setCodeTagsAndSuggestions(self.Code.dummyCodeFilePath())
        #self.Dock.file_open_btn.click()
        self.sendDocumentSymbolsRequest()
        self.Code.startMiniMapDeboucingTimer()
        

    def onSubWindowSwitche(self):
        
        #print(".....switch calledd")
        file_path=self.Code.codefile_path
        
        
        #self.loadEditorSettings()
        #self.loadMdiAndSubWindowSettings()
        #self.Code.current_textedit_editor.connect_completion=self.parentCompletion
    
        #self.Dock.Panel.map_model.clear()
        #self.lang_handler.setLangPath(self.Code.dummyCodeFilePath())
        
        self.setCodeTagsAndSuggestions(file_path)
        self.Code.startMiniMapDeboucingTimer()
        #self.Code.running_textedit_editor.whenLinePosChangeGetLineNo.connect(lambda x:self.Code.running_subwindow.titlebar.block_path_navigation_bar.setBlockSymbols((self.getSymbolsParentBlocksName(x))))
        if file_path!=None:
            #print(file_path,"pathhhhhh")

            if self.Code.subwindow_service_buffer[self.Code.running_subwindow].textedit_obj != None:
                self.lsp_handler.onSwitchCodeFile(file_path,self.Code.running_textedit_editor,self.Code.mini_map)

        
    
    def parentCompletion(self):
        self.suggestions.clear()
        completion=self.Code.textedit_code_editor.last_completion
        
        s=None
        
        for i, code_tag in enumerate(self.code_tags_list, 0):
            if s!=None:    
                if code_tag[2]==s:
                    self.suggestions.append(code_tag[3])

                if code_tag[2]==1-s:
                    s=None

            if code_tag[3]==completion:
                s=code_tag[2]+1
        self.Code.running_textedit_editor.setCompletions(self.suggestions)




    def setCodeTagsAndSuggestions(self, path):
        #self.Dock.Panel.map_tree.setModel(self.Dock.Panel.map_model)

        
        # self.removeComponents()
        if path != None:
            pass
            #self.pylsp.request_document_symbols(self.Code.dummy_codefile_path)
            #self.code_tags_list=self.lang_handler.getTags()
            # self.t_components=len(code_lst)

            # self.frame_code_map_size=len(code_lst)*self.map_btn_spacing_size
            # self.frame_components_map.setFixedHeight(self.frame_code_map_size)
            #self.Dock.setCodeTagsOnModel(self.code_tags_list)
            # print(swin_addr[1].toPlainText())
            
            """for i, code_tag in enumerate(self.code_tags_list, 0):
                # self.codeListMap(i,code_components)
                if len(code_tag) == 6:...

                
                #if code_tag[2]==0:
                self.suggestions.append(code_tag[3])
            """# return code_lsti
            #self.Code.current_textedit_editor.setSuggestions(self.lang_handler.getCompletions())


    def openSettingWidget(self):
        if self.Code.setting_dialog_flag==False:    
            self.Setting_D=Setting_Dialog_Widgets()
            self.setSettingList()
            # self.setting_dialog.show()
            self.Code.subWinWidgets(self.Setting_D,"setting")
            self.Code.setting_dialog_flag=True
            self.settingDialogSaveObj()

        else:pass

    def settingDialogSaveObj(self):
        
        if self.Code.setting_dialog_flag==True:    
            self.virtual_desk_list[self.virtual_running_index][4]=self.Setting_D
        else:
            self.virtual_desk_list[self.virtual_running_index][4]=None

    
    def onThemeChange(self,file_path_list):
        dock_path=self.Path_h.pathJoin(file_path_list,"Dock")
        code_path=self.Path_h.pathJoin(file_path_list,"Code")

        for i,file_path in enumerate(Dir_Scanner.child_deep_scan(dock_path)):
            for i,var_str in enumerate(self.Path_h.Dock.__dict__):
                if var_str.startswith("__"):continue
                var=getattr(self.Path_h.Dock,var_str)
                if self.Path_h.filePathToFileName(var)==self.Path_h.filePathToFileName(file_path):
                    #print(self.Path_h.filePathToFileName(file_path))
                    setattr(self.Path_h.Dock,var_str,file_path)
                    
        for i,file_path in enumerate(Dir_Scanner.child_deep_scan(code_path)):
            for i,var_str in enumerate(self.Path_h.Code.__dict__):
                if var_str.startswith("__"):continue
                var_data=getattr(self.Path_h.Code,var_str)
                if self.Path_h.filePathToFileName(var_data)==self.Path_h.filePathToFileName(file_path):
                    setattr(self.Path_h.Code,var_str,file_path)
                    

        self.loadOthers()
        self.loadCodeTabbar()
        self.loadTextEditorSettings()

        self.loadDockWidgetSettings()
        self.loadPanelFileTreeSettings()
        self.loadPaneSymbolTreeSettings()
        self.loadToolBoxWindgetSsttings()
        self.loadSyntaxThemes()



    def settingMainWindow(self):
        self.Setting_D.addStyleSheetTextEditDock(0,"test",self.main_splitter.styleSheet(),lambda text:self.main_splitter.setStyleSheet(text))

        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)
        self.layout_groupbox = self.Setting_D.createGroupBox("Main Window", self.Setting_D.layout_frame_2,0)
        
        box_layout = self.Setting_D.createGroupBox("TitleBar", self.layout_groupbox, 1)
        self.Setting_D.createColorOption("Background", self.linkWindowTitleBarBgColor,self.MainWindow.ttlbr_bg_clr)
        self.Setting_D.createColorOption("Hover", self.linkWindowTitleBarHover,self.MainWindow.ttlbr_hover)
        
        self.Setting_D.createColorOption("Border", self.linkWindowBorderColor,self.MainWindow.window_brdr_color)
        self.Setting_D.createColorOption("Title Text", self.linkWindowTitleTextColor,self.MainWindow.ttlbr_text_clr)
        self.Setting_D.createColorOption("Close Button", self.linkWindowCloseBtnBgColor,self.MainWindow.close_btn_clr)
        self.Setting_D.createColorOption("Close Button Hover", self.linkWindowCloseBtnHoverBgColor,self.MainWindow.close_btn_hover)
        self.Setting_D.createColorOption("MAximize Button", self.linkWindowMaximizeBtnBgColor,self.MainWindow.maximize_btn_clr)
        self.Setting_D.createColorOption("Maximize Button Hover", self.linkWindowMaximizeBtnHoverBgColor,self.MainWindow.maximize_btn_hover)

        self.Setting_D.createSpinBox("Titlebar Hiegth",self.linkWindowTitlebarHeight,self.MainWindow.ttlbr_hsize)
        self.Setting_D.createSpinBox("CD Size",self.linkWindowTitlebarCDIconSize,self.MainWindow.ttlbr_icon_size)
        self.Setting_D.createSpinBox("Buttons Size",self.linkWindowTitlebarButtonSize,self.MainWindow.ttlbr_btns_size)
        self.Setting_D.createSpinBox("Title Font Size",self.linkWindowTitleFontSize,self.MainWindow.ttlbr_title_font)
        #self.Setting_D.createSpinBox("Title Font Size",self.linkWindowTitleFontSize,self.MainWindow.ttlbr_title_font)
        #self.Setting_D.createSpinBox("Title Font Size",self.linkWindowTitleFontSize,self.MainWindow.ttlbr_title_font)
        
        self.Setting_D.createDoubleSpinBox("Buttons radius",self.linkWindowBtnsRadius,self.MainWindow.btns_radius)

        box_layout = self.Setting_D.createGroupBox("Virtual Widget", self.layout_groupbox, 2)
        self.Setting_D.createColorOption("Tab Color", self.linkVirtualTabBgColor,self.virtual_CD.tabbar.tab_clr)
        self.Setting_D.createColorOption("Tab Hover", self.linkVirtualTabHoverColor,self.virtual_CD.tabbar.tab_hover_clr)
        self.Setting_D.createColorOption("Tab Selected", self.linkVirtualTabSelectedColor,self.virtual_CD.tabbar.tab_selected_clr)
        self.Setting_D.createColorOption("Tab Font", self.linkVirtualTabTextColor,self.virtual_CD.tabbar.font_clr)
        self.Setting_D.createSpinBox("Tab Width", self.linkVirtualTabWidth,self.virtual_CD.tabbar.tab_w)
        self.Setting_D.createSpinBox("Tab Height", self.linkVirtualTabHeight,self.virtual_CD.tabbar.tab_h)
        

        
        box_layout = self.Setting_D.createGroupBox("Tab Switcher", self.layout_groupbox, 3)
        self.Setting_D.createColorOption("Color", self.Code.ui_tab_switcher.setBgColor,self.virtual_CD.tabbar.tab_clr)
        #self.Setting_D.createColorOption("Tab Selected", self.linkVirtualTabSelectedColor,self.virtual_CD.tabbar.tab_selected_clr)
        #self.Setting_D.createColorOption("Tab Font", self.linkVirtualTabTextColor,self.virtual_CD.tabbar.font_clr)
        self.Setting_D.createSpinBox("Alfa", self.Code.ui_tab_switcher.setBgAlfa,180,255)
        self.Setting_D.createSpinBox("Radius", self.Code.ui_tab_switcher.setBrdrRadius,self.Code.ui_tab_switcher.brdr_radius)
        #self.Setting_D.createSpinBox("Image Spacing", self.Code.ui_tab_switcher.setImageSpacing,self.Code.ui_tab_switcher.img_spacing)
        self.Setting_D.createSpinBox("Item per C", self.Code.ui_tab_switcher.setItemPerRow,self.Code.ui_tab_switcher.columns)
        
        self.Setting_D.createSpinBox("Hight", self.Code.ui_tab_switcher.setImageHight,self.Code.ui_tab_switcher.image_labeler.h,1000)
        self.Setting_D.createSpinBox("Widgth", self.Code.ui_tab_switcher.setImageWidth,self.Code.ui_tab_switcher.image_labeler.w,1000)
        self.Setting_D.createSpinBox("ImageRadius", self.Code.ui_tab_switcher.setImageBrdrRadius,self.Code.ui_tab_switcher.image_labeler.radius)
        self.Setting_D.createSpinBox("selected think...", self.Code.ui_tab_switcher.setImageSelectedBrdrThinkness,self.Code.ui_tab_switcher.image_labeler.selected_brdr_thinkess)
        self.Setting_D.createSpinBox("font size", self.Code.ui_tab_switcher.setImageTitileFontSize,self.Code.ui_tab_switcher.image_labeler.font_size)
        
        self.Setting_D.createColorOption("Border color", self.Code.ui_tab_switcher.setImageBorderColor,self.Code.ui_tab_switcher.image_labeler.brdr_clr)
        self.Setting_D.createColorOption("selected color", self.Code.ui_tab_switcher.setImageSelectedColor,self.Code.ui_tab_switcher.image_labeler.selected_clr)
        self.Setting_D.createColorOption("titlw fcolro", self.Code.ui_tab_switcher.setImageTitleFontColor,self.Code.ui_tab_switcher.image_labeler.font_clr)

        


        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.CodeDock.WINDOW_TITLEBAR_S, self.MainWindow.getVarDict()
                ),

                self.saveSettings(
                    self.Path_h.CodeDock.VIRTUAL_CD_WIDGET_S, self.virtual_CD. getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.CodeDock.VIRTUAL_CD_TABBAR_S, self.virtual_CD.tabbar.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.CodeDock.PREVIEW_TAB_SWITCHER, self.Code.ui_tab_switcher.getVarDict()
                ),
                
            )
        )
    
    def settingToolBox(self):
        #self.Setting_D.addStyleSheetTextEditDock("test",self.Code.tabbar_editor.styleSheet(),lambda text:self.Code.tabbar_editor.setStyleSheet(text))
        
        #self.Setting_D.addStyleSheetTextEditDock("test",self.Code.running_textedit_editor.styleSheet())
        #self.Setting_D.addStyleSheetTextEditDock("test",self.Code.running_textedit_editor.styleSheet())
        #self.Setting_D.addStyleSheetTextEditDock("test",self.Code.running_textedit_editor.styleSheet())
        #self.Setting_D.addStyleSheetTextEditDock("test",self.Code.running_textedit_editor.styleSheet())

        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)
        self.layout_groupbox = self.Setting_D.createGroupBox("ToolBox", self.Setting_D.layout_frame_2, 0)

        box_layout = self.Setting_D.createGroupBox("Color", self.layout_groupbox, 0)

        self.Setting_D.createColorOption(
            "Background",
            lambda x: (
                self.Code.linkToolBoxBgColor(x),
                self.Dock.linkToolBoxBgColor(x),
                
            ),
            self.Code.frame_toolbox.bg_clr,
        )
        self.Setting_D.createColorOption(
            "Boreder",
            lambda x: (
                self.Code.linkToolBoxBrdrColor(x),
                self.Dock.linkToolBoxBrdrColor(x),
            ),
            self.Code.frame_toolbox.brdr_clr,
        )
        self.Setting_D.createColorOption(
            "Buttons",
            lambda x: (
                self.Code.linkToolBoxButtonColor(x),
                self.Dock.linkToolBoxButtonColor(x),
            ),
            self.Code.stylish_t_btn.bg_clr,
        )
        self.Setting_D.createColorOption(
            "Border",
            lambda x: (
                self.Code.linkToolBoxButtonBrdrColor(x),
                self.Dock.linkToolBoxButtonBrdrColor(x),
            ),
            self.Code.stylish_t_btn.brdr_clr,
        )


        # self.Setting_D.createColorOption('Border',lambda:(self.Code.linkToolBoxBgColor,self.Dock.linkToolBoxBgColor))

        box_layout = self.Setting_D.createGroupBox("Size", self.layout_groupbox,1)

        self.Setting_D.createSpinBox(
            "Toolbox Height",
            lambda x: (self.Dock.linkToolBoxSize(x)),
            self.Dock.frame_toolbox.h,
        )

        self.Setting_D.createSpinBox(
            "Toolbox Radius",
            self.Dock.linkToolBoxRadius,
            int(self.Dock.frame_toolbox.brdr_radius),
            
        )
        self.Setting_D.createDoubleSpinBox(
            "Toolbox Border",
            lambda x: (self.Code.linkToolBoxBrdrThinkness(x), self.Dock.linkToolBoxBrdrThinkness(x)),
            self.Dock.frame_toolbox.brdr_think,
            0.50
        )
        # self.Setting_D.createDoubleSpinBox("Border",self.changeBorderSizeToolbox,0.50)
        # self.Setting_D.createDoubleSpinBox("Toolbox Radius",self.setValToolboxRadius,0.50)

        self.Setting_D.createSpinBox(
            "Button",
            lambda x: (
                self.Code.linkToolBoxButtonSize(x),
                self.Dock.linkToolBoxButtonSize(x),
            ),
            self.Code.stylish_t_btn.wh,
        )
        self.Setting_D.createDoubleSpinBox(
            "Button Border",
            lambda x: (
                self.Code.linkToolBoxButtonBrdrThinkness(x),
                self.Dock.linkToolBoxButtonBrdrThinkness(x),
            ),
            self.Code.stylish_t_btn.brdr_think,
            0.50
        )
        
        self.Setting_D.createSpinBox(
            "Icons",
            lambda x: (
                self.Code.linkToolBoxIconSize(x),
                self.Dock.linkToolBoxIconSize(x),
            ),
            self.Code.stylish_t_btn.icon_size,
        )

        self.Setting_D.createDoubleSpinBox(
            "Buttton Radius",
            lambda x: (
                self.Code.linkToolBoxButtonBrdrRadius(x),
                self.Dock.linkToolBoxButtonBrdrRadius(x),
            ),
            self.Code.stylish_t_btn.brdr_think,
            0.50,
        )
        
        # self.Setting_D.createDoubleSpinBox("Border",self.changeBorderSizeToolButton,0.50)
        # self.Setting_D.createSpinBox("Spacing",lambda:...)
        self.Setting_D.createSpinBox("Spacing",
                            lambda x: 
                                (self.Code.linkToolBoxBtnSpacing(x),
                                self.Dock.linkToolBoxBtnSpacing(x))
                           ,int(self.Dock.frame_toolbox.e_spacing))

        box_layout = self.Setting_D.createGroupBox("Bool", self.layout_groupbox, 2)
        # self.createToggleButton("Toolbox Border",0,self.setBoolToolboxBorder)
        # self.createToggleButton("Button Border",self.setBoolToolButtonBorder)
        # self.createToggleButton("Button Background",self.setBoolToolButtonBg)
        # box_layout=self.Setting_D.createGroupBox('Setting',self.layout_groupbox)
        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.Code.TOOLBOX_S, self.Code.frame_toolbox.__dict__
                ),
                self.saveSettings(
                    self.Path_h.Code.TOOLBUTTON_S, self.Code.stylish_t_btn.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Dock.TOOLBOX_S, self.Dock.frame_toolbox.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Dock.TOOLBUTTON_S, self.Dock.stylish_t_btn.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Dock.TOOL_CONTAINER_S, self.Dock.frame_toolbox.getVarDict()
                ),
         ),
        )
        

    def settingDockPanel(self):
        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)

        self.layout_groupbox = self.Setting_D.createGroupBox("Panel", self.Setting_D.layout_frame_2, 0)

        box_layout = self.Setting_D.createGroupBox("Color", self.layout_groupbox,0)

        self.Setting_D.createColorOption("Background", self.Dock.linkPanelBgColor,self.Dock.Panel.file_tree.bg_clr)
        self.Setting_D.createColorOption("Border", self.Dock.linkPanelBrdrColor,self.Dock.Panel.file_tree.brdr_clr)
        self.Setting_D.createColorOption("Tool Bar", self.Dock.linkPanelToolBarColor,self.Dock.Panel.toolbar_file_tree.bg_clr)
        
        self.Setting_D.createColorOption("Buttons", self.Dock.linkPanelButtonColor,self.Dock.Panel.file_tree.btn_clr)
        #self.Setting_D.createColorOption("Button Border", self.Dock.linkPanelBtnBrdrColor,self.Dock.Panel.file_tree.btn_brdr_clr)
        # self.Setting_D.createColorOption('Border',lambda:...)

        box_layout = self.Setting_D.createGroupBox("Size", self.layout_groupbox, 1)

        #self.Setting_D.createSpinBox("Panel",0,self.Dock.panel)
        self.Setting_D.createSpinBox("Item Size",self.Dock.linkPanelItemSize,self.Dock.Panel.file_tree.font_size)
        self.Setting_D.createDoubleSpinBox("Map Border",self.Dock.linkPanelBrdrThink,self.Dock.Panel.file_tree.brdr_think,0.50)
        self.Setting_D.createDoubleSpinBox("Map Border Radius",self.Dock.linkPanelBrdrRadius,self.Dock.Panel.file_tree.brdr_radius,0.50)
        
        self.Setting_D.createSpinBox("Tool Bar",self.Dock.linkPanelToolBarHieght,self.Dock.Panel.toolbar_file_tree.h)
        self.Setting_D.createSpinBox("Tool Button ",self.Dock.linkPanelToolButtonSize,self.Dock.Panel.add_file_ft_btn.h)
    

        #self.Setting_D.createDoubleSpinBox("Button Border",self.Dock.linkPanelBtnBrdrThink,self.Dock.Panel.file_tree.btn_brdr_think,0.50)
        
        # self.Setting_D.createDoubleSpinBox("Map Radius",self.changeMapBorderRadius,0.50)
        # self.Setting_D.createSpinBox("Button",self.chnageSizeMapButton)
        # self.Setting_D.createDoubleSpinBox("Border",self.changeBorderSizeMapButton,0.50)
        # self.Setting_D.createDoubleSpinBox("Button Radius",self.setValMapButtonRadius,0.50)
        # self.Setting_D.createSpinBox("Button Spacing",self.setMapButtonSpacing)
        # self.Setting_D.createSpinBox("Font",7,self.changeSizeMapFont)

        """
        self.Setting_D.createSpinBox("Button",self.changeToolButtonIconSize)
        self.Setting_D.createDoubleSpinBox("Buttton Radius",self.setValToolBtnRadius,0.50)
        self.Setting_D.createDoubleSpinBox("Border",self.changeBorderSizeToolButton,0.50)
        self.Setting_D.createSpinBox("Spacing",lambda:...)
        """

        box_layout = self.Setting_D.createGroupBox("Bool", self.layout_groupbox, 2)
        # self.createToggleButton("Map Border",0,self.setBoolMapBorder)
        # self.createToggleButton("Button Border",self.setBoolMapButtonBorder)
        # self.createToggleButton("Button Background",self.setBoolMapButtonBg)
        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.Dock.PMAP_TREE_S, self.Dock.Panel.map_tree.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Dock.PFILE_TREE_S, self.Dock.Panel.file_tree.getVarDict()
                ),
            ),
        )
    
    def settingDockWidgets(self):

        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)
        self.layout_groupbox = self.Setting_D.createGroupBox("Mdi", self.Setting_D.layout_frame_2,0)

        #box_layout = self.Setting_D.createGroupBox("Mdi", self.layout_groupbox, 1)
        #self.Setting_D.createColorOption("mdi", self.Code.linkMdiBgColor,self.Code.mdi_area.mdi_bg_clr)
        #self.Setting_D.createColorOption("border", self.Code.linkMdiBrdrColor,self.Code.mdi_area.mdi_brdr_clr)
        #self.Setting_D.createDoubleSpinBox("border",self.Code.linkMdiBrdrThinkness,self.Code.mdi_area.mdi_brdr_think,0.50)    

        box_layout = self.Setting_D.createGroupBox("Dock Widgets", self.layout_groupbox, 2)
        #self.Setting_D.createColorOption("Back", self.Code.linkSubWindowBgColor,self.Code.mdi_area.subw_bg_clr)
        
        self.Setting_D.createColorOption("Border", DockWidgetStyle.setBorderColor,DockWidgetStyle.border_color)
        self.Setting_D.createColorOption("active border", DockWidgetStyle.setActiveBorderColor,DockWidgetStyle.activated_border_color)
        #self.Setting_D.createColorOption("border hover", self.Code.linkSubWindowBorderHover,self.Code.mdi_area.subw_ttlbr_hover)
        self.Setting_D.createDoubleSpinBox("border",DockWidgetStyle.setBorderThickness,DockWidgetStyle.border_thickness,0.50)
        self.Setting_D.createDoubleSpinBox("radius",DockWidgetStyle.setBorderRadius,DockWidgetStyle.border_radius)
        
        box_layout = self.Setting_D.createGroupBox("TitleBar", self.layout_groupbox, 3)
        self.Setting_D.createColorOption("Background", DockWidgetStyle.setTitleBarBgColor,DockWidgetStyle.titlebar_bg_color)
        self.Setting_D.createColorOption("Active Background", DockWidgetStyle.setActiveTitleBarBgColor,DockWidgetStyle.titlebar_activated_bg_color)     
        self.Setting_D.createColorOption("Title Text", DockWidgetStyle.setTitleTextColor,DockWidgetStyle.title_text_color)
        self.Setting_D.createColorOption("Close Button", DockWidgetStyle.setCloseBtnBgColor,DockWidgetStyle.close_button_color)
        self.Setting_D.createColorOption("Maximize Button", DockWidgetStyle.setMaximizeBtnBgColor,DockWidgetStyle.maximize_button_color)
        self.Setting_D.createColorOption("MiniMize Button", DockWidgetStyle.setMinimizeBtnBgColor,DockWidgetStyle.minimize_button_color)
        self.Setting_D.createColorOption("Button Hover", DockWidgetStyle.setControllBtnHoverColor,DockWidgetStyle.controll_button_hover_color)

        self.Setting_D.createSpinBox("Titlebar Hiegth",DockWidgetStyle.setTitlebarHeight,DockWidgetStyle.titlebar_hsize)
        self.Setting_D.createSpinBox("Buttons Size",DockWidgetStyle.setControllButtonSize,DockWidgetStyle.controll_button_size)
        self.Setting_D.createSpinBox("Title Font Size",DockWidgetStyle.setTitleFontSize,DockWidgetStyle.title_text_font)
        
        #self.Setting_D.createDoubleSpinBox("border radius",DockWidgetStyle.bore,DockWidgetStyle.controll_button_hover_color)
        self.Setting_D.createDoubleSpinBox("Buttons radius",DockWidgetStyle.setControllBtnsRadius,DockWidgetStyle.controll_button_radius)
            
        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.Code.MDI_S, DockWidgetStyle.getVarDict()
                ),
            )
        )


    
    def settingEditor(self):
        self.Setting_D.addStyleSheetTextEditDock(4,"subwindow",self.Code.subwindow.styleSheet(),lambda text:self.Code.setSubWidowStyleSheet(text))
        self.Setting_D.addStyleSheetTextEditDock(4,"Editor",self.Code.textedit_code_editor.styleSheet(),lambda text:self.Code.setEditorStyleSheet(text))
        self.Setting_D.addStyleSheetTextEditDock(4,"subwindow",self.Code.tabbar_editor.styleSheet(),lambda text:self.Code.tabbar_editor.setStyleSheet(text))

        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)
        self.layout_groupbox = self.Setting_D.createGroupBox("Editor", self.Setting_D.layout_frame_2,0)

        box_layout = self.Setting_D.createGroupBox("Editor Color", self.layout_groupbox, 1)
        #self.Setting_D.createColorOption("mdi", self.Code.linkMdiBgColor,self.Code.mdi_area.mdi_bg_clr)
        self.Setting_D.createColorOption("Background", self.Code.linkEditorBgColor,self.Code.style_editor.bg_clr)
        self.Setting_D.createColorOption("Boreder", self.Code.linkEditorBrdrColor,self.Code.style_editor.brdr_clr)
        self.Setting_D.createColorOption("Indent", self.Code.linkIndentColor,
                               f"""rgba({self.Code.style_editor.indent_rgba[0]},
                               {self.Code.style_editor.indent_rgba[1]},
                               {self.Code.style_editor.indent_rgba[2]},
                               {self.Code.style_editor.indent_rgba[3]})""")
        self.Setting_D.createDoubleSpinBox("Indent alfa", self.Code.linkIndentAlfa, self.Code.style_editor.indent_alfa,10)
        
        self.Setting_D.createDoubleSpinBox("Border", self.Code.linkEditorBrdrThinkness, self.Code.style_editor.brdr_think,0.50)
        self.Setting_D.createDoubleSpinBox("Radius", self.Code.linkEditorBrdrRadius,self.Code.style_editor.brdr_radius, 0.50)
        self.Setting_D.createDoubleSpinBox("Font Size", self.Code.linkEditorFontSize,self.Code.style_editor.font_size, 2)
                

        box_layout = self.Setting_D.createGroupBox("Numpad Color", self.layout_groupbox, 2)
        #self.Setting_D.createColorOption("Background", self.Code.linkNumpadBgColor,self.Code.style_numpad.bg_clr)
        #self.Setting_D.createColorOption("Border", self.Code.linkNumpadBrdrColor,self.Code.style_numpad.brdr_clr)
        #self.Setting_D.createDoubleSpinBox("Width", self.Code.linkNumpadWidth,self.Code.style_numpad.w, 1)
        #self.Setting_D.createDoubleSpinBox("Border", self.Code.linkNumpadBrdrThinkness,self.Code.style_numpad.brdr_think,0.50)
        #self.Setting_D.createDoubleSpinBox("Radius", self.Code.linkNumpadBrdrRadius,self.Code.style_numpad.brdr_radius, 0.50)

        # box_layout=self.Setting_D.createGroupBox('Border',self.layout_groupbox)

        #box_layout = self.Setting_D.createGroupBox("Bool", self.layout_groupbox, 3)
        box_layout = self.Setting_D.createGroupBox("Minimap", self.layout_groupbox, 3)
        self.Setting_D.createColorOption("Minimap Background", self.Code.linkMiniMapBgColor,self.Code.mini_map.minimap_bg)
        self.Setting_D.createColorOption("Viewport Color", self.Code.linkMiniMapViewPortColor,
                               f"""rgba({self.Code.mini_map.vp_rgba[0]},
                               {self.Code.mini_map.vp_rgba[1]},
                               {self.Code.mini_map.vp_rgba[2]},
                               {self.Code.mini_map.vp_rgba[3]}
                               )""")
        self.Setting_D.createDoubleSpinBox("Alfa", self.Code.linkMiniMapViewPortAlfa,self.Code.mini_map.vp_rgba[3],10)
        
        self.Setting_D.createColorOption("Border Color", self.Code.linkMiniMapViewPortBorderColor,
                               f"""rgba({self.Code.mini_map.vp_brdr_rgba[0]},
                               {self.Code.mini_map.vp_brdr_rgba[1]},
                               {self.Code.mini_map.vp_brdr_rgba[2]},
                               {self.Code.mini_map.vp_brdr_rgba[3]}
                               )""")
        self.Setting_D.createDoubleSpinBox("Alfa", self.Code.linkMiniMapVieywPortBorderAlfa,self.Code.mini_map.vp_brdr_rgba[3],10)

        self.Setting_D.createColorOption("Border Hover", self.Code.linkMiniMapViewPortBorderHover,
                               f"""rgba({self.Code.mini_map.vp_brdr_hover_rgba[0]},
                               {self.Code.mini_map.vp_brdr_hover_rgba[1]},
                               {self.Code.mini_map.vp_brdr_hover_rgba[2]},
                               {self.Code.mini_map.vp_brdr_hover_rgba[3]}
                               )""")
        
        self.Setting_D.createDoubleSpinBox("Alfa", self.Code.linkMiniMapViewPortBorderHoverAlfa,self.Code.mini_map.vp_brdr_hover_rgba[3],10)
        
        self.Setting_D.createDoubleSpinBox("Width", self.Code.linkMiniMapViewPortBorderWidth,self.Code.mini_map.brdr_width)

        
        box_layout=self.Setting_D.createGroupBox("Completer",self.layout_groupbox,4)

        self.Setting_D.createColorOption("Background",self.Code.linkCompleterBgColor)
        self.Setting_D.createColorOption("Border",self.Code.linkCompleterBrdrColor)
        self.Setting_D.createColorOption("Item Text",self.Code.linkCompleterTextColor)
        self.Setting_D.createColorOption("Select Item",self.Code.linkCompleterSelecteItemColor)
        self.Setting_D.createColorOption("Select Item Text",self.Code.linkCompleterSelecteItemTextColor)

        self.Setting_D.createDoubleSpinBox("Border",self.Code.linkCompleterBrdrThinkness,self.Code.style_completer.brdr_think)
        #self.Setting_D.createDoubleSpinBox("Font Size",self.Code.linkCompleterFontSize,self.Code.style_completer.font_size)
        

        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.Code.EDITOR_S, self.Code.style_editor.getVarDict()
                
                ),
                self.saveSettings(
                    self.Path_h.Code.MDI_S, self.Code.mdi_area.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Code.MINIMAP_S, self.Code.mini_map.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Code.COMPLITER_S, self.Code.style_completer.getVar()
                )
                
            )
        )

        # self.Setting_D.createSpinBox("Toolbox",0,self.changeSizeToolbox)
        # self.Setting_D.createSpinBox("Size",0,self.changeSizeCodeEditor)

        # box_layout=self.Setting_D.createGroupBox('Numpad Size',self.layout_groupbox)

        # self.Setting_D.createSpinBox("Toolbox",0,self.changeSizeToolbox)
        # self.Setting_D.createDoubleSpinBox("Border",self.changeBorderSizeToolbox,0.50)
        # self.Setting_D.createDoubleSpinBox("Toolbox Radius",self.setValToolboxRadius,0.50)

        """
        self.Setting_D.createSpinBox("Button",self.changeToolButtonIconSize)
        self.Setting_D.createDoubleSpinBox("Buttton Radius",self.setValToolBtnRadius,0.50)
        self.Setting_D.createDoubleSpinBox("Border",self.changeBorderSizeToolButton,0.50)
        self.Setting_D.createSpinBox("Spacing",lambda:...)
        """

        """"box_layout=self.Setting_D.createGroupBox('Bool',self.layout_groupbox)
        self.createToggleButton("Toolbox Border",0,self.setBoolToolboxBorder)
        self.createToggleButton("Button Border",self.setBoolToolButtonBorder)
        self.createToggleButton("Button Background",self.setBoolToolButtonBg)
    """

    def settingTabbar(self):

        
        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)
        self.layout_groupbox = self.Setting_D.createGroupBox("Editor", self.Setting_D.layout_frame_2, 0)
        box_layout = self.Setting_D.createGroupBox("Color", self.layout_groupbox, 1)
        self.Setting_D.createColorOption(
            "Tab Bar",
            lambda x: (self.Code.linkTabbarBgColor(x), self.Dock.linkTabbarBgColor(x)),
            self.Code.frame_tabbar.bg_clr
        )
        self.Setting_D.createColorOption(
            "Border",
            lambda x: (
                self.Code.linkTabbarBrdrColor(x),
                self.Dock.linkTabbarBrdrColor(x),
            ),
            self.Code.frame_tabbar.brdr_clr
        )
        
        self.Setting_D.createColorOption(
            "Tab Button",
            lambda x: (self.Code.linkTabBtnBgColor(x), self.Dock.linkTabBtnBgColor(x)),
            self.Code.tabbar_editor.tab_clr
        )

        self.Setting_D.createColorOption(
            "Working",
            lambda x: (
                self.Code.linkTabBtnWorkingBrdrColor(x),
                self.Dock.linkTabBtnWorkingBrdrColor(x),
            ),
            self.Code.tabbar_editor.brdr[0]
        )

        self.Setting_D.createColorOption(
            "Working Font",
            lambda x: (
                self.Code.linkTabBtnWorkingFontColor(x),
                
            ),
            self.Code.tabbar_editor.font_clr
        )



        self.Setting_D.createColorOption(
            "Non-Working",
            lambda x: (
                self.Code.linkTabBtnNonWorkingBrdrColor(x),
                self.Dock.linkTabBtnNonWorkingBrdrColor(x),
            ),
            self.Code.tabbar_editor.brdr[1]
        )

        self.Setting_D.createColorOption(
            "Non-Working Font",
            lambda x: (
                self.Code.linkTabBtnNonWorkingFontColor(x),
                
            ),
            self.Code.tabbar_editor.selected_font_clr
        )


        self.Setting_D.createColorOption(
            "Border",
            lambda x: (
                self.Code.linkTabbarBrdrColor(x),
                self.Dock.linkTabbarBrdrColor(x),
            ),
            self.Code.frame_tabbar.brdr_clr
        )
        """        self.Setting_D.createColorOption(
            "Font",
            lambda x: (
                self.Code.linkNonWorkingFontColor(x),
                self.Dock.linkTabBtnFontColor(x),
            ),
            self.Code.tabbar_editor.font_clr
        )
"""
        self.Setting_D.createColorOption(
            "Tab Hover",
            lambda x: (
                self.Code.linkTabBtnHoverColor(x),
                self.Dock.linkTabBtnHoverColor(x),
            ),
            self.Code.tabbar_editor.tab_hover_clr
        )
        self.Setting_D.createColorOption(
            "Tab Selecte",
            lambda x: (
                self.Code.linkTabBtnSelectedColor(x),
                self.Dock.linkTabBtnSelectedColor(x),
            ),
            self.Code.tabbar_editor.tab_selected_clr
        )


        box_layout = self.Setting_D.createGroupBox("Size", self.layout_groupbox, 2)

        self.Setting_D.createSpinBox(
            "TabBar",
            lambda x: (
                self.Code.linkTabbarFrameHSize(x),
                self.Dock.linkTabbarFrameHSize(x),
            ),
            28
        )

        self.Setting_D.createSpinBox(
            "Tab Button",
            lambda x: (self.Code.linkTabbarHSize(x), self.Dock.linkTabbarHSize(x)),
            self.Code.tabbar_editor.tab_h
        )

        self.Setting_D.createDoubleSpinBox(
            "Tab Radius",
            lambda x: (self.Code.linkTabBtnRadius(x), self.Dock.linkTabBtnRadius(x)),
            self.Code.tabbar_editor.tab_radius,
            0.50
        )

        box_layout = self.Setting_D.createGroupBox("Bool", self.layout_groupbox, 3)
        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.Code.TABBAR_S, self.Code.tabbar_editor.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Dock.TABBAR_S, self.Dock.Panel.tabbar_panel.getVarDict()
                ),
            ),
        )
        # self.Setting_D.createSpinBox("Toolbox",0,self.changeSizeToolbox)
        # self.Setting_D.createDoubleSpinBox("Toolbox Radius",self.setValToolboxRadius,0.50)

    def settingScrollBars(self):
        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)
        self.layout_groupbox = self.Setting_D.createGroupBox("Scrollbar", self.Setting_D.layout_frame_2, 0)

        box_layout = self.Setting_D.createGroupBox("Color", self.layout_groupbox, 0)

        self.Setting_D.createColorOption(
            "Scroll bar",
            lambda x: (
                self.Code.linkEditorScrollBarColor(x),
                self.Dock.linkPanelScrollBarColor(x),
            ),
            self.Dock.Panel.file_tree.scroll_bar_clr
        )

        self.Setting_D.createColorOption(
            "Scroll Handel",
            lambda x: (
                self.Code.linkEditorScrollHandelColor(x),
                self.Dock.linkPanelScrollHandelColor(x),
            ),
            self.Dock.Panel.file_tree.scroll_handel_clr
        )

        # self.Setting_D.createColorOption('Button',lambda x:(self.Code.linkTabBtnBgColor(x),self.Dock.linkTabBtnBgColor(x)))
        # self.Setting_D.createColorOption('Border',lambda x:(self.Code.linkTabBtnBrdrColor(x),self.Dock.linkTabBtnBrdrColor(x)))

        box_layout = self.Setting_D.createGroupBox("Bool", self.layout_groupbox, 1)
        # self.Setting_D.createSpinBox("TabBar",0,lambda x:(self.Code.linkTabbarFrameHSize(x),self.Dock.linkTabbarFrameHSize(x)))

        # self.Setting_D.createSpinBox("Tab Button",lambda x:(self.Code.linkTabbarHSize(x),self.Dock.linkTabbarHSize(x)))

        # self.Setting_D.createDoubleSpinBox("Tab Radius",lambda x:(self.Code.linkTabBtnRadius(x),self.Dock.linkTabBtnRadius(x)),0.50)
        self.Setting_D.createSaveButton(
            "Save Setting",
            lambda: (
                self.saveSettings(
                    self.Path_h.Dock.PMAP_TREE_S, self.Dock.Panel.map_tree.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Dock.PFILE_TREE_S, self.Dock.Panel.file_tree.getVarDict()
                ),
                self.saveSettings(
                    self.Path_h.Code.EDITOR_S, self.Code.style_editor.getVarDict()
                ),
            ),
        )

    def onSelectSyntaxtTheme(self,file_path):
        with open(file_path,"r")as f:
            colors=f.read()

        colors=eval(colors.splitlines()[0])
        h_ext=colors["language"]
        self.Setting_D.removeWidgets(self.layout_groupbox_for_theme)
        box_layout=self.Setting_D.createGroupBox("Theme Color", self.layout_groupbox_for_theme, 1)

        highlighter_list:str=self.lsp_handler.running_highlighters[h_ext]
        
        
        self.Code.setSyntaxThemeAndSet(highlighter_list,colors)
        self.lsp_handler.updateSelectedSntxThemeInConfigs(h_ext,file_path)
        #self.lsp_handler.saveSelectedSyntxThemeAllCongigs()
        minimap_highlighter=self.lsp_handler.current_minimap_highlighter        
        if minimap_highlighter and self.lsp_handler.current_minimap_type==h_ext:
            self.Code.setSyntaxThemeAndSet([self.lsp_handler.current_minimap_highlighter],colors)

        #colors["language"]
        for key, value in colors.items():
            if key=="language":
                continue
            self.addThemeChangerButtons(key,value,h_ext,highlighter_list)

        self.Setting_D.createColorOption("Background", self.Code.linkEditorBgColor,self.Code.style_editor.bg_clr)
        

        if len(highlighter_list)>0:
            self.Setting_D.createSaveButton("",self.lsp_handler.saveSelectedSyntxTheme,[file_path,h_ext,highlighter_list[0]])

    def addThemeChangerButtons(self,key,value,ext,highlighter_list):
        self.Setting_D.createColorOption(
            key,
            lambda x:
            (self.Code.updateEditorSyntaxTheme(highlighter_list,key,x),
             self.Code.updateMinimapSyntaxTheme(self.lsp_handler,ext,key,x)),
            value
            )



    def settingCustomCodeTheme(self):
        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)

        #self.layout_groupbox_for_theme,group_bx = self.Setting_D.createGroupBoxForCustomWidgets("Code Theme",0)
        try:
            
            self.container_for_gropbx.deleteLater()
            self.file_tree_container.deleteLater()
            self.stheme_dock.close()
            self.ctheme_dock.close()


        except:
            pass

        self.container_for_gropbx=QtWidgets.QWidget()
        self.layout_groupbox_for_theme=QtWidgets.QGridLayout()
        self.container_for_gropbx.setLayout(self.layout_groupbox_for_theme)
        self.file_tree_container=self.Setting_D.createFileTreeModel("Theme List",
                                           self.onSelectSyntaxtTheme,
                                           self.Path_h.SYNTAX_HIGHLIGHTER_DIR,
                                           self.Path_h)
        
        self.stheme_dock=self.Setting_D.addCustomWidgetsInDock(7,"Select Theme",self.file_tree_container)
        
        self.ctheme_dock=self.Setting_D.addCustomWidgetsInDock(7,"Change Theme",self.container_for_gropbx)


    def onCDThemeSelected(self,file_path,load_full=True):
        print(file_path)
        theme_name=self.Path_h.filePathToFileName(file_path)
        
        if load_full:    
            with open(file_path,"r")as f:
                self.loadFullCDTheme(f.read())

        dir_childs:list=Dir_Scanner.child_scan(self.Path_h.SYNTAX_HIGHLIGHTER_DIR)
        #print(dir_childs)
        for child in dir_childs:
            h_ext=f'.{child}'
            stheme_path=os.path.join(self.Path_h.SYNTAX_HIGHLIGHTER_DIR,child,theme_name)
            self.lsp_handler.updateSelectedSntxThemeInConfigs(h_ext,stheme_path)
            if os.path.exists(stheme_path):
                    
                with open(stheme_path,"r")as f:
                    colors=eval(f.readline())
                highlighter_list:str=self.lsp_handler.running_highlighters[h_ext]

                self.Code.setSyntaxThemeAndSet(highlighter_list,colors)
                self.lsp_handler.updateSelectedSntxThemeInConfigs(h_ext,file_path)
                #self.lsp_handler.saveSelectedSyntxThemeAllCongigs()
                minimap_highlighter=self.lsp_handler.current_minimap_highlighter        
                if minimap_highlighter and self.lsp_handler.current_minimap_type==h_ext:
                    self.Code.setSyntaxThemeAndSet([self.lsp_handler.current_minimap_highlighter],colors)

        with open(self.Path_h.Code.SELECTED_CD_THEME,'w')as f:
            print("saved ",file_path)
            f.write(file_path)

    def settingCDThemes(self):
        self.Setting_D.removeWidgets(self.Setting_D.layout_frame_2)

        #self.layout_groupbox_for_theme,group_bx = self.Setting_D.createGroupBoxForCustomWidgets("Code Theme",0)
        try:
            
            self.container_for_gropbx.deleteLater()
            self.file_tree_container.deleteLater()
            self.stheme_dock.close()
            self.ctheme_dock.close()


        except:
            pass

        self.container_for_gropbx=QtWidgets.QWidget()
        self.layout_groupbox_for_theme=QtWidgets.QGridLayout()
        self.container_for_gropbx.setLayout(self.layout_groupbox_for_theme)
        self.file_tree_container=self.Setting_D.createFileTreeModel("Theme List",
                                           self.onCDThemeSelected,
                                           self.Path_h.CD_THEMELIST_DIR,
                                           self.Path_h)
        
        self.scdtheme_dock=self.Setting_D.addCustomWidgetsInDock(8,"Select Theme",self.file_tree_container)
        
        #self.ctheme_dock=self.Setting_D.addCustomWidgetsInDock(7,"Change Theme",self.container_for_gropbx)




        #box_layout = self.Setting_D.createGroupBox("Theme Color", self.layout_groupbox_for_theme, 1)
        """
        self.Setting_D.createColorOption("Other", lambda x:self.Code.linkCodeThemeOther("other",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['other'])
        self.Setting_D.createColorOption("Keyword", lambda x:self.Code.linkCodeThemeOther("keyword",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['keyword'])
        self.Setting_D.createColorOption("Operator", lambda x:self.Code.linkCodeThemeOther("operator",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['operator'])
        self.Setting_D.createColorOption("Class", lambda x:self.Code.linkCodeThemeOther("class",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['class'])
        self.Setting_D.createColorOption("Function", lambda x:self.Code.linkCodeThemeOther("function",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['function'])
        self.Setting_D.createColorOption("Def_Name", lambda x:self.Code.linkCodeThemeOther("def_func",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['def_func'])
        self.Setting_D.createColorOption("String", lambda x:self.Code.linkCodeThemeOther("string",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['string'])
        self.Setting_D.createColorOption("Comment", lambda x:self.Code.linkCodeThemeOther("comment",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['comment'])
        self.Setting_D.createColorOption("Number", lambda x:self.Code.linkCodeThemeOther("number",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['number'])
        self.Setting_D.createColorOption("Constant", lambda x:self.Code.linkCodeThemeOther("constants",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['constants'])
        self.Setting_D.createColorOption("Brackets", lambda x:self.Code.linkCodeThemeOther("brackets",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['brackets'])
        self.Setting_D.createColorOption("Self", lambda x:self.Code.linkCodeThemeOther("self",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['self'])
        self.Setting_D.createColorOption("Object", lambda x:self.Code.linkCodeThemeOther("object",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['object'])
        self.Setting_D.createColorOption("Method", lambda x:self.Code.linkCodeThemeOther("method",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['method'])
        self.Setting_D.createColorOption("Method_Call", lambda x:self.Code.linkCodeThemeOther("method_call",x),self.Code.highlighter[len(self.Code.highlighter)-1].colors['method_call'])
        """
        #self.Setting_D.createColorOption("", self.Code.linkEditorBrdrColor,self.Code.style_editor.brdr_clr)
            
    
    def setSettingList(self):
        self.Setting_D.multiVButtons(
            [
                ["Window",self.settingMainWindow],
                ["Toolbox", self.settingToolBox],
                ["Map", self.settingDockPanel],
                ["DockWidget", self.settingDockWidgets],
                ["Editor", self.settingEditor],
                ["TabBar", self.settingTabbar],
                ["ScrollBar", self.settingScrollBars],
                ["Theme",self.settingCustomCodeTheme],
                ["CDTheme",self.settingCDThemes]
            ],
            self.Setting_D.layout_frame_1,
        )
        self.Setting_D.addStyleSheetTextEditDock(5,"Tabbar",self.Code.tabbar_editor.styleSheet(),
                                                 lambda text:self.Code.tabbar_editor.setStyleSheet(text))
        self.Setting_D.addStyleSheetTextEditDock(1,"Frame",self.Code.frame_toolbox.styleSheet(),
                                                 lambda text:(self.Code.frame_tabbar.setStyleSheet(text),self.Dock.frame_toolbox.setStyleSheet(text)))
        
        self.Setting_D.addStyleSheetTextEditDock(1,"Button",self.Code.add_subwindow_btn.styleSheet(),
                                                 lambda text:(self.Code.setToolButtonStyleSheet(text),self.Dock.setToolButtonStyleSheet(text)))
        

    def saveSettings(self, path, var_dict): 
        with open(path, "w") as file:
            file.write(f"{var_dict}")

            file.close()
                           
    
    #settings loaders
    
    
    def loadPanelFileTreeSettings(self,var_dict=None):
        if not var_dict:
                
            with open(self.Path_h.Dock.PFILE_TREE_S, "r") as file:
                var_dict = file.read()

                var_dict = eval(var_dict.splitlines()[0])

        self.Dock.Panel.file_tree.bg_clr = var_dict["bg_clr"]
        self.Dock.Panel.file_tree.brdr_clr = var_dict["brdr_clr"]
        self.Dock.Panel.file_tree.btn_clr = var_dict["btn_clr"]

        self.Dock.Panel.file_tree.scroll_bar_clr = var_dict["scroll_bar_clr"]
        self.Dock.Panel.file_tree.scroll_handel_clr = var_dict["scroll_handel_clr"]

        self.Dock.Panel.file_tree.applyStyle()

        

    def loadPaneSymbolTreeSettings(self,var_dict=None):
        if not var_dict:
                
            with open(self.Path_h.Dock.PMAP_TREE_S, "r") as file:
                var_dict = file.read()

                var_dict = eval(var_dict.splitlines()[0])

        self.Dock.Panel.map_tree.bg_clr = var_dict["bg_clr"]
        self.Dock.Panel.map_tree.brdr_clr = var_dict["brdr_clr"]
        self.Dock.Panel.map_tree.btn_clr = var_dict["btn_clr"]

        self.Dock.Panel.map_tree.scroll_bar_clr = var_dict["scroll_bar_clr"]
        self.Dock.Panel.map_tree.scroll_handel_clr = var_dict["scroll_handel_clr"]

        self.Dock.Panel.map_tree.applyStyle()

        
    def loadToolBoxWindgetSsttings(self,var_dict=None):
        if not var_dict:
                
            with open(self.Path_h.Dock.TOOLBOX_S, "r") as file:
                var_dict = file.read()
                file.close()

                var_dict = eval(var_dict.splitlines()[0])
                print(var_dict)

        self.Dock.frame_toolbox.updateVar(var_dict)

        with open(self.Path_h.Dock.TOOL_CONTAINER_S, "r") as file:
            var_dict = file.read()
            file.close()

            var_dict = eval(var_dict.splitlines()[0])
            print(var_dict)
        
        self.Dock.frame_toolbox.h=var_dict['h']
        self.Dock.frame_toolbox.e_spacing=var_dict['spacing']
        self.Dock.frame_toolbox.brdr_radius=var_dict['brdr_radius']
        self.Dock.linkToolBoxRadius(self.Dock.frame_toolbox.brdr_radius)
            
        self.Dock.linkToolBoxSize(self.Dock.frame_toolbox.h)
        
        self.Dock.frame_toolbox.applyStyle()
        #self.Dock.sizeToolbox(self.Dock.frame_toolbox.h)
        
        self.loadToolButtonSettings()


    def loadToolBoxContainerSettings(self,var_dict=None):
        """if not var_dict:
                
            with open(self.Path_h.Code.TOOLBUTTON_S, "r") as file:
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])
        self.Code.stylish_t_btn.bg_clr = var_dict["bg_clr"]
        self.Code.stylish_t_btn.brdr_clr = var_dict["brdr_clr"]
        self.Code.stylish_t_btn.brdr_think = var_dict["brdr_think"]
        self.Code.stylish_t_btn.radius = var_dict["radius"]
        self.Code.stylish_t_btn.hover = var_dict["hover"]
        self.Code.stylish_t_btn.wh = var_dict["wh"]
        self.Code.stylish_t_btn.icon_size = var_dict["icon_size"]

        self.Code.linkToolBoxButtonSize(self.Code.stylish_t_btn.wh)
        # self.Code.sizeIconsToolbox(self.Code.stylish_t_btn.icon_size)
        self.Code.setPngIconsOnButton()
        file.close()

        with open(self.Path_h.Code.TOOL_CONTAINER_S, "r") as file:
            var_dict = file.read()
            var_dict = eval(var_dict.splitlines()[0])
            self.Code.tool_container_frame.h=var_dict['h']
            self.Code.linkToolBoxBtnSpacing(int((self.Code.tool_container_frame.h-self.Code.stylish_t_btn.wh*8)/8))
            file.close()
        """        
        """if not var_dict:

                with open(self.Path_h.Dock.TOOLBOX_S, "r") as file:
                    var_dict = file.read()
                    var_dict = eval(var_dict.splitlines()[0])
            self.Dock.frame_toolbox.bg_clr = var_dict["bg_clr"]
            self.Dock.frame_toolbox.brdr_clr = var_dict["brdr_clr"]
            self.Dock.frame_toolbox.brdr_think = var_dict["brdr_think"]
            self.Dock.frame_toolbox.brdr_radius = var_dict["brdr_radius"]
            self.Dock.frame_toolbox.w = var_dict["w"]

            self.Dock.linkToolBoxSize(self.Dock.frame_toolbox.w)
            self.Dock.frame_toolbox.applyStyle()
        """
        pass

    def loadToolButtonSettings(self,var_dict=None):

        if not var_dict:
                
            with open(self.Path_h.Dock.TOOLBUTTON_S, "r") as file:
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])

        self.Dock.stylish_t_btn.bg_clr = var_dict["bg_clr"]
        self.Dock.stylish_t_btn.brdr_clr = var_dict["brdr_clr"]
        self.Dock.stylish_t_btn.brdr_think = var_dict["brdr_think"]
        self.Dock.stylish_t_btn.radius = var_dict["radius"]
        self.Dock.stylish_t_btn.hover = var_dict["hover"]
        self.Dock.stylish_t_btn.wh = var_dict["wh"]
        self.Dock.stylish_t_btn.icon_size = var_dict["icon_size"]

        self.Dock.linkToolBoxButtonSize(self.Dock.stylish_t_btn.wh)
        #self.Dock.sizeIconsToolbox(self.Dock.stylish_t_btn.icon_size)
        self.Dock.setPngIconsOnButton()
                    
        self.Code.stylish_t_btn.bg_clr = var_dict["bg_clr"]
        self.Code.stylish_t_btn.brdr_clr = var_dict["brdr_clr"]
        self.Code.stylish_t_btn.brdr_think = var_dict["brdr_think"]
        self.Code.stylish_t_btn.radius = var_dict["radius"]
        self.Code.stylish_t_btn.hover = var_dict["hover"]
        self.Code.stylish_t_btn.wh = var_dict["wh"]
        self.Code.stylish_t_btn.icon_size = var_dict["icon_size"]
        self.Code.linkToolBoxButtonSize(self.Code.stylish_t_btn.wh)
        #self.Code.sizeIconsToolbox(self.Code.stylish_t_btn.icon_size)
        self.Code.setPngIconsOnButton()
        self.Dock.linkToolBoxButtonSize(24)
        self.Code.linkToolBoxButtonSize(24)

        

        with open(self.Path_h.Dock.TOOL_CONTAINER_S, "r") as file:
            var_dict = file.read()
            var_dict = eval(var_dict.splitlines()[0])
            
        
            #self.Dock.tool_container_frame.h=var_dict['h']
            #self.Dock.linkToolBoxBtnSpacing(int((self.Dock.tool_container_frame.h-self.Dock.stylish_t_btn.wh*6)/6))
            


            
    def loadDockWidgetSettings(self,var_dict=None):
        if not var_dict:    
            with open(self.Path_h.Code.MDI_S, "r") as file:
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])
        print("updaededededed......")
        #print(var_dict)
        DockWidgetStyle.updateVar(var_dict)
        DockWidgetStyle.updateAllStyle(var_dict,self.Code.dock_zone.dock_widgets_list)
        print(self.Code.dock_zone.activated_dock_widget)
        self.Code.dock_zone.setActivatDock(self.Code.dock_zone.activated_dock_widget)
        #self.Code.dock_zone.updateAllDockTheme(var_dict)
        
        #self.Code.mdi_area.applyStyle()

    def loadTextEditorSettingsByObj(self,text_edit:Custom.TextEditor):
    
        print("\n\n\n\n\n\n khdkadhskjds \n\n\n\n")
        try:
            self.Code.style_editor.applyStyle(text_edit)
            text_edit.update()
        except:pass

        

    def loadTextEditorSettings(self,var_dict=None):
        if not var_dict:
                    
            with open(self.Path_h.Code.EDITOR_S, "r") as file:
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])

        self.Code.style_editor.bg_clr = var_dict["bg_clr"]
        self.Code.style_editor.brdr_clr = var_dict["brdr_clr"]
        self.Code.style_editor.scroll_bar_clr = var_dict["scroll_bar_clr"]
        self.Code.style_editor.scroll_handel_clr = var_dict["scroll_handel_clr"]
        self.Code.style_editor.font_size = var_dict['font_size']
        self.Code.running_textedit_editor.indent_alfa=var_dict['indent_alfa']
        
        self.Code.running_textedit_editor.indent_rgba=var_dict['indent_rgba']
        
        self.Code.style_completer.scroll_bar_clr=var_dict["scroll_bar_clr"]
        self.Code.style_completer.scroll_handel_clr=var_dict["scroll_bar_clr"]
        
        try:
            self.Code.style_editor.applyStyle(self.Code.running_textedit_editor)
            self.Code.running_textedit_editor.update()
            self.Code.style_completer.applyStyle(self.Code.running_textedit_editor)
        except:pass

    

    def loadCompleterSettings(self,var_dict=None):
        if not var_dict:
                
            with open(self.Path_h.Code.COMPLITER_S,"r")as f:
                var_dict = f.read()
                var_dict = eval(var_dict.splitlines()[0])

            self.saveSettings(self.Path_h.Code.COMPLITER_S,var_dict)
        
        self.Code.style_completer.updateVar(var_dict)
        self.Code.style_completer.applyStyle(self.Code.running_textedit_editor)

        """with open(self.Path_h.Code.EDITOR_NUMPAD_S, "r") as file:
            var_dict = file.read()
            var_dict = eval(var_dict.splitlines()[0])

            self.Code.style_numpad.bg_clr = var_dict["bg_clr"]
            self.Code.style_numpad.brdr_clr = var_dict["brdr_clr"]
            self.Code.style_numpad.w=var_dict['w']
            # self.Code.textedit_numpad.scroll_bar_clr=var_dict['scroll_bar_clr']
            # self.Code.textedit_numpad.scroll_handel_clr=var_dict['scroll_handle_clr']
            try:
                self.Code.style_numpad.applyStyle(self.Code.textedit_numpad)
            except:pass
            file.close()"""

    def loadMiniMapSettings(self,var_dict=None):
        if not var_dict:

            with open(self.Path_h.Code.MINIMAP_S, "r") as file:
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])
        
        self.Code.mini_map.minimap_bg = var_dict["minimap_bg"]
        self.Code.mini_map.vp_brdr_rgba = var_dict["vp_brdr_rgba"]
        self.Code.mini_map.vp_brdr_hover_rgba = var_dict["vp_brdr_hover_rgba"]
        self.Code.mini_map.brdr_width=var_dict["brdr_width"]
        self.Code.mini_map.applyMiniMapStyle()
        self.Code.mini_map.applyViewPortBorderStyle()
        self.Code.mini_map.applyViewPortStyle()
        self.Code.configCodeEditor()
        """
        for i,subwindow in enumerate(self.Code.subwindow_addr_buffer):
            self.Code.style_editor.applyStyle(subwindow[1])
            #self.Code.style_numpad.applyStyle(subwindow[2])
            self.Code.style_completer.applyStyle(subwindow[1])
            """

    def loadCodeTabbar(self,var_dict=None):
        if not var_dict:
                
            with open(self.Path_h.Code.TABBAR_S, "r") as file:
                var_dict = file.read()

                var_dict = eval(var_dict.splitlines()[0])

        self.Code.tabbar_editor.bg_clr = var_dict["bg_clr"]
        # self.Code.textedit_code_editor.brdr_clr=var_dict['brdr_clr']
        self.Code.tabbar_editor.tab_clr = var_dict["tab_clr"]

        #self.Code.frame_tabbar.h=var_dict["h"]
        #self.Code.tabbar_editor.tab_size=var_dict["tab_size"]
        self.Code.tabbar_editor.tabbar_h=var_dict["tabbar_h"]
        self.Code.frame_tabbar.setFixedHeight(var_dict["tabbar_h"])
        self.Code.tabbar_editor.tab_padding_rl=var_dict["tab_padding_rl"]
        self.Code.tabbar_editor.tab_padding_tb=var_dict["tab_padding_tb"]
        self.Code.tabbar_editor.brdr=var_dict["tab_brdr_clr"]
        
        self.Code.tabbar_editor.tab_selected_clr=var_dict["tab_selected_clr"]
        self.Code.tabbar_editor.tab_hover_clr=var_dict["tab_hover_clr"]
        self.Code.tabbar_editor.selected_font_clr=var_dict["selected_font_clr"]
        self.Code.tabbar_editor.font_clr=var_dict["font_clr"]
        #self.Code.tabbar_editor.font_clr=var_dict["font_clr"]
        
        # self.Code.tabbar_editor.clr['scroll_handle_clr']

        self.Code.tabbar_editor.applyStyle()
        #self.Code.linkTabbarFrameHSize(self.Code.tabbar_editor.tab_size)
        self.Code.linkTabbarHSize(self.Code.tabbar_editor.tab_padding_tb)

        self.Dock.Panel.toolbar_file_tree.bg_clr=var_dict["tab_clr"]
        self.Dock.Panel.toolbar_file_tree.brdr_clr=var_dict["tab_brdr_clr"]
        self.Dock.Panel.toolbar_file_tree.applyStyle()
        self.Dock.Panel.toolbar_file_tree.setStyleSheet(f"background-color:{var_dict['tab_clr']}")


        self.Dock.Panel.toolbar_map_tree.bg_clr=var_dict["tab_clr"]
        self.Dock.Panel.toolbar_map_tree.brdr_clr=var_dict["tab_brdr_clr"]
        self.Dock.Panel.toolbar_map_tree.applyStyle()
        self.Dock.Panel.toolbar_map_tree.setStyleSheet(f"background-color:{var_dict['tab_clr']}")
        
        
        self.virtual_CD.tabbar.bg_clr = var_dict["bg_clr"]
        # self.Code.textedit_code_editor.brdr_clr=var_dict['brdr_clr']
        self.virtual_CD.tabbar.tab_clr = var_dict["tab_clr"]
        #self.Code.frame_tabbar.h=var_dict["h"]
        #self.virtual_CD.tabbar.tab_size=var_dict["tab_size"]
        #self.virtual_CD.tabbar.tabbar_h=var_dict["tabbar_h"]
        #self.virtual_CD.tabbar.tab_padding_rl=var_dict["tab_padding_rl"]
        #self.virtual_CD.tabbar.tab_padding_tb=var_dict["tab_padding_tb"]
        self.virtual_CD.tabbar.brdr=var_dict["tab_brdr_clr"]
        self.virtual_CD.tabbar.tab_selected_clr=var_dict["tab_selected_clr"]
        self.virtual_CD.tabbar.tab_hover_clr=var_dict["tab_hover_clr"]
        self.virtual_CD.tabbar.selected_font_clr=var_dict["selected_font_clr"]
        self.virtual_CD.tabbar.font_clr=var_dict["font_clr"]
        self.virtual_CD.tabbar.applyStyle()
        

        



    def loadDockTabbar(self):
        with open(self.Path_h.Dock.TABBAR_S, "r") as file:
            var_dict = file.read()
            var_dict = eval(var_dict.splitlines()[0])
            """
            self.Dock.Panel.tabbar_panel.bg_clr = var_dict["bg_clr"]
            # self.Dock.Panel.textedit_code_editor.brdr_clr=var_dict['brdr_clr']
            self.Dock.Panel.tabbar_panel.tab_clr = var_dict["tab_clr"]
            # self.Dock.Panel.tabbar_panel.clr['scroll_handle_clr']
            #self.Dock.Panel.tabbar_panel.tab_size=var_dict["tab_size"]
            self.Dock.Panel.tabbar_panel.tab_padding_rl=var_dict["tab_padding_rl"]
            self.Dock.Panel.tabbar_panel.tab_padding_tb=var_dict["tab_padding_tb"]
            self.Dock.Panel.tabbar_panel.brdr=var_dict["tab_brdr_clr"]
            
            self.Dock.Panel.tabbar_panel.tab_selected_clr=var_dict["tab_selected_clr"]
            self.Dock.Panel.tabbar_panel.tab_hover_clr=var_dict["tab_hover_clr"]
            self.Dock.Panel.tabbar_panel.font_clr=var_dict["font_clr"]
            self.Dock.Panel.tabbar_panel.applyStyle()
            self.Dock.linkTabbarHSize(self.Dock.Panel.tabbar_panel.tab_padding_tb)
            file.close()
            """

    def loadSyntaxThemes(self,theme_p=None):

        with open(self.Path_h.Code.SELECTED_SYNTAX_THEME, "r") as file:
            theme_p = file.readline()
            print(theme_p)
            print("\n\n\n\n\n\n\n\n\n\n\nDock...........")
            self.onCDThemeSelected(theme_p,False)

    def loadFullCDTheme(self,theme:str):
        
        for var_line in theme.splitlines():
            #print(var_line)

            try:
                var_dict=eval(var_line)
                loader=self.get_loader[var_dict['w_type']] 
                loader(var_dict)
                print("theme loaded....")
                
            except Exception as e:
                print(var_line)
                print(".........Error iN 'oadFUllCDTheme'......",e)
                pass

    def loadWindowTitleBarSettings(self,var_dict=None):
        if not var_dict:
                
            with open(self.Path_h.CodeDock.WINDOW_TITLEBAR_S, "r") as file:
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])

        self.MainWindow.ttlbr_bg_clr=var_dict["ttlbr_bg_clr"]
        self.MainWindow.ttlbr_text_clr=var_dict["ttlbr_text_clr"]
        self.MainWindow.close_btn_clr=var_dict["close_btn_clr"]
        self.MainWindow.maximize_btn_clr=var_dict["maximize_btn_clr"]
        self.MainWindow.btns_radius=var_dict["btns_radius"]
        self.MainWindow.ttlbr_hover=var_dict["ttlbr_hover"]
        self.MainWindow.maximize_btn_hover=var_dict["maximize_btn_hover"]
        self.MainWindow.close_btn_hover=var_dict["close_btn_hover"]
        self.MainWindow.ttlbr_hsize=var_dict["ttlbr_size"]
        self.MainWindow.ttlbr_btns_size=var_dict["ttlbr_btns_size"]
        self.MainWindow.ttlbr_title_font=var_dict["ttlbr_title_font"]
        


        self.MainWindow.applyStyle()

    def loadVirtualCDTabbarSettings(self,var_dict=None):
        if not var_dict:

            with open(self.Path_h.CodeDock.VIRTUAL_CD_TABBAR_S, "r") as file:
                
                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])
            
        self.virtual_CD.tabbar.updateVar(self.virtual_CD.tabbar,var_dict)
    
    def loadVirtualCDWidget(self,var_dict=None):
        if var_dict:
            with open(self.Path_h.CodeDock.VIRTUAL_CD_WIDGET_S, "r") as file:

                var_dict = file.read()
                var_dict = eval(var_dict.splitlines()[0])
        self.virtual_CD.updateVar(self.virtual_CD,var_dict)
            
    def loadPreviewTabSwitcher(self):
                
        with open(self.Path_h.CodeDock.PREVIEW_TAB_SWITCHER, "r") as file:

            var_dict = file.read()
            var_dict = eval(var_dict.splitlines()[0])

            self.Code.ui_tab_switcher.updateVar(var_dict)
            

    def loadOthers(self):
        with open(self.Path_h.Dock.OTHER, "r") as file:
            var_dict = file.read()

            var_dict = eval(var_dict.splitlines()[0])

            self.Code.Path_h.LANG_THEME=var_dict["icon_theme"]
            self.Code.Path_h.TOOLS_THEME=var_dict["icon_theme"]
            self.Dock.Path_h.LANG_THEME=var_dict["icon_theme"]
            self.Dock.Path_h.TOOLS_THEME=var_dict["icon_theme"]

            self.Code.Path_h.updateIcon()
            self.Dock.Path_h.updateIcon()
            self.Code.updateIconInSubwindowAndTabbar()
            

    def popUpTabSwitcher(self):
        #self.popup = Tab_V_Switcher(self.screen_size)
        widgets=[]


        theme_list=Dir_Scanner.child_scan(self.Path_h.CD_THEMELIST_DIR)
        selected_theme=self.Path_h.filePathToFileName(open(self.Path_h.Code.SELECTED_CD_THEME,"r").read())
        
        index=0
        for i,theme_name in enumerate(theme_list):
            theme=self.Path_h.pathJoin(self.Path_h.CD_THEMELIST_DIR,theme_name)
            widgets.append([theme,theme_name,None])
            
            if selected_theme==theme_name:
                index=i
        
        self.basic_tab_switcher.setTabsItems(widgets)
        self.basic_tab_switcher.setCurrentRow(index)
        self.basic_tab_switcher.show()

    