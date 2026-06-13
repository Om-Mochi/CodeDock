from CodeDock.C_Widgets.Custom import Custom
from CodeDock.C_Widgets.CodeArea import MDISubWindow,RefrenceItemWidget,RefrenceManager
from CodeDock.C_Widgets.WebEngine import WebBrowserWidget
from CodeDock.Code.src.controllers.CodeSettings import Code_Settings
from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.Code.src.controllers.CodePadHighlighter import PythonHighlighter,IndentationHighlighter,CppHighlighter
#from CodeDock.Code.src.controllers.KeysHandler import KeyPressHandler
#from CodeDock.Lang.L_py.PyTags import PyLsp
from CodeDock.src.controllers.TabSwitcher import Tab_V_Switcher,Ui_Tab_Switcher,BasicTabSwitcher
from CodeDock.src.controllers.WorkSpaceHandler import WorkSpace_Handler


from CodeDock.DockingSystem.widgets.DockWidget import DockWidget
from CodeDock.Debuger import Debug
#from CodeDock.Code.src.views. import 
import hashlib
import dataclasses
import typing
                

@dataclasses.dataclass
class subWindowServiceConfigs:
    subwindow_obj:MDISubWindow
    tab_index:int
    file_path:typing.Union[str,None]
    textedit_obj:typing.Union[Custom.TextEditor,None]
    subwindow_ssmngr_obj:WorkSpace_Handler.Store.SubWindow



