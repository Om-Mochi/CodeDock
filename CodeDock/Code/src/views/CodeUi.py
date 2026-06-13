from CodeDock.C_Widgets.Custom import Custom
from CodeDock.C_Widgets.CodeArea import MDIArea
from CodeDock.DockingSystem.core.DockZone import DockZone 
from PyQt6 import QtCore,QtGui,QtWidgets

class Code_Ui(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.Custom=Custom
        self.main_frame = Custom.Frame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_frame.sizePolicy().hasHeightForWidth())
        self.main_frame.setSizePolicy(sizePolicy)
        self.main_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.main_frame.setObjectName("frame_b")
        
        self.gridLayout_frame_b = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout_frame_b.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_frame_b.setObjectName("gridLayout_2")
        
        
        
        
        self.frame_toolbox =Custom.Frame(parent=self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_toolbox.sizePolicy().hasHeightForWidth())
        self.frame_toolbox.setSizePolicy(sizePolicy)
        self.frame_toolbox.setMinimumSize(QtCore.QSize(40, 0))
        self.frame_toolbox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.frame_toolbox.setBaseSize(QtCore.QSize(0, 0))

        self.frame_toolbox.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_toolbox.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_toolbox.setObjectName("frame_toolbox_of_editor")
        self.gridLayout_frame_b.addWidget(self.frame_toolbox, 0, 2, 2, 1)

        self.frame_mini_map_b=Custom.Frame(parent=self.main_frame)
        self.mini_map=Custom.TextEditMinimap()
        self.layout_mini_map=QtWidgets.QVBoxLayout()
        self.frame_mini_map_b.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mini_map_b.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_mini_map_b.setObjectName("frame_toolbox_of_editor")
        self.frame_mini_map_b.setFixedWidth(110)
        self.frame_mini_map_b.setLayout(self.layout_mini_map)
        self.layout_mini_map.addWidget(self.mini_map)
        #self.mini_map.setReadOnly(True)
        #self.mini_map.setStyleSheet("font-size:2px;")
        self.frame_mini_map_b.hide()
        self.layout_mini_map.setContentsMargins(0,0,0,0)


        #self.textedit_mini_map.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.mini_map.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mini_map.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Enable scrolling using the mouse wheel
        self.mini_map.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.tool_container_frame = QtWidgets.QFrame(parent=self.frame_toolbox)
        self.tool_container_frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.tool_container_frame.setGeometry(QtCore.QRect(0, 0, 40, 250))
        self.tool_container_frame.setObjectName("widget")
        self.gridLayout_toolbox_b = QtWidgets.QGridLayout(self.tool_container_frame)
        self.gridLayout_toolbox_b.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_toolbox_b.setSpacing(0)
        self.gridLayout_toolbox_b.setObjectName("gridLayout_6")
        
        #self.frame_toolbox.setFixedHeight(40)
        self.mdi_area=MDIArea()
        self.dock_zone=DockZone()
        
        self.layout_code_components_map=QtWidgets.QGridLayout()

        #self.gridLayout_frame_b.setColumnStretch(0, 10)
        
        #self.gridLayout_frame_b.setColumnStretch(1, 1)
        
        
        self.frame_tabbar=Custom.Frame(parent=self.main_frame)
        self.layout_tabbar=QtWidgets.QHBoxLayout()
        self.frame_tabbar.setLayout(self.layout_tabbar)
        

        self.hscroll_tabbar=QtWidgets.QScrollArea()
        self.hscroll_tabbar.setWidgetResizable(True)
        
        
        self.gridLayout_frame_b.addWidget(self.dock_zone, 0, 0, 1, 1)
        self.gridLayout_frame_b.addWidget(self.frame_tabbar,1,0,1,2)
        self.gridLayout_frame_b.addWidget(self.frame_mini_map_b, 0, 1, 1, 1)
        
        self.tabbar_widget=QtWidgets.QWidget()
        #self.layout_tabbar=QtWidgets.QHBoxLayout()
        
        #self.layout_tabbar.addWidget(self.)
        #self.tabbar_widget.setLayout(self.layout_tabbar)
        #self.hscroll_tabbar.setWidget(self.tabbar_widget)

        
        #self.layout_tabbar.setContentsMargins(0,0,0,0)
        self.layout_tabbar.setContentsMargins(0,0,0,0)
        #self.hscroll_tabbar.setFixedHeight(40)
        self.frame_tabbar.setFixedHeight(45)
        #self.main_layout_tabbar.setSpacing(5)
        #self.frame_tabbar.setFixedHeight(50)
        self.tabbar_editor=Custom.TabBar()
            
        
        self.gridLayout_frame_b.setSpacing(0)
        self.long_view_code_btn = Custom.PushButton()
        
        self.zoom_in_btn = Custom.PushButton()
        self.zoom_in_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.zoom_in_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.zoom_in_btn.setText("")
        self.zoom_in_btn.setObjectName("zoom_in_btn")

        self.zoom_out_btn = Custom.PushButton()
        self.zoom_out_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.zoom_out_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.zoom_out_btn.setText("")
        self.zoom_out_btn.setObjectName("zoom_out_btn")
        
        self.up_arrow_btn = Custom.PushButton()
        self.up_arrow_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.up_arrow_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.up_arrow_btn.setText("")
        self.up_arrow_btn.setObjectName("up_arrow_btn")
        
        self.down_arrow_btn = Custom.PushButton()
        self.down_arrow_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.down_arrow_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.down_arrow_btn.setText("")
        self.down_arrow_btn.setObjectName("down_arrow_btn")
       
        self.add_subwindow_btn = Custom.PushButton()
        self.add_subwindow_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.add_subwindow_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.add_subwindow_btn.setText("")
        self.add_subwindow_btn.setObjectName("add_subwindow_btn")

        self.web_browser_btn = Custom.PushButton()
        self.web_browser_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.web_browser_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.web_browser_btn.setText("")
        self.web_browser_btn.setObjectName("close_subwindow_btn")
       
        
        self.auto_subwindow_arrange_btn = Custom.PushButton()
        self.auto_subwindow_arrange_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.auto_subwindow_arrange_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.auto_subwindow_arrange_btn.setText("")
        self.auto_subwindow_arrange_btn.setObjectName("auto_subwindow_arrange_btn")
                  
        """
        self.gridLayout_toolbox_b.addWidget(self.zoom_in_btn,2, 0)
        self.gridLayout_toolbox_b.addWidget(self.zoom_out_btn,3, 0)
        self.gridLayout_toolbox_b.addWidget(self.up_arrow_btn,4, 0)
        self.gridLayout_toolbox_b.addWidget(self.down_arrow_btn,5, 0)
        self.gridLayout_toolbox_b.addWidget(self.add_subwindow_btn,6, 0)
        self.gridLayout_toolbox_b.addWidget(self.web_browser_btn,7, 0)
        self.gridLayout_toolbox_b.addWidget(self.auto_subwindow_arrange_btn,8, 0)

        """
    def activeEditor(self,path_h,transparent=False):
        self.widget_code_editor=QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_code_editor.sizePolicy().hasHeightForWidth())
        self.widget_code_editor.setSizePolicy(sizePolicy)
        #self.frame_code_editor.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        #self.frame_code_editor.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        #self.frame_code_editor.setObjectName("frame_code_editor")
        self.gridLayout_frame_editor = QtWidgets.QGridLayout(self.widget_code_editor)
        self.gridLayout_frame_editor.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_frame_editor.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_frame_editor.setSpacing(0)
        self.gridLayout_frame_editor.setObjectName("gridLayout_5")
        
        
        #self.gridLayout_frame_editor.addWidget(self.textedit_numpad, 0, 1, 1, 1)
        

        #self.textedit_numpad_2 = QtWidgets.QTextEdit(parent=self.frame_code_editor)
        #self.textedit_numpad_2.setObjectName("textedit_long_view_numbers")
        #self.gridLayout_frame_editor.addWidget(self.textedit_numpad_2, 0, 3, 1, 1)
        
        self.textedit_code_editor =Custom.TextEditor(path_h=path_h,transparent=transparent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_code_editor.sizePolicy().hasHeightForWidth())
        self.textedit_code_editor.setSizePolicy(sizePolicy)
        self.textedit_code_editor.setSizeIncrement(QtCore.QSize(0, 0))
        self.textedit_code_editor.setBaseSize(QtCore.QSize(0, 0))
        self.textedit_code_editor.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.textedit_code_editor.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.textedit_code_editor.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        #self.textedit_for_code_editor.setLineWidth(1)
        #self.textedit_for_code_editor.setMidLineWidth(0)
        self.textedit_code_editor.setObjectName("TextEdit")
        self.gridLayout_frame_editor.addWidget(self.textedit_code_editor, 0, 2, 1, 1)
        #self.gridLayout_5.setColumnStretch(0, 1)
        #self.gridLayout_5.setColumnStretch(2, 10)
        #self.widget_code_editor.setLayout(self.frame_code_editor)

        """self.textedit_code_editor_2 = QtWidgets.QTextEdit(parent=self.frame_code_editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_code_editor_2.sizePolicy().hasHeightForWidth())
        self.textedit_code_editor_2.setSizePolicy(sizePolicy)
        self.textedit_code_editor_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.textedit_code_editor_2.setBaseSize(QtCore.QSize(0, 0))
        self.textedit_code_editor_2.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.textedit_code_editor_2.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.textedit_code_editor_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        #self.textedit_long_view_editor.setLineWidth(1)
        #self.textedit_long_view_editor.setMidLineWidth(0)
        self.textedit_code_editor_2.setObjectName("textedit_long_view_editor")
        self.gridLayout_frame_editor.addWidget(self.textedit_code_editor_2, 0, 4, 1, 1)
        self.textedit_code_editor_2.hide()
        self.textedit_numpad_2.hide()
        #self.gridLayout_5.setColumnStretch(0, 1)"""