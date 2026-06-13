from CodeDock.C_Widgets.Custom import Custom
from PyQt6 import QtCore,QtGui,QtWidgets

class Dock_Ui():
    def __init__(self):
        
        self.main_frame = Custom.Frame()
        self.main_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.main_frame.setSizeIncrement(QtCore.QSize(0, 0))
        self.main_frame.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.main_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.main_frame.setMidLineWidth(0)
        self.main_frame.setObjectName("frame_a")
        self.gridLayout_frame_a = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout_frame_a.setContentsMargins(0, 0, 0, 0)
        
        self.gridLayout_frame_a.setObjectName("gridLayout")
        
        
        self.frame_toolbox = Custom.SmartToolBar()
        
        self.frame_toolbox_v_layout=QtWidgets.QVBoxLayout()
        self.frame_toolbox.setLayout(self.frame_toolbox_v_layout)

        #self.panel_list_btn.bg_clr=""
        #self.panel_list_btn.applyStyle()
        
        self.frame_panel=Custom.Frame(parent=self.main_frame)
        
        self.layout_main_tree=QtWidgets.QGridLayout()
        self.layout_main_tree.setContentsMargins(0, 0, 0, 0)
        self.layout_main_tree.setSpacing(0)
        
        
        
        self.frame_panel.setLayout(self.layout_main_tree)

        self.gridLayout_frame_a.addWidget(self.frame_panel,1,1,1,1)
        self.gridLayout_frame_a.setSpacing(0)


        self.gridLayout_frame_a.addWidget(self.frame_toolbox, 0, 0, 1, 2)


        self.frame_panel = Custom.Frame(parent=self.main_frame)

        self.layout_main_tree = QtWidgets.QGridLayout()
        self.layout_main_tree.setContentsMargins(0, 0, 0, 0)
        self.layout_main_tree.setSpacing(0)

        self.frame_panel.setLayout(self.layout_main_tree)

        self.gridLayout_frame_a.addWidget(self.frame_panel, 1, 0, 1, 2)
        self.gridLayout_frame_a.setSpacing(0)

        self.file_open_btn = Custom.PushButton()
        self.file_open_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.file_open_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.file_open_btn.setText("")
        self.file_open_btn.setObjectName("file_open_btn")
        #self.gridLayout_6.addWidget(self.file_open_btn, 1, 2, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.file_save_btn = Custom.PushButton()
        self.file_save_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.file_save_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.file_save_btn.setText("")
        self.file_save_btn.setObjectName("file_save_btn")
        #self.gridLayout_6.addWidget(self.file_save_btn, 1, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.color_dialog_open = Custom.PushButton()
        self.color_dialog_open.setMinimumSize(QtCore.QSize(33, 33))
        self.color_dialog_open.setMaximumSize(QtCore.QSize(33, 33))
        self.color_dialog_open.setText("")
        self.color_dialog_open.setObjectName("color_dialog_open")
        #self.gridLayout_6.addWidget(self.color_dialog_open, 4, 1, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.settings_btn = Custom.PushButton()
        self.settings_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.settings_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.settings_btn.setText("")
        self.settings_btn.setObjectName("settings_btn")
        #self.gridLayout_6.addWidget(self.settings_btn, 4, 3, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        
        #self.gridLayout_6.addWidget(self.pushButton_3, 1, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.pushButton_t = Custom.PushButton()
        self.pushButton_t.setMinimumSize(QtCore.QSize(33, 33))
        self.pushButton_t.setMaximumSize(QtCore.QSize(33, 33))
        self.pushButton_t.setText("")
        self.pushButton_t.setObjectName("pushButton")
        #self.gridLayout_6.addWidget(self.pushButton, 4, 2, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.color_widget_btn = Custom.PushButton()
        self.color_widget_btn.setMinimumSize(QtCore.QSize(33, 33))
        self.color_widget_btn.setMaximumSize(QtCore.QSize(33, 33))
        self.color_widget_btn.setText("")
        self.color_widget_btn.setObjectName("color_widget_btn")
        self.frame_toolbox.setFixedWidth(40)  

        self.frame_toolbox.addToolButton(self.file_open_btn)
        #self.frame_toolbox.addToolButton(self.file_save_btn)
        self.frame_toolbox.addToolButton(self.color_dialog_open)
        #self.frame_toolbox.addToolButton(self.color_widget_btn)
        self.frame_toolbox.addToolButton(self.settings_btn)
        self.frame_toolbox.addToolButton(self.pushButton_t)
        
        #self.frame_components_map = Custom.Frame(parent=self    
        #self.frame_components_map.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        #self.frame_components_map.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        #self.frame_components_map.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        #self.frame_components_map.setObjectName("frame_code_map")
        #self.gridLayout_frame_a.addWidget(self.frame_code_map, 1, 1, 1, 1)
        
        #self.scroll_map=QtWidgets.QScrollArea(parent=self.main_frame_map)
        #self.scroll_map.setWidgetResizable(True)
        
        #self.scroll_map.setWidget(self.frame_components_map)
        #self.layout_main_frame_map.addWidget(self.scroll_map,0,0)
    