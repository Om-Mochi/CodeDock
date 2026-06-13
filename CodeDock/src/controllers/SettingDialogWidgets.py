

from CodeDock.src.views.SettingDialog import Setting_Dilaog

from CodeDock.Code.src.controllers.CodePadHighlighter import PythonHighlighter

from PyQt6 import QtWidgets,QtCore
from CodeDock.C_Widgets.Custom import Custom
import os 




class PopUp(QtWidgets.QWidget):
    def __init__(self, message="Saved!", duration=1000):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Popup)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(message, self)
        self.label.setStyleSheet("font-size: 18px; color: white; background-color: rgba(184, 188, 255, 0.5); padding: 10px; border-radius: 5px;")
        self.label.adjustSize()

        self.resize(self.label.sizeHint())

        QtCore.QTimer.singleShot(duration, self.close)  # Close after `duration` milliseconds

class Setting_Dialog_Widgets(Setting_Dilaog):
    def __init__(self):
        super().__init__()
        #self.frameOne()
        self.nested_widget_buffer=[]
        self.hightlgtr_holder=[]

        self.layoutV1=None
        self.layoutV2=None
        
    def removeLayouts(self,main_layout):

        for i in reversed(range(main_layout.count())):
            item = main_layout.itemAt(i)

            self.removeWidgets(item.layout())  
            main_layout.removeItem(item)  
            if item.widget() is not None:  
                continue
    
    def removeWidgets(self,layout):
        while layout.count():
            item=layout.takeAt(0)
            widget=item.widget()
            if widget is not None:
                widget.deleteLater()
            else:pass
           

    def multiVButtons(self,btn_list,layout):
        def createButton(i,text,link,layout):
            btns=QtWidgets.QPushButton(text)

            layout.addWidget(btns,i,0)
            btns.clicked.connect(link)
            
            btns.clicked.connect(lambda:self.changeStyleSheetWidget(i))
            self.nested_widget_buffer.append(Custom.NestedMainWindow())
            btns.setStyleSheet("border:1px solid white;color:#AEAFB1;")

        for index,component in enumerate(btn_list):
            createButton(index,component[0],component[1],layout)

    def createColorOption(self,option,link,set_color=None):
        
        color_button=QtWidgets.QPushButton()
        
        option_label=QtWidgets.QLabel(option)
        option_label.setStyleSheet("background-color:#3f3f3f;")

        self.layoutV1.addWidget(option_label)
        self.layoutV2.addWidget(color_button)
        color_button.setFixedHeight(40)
        color_button.setFixedWidth(90)

        """
        color_button.setFixedHeight(40)
        color_button.setFixedWidth(90)
        option_label.setFixedHeight(40)
        option_label.setFixedWidth(90)"""

        if set_color!=None:
            self.setColorOnButton(set_color,btns=color_button)

        color_button.clicked.connect(lambda:self.openColorDilaog(color_button,link))
        
    def openColorDilaog(self,btns,link):
        self.color_d=QtWidgets.QColorDialog()
        self.color_d.show()
        #self.color_d.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.color_d.currentColorChanged.connect(lambda:self.setColorOnButton(self.color_d.currentColor().name(),btns=btns))
        self.color_d.currentColorChanged.connect(link)



    def setColorOnButton(self,color,btns):
        
        btns.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}; /* Light Blue */
                color: white;            /* White text */
                border: 0px solid #2980b9; /* Darker blue border */
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #2980b9; /* Darker blue on hover */
            }}
            QPushButton:pressed {{
                background-color: #1c6a9e; /* Even darker blue when pressed */
            }}
        """)

    def createSaveButton(self,option,link,button_data=None):
        def toggle_state():
        
            self.popup=PopUp("Saved Successfully",1000)

            self.popup.setGeometry(self.x()+400,self.y()+300,self.popup.width(),self.popup.height())
            if button_data:
                link(button_data)
            else:
                link()
            self.popup.show()


            
        save_btn=QtWidgets.QPushButton()
        option_label=QtWidgets.QLabel(option)
        option_label.setStyleSheet("background-color:#3f3f3f;")
        save_btn.setText("Save")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #747877; /* Light Blue */
                color: #000000;            /* White text */
                border: 0px solid none; /* Darker blue border */
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #99beaa; /* Darker blue on hover */
            }}
            QPushButton:pressed {{
                background-color: #747877; /* Even darker blue when pressed */
            }}
        """)
        #save_btn.setStyleSheet("background-color: #4f708f;border:0px solid none; font-size: 18px; padding: 10px; color: red;")
        self.layoutV1.addWidget(option_label)
        self.layoutV2.addWidget(save_btn)
        
        
        save_btn.clicked.connect(toggle_state)

        save_btn.setFixedHeight(40)
        save_btn.setFixedWidth(100)
        

        
        return save_btn

    def createToggleButton(self,option,link):
        def toggle_state():
            if toggle_btn.isChecked():
                toggle_btn.setText("Show")
                toggle_btn.setStyleSheet("background-color: green;border:0px solid none; font-size: 18px; padding: 10px; color: white;")
                link(True)
            else:
                toggle_btn.setText("Hide")
                toggle_btn.setStyleSheet("background-color: red;border:0px solid none; font-size: 18px; padding: 10px; color: white;")
                link(False)
        toggle_btn=QtWidgets.QPushButton()
        option_label=QtWidgets.QLabel(option)
        option_label.setStyleSheet("background-color:#3f3f3f;")
        toggle_btn.setText("Show")
        toggle_btn.setStyleSheet("background-color: red;border:0px solid none; font-size: 18px; padding: 10px; color: white;")
        self.layoutV1.addWidget(option_label)
        self.layoutV2.addWidget(toggle_btn)
        toggle_btn.setCheckable(True)
        
        toggle_btn.clicked.connect(toggle_state)
        toggle_btn.setFixedHeight(40)
        toggle_btn.setFixedWidth(90)
        
        
        return toggle_btn




    def createDoubleSpinBox(self,option,link,set_value=0,step=1.00):

        option_label=QtWidgets.QLabel(option)
        option_label.setStyleSheet("background-color:#3f3f3f;")
        spinbox=QtWidgets.QDoubleSpinBox()

        self.layoutV1.addWidget(option_label)
        self.layoutV2.addWidget(spinbox)
        spinbox.setFixedHeight(40)
        spinbox.setFixedWidth(90)
        spinbox.setValue(set_value)
        spinbox.setSingleStep(step)
        spinbox.setRange(0,255)

        spinbox.valueChanged.connect(link)
        spinbox.setStyleSheet("background-color:#555555;")

        return spinbox

    def createSpinBox(self,option,link,set_value=0,set_max_range=100):
        option_label=QtWidgets.QLabel(option)
        option_label.setStyleSheet("background-color:#3f3f3f;")
        spinbox=QtWidgets.QSpinBox()

        self.layoutV1.addWidget(option_label)
        self.layoutV2.addWidget(spinbox)
        spinbox.setFixedHeight(40)
        spinbox.setFixedWidth(90)
        spinbox.setRange(0,set_max_range)
        if set_value:
            spinbox.setValue(set_value)
        else:spinbox.setValue(0)
        spinbox.setStyleSheet("background-color:#555555;")
        spinbox.valueChanged.connect(link)
        return spinbox

    def openFontDialog(self,font,link):
        self.f_dialog=QtWidgets.QFontDialog()

        #font, ok = QtWidgets.QFontDialog.currentFontChanged(edtr.font(), QtWidgets.QWidget(), "Select Font")
        self.f_dialog.setCurrentFont(font)
        self.f_dialog.fontSelected.connect(link)
        self.f_dialog.currentFontChanged.connect(link)
        self.f_dialog.show()

    def createFileTreeModel(self,option,link,root_path,path_h):

        
        self.file_model=Custom.FileSystemModel()
        self.file_tree=Custom.TreeView(self.file_model)
        self.file_tree_container=QtWidgets.QWidget()
        self.file_tree_layout=QtWidgets.QVBoxLayout()
        
        
        #self.layout_custom_windget.addWidget(self.file_tree_container,1,0)
        
        self.file_tree_container.setLayout(self.file_tree_layout)
        self.file_tree_layout.setContentsMargins(0,0,0,0)

        
        self.toolbar_file_tree=Custom.ToolBar()
        self.toolbar_file_tree.layout_right_h.addStretch(40)
        self.toolbar_file_tree.setFixedHeight(25)        
        self.toolbar_file_tree.h=25
        self.toolbar_file_tree.bg_clr="#3B3B3B"
        self.toolbar_file_tree.brdr_think=0
        self.toolbar_file_tree.brdr_clr="#2B5780"
        self.toolbar_file_tree.applyStyle()

        #file tree view panel
        self.toolbar_file_tree.layout_left_h.addWidget(QtWidgets.QLabel(option),alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.toolbar_file_tree.layout_right_h.addStretch()
        self.close_panel_ft_btn,l=self.toolbar_file_tree.addToolButton(icon=(path_h.CLOSE_PANEL_ICON,16,16))
        self.add_file_ft_btn,add_file_container=self.toolbar_file_tree.addToolButton(icon=(path_h.ADD_FILE_ICON,16,16))
        self.add_folder_ft_btn,add_folder_container=self.toolbar_file_tree.addToolButton(icon=(path_h.ADD_FOLDER_ICON,16,16))
        #refresh btn left
        self.filter_ft_btn,filter_container=self.toolbar_file_tree.addToolButton(icon=(path_h.FILTER_ICON,16,16))

        #self.file_tree_layout.addWidget(self.toolbar_file_tree)
        
        self.file_tree_layout.addWidget(self.file_tree)
        
        self.file_tree.setModel(self.file_model)

        self.file_model.setRootPath(root_path)  # Set the root path in the model
        self.file_tree.setRootIndex(self.file_model.index(root_path))
        

        self.file_tree.hideColumn(1)
        self.file_tree.hideColumn(2)
        self.file_tree.hideColumn(3)
        #self.file_tree.doubleClicked.connect(lambda i:self._onDoubleClickFileItem(i,link))
        self.file_tree.clicked.connect(lambda i:self._clickedFileItem(i,link))
        
        return self.file_tree_container
    
    def _onDoubleClickFileItem(self,index,callable):
        if self.file_model.isDir(index):pass
        else:
            path=self.file_model.filePath(index)
            callable(path)
    def _clickedFileItem(self,index,callable):
        if self.file_model.isDir(index):pass
        else:
            path=self.file_model.filePath(index)
            callable(path)
        


    def createTxtFileSelectore(self,option,link,folder_path):
        self.folder_path=folder_path
        self.list_widget = QtWidgets.QListWidget()
        self.layout_custom_windget.addWidget(self.list_widget)

        self.callable=link
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #dcdcdc;
                border: 1px solid #444;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 6px;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
                border-radius: 4px;
            }
        """)

        self._loadTxtFIles(folder_path)

        # Connect signals
        self.list_widget.itemDoubleClicked.connect(self._fileSelected)  # double click
        self.list_widget.itemActivated.connect(self._fileSelected)      # Enter key

    def _loadTxtFIles(self, folder_path):
        if os.path.isdir(folder_path):
            txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
            self.list_widget.addItems(txt_files)

    def _fileSelected(self, item):
        self.callable(os.path.join(self.folder_path,item))

    def createGroupBoxForCustomWidgets(self,title,pos):
        group_bx=QtWidgets.QGroupBox(title)
        layout_group_bx=QtWidgets.QGridLayout()
        self.layout_custom_windget=QtWidgets.QGridLayout()
        layout_group_bx.addLayout(self.layout_custom_windget,0,0)
        group_bx.setLayout(layout_group_bx)

        #layout.addWidget(group_bx,pos,0)
        group_bx.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                
                color: #ffffff;
                border: none;
                border-radius:0px;
                margin-top: 25px; /* space for the title */
                background-color:#3f3f3f;
            }
            QGroupBox::title {
                font-weight: bold;
                subcontrol-origin: margin; /* position relative to border */
                subcontrol-position: top left; /* align title to the top-left */
                padding: 0 10px; /* add some padding around the title */
                background-color: #a8a8a8;
                color: #000000;
                border-radius:0px;
            }
        """)

        return layout_group_bx,group_bx


    def createGroupBox(self,title,layout,pos):
        
        group_bx=QtWidgets.QGroupBox(title)

        layout_group_bx=QtWidgets.QGridLayout()
        self.layoutV1=QtWidgets.QVBoxLayout()
        self.layoutV2=QtWidgets.QVBoxLayout()
        layout_group_bx.addLayout(self.layoutV1,0,0)
        layout_group_bx.addLayout(self.layoutV2,0,1)
        group_bx.setLayout(layout_group_bx)

        layout.addWidget(group_bx,pos,0)
        group_bx.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                
                color: #ffffff;
                border: none;
                border-radius:0px;
                margin-top: 25px; /* space for the title */
                background-color:#3f3f3f;
            }
            QGroupBox::title {
                font-weight: bold;
                subcontrol-origin: margin; /* position relative to border */
                subcontrol-position: top left; /* align title to the top-left */
                padding: 0 10px; /* add some padding around the title */
                background-color: #a8a8a8;
                color: #000000;
                border-radius:0px;
            }
        """)

        return layout_group_bx


    def changeStyleSheetWidget(self,i):
        print(i)
        for wi,widget in enumerate(self.nested_widget_buffer):
            if wi!=i:
                #print("is hiide")
                widget.hide()
                self.gridLayout.removeWidget(widget)
            if wi==i:
                #print("is show")
                widget.show()
                self.gridLayout.addWidget(widget, 0, 0, 1, 1)


    def addCustomWidgetsInDock(self,index,title,c_widget):
        dock = QtWidgets.QDockWidget(title, self.nested_widget_buffer[index])
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        

        dock.setWidget(c_widget)
        self.nested_widget_buffer[index].addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        return dock
    

    def addStyleSheetTextEditDock(self,index, title, default_text="",collable_connection:callable=lambda:...):
        dock = QtWidgets.QDockWidget(title, self.nested_widget_buffer[index])
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        
        text_edit = Custom.TextEditStyleSheetManager()
        self.hightlgtr_holder.append(PythonHighlighter(text_edit.document()))

        text_edit.setPlainText(default_text)
        dock.setWidget(text_edit)
        self.nested_widget_buffer[index].addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        text_edit.textChanged.connect(lambda:collable_connection(text_edit.toPlainText()))
        #self.gridLayout.addWidget(self.nested_widget_buffer[index], 0, 0, 1, 1)

        





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Setting_Dialog_Widgets(Form)
    #ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())