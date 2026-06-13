from CodeDock.C_Widgets.Custom import Custom
from CodeDock.src.views.CodeDockUi import Code_Dock_Ui
from CodeDock.src.controllers.VirtualCodeDock import Virtual_Code_Dock_Widget

class Code_Dock_Settings(Code_Dock_Ui):
    def __init__(self):
        super().__init__()
        self.virtual_CD=Virtual_Code_Dock_Widget()



    #Window Titlebar

    def linkWindowTitleBarBgColor(self,color):
        self.MainWindow.ttlbr_bg_clr=color.name()
        self.MainWindow.applyStyle()
    def linkWindowTitleBarBrdrColor(self,color):...

    def linkWindowBorderColor(self,color):
        self.MainWindow.window_brdr_color=color.name()
        self.MainWindow.applyWindowStyle()

    def linkWindowBorderThinkness(self,size):
        self.MainWindow.window_brdr_think=size
        self.MainWindow.applyStyle()
    
    def linkWindowTitleTextColor(self,color):
        self.MainWindow.ttlbr_text_clr=color.name()
        self.MainWindow.applyStyle()

    def linkWindowCloseBtnBgColor(self,color):
        self.MainWindow.close_btn_clr=color.name()
        self.MainWindow.applyStyle()

    def linkWindowCloseBtnHoverBgColor(self,color):
        self.MainWindow.close_btn_hover=color.name()
        self.MainWindow.applyStyle()
    
    def linkWindowMaximizeBtnBgColor(self,color):
        self.MainWindow.maximize_btn_clr=color.name()
        self.MainWindow.applyStyle()


    def linkWindowMaximizeBtnHoverBgColor(self,color):
        self.MainWindow.maximize_btn_hover=color.name()
        self.MainWindow.applyStyle()

    def linkWindowTitleBarHover(self,color):
        self.MainWindow.ttlbr_hover=color.name()
        self.MainWindow.applyStyle()

    
    def linkWindowBtnsRadius(self,size):
        self.MainWindow.btns_radius=size
        self.MainWindow.applyStyle()

    def linkWindowTitlebarHeight(self,size):
        self.MainWindow.ttlbr_hsize=size
        self.MainWindow.applyStyle()
        self.virtual_CD.setFixedHeight(size)
        self.virtual_CD.tabbar.setFixedHeight(size)
        
    def linkWindowTitleFontSize(self,size):
        self.MainWindow.ttlbr_title_font=size
        self.MainWindow.applyStyle()

    def linkWindowTitlebarButtonSize(self,size):
        self.MainWindow.ttlbr_btns_size=size
        self.MainWindow.applyStyle()

    def linkWindowTitlebarCDIconSize(self,size):
        self.MainWindow.ttlbr_icon_size=size
        self.MainWindow.applyStyle()


    def linkVirtualTabBgColor(self,color):
        self.virtual_CD.tabbar.tab_clr=color.name()
        self.virtual_CD.tabbar.applyStyle()
    
    def linkVirtualTabHoverColor(self,color):
        self.virtual_CD.tabbar.tab_hover_clr=color.name()
        self.virtual_CD.tabbar.applyStyle()

    def linkVirtualTabSelectedColor(self,color):
        self.virtual_CD.tabbar.tab_selected_clr=color.name()
        self.virtual_CD.tabbar.applyStyle()
    
    def linkVirtualTabTextColor(self,color):
        self.virtual_CD.tabbar.font_clr=color.name()
        self.virtual_CD.tabbar.applyStyle()



    def linkVirtualTabWidth(self,size):
        self.virtual_CD.tabbar.tab_w=size
        
        self.virtual_CD.tabbar.updateGeometry()
        self.virtual_CD.tabbar.update()

    def linkVirtualTabHeight(self,size):
        self.virtual_CD.tabbar.tab_h=size
        self.virtual_CD.tabbar.updateGeometry()
        self.virtual_CD.tabbar.update()

    
