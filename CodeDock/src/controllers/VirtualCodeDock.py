from PyQt6 import QtCore,QtGui,QtWidgets
from CodeDock.C_Widgets.Custom import Custom

class Virtual_Code_Dock_Widget(Custom.Widget):
    whenVirtualTabChange=QtCore.pyqtSignal(int)
    whenVirtualTabAdd=QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()

        self.w=200
        self.h=32
        #self.setFixedSize(self.w,self.h)
        
        self.container_layout=QtWidgets.QGridLayout()
        self.container_layout.setContentsMargins(0,2,0,2)
        self.setLayout(self.container_layout)
        
        self.tab_list=[]
        self.current_tab_index=0
        self.tabbar=Custom.TabBar()

        self.tabbar.tab_w=60
        self.tabbar.tab_h=26
        
        self.tabbar.setFixedWidth(self.tabbar.tab_w)
        
        self.tabbar.tab_size_flag=True  
        self.tabbar.setFixedHeight(32)
        self.tabbar.tab_clr="#ac793e"
        self.tabbar.tab_hover_clr="#6B4763"
        self.tabbar.tab_selected_clr="#5C377A"        
        self.tabbar.tab_brdr_size=0
        self.tabbar.applyStyle()
        
        self.tabbar.tabBarClicked.connect(lambda i:self.whenVirtualTabChange.emit(int(self.tabbar.tabText(i))-1))
        self.container_layout.addWidget(self.tabbar,0,0)

        self.tab_add_btn=Custom.PushButton()
        self.tab_add_btn.setFixedSize(28,28)
        self.tab_add_btn.setIconSize(QtCore.QSize(28,28))
        #self.tab_add_btn.bg_clr="#EEFF03"

        self.tab_add_btn.whenCursorEnter.connect(lambda:self.tab_add_btn.setIconSize(QtCore.QSize(self.tab_add_btn.size().width()+3,self.tab_add_btn.size().height()+3)))
        self.tab_add_btn.whenCursorLeave.connect(lambda:self.tab_add_btn.setIconSize(QtCore.QSize(28,28)))
        self.tab_add_btn.hover_clr="none"
        self.tab_add_btn.applyStyle()
        self.container_layout.addWidget(self.tab_add_btn,0,1,alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        #self.container_layout.setColumnStretch(0,1)
        #self.container_layout.setColumnStretch(0,1)
        self.tab_add_btn.clicked.connect(self.addVirtualTab)  
        
        #self.tabbar.applyStyle()
        
        #default virtualtab
        #self.tabbar.addTab(f"{len(self.tab_list)+1}")
        #self.current_tab_index=len(self.tab_list)
        #self.tab_list.append(f"{self.tabbar.tabText(self.current_tab_index)}")
        
        self.tabbar.updateGeometry()
        self.tabbar.update()

    def addVirtualTab(self):
        self.tabbar.addTab(f"{len(self.tab_list)+1}")
        self.tabbar.setCurrentIndex(len(self.tab_list))
        self.current_tab_index=len(self.tab_list)        
        self.tab_list.append(f"{self.tabbar.tabText(self.current_tab_index)}")
        
        print("\n\nInedexexexexxexexex ",len(self.tab_list)+1)
        
        if self.w>self.tabbar.tab_w*len(self.tab_list):
            print(self.tabbar.tab_w,"--------")
            
            self.tabbar.setFixedWidth(self.tabbar.tab_w*len(self.tab_list))
            
        else:
            self.tabbar.setFixedWidth(self.w)

        self.whenVirtualTabAdd.emit()
        
        
        

