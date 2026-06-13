from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.C_Widgets.Custom import Custom
from CodeDock.Code.src.controllers.CodePadHighlighter import HTMLDelegate
from CodeDock.src.controllers.PathHandler import Path_Handler

class Dock_Panel(Custom.NestedMainWindow):
    whenProjectRootSetedInFileModel=QtCore.pyqtSignal(str)
    def __init__(self,path_h:Path_Handler):
        super().__init__()

        self.Path_h=path_h
        self.map_c_font_size=40
        self.map_tags_expand_state=[]


        self.map_model=Custom.StandardItemModel()
        self.map_tree=Custom.TreeView(self.map_model)
        self.map_tree_container=QtWidgets.QWidget()
        self.map_tree_layout=QtWidgets.QVBoxLayout()
        self.map_dock=QtWidgets.QDockWidget("Symbol")

        self.map_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable
        )

        self.map_dock.setWidget(self.map_tree_container)
        self.map_tree_container.setLayout(self.map_tree_layout)
        self.map_tree_container.setContentsMargins(0,0,0,0)
        self.map_tree_layout.setContentsMargins(0,0,0,0)
        self.map_dock.setContentsMargins(0,0,0,0)        
        

        self.file_model=Custom.FileSystemModel()
        self.file_tree=Custom.TreeView(self.file_model)
        self.file_tree_container=QtWidgets.QWidget()
        self.file_tree_layout=QtWidgets.QVBoxLayout()
        self.file_dock=QtWidgets.QDockWidget("File")
        self.file_dock.setContentsMargins(0,0,0,0)

        self.file_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable
        )

        self.file_dock.setWidget(self.file_tree_container)        
        self.file_tree_container.setLayout(self.file_tree_layout)
        self.file_tree_layout.setContentsMargins(0,0,0,0)
        

        #self.file_model.setIconProvider(self.file_model.iconProvider())
        
        #self.main_model=QtGui.QStandardItemModel() 
        self.layout_tree_w=QtWidgets.QGridLayout()
        self.layout_tree_w.setContentsMargins(0,0,0,0)
        
        self.tabbar_panel=Custom.TabBar()

        self.frame_tabbar=Custom.Frame()
        self.layout_tabbar=QtWidgets.QHBoxLayout(self.frame_tabbar)
        self.layout_tabbar.setContentsMargins(0,0,0,0)
        
        self.layout_tabbar.addWidget(self.tabbar_panel)
        self.test_tool=Custom.ToolBar()
        #self.layout_tabbar.addWidget(self.test_tool)

        self.test_tool.bg_clr="#293C4E"
        self.test_tool.applyStyle()
 
        """tl1,lay1=self.test_tool.addToolButton(icon=("/home/omx/tree_v_folderw1.png",30,30))
        tl2,lay2=self.test_tool.addToolButton(icon=("/home/omx/symbol_treew.png",30,30))
        tl1.setFixedSize(40,40)
        tl2.setFixedSize(34,34)
        
        #tl1.setCheckable()
        #tl2.setCheckable(False)
        
        tl1.brdr_think=1
        tl1.brdr_clr="#7AADA9"
        tl1.applyStyle()
        
        tl2.brdr_think=1

        tl2.brdr_clr="#58948A"
        tl2.applyStyle()
    

        self.test_tool.layout_right_h.addStretch(100)

        tl1.clicked.connect(lambda:self.changeTab(index=0))
        tl2.clicked.connect(lambda:self.changeTab(index=1))
        """


        self.toolbar_map_tree=Custom.ToolBar()
        self.toolbar_map_tree.layout_right_h.addStretch(40)
        self.toolbar_map_tree.setFixedHeight(25)
        self.toolbar_map_tree.h=25
        self.toolbar_map_tree.bg_clr="#3B3B3B"
        self.toolbar_map_tree.brdr_think=0
        self.toolbar_map_tree.brdr_clr="#2B5780"
        self.toolbar_map_tree.applyStyle()

        self.toolbar_map_tree.layout_left_h.addWidget(QtWidgets.QLabel("Symbol"),alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.toolbar_map_tree.layout_right_h.addStretch()
        self.close_panel_mt_btn,l=self.toolbar_map_tree.addToolButton(icon=(path_h.CLOSE_PANEL_ICON,16,16))
        self.refresh_mt_btn,l=self.toolbar_map_tree.addToolButton(icon=(path_h.SYMBOL_REFERENCE_CHAIN_ICON,16,16))
        self.filter_mt_btn,l=self.toolbar_map_tree.addToolButton(icon=(path_h.FILTER_ICON,16,16))
        self.setting_mt_button,setting_container=self.toolbar_map_tree.addToolButton(icon=(path_h.SETTINGS_ICON,16,16))

        
        self.close_panel_mt_btn.clicked.connect(self.whenClosePanelClicked)
        self.close_panel_mt_btn.setFixedSize(18,18)
        self.refresh_mt_btn.setFixedSize(18,18)
        #btn3.setFixedSize(18,18)
        self.filter_mt_btn.setFixedSize(18,18)
        
        self.toolbar_map_tree.addOnOffFlagButton("KeyWOrd",setting_container,0)
        self.toolbar_map_tree.addOnOffFlagButton("Method",setting_container,1)
        self.toolbar_map_tree.addOnOffFlagButton("Class",setting_container,2)
        self.toolbar_map_tree.addOnOffFlagButton("Paremeter",setting_container,3)
        self.toolbar_map_tree.addOnOffFlagButton("Test",setting_container,4)

        self.map_dock.setTitleBarWidget(self.toolbar_map_tree)
        #self.map_tree_layout.addWidget(self.toolbar_map_tree)
        self.map_tree_layout.addWidget(self.map_tree)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self.map_dock)
        


        
        self.toolbar_file_tree=Custom.ToolBar()
        self.toolbar_file_tree.layout_right_h.addStretch(40)
        self.toolbar_file_tree.setFixedHeight(25)        
        self.toolbar_file_tree.h=25
        self.toolbar_file_tree.bg_clr="#3B3B3B"
        self.toolbar_file_tree.brdr_think=0
        self.toolbar_file_tree.brdr_clr="#2B5780"
        self.toolbar_file_tree.applyStyle()

        #file tree view panel
        self.toolbar_file_tree.layout_left_h.addWidget(QtWidgets.QLabel("CodeDock"),alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.toolbar_file_tree.layout_right_h.addStretch()
        self.close_panel_ft_btn,l=self.toolbar_file_tree.addToolButton(icon=(path_h.CLOSE_PANEL_ICON,16,16))
        self.add_file_ft_btn,add_file_container=self.toolbar_file_tree.addToolButton(icon=(path_h.ADD_FILE_ICON,16,16))
        self.add_folder_ft_btn,add_folder_container=self.toolbar_file_tree.addToolButton(icon=(path_h.ADD_FOLDER_ICON,16,16))
        #refresh btn left
        self.filter_ft_btn,filter_container=self.toolbar_file_tree.addToolButton(icon=(path_h.FILTER_ICON,16,16))

        #self.file_tree_layout.addWidget(self.toolbar_file_tree)
        
        self.file_dock.setTitleBarWidget(self.toolbar_file_tree)
        self.file_tree_layout.addWidget(self.file_tree)

        self.layout_tree_w.addWidget(self.frame_tabbar,0,0)
        #self.layout_tree_w.addWidget(self.map_dock,1,0)
        #self.layout_tree_w.addWidget(self.file_dock,2,0)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self.file_dock)
        
        #self.main_tree.setModel(self.main_model)
        self.layout_tree_w.setContentsMargins(0,0,0,0)
        self.layout_tree_w.setSpacing(0)
        self.file_tree_layout.setSpacing(0)
        self.map_tree_layout.setSpacing(0)
        #self.tabbar_panel.addTab("File")
        #self.tabbar_panel.addTab( "Map")

        
        self.tabbar_panel.currentChanged.connect(self.changeTab)
        #self.tabs.setCornerWidget(add_tab_button, QtCore.Qt.Corner.TopRightCorner)
        #self.map_tree_container.hide()
        #self.map_model.setHeaderData("Map")
        #self.file_model.setHorizontalHeaderLabels(QtWidgets.QLabel("File"))
        #self.map_parent=QtGui.QStandardItem("Map")
        #self.file_parent=QtGui.QStandardItem("File")

        #self.main_model.appendRow(self.file_parent)
        #self.main_model.appendRow(self.map_parent)
        self.file_tree.setModel(self.file_model)
        
        self.map_tree.setModel(self.map_model)
        self.map_tree.expanded.connect(self.mapTagExpand)
        self.map_tree.collapsed.connect(self.mapTagCollaps)
        self.map_tree.expandAll()

        
        self.file_tree.connect_url_droper=self.setPathUrlInFileModel
        #self.file_tree.connect_drop_url=self.setPathUrlInFileModel
        #self.map_parent.appendRow(self.map_model)


        self.file_tree.hideColumn(1)
        self.file_tree.hideColumn(2)
        self.file_tree.hideColumn(3)
        
        self.file_tree.setDragEnabled(True)
        self.file_tree.setDropIndicatorShown(True)
        self.file_tree.setAcceptDrops(True)
        
        
        
        #self.file_model.setRootPath("")
        
        #self.main_file_tree.showDropIndicator(True)
        self.file_model.supportedDragActions()
        #self.map_tree.setItemDelegate(HTMLDelegate(self.map_tree,self.map_c_font_size))
        #self.map_tree.setItemDelegate(SpacingDelegate())
        #self.map_tree.setHeaderHidden(True)
        #self.map_tree.clicked.connect(self.onComponentsClicked)
        self.on_double_click_file_tree=None
        self.file_tree.doubleClicked.connect(self.onDoubleClickFileItem)
        self.setLayout(self.layout_tree_w)
        

    def whenClosePanelClicked(self,widget=None):
        pass
        
    
    def setPathUrlInFileModel(self,path=None):
        if path==None:
            path=self.Path_h.HOME_USER_PATH
        
        self.file_model.setRootPath(path)  # Set the root path in the model
        #self.main_tree.setRootIndex(self.file_model.index(directory_path)) 
        #initial_dir = self.file_model.rootPath("/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBooka")
        self.file_tree.setRootIndex(self.file_model.index(path))
        #print(self.file_model.rowCount(self.file_model.index(path)))
        # Print full path of each item
        
        self.whenProjectRootSetedInFileModel.emit(path)



    def mapTagExpand(self,index):
        self.map_tags_expand_state.append(index.data())

    def mapTagCollaps(self,index):
        self.map_tags_expand_state.remove(index.data())
    
    def setIconsInFileMode(self):
        self.file_model.f_icons=self.Path_h.lang_icons_dict
        
    def onDoubleClickFileItem(self,index):
        if self.file_model.isDir(index):pass
        else:
            path=self.file_model.filePath(index)
            self.on_double_click_file_tree(False,path)
    
    def changeTab(self,index):
        if index==0:
            self.map_tree_container.hide()
            self.file_tree_container.show()
        elif index==1:
            self.file_tree_container.hide()
            self.map_tree_container.show()
        else:pass
        