class Code_Main(Code_Settings):
    whenSubWindowEditorAdded=QtCore.pyqtSignal()
    whenSubWindowSwitch=QtCore.pyqtSignal()
    whenKeyEnterPressedInTextEdit=QtCore.pyqtSignal()    
    whenMiniMapRefresh=QtCore.pyqtSignal()
    SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
    
    
    def __init__(self,app):
        super().__init__()
        self.mdi_area.setPathHandler(self.Path_h)
                
        self.app=app
        #self.pyright=PyrightLSP()
        self.screen_size=self.app.primaryScreen().geometry()

        self.ui_tab_switcher=Ui_Tab_Switcher()
        self.basic_tab_switcher=BasicTabSwitcher()
        #self.which_tab_swicher=self.basic_tab_switcher
        self.ui_tab_switcher.whenTabSelected.connect(lambda i:self.activeEditorByTab(i))
        self.basic_tab_switcher.whenTabSelected.connect(lambda i:self.activeEditorByTab(i))
        #self.pylsp=PyLsp()
        self.mdi_area.setAcceptDrops(True)
            
        self.setting_dialog_flag=False
        
        self.subwindow_service_buffer:dict[MDISubWindow,subWindowServiceConfigs]={}
        self.subwindow_addr_buffer:list[list[MDISubWindow,Custom.TextEditor,WorkSpace_Handler.Store.SubWindow]]=[]
        self.other_subwin_obj_buffer=[]
        self.running_subwindow:MDISubWindow=None
        self.running_subwindow_session_mngr:WorkSpace_Handler.Store.SubWindow=None
        self.previous_textedit=None
        
        self.sub_editor_textedit=None
        
        self.subwindow_index_id=0
        
        self.line_no=1
        self.last_rpath=None
        self.codefile_path_list=[]
        self.codefile_path=None
        self.dummy_codefile_path=None

        self.rm_subwin_filter=None
        self.d_click_nrml_mxmz=False #set bool for normal and maximize subwindow
        self.untitled_title_i=1
        self.refrence_title_i=1
        #self.set_tab_size(self.textedit_for_code_editor,4)
        self.frame_tabbar.show()
        
        self.tab_list=[]
        self.mini_map_highlighter=PythonHighlighter(self.mini_map.document())
        
        #self.tabbar_editor.setUsesScrollButtons(False)
        #self.tabbar_editor.setExpanding(True)
        self.tabbar_editor.tabMoved.connect(self.whenTabMoved)
        self.tabbar_editor.setTabsClosable(True)
        self.layout_tabbar.addWidget(self.tabbar_editor)
        self.tabbar_editor.setFixedHeight(40)

        for btn in self.tabbar_editor.findChildren(QtWidgets.QToolButton):
            btn.setFixedWidth(2)   # Bigger buttons
            #btn.setIconSize(QtCore.QSize(24, 24))  # Bigger icons
        self.onNewTextCode=lambda:...
        self.onTypeInEditor=lambda:...
        #self.themeComponentsMap()
        #self.label_address_list=[]
        #self.setComponentsBtns(self.components_list,self.label_address_list)
        #self.layout_code_components_map.addWidget(self.zoom_in_btn,0,0)
        #self.mdi_area.subWindowActivated.connect(self.subWindowActiveSingnal)

        self.mdi_area.whenWindowActivated.connect(self.onDockWidgetActivate)
        self.mdi_area.whenWindowClose.connect(self.closeSubWindowAndTab)

        self.mdi_area.linkDropUrls(self.openUrlSubwindow)
        
        self.dock_zone.whenPathUrlDroped.connect(self.openUrlDockWidget)
        #self.dock_zone.whenMouseReleaseWithDrop.connect(self.openUrlSubwindow)
        #self.dock_zone.whenDockActivated.connect(self.onDockWidgetActivate)




        self.tabbar_editor.tabBarClicked.connect(self.activeEditorByTab)
        #self.tabbar_editor.currentChanged.connect(self.activeEditorByTab)
        self.tabbar_editor.whenDoubleClick.connect(self.setMaxAndMinOnDoubleclick)
        self.tabbar_editor.tabCloseRequested.connect(self.onTabClose)
        self.dock_zone.whenKey_Ctrl_Shift_Tab_Pressed.connect(lambda:self.popUpTabSwitcher(self.ui_tab_switcher))
        self.dock_zone.whenKey_Ctrl_Tab_Pressed.connect(lambda:self.popUpTabSwitcher(self.basic_tab_switcher))
        self.dock_zone.whenDockClose.connect(self.closeSubWindowAndTab)
        self.dock_zone.setPathH(self.Path_h)
        #self.refrenceDisplaySubWindow()
        #self.setNumpadWidth()
        self.frame_mini_map_b.show()

            
        self.save_subwindow_session_debouncer=QtCore.QTimer()
        self.save_subwindow_session_debouncer.setInterval(300)
        self.save_subwindow_session_debouncer.setSingleShot(True)
        self.save_subwindow_session_debouncer.timeout.connect(self.saveSubwindowSession)

        self.mini_map_debounce_timer=QtCore.QTimer()
        self.mini_map_debounce_timer.setInterval(1000)
        self.mini_map_debounce_timer.setSingleShot(True)
        self.mini_map_debounce_timer.timeout.connect(self.setEdtrCodeInMiniMap)

        #self.last_hash=""



    def dummyCodeFilePath(self):
        return self.dummy_codefile_path

    def onDockWidgetActivate(self,dock_widget:DockWidget):
        self.running_subwindow=dock_widget
        
        self.setSelectedTab(dock_widget)


        if self.lsp_server!=None:
            self.lsp_server.pause=True


        subwin_services=self.subwindow_service_buffer[dock_widget]

        if subwin_services.file_path!=None:
            self.lsp_server.pause=False            
            self.sub_editor_textedit=subwin_services.textedit_obj
            self.running_textedit_editor=subwin_services.textedit_obj

            self.running_subwindow_session_mngr=subwin_services.subwindow_ssmngr_obj
            
            self.codefile_path=subwin_services.file_path
            self.mini_map.editor=self.running_textedit_editor
            self.mini_map.subwindow=self.running_subwindow
            self.running_textedit_editor.verticalScrollBar().valueChanged.connect(self.mini_map.sync_minimap_scroll)
            
            self.onNewTextCode()

            self.whenSubWindowSwitch.emit()
            self.startMiniMapDeboucingTimer()
    

    def popUpTabSwitcher(self,which_tab_switcher):
        #self.popup = Tab_V_Switcher(self.screen_size)
        widgets=[]

        for i,subwindow in enumerate(self.dock_zone.dock_widgets_list):

            widgets.append([subwindow,subwindow.title(),self.Path_h.getExtensionIcon(subwindow.title(),False)])

        if self.ui_tab_switcher==which_tab_switcher:    
            #self.popup.connect_on_tabchange=self.onTabSwitcherChangeTab
            
            self.ui_tab_switcher.grabAndSet(widgets,self.Path_h.TAB_IMAGE_DIRPATH)
            #self.ui_tab_switcher.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            self.ui_tab_switcher.show()
            self.ui_tab_switcher.activateWindow()
            self.ui_tab_switcher.raise_()

            #self.ui_tab_switcher.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            
            self.ui_tab_switcher.set_selected_index(self.tabbar_editor.currentIndex())
        
        elif self.basic_tab_switcher==which_tab_switcher:
            self.basic_tab_switcher.setTabsItems(widgets)
            self.basic_tab_switcher.setCurrentRow(self.tabbar_editor.currentIndex())
            self.basic_tab_switcher.show()


    def onTabSwitcherChangeTab(self,tab_index):

        subwin_list=self.mdi_area.subWindowList()
        self.onDockWidgetActivate(subwin_list[tab_index])
             
    def setMaxAndMinOnDoubleclick(self,index):
        widget=self.tabbar_editor.tabData(index)
        widget:DockWidget

        if widget.isHidden():
            widget.show()
            return
            

        if self.d_click_nrml_mxmz==False:
            self.d_click_nrml_mxmz=True    
            self.dock_zone.setDockToMaximize(widget)
            self.dock_zone.is_any_dock_maximized=True

        else:
            self.d_click_nrml_mxmz=False    
            self.dock_zone.setMaximizedToDock(widget)
            self.dock_zone.is_any_dock_maximized=False
            
            
    ######################
    def isSubWindowHere(self,path):
        for subw in self.subwindow_addr_buffer:
            if self.Path_h.filePathToFileName(path)==subw[0].windowTitle():
                return True
        
    def setSubWindowActiveViaPath(self,path):
        for subw in self.codefile_path_list:
            if path==subw[1]:

                self.onDockWidgetActivate(subw[0])

    #####################

    def openUrlDockWidget(self,file_url,dock_widget):
        file_name:str=self.Path_h.filePathToFileName(file_url)
        
        if not file_url:
            self.addSubWindowEditor(dock_widget=dock_widget)

        elif self.Path_h.isSupportFileExt(file_name):
                
            with open(file_url,'r')as file:
                text_code=file.read()
                file.close()
            
            self.dummy_codefile_path=self.Path_h.createDummyFile(file_url,text_code)

            if file_url:
                self.codefile_path=file_url
                file_name:str=self.Path_h.filePathToFileName(file_url)
                subwindow=self.addSubWindowEditor(file_name,True,dock_widget)
            #self.components_list=tagsPython(self.dummy_codefile_path)
            self.textedit_code_editor.setPlainText(text_code)
            

            self.onNewTextCode()
            if file_url:
                return subwindow

    
        elif self.Path_h.isSupportImgExt(file_name):
            d=self.subWinImageViewer(file_url,dock_widget)
            return d
        
    def openUrlSubwindow(self,file_url):
        
        file_name:str=self.Path_h.filePathToFileName(file_url)
        
        if not file_url:
            self.addSubWindowEditor()

        elif self.Path_h.isSupportFileExt(file_name):
                
            with open(file_url,'r')as file:
                text_code=file.read()
                file.close()
            
            self.dummy_codefile_path=self.Path_h.createDummyFile(file_url,text_code)

            if file_url:
                self.codefile_path=file_url
                file_name:str=self.Path_h.filePathToFileName(file_url)
                subwindow=self.addSubWindowEditor(file_name,True)
            #self.components_list=tagsPython(self.dummy_codefile_path)
            self.textedit_code_editor.setPlainText(text_code)
            

            self.onNewTextCode()
            if file_url:
                return subwindow

    
        elif self.Path_h.isSupportImgExt(file_name):
            self.subWinImageViewer(file_url)
            
    
    def activeEditorByTab(self,index):
        wiidget=self.tabbar_editor.tabData(index)
        
        if wiidget!=None:
            
            if self.dock_zone.is_any_dock_maximized:
                self.dock_zone.setDockToMaximize(wiidget)
            self.dock_zone.setActivatDock(wiidget)


        """
        for subwindow in self.tab_list:
            if self.tabbar_editor.tabText(index)==subwindow.windowTitle():
                if self.running_subwindow.isMaximized():
                    subwindow.show()
                    subwindow.showMaximized()
                else:
                    subwindow.show()
                    subwindow.setWindowActivate()
    
        """    
    #def appendTabs(self,swin_addr,tab_name='untitled'):
        
    """
    def createTabBarButtons(self,swin_addr,tab_name='untitled'):
        button=QtWidgets.QPushButton(f'{tab_name}')
        #button.setIcon(QtGui.QIcon("/home/omx/Downloads/python.png"))  # Replace with a valid icon file path
        button.setIconSize(QtCore.QSize(15,15))  # Set icon size to 30x30
        button.setFixedHeight(25)
        #button.setFixedWidth(110)
        button.setCheckable(False) 
        button.clicked.connect(lambda:(self.maximizeSubWindow(button,swin_addr)))
        #self.layout_tabbar.addWidget(button)
    
        self.linkTabbarColorAndSize()
        return button
        """
    
    
    def setSelectedTab(self,dock_widget:DockWidget):
        if dock_widget:
            tab_i=self.subwindow_service_buffer[dock_widget].tab_index
            self.tabbar_editor.setCurrentIndex(tab_i)
        else:print("\n\n\n\n\ndockwidget is NONE so Not Seletected .......\n\n\n\n\n")


    def whenTabMoved(self,from_i,to_i):
        #update tab indexes

        for t_i in range(to_i,self.tabbar_editor.count()):
            subwin_obj=self.tabbar_editor.tabData(t_i)
            self.subwindow_service_buffer[subwin_obj].tab_index=t_i
            


    def onTabClose(self,index):
        subwindow=self.tabbar_editor.tabData(index)
        #print(index,"index")
        self.closeSubWindowAndTab(subwindow,index)



    def closeSubWindowAndTab(self,subwindow,index=None):
        if not index:
            index=self.subwindow_service_buffer[subwindow].tab_index
        
        if self.tabbar_editor.tabText(index)=="setting":
            self.setting_dialog_flag=False
            
        self.tabbar_editor.removeTab(index)
        self.subwindow_service_buffer.pop(subwindow)
        #self.mdi_area.closeSubWindow(subwindow)
        self.mdi_area.subwindow_buffer.pop(index)
        for t_i in range(index,self.tabbar_editor.count()):
            subwin_obj=self.tabbar_editor.tabData(t_i)
            
            self.mdi_area.subwindow_states[subwin_obj].index=t_i
            
            self.subwindow_service_buffer[subwin_obj].tab_index=t_i


        self.activeEditorByTab(self.tabbar_editor.currentIndex())

        """
        if subwindow.windowTitle()=="setting":
            self.setting_dialog_flag=False

        self.subwindow_service_buffer.pop(subwindow)
        self.activeEditorByTab(self.tabbar_editor.currentIndex())
        """
            
    def maximizeSubWindow(self,tab_i,swin_addr):
        #self.setCheckableTabbarButton()
        swin_addr.showMaximized()


    def startMiniMapDeboucingTimer(self):
        
        self.mini_map_debounce_timer.start()
    
    
    def setEdtrCodeInMiniMap(self):
        self.mini_map.setPlainText(self.running_textedit_editor.toPlainText())
        self.whenMiniMapRefresh.emit()
        #if self.dummy_codefile_path!=None:
            
            #self.mini_map.setDocument(None)
            #self.mini_map.setDocument(self.running_textedit_editor.document())
            
            #current_text = self.running_textedit_editor.toPlainText()
            #current_hash = hashlib.md5(current_text.encode()).hexdigest()

            #if current_hash != self.last_hash:
            #    self.last_hash = current_hash
            #    self.mini_map.document().setPlainText(current_text)
            #self.frame_mini_map_b.show()
            #self.animation_mini_map_frame.show(QtCore.QRect(400, 50, 90, 200),QtCore.QRect(310, 50, 90, 200))
            #self.mini_map.clear()
            #self.mini_map.setPlainText(self.running_textedit_editor.toPlainText())
            #cursor = self.running_textedit_editor.textCursor()
            #block = cursor.block()
            #line = block.blockNumber()

            #scrollbar = self.mini_map.verticalScrollBar()
            #ratio=line / max(1, self.minimap.document().blockCount() - 1)
            #scrollbar.setValue(int(scrollbar.maximum() * ratio))
        
            
            # self.frame_mini_map_b.hide()
            #self.mini_map.clear()
        #self.animation_mini_map_frame.hide(QtCore.QRect(310, 50, 90, 200),QtCore.QRect(400, 50, 90, 200))

    def dropTextByUrl(self,file_path):pass

    def createNewSubWindowCodeEditor(self,code_source='',dock_widget:DockWidget=None):

        self.activeEditor(path_h=self.Path_h)
        
        self.code_source=code_source
        self.subwindow=MDISubWindow(self.mdi_area)
        
        
        #self.textedit_code_editor_2.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        
        self.mini_map.editor=self.textedit_code_editor
        self.mini_map.subwindow=self.subwindow
        self.textedit_code_editor.verticalScrollBar().valueChanged.connect(self.mini_map.sync_minimap_scroll)
        
        #self.mini_map.setVa()

        #for connect both scorllbar each other for scroll both in one time
        

        self.textedit_code_editor.link_url=self.dropTextByUrl



        
        #self.textedit_code_editor.textChanged.connect(self.eventTextEdit)
        #self.long_view_code_btn.setMinimumSize(QtCore.QSize(33, 33))
        #self.long_view_code_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.long_view_code_btn.setText("")
        #self.gridLayout_toolbox_b.addWidget(self.long_view_code_btn, 1, 0)

        #self.long_view_code_btn.clicked.connect(self.onLongViewFeature)
        #self.long_view_code_btn.setCheckable(True)
        

        #self.codeEditorSetCode()
        #self.subwindow.setWidget(self.widget_code_editor)
        #self.dock_zone.addDockWidget(self.widget_code_editor)
        if dock_widget:
            dock_widget.addWidget(self.textedit_code_editor)
            self.textedit_code_editor.whenFocusIn.connect(dock_widget.onFocusInWidgets)

        else:    
            dock_widget=self.dock_zone.addDockWidget(self.widget_code_editor)
            self.textedit_code_editor.whenFocusIn.connect(dock_widget.onFocusInWidgets)

        self.textedit_code_editor.dock_parent=dock_widget
        
        #self.frame_mini_map_b.hide()

        return dock_widget
    
    def setCodeSourceInEditor(self):
        codet_len=""
        
        #for i in range(1,self.code_len+1):codet_len+=f"{i}\n"
        
        #self.numpad_last_dig=self.code_len

        #self.textedit_numpad_2.setText(codet_len)
        #self.textedit_for_code_editor.setReadOnly(True)
        #fixed_source_code = self.code_source.replace("\n\n", "\n \n")
        
        self.textedit_code_editor.setPlainText(self.code_source)
        #self.textedit_code_editor_2.setPlainText(self.code_source)
        #self.set_fixed_font()
        #self.textedit_for_code_editor.setFont(QFont("Courier", 10))  # Set a monospace font for better readability
        #self.textedit_for_code_editor.setFont(QFont("Courier", 10))  # Monospace font
        
            

    def autoSaveCodeFile(self):

        if self.codefile_path!=None: 
            print("file goto saved")
            with open(self.codefile_path,'w')as file:
                file.write(self.running_textedit_editor.toPlainText())
                file.close()
            """
            with open(self.dummy_codefile_path,'w')as file:
                file.write(self.running_textedit_editor.toPlainText())
                file.close()"""
        

    def enterStrockInTextEditor(self):

        #code_lst=self.setComponents()
        if self.codefile_path!=None:
            self.whenKeyEnterPressedInTextEdit.emit()
            self.setScrollValueInEditor()




            """code_lst=tagsPython(self.dummy_codefile_path)
            
            self.t_components=len(code_lst)
            self.frame_code_map_size=len(code_lst)*self.map_btn_spacing_size
            """
            #self.frame_components_map.setFixedHeight(self.frame_code_map_size)
        """        
        self.current_line_no=self.cursor.blockNumber()+1
        for codes in code_lst:
            if self.current_line_no==codes[0]:
                self.componentsListMap(0,codes,self.callCodeListBtn)
            """
    def setScrollValueInEditor(self):...
        #self.textedit_code_editor.setScrollState()

        
    def saveCodeFile(self):
        if self.running_subwindow.windowTitle().startswith("untitled")==True:
            self.codefile_path,_=QtWidgets.QFileDialog.getSaveFileName()
            
            with open(self.codefile_path,'w')as file:
                file.write(self.running_textedit_editor.toPlainText())
                file.close()

                self.running_subwindow.setWindowTitle(self.Path_h.filePathToFileName(self.codefile_path))

                self.dummy_codefile_path=self.Path_h.createDummyFile(
                    self.codefile_path,
                    self.running_textedit_editor.toPlainText())
                
                for i,f_data in enumerate(self.codefile_path_list):
                    if f_data[0]==self.running_subwindow:
                        self.codefile_path_list[i][1]=self.codefile_path
                        self.codefile_path_list[i][2]=self.dummy_codefile_path
                        self.onDockWidgetActivate(self.running_textedit_editor)
        
        else:
            for i,f_data in enumerate(self.codefile_path_list,0):
                if f_data[0]==self.running_subwindow:
        
                    with open(f_data[1],'w')as file:
                        file.write(self.running_textedit_editor.toPlainText())
                        file.close()
          
    def subWinWidgets(self,widget,title="",icon_path=None):
        subwindow=MDISubWindow(self.mdi_area)
        dock_widget=self.dock_zone.addDockWidget(widget=widget)
        dock_widget.setTitle(title)        
        t_index=self.tabbar_editor.addTab(title)
        self.tabbar_editor.setTabData(t_index,dock_widget)
    
        #self.other_subwin_obj_buffer.append(subwindow)

        if icon_path==None:
            dock_widget.setDockIcon(QtGui.QIcon(self.Path_h.SETTINGS_ICON))
            
            self.tabbar_editor.setTabIcon(self.tabbar_editor.count()-1 ,QtGui.QIcon(self.Path_h.SETTINGS_ICON))
        else:
            dock_widget.setDockIcon(QtGui.QIcon(icon_path))
            self.tabbar_editor.setTabIcon(self.tabbar_editor.count()-1 ,QtGui.QIcon(icon_path))
        self.tab_list.append(dock_widget)
        
        #self.sub_window_addr.append([subwindow,None])

        """    
        self.subwindow_service_buffer[subwindow]=subWindowServiceConfigs(
            subwindow_obj=subwindow,
            tab_index=t_index,
            file_path=None,
            textedit_obj=None,
            subwindow_ssmngr_obj=None
            )
        """
        #self.mdi_area.addSubWindow(subwindow)

    def updateIconInSubwindowAndTabbar(self):
        for i,subwindow in enumerate(self.mdi_area.subwindow_list):
            title=self.mdi_area.windowTitle(subwindow)
            subwindow.setWindowIcon(self.Path_h.getExtensionIcon(title,False))

            title=self.tabbar_editor.tabText(i)
            self.tabbar_editor.setTabIcon(i,QtGui.QIcon(self.Path_h.getExtensionIcon(title,False)))
    
    def subWinImageViewer(self,img_path,dock_widget:DockWidget=None):
        img_name=self.Path_h.filePathToFileName(img_path)

        #subwindow=MDISubWindow(self.mdi_area)

        
        
        img_viewer=Custom.ImageViewer(img_path)
        dock_widget.addWidget(img_viewer)
        #img_viewer.setStyleSheet(f"background-color:{}")
        dock_widget.setTitle(img_name)
        #dock_widget.setDockIcon()
        

        t_index=self.tabbar_editor.addTab(img_name)
        self.tabbar_editor.setTabData(t_index,dock_widget)
        self.other_subwin_obj_buffer.append(dock_widget)
        #if icon_path==None:
        #else:
        dock_widget.setDockIcon(QtGui.QIcon(self.Path_h.IMAGE_EXT_ICON))
        dock_widget.title_bar.icon_button.setIconSize(QtCore.QSize(13,13))
        self.tabbar_editor.setTabIcon(self.tabbar_editor.count()-1 ,QtGui.QIcon(self.Path_h.IMAGE_EXT_ICON))
        
        self.tab_list.append(dock_widget)
        """
        self.subwindow_service_buffer[subwindow]=subWindowServiceConfigs(
            subwindow_obj=subwindow,
            tab_index=t_index,
            file_path=None,
            textedit_obj=None,
            subwindow_ssmngr_obj=None
            )"""
        if dock_widget:

            return dock_widget
    def subWinWebBrowser(self):
        subwindow=MDISubWindow(self.mdi_area)
        web_browser=WebBrowserWidget()
        dock_widget=self.dock_zone.addDockWidget(web_browser)
        
        #subwindow.setWidget(web_browser)
        #subwindow.setWindowTitle("web browser")
        #subwindow.resize(400,250)
        #dock_widget=self.dock_zone.addDockWidget(DockWidget())



        t_index=self.tabbar_editor.addTab("web browser")
        self.tabbar_editor.setTabData(t_index,dock_widget)

        self.other_subwin_obj_buffer.append(dock_widget)
        #if icon_path==None:
        #else:
        dock_widget.setDockIcon(QtGui.QIcon(self.Path_h.WEB_BROWSER_ICON))
        #subwindow.titlebar.icon_button.setIconSize(QtCore.QSize(30,30))
        self.tabbar_editor.setTabIcon(self.tabbar_editor.count()-1 ,QtGui.QIcon(self.Path_h.WEB_BROWSER_ICON))
        
        self.tab_list.append(dock_widget)
        
        """
        self.subwindow_service_buffer[subwindow]=subWindowServiceConfigs(
            # subwindow_obj=subwindow,
            tab_index=t_index,
            file_path=None,
            textedit_obj=None,
            subwindow_ssmngr_obj=None
            )"""

        #self.mdi_area.addSubWindow(subwindow)
    #def addDockWidgetEditor(self,title="untitled",is_source_file=False)
    def addSubWindowEditor(self,title="untitled",is_source_file=False,dock_widget:DockWidget=None):

        self.subwindow_session_handler=WorkSpace_Handler.Store.SubWindow()
        subwindow=self.createNewSubWindowCodeEditor(dock_widget=dock_widget)

        if not is_source_file:
            self.codefile_path=None

        Debug.red(subwindow)
        Debug.red(dock_widget)

        #self.themeNumberPad_2()
        if title=='untitled':

            t_index=self.tabbar_editor.addTab(f"{title}-{self.untitled_title_i}")
            self.tabbar_editor.setTabData(t_index,subwindow)
            
            self.tabbar_editor.setTabIcon(t_index ,QtGui.QIcon(self.Path_h.lang_icons_dict[".txt"]))
            subwindow.setTitle(f"{title}-{self.untitled_title_i}")
            subwindow.setDockIcon(QtGui.QIcon(self.Path_h.lang_icons_dict[".txt"]))



            self.untitled_title_i+=1


            self.subwindow_service_buffer[subwindow]=subWindowServiceConfigs(subwindow_obj=subwindow,
                                                                         tab_index=t_index,
                                                                         file_path=None,
                                                                         textedit_obj=self.textedit_code_editor,
                                                                         subwindow_ssmngr_obj=None
                                                                         )
            #print(self.subwindow_service_buffer)    

        else:



            subwindow.setTitle(title)
            #else:subwindow.setTitle(title)
            t_index=self.tabbar_editor.addTab(title)
            #bind tab with subwindow
            self.tabbar_editor.setTabData(t_index,subwindow)


            extension=self.dummy_codefile_path[self.dummy_codefile_path.rfind("."):]
            
            self.subwindow_service_buffer[subwindow]=subWindowServiceConfigs(subwindow_obj=subwindow,
                                                                         tab_index=t_index,
                                                                         file_path=self.codefile_path,
                                                                         textedit_obj=self.textedit_code_editor,
                                                                         subwindow_ssmngr_obj=self.subwindow_session_handler
                                                                         )
        
            if extension in self.Path_h.lang_icons_dict:
                dock_widget.setDockIcon(QtGui.QIcon(self.Path_h.lang_icons_dict[extension]))

                        
                self.tabbar_editor.setTabIcon(t_index,QtGui.QIcon(self.Path_h.lang_icons_dict[extension]))
            subwindow.text_editor=self.running_textedit_editor

        
        #self.feature=Features(MainWindow,self.textedit_code_editor_2,self.textedit_numpad_2,self.textedit_code_editor,self.textedit_numpad)
        
        #self.key_h_editor=KeyPressHandler(self.textedit_code_editor)
        self.running_textedit_editor=self.textedit_code_editor

        self.subwindow_index_id+=1
        
        self.subwindow_addr_buffer.append([subwindow,self.textedit_code_editor,self.subwindow_session_handler,None])
        
        self.tab_list.append(subwindow)

        #setattr(self,f"highlighter{len(self.sub_window_addr)}",PythonHighlighter(self.textedit_code_editor.document()))
        #setattr(self,f"indent{len(self.sub_window_addr)}",PythonHighlighter(self.textedit_code_editor.document()))
        
        #self.highlighter.append(PythonHighlighter(self.textedit_code_editor.document()))
        #self.linkCodeThemeOther()
        
        #self.textedit_code_editor.cursorPositionChanged.connect(lambda: self.mini_map.viewport().update())
        """self.textedit_code_editor.cursorPositionChanged.connect(lambda: 
                                                                self.mini_map.sync_editor_scroll(self.textedit_code_editor.verticalScrollBar().value()))
        """
        self.textedit_code_editor.cursorPositionChanged.connect(
        self.mini_map.sync_minimap_to_editor_scroll
        )

        #self.key_h_editor.connectKeysType(self.eventTextEdit)
        #self.key_h_editor.returnCurrentLineText(lambda a:...)        
        #self.key_h_editor.connectKey_ctrl_s(self.saveCodeFile)
        #self.key_h_editor.connectKey_enter(self.singleLineBlock)

        #self.textedit_code_editor.whenMouseEnter.connect(lambda:(subwindow.border_hover_debouncer.stop(),subwindow.border_hover_unset_debouncer.start()))


        self.textedit_code_editor.when_Key_Ctrl_s_pressed.connect(self.saveCodeFile)
        self.textedit_code_editor.when_Key_Enter_pressed.connect(self.enterStrockInTextEditor)

        
        self.style_editor.applyStyle(self.textedit_code_editor)
        

        
        self.whenSubWindowEditorAdded.emit()
        
        #self.mdi_area.addSubWindow(subwindow)
        self.onDockWidgetActivate(subwindow)

        
        #self.textedit_code_editor.textChanged.connect(self.autoSaveCodeFile)

        self.setNumpadWidth()
        
        self.textedit_code_editor.whenFocusIn.connect(self.onFocusInEditor)

        #subwindow.whenResize.connect(lambda:self.save_subwindow_session_debouncer.start())
        #subwindow.whenMove.connect(lambda:self.save_subwindow_session_debouncer.start())


        ####################################################

        self.textedit_code_editor.getCursorPosition.connect(lambda cur,l,c:self.mini_map.setCursorPosition(l,c))

        self.textedit_code_editor.getCharWhenType.connect(lambda x:self.mini_map.setChar(x))
        self.textedit_code_editor.when_Key_Ctrl_BackSpace_Pressed.connect(self.mini_map.trigger_ctrl_backspace)
        self.textedit_code_editor.when_Key_BackSpace_Pressed.connect(self.sendBackSpaceSiganlToMinimap)
        self.textedit_code_editor.selectionChanged.connect(self.mini_map.setSelection)  # Sync selection
        self.textedit_code_editor.when_Key_Ctrl_c_pressed.connect(self.mini_map.trigger_ctrl_c)
        self.textedit_code_editor.when_Key_Ctrl_v_pressed.connect(self.mini_map.trigger_ctrl_v)
        self.textedit_code_editor.when_Key_Ctrl_a_pressed.connect(self.mini_map.trigger_ctrl_a)
        self.textedit_code_editor.when_Key_Ctrl_z_pressed.connect(self.mini_map.trigger_ctrl_z)
        self.textedit_code_editor.when_Key_Ctrl_shift_z_pressed.connect(self.mini_map.trigger_ctrl_shift_z)
        self.textedit_code_editor.when_Key_delete_pressed.connect(self.mini_map.trigger_delete)
        self.textedit_code_editor.when_Key_Tab_pressed.connect(self.mini_map.trigger_Tab)
        self.textedit_code_editor.when_Key_Shift_Tab_pressed.connect(self.mini_map.trigger_Shift_Tab)

        self.textedit_code_editor.when_Key_Enter_pressed.connect(self.mini_map.trigger_enter)

        
    
        #self.textedit_code_editor.when_Key_PageUp_pressed.connect(self.mini_map.trigger_PageUp)
        #self.textedit_code_editor.when_Key_Shift_PageDown_pressed.connect(self.mini_map.trigger_Shift_PageUp)
        #self.textedit_code_editor.when_Key_PageDown_pressed.connect(self.mini_map.trigger_PageDown)
        #self.textedit_code_editor.when_Key_Shift_PageDown_pressed.connect(self.mini_map.trigger_Shift_PageDown)
        
        #self.textedit_code_editor.when_Key_Up_pressed.connect(self.mini_map.trigger_Up)
        #self.textedit_code_editor.when_Key_Down_pressed.connect(self.mini_map.trigger_Down)
        #self.textedit_code_editor.when_Key_Left_pressed.connect(self.mini_map.trigger_Left)
        #self.textedit_code_editor.when_Key_Right_pressed.connect(self.mini_map.trigger_Right)


        self.textedit_code_editor.when_Key_Ctrl_Up_pressed.connect(self.mini_map.trigger_Ctrl_Up)
        self.textedit_code_editor.when_Key_Ctrl_Down_pressed.connect(self.mini_map.trigger_Ctrl_Down)
        self.textedit_code_editor.when_Key_Ctrl_Left_pressed.connect(self.mini_map.trigger_Ctrl_Left)
        self.textedit_code_editor.when_Key_Ctrl_Right_pressed.connect(self.mini_map.trigger_Ctrl_Right)

        self.startMiniMapDeboucingTimer()

        return subwindow
        #self.themeNumberPad()
        #self.themeCodeEditor()
        #self.sizeCodeEditor()
        #self.sizeCodeEditor_2()

    def sendBackSpaceSiganlToMinimap(self):
        cur,line,col=self.running_textedit_editor.getCurrentLineOrColumnPos()
        self.mini_map.setCursorPosition(line,col)
        self.mini_map.trigger_backspace()

    def saveSubwindowSession(self):
        if self.dummy_codefile_path!=None:
            self.running_subwindow_session_mngr.storeBuf()

    def refrenceDisplaySubWindow(self,r_word):
        
        self.refrence_textedit=Custom.TextEditor(path_h=self.Path_h)
        self.style_editor.applyStyle(self.refrence_textedit)
        
        self.R_MNGR=RefrenceManager(self.refrence_textedit)
        self.R_MNGR.item_bgcolor=self.style_editor.bg_clr
        self.R_MNGR.refrence_container.setStyleSheet(f"background-color:{self.style_editor.bg_clr};")
        self.R_MNGR.whenItemSelect.connect(self.setRefrenceCodeInTextEditor)
        
        refrence_window=self.dock_zone.addDockWidget(self.R_MNGR.container)
        print(refrence_window)
        refrence_window.setTitle(f"reference-{r_word}")

    
        self.tabbar_editor.addTab(f"reference-{r_word}")
        self.other_subwin_obj_buffer.append(refrence_window)
        refrence_window.setDockIcon(QtGui.QIcon(self.Path_h.SYMBOL_REFERENCE_CHAIN_ICON))
        self.tabbar_editor.setTabIcon(self.tabbar_editor.count()-1 ,QtGui.QIcon(self.Path_h.SYMBOL_REFERENCE_CHAIN_ICON))


        self.R_MNGR.whenGoButtonClick.connect(lambda p,l:(
            self.openUrlSubwindow(p),
            self.textedit_code_editor.goToLine(l),
            self.textedit_code_editor.highlight_current_line()
            ))

        

        #self.mdi_area.addSubWindow(refrence_window)
        refrence_window.show()
        #style_textedit=self.customStyleTextEdit()
        self.rf_hightlighetr=PythonHighlighter(self.refrence_textedit.document())
        
        theme_name=self.Path_h.filePathToFileName(open(self.Path_h.Code.SELECTED_SYNTAX_THEME,"r").read())
        theme_data=self.Path_h.pathJoin(self.Path_h.SYNTAX_HIGHLIGHTER_DIR,
                                        self.Path_h.pathJoin("py",theme_name))
        theme_data=eval(open(theme_data,"r").read())
        #with open(self.Path_h.Code.SELECTED_SYNTAX_THEME,"r")as f:
        #theme=f.read()
        #theme=eval(theme.splitlines()[0])
        self.rf_hightlighetr.colors=theme_data
        self.rf_hightlighetr.setColors()
        self.rf_hightlighetr.rehighlight()

    def setRefrenceCodeInTextEditor(self,path,ln):
        if self.last_rpath!=path:
            with open(path,"r")as file:
                fcode=file.read()
                self.refrence_textedit.setPlainText(fcode)
        self.last_rpath=path
        self.refrence_textedit.goToLine(ln,True)
        self.refrence_textedit.highlight_current_line()

    def addRefrenceGroup(self,r_list):
    
        self.R_MNGR.addFileRefrenceGroup(r_list[0],r_list[1],r_list)

        #self.refrence_textedit.setFixedSize(QtCore.QSize(250,300))

    
    
    def onFocusInEditor(self,textedit:Custom.TextEditor):
        dock=textedit.dock_parent
        print("focuse in (text edite) : ",dock.title())
        self.onDockWidgetActivate(dock)
        if self.dock_zone.activated_dock_widget==dock:
            return
        else:...

    def setEditorStyleSheet(self,styledheet):
        print("style on going of texteditote")
        for services in self.subwindow_service_buffer.values():
            services.subwindow_obj.setStyleSheet(styledheet)


    def setSubWidowStyleSheet(self,styledheet):
        print("style on going of subwindo")
        
        for subwindow in self.subwindow_service_buffer.keys():
            subwindow.setStyleSheet(styledheet)

    
        