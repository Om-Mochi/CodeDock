from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.Dock.src.views.DockUi import Dock_Ui
from CodeDock.src.controllers.PathHandler import Path_Handler
from CodeDock.Dock.src.controllers.DockPanel import Dock_Panel

class Dock_Settings(Dock_Ui):
    def __init__(self):
        super().__init__()
        self.Path_h=Path_Handler()
        self.Panel=Dock_Panel(self.Path_h)
        
        
        self.Panel.map_tree.od_path=self.Path_h.OPEN_DOWN_ICON
        self.Panel.map_tree.cr_path=self.Path_h.CLOSE_RIGHT_ICON
        
        self.Panel.file_tree.od_path=self.Path_h.OPEN_DOWN_ICON
        self.Panel.file_tree.cr_path=self.Path_h.CLOSE_RIGHT_ICON
        
        self.screen_w=1920
        self.screen_h=1080 


        self.stylish_t_btn=self.customStyleToolBtn()
        self.stylish_t_btn.icon_size=33
        self.toolbox_size=46
        self.toolbox_btn_size=33


        #self.sizeToolbox()
        self.sizeIconsAndToolbox()
        self.setPngIconsOnButton()



   
    class customStyleToolBtn:
        def __init__(self):

            self.brdr_think=0
            self.brdr_clr=None
            self.bg_clr=None
            self.radius=0
            self.hover=None
            self.wh=0
            
            self.icon_size=0

        def getVarDict(self):
            return {'brdr_think':self.brdr_think,
                    'brdr_clr':self.brdr_clr,
                    'bg_clr':self.bg_clr,
                    'radius':self.radius,
                    'hover':self.hover,        
                    'wh':self.wh,
                    'icon_size':self.icon_size
                    }
        
        def applyStyle(self,button):
            button.setStyleSheet(f"""
                QPushButton {{
                    border: {self.brdr_think}px solid {self.brdr_clr};
                    background-color: {self.bg_clr}; /* Green background */
                    border-radius: {self.radius}px; /* Radius = half of the width/height */
                }}
                QPushButton:hover {{
                    background-color: {self.hover}; /* Slightly lighter green on hover */
                }}
                QPushButton:pressed {{
                    background-color: {self.bg_clr}; /* Darker green on press */
                }}
            """)
    
    def setPngIconsOnButton(self):
       #set icons in the btn
        
        self.file_open_btn.setIcon(QtGui.QIcon(self.Path_h.OPEN_FILE_ICON))
        #self.file_open_btn.setFlat(self.tool_btn_brdr)
        #self.file_open_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.file_open_btn)
        
        self.file_save_btn.setIcon(QtGui.QIcon(self.Path_h.SAVE_FILE_ICON))
        #self.file_save_btn.setFlat(self.tool_btn_brdr)
        #self.file_save_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.file_save_btn)

        self.settings_btn.setIcon(QtGui.QIcon(self.Path_h.SETTINGS_ICON))        
        #self.settings_btn.setFlat(self.tool_btn_brdr)
        #self.settings_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.settings_btn)

        self.pushButton_t.setIcon(QtGui.QIcon(self.Path_h.PARAMETER_ICON))        
        #self.pushButton_t.setFlat(self.tool_btn_brdr)
        #self.pushButton.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.pushButton_t)

        self.color_dialog_open.setIcon(QtGui.QIcon(self.Path_h.COLOR_DIALOG_ICON))        
        #self.color_dialog_open.setFlat(self.tool_btn_brdr)
        #self.color_dialog_open.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.color_dialog_open)

        self.color_widget_btn.setIcon(QtGui.QIcon(self.Path_h.PAINT_DIALOG_ICON))        
        #self.color_widget_btn.setFlat(self.tool_btn_brdr)
        #self.color_widget_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.color_widget_btn)
        self.color_dialog_open.setIcon(QtGui.QIcon(self.Path_h.COLOR_DIALOG_ICON))        
        #self.color_dialog_open.setFlat(self.tool_btn_brdr)
        #self.color_dialog_open.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.color_dialog_open)
    
    def sizeIconsAndToolbox(self,val=0):

        #icons
        self.file_open_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size)) 
        self.file_save_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.settings_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.pushButton_t.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.color_dialog_open.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.color_widget_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        
        #buttons
        self.file_open_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.file_open_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        
        self.file_save_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.file_save_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        
        self.settings_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.settings_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))

        self.pushButton_t.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.pushButton_t.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        
        self.color_dialog_open.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.color_dialog_open.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
    
        self.color_widget_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.color_widget_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
             
    def setToolButtonStyleSheet(self,stylesheet):
        self.file_open_btn.setStyleSheet(stylesheet)
        self.file_save_btn.setStyleSheet(stylesheet)
        self.settings_btn.setStyleSheet(stylesheet)
        self.pushButton_t.setStyleSheet(stylesheet)
        self.color_dialog_open.setStyleSheet(stylesheet)
        self.color_widget_btn.setStyleSheet(stylesheet)
    
    def sizeToolbox(self,val=0):
        self.frame_toolbox.setContentsMargins(self.frame_toolbox.e_spacing,0,self.frame_toolbox.e_spacing,0)
        self.frame_toolbox.hlayout.setSpacing(self.frame_toolbox.e_spacing)
        self.frame_toolbox.setFixedHeight(val)

        self.frame_toolbox.updateWidth()
        #self.frame_toolbox.setMaximumWidth(600)
        #self.frame_toolbox.setMinimumWidth(30)

        pass
        #print(val,"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        #self.tool_container_frame.setGeometry(QtCore.QRect(self.frame_toolbox.x(), self.frame_toolbox.y(),int(self.screen_w/2),val))
        #self.frame_toolbox.setFixedWidth(val) 
        #self.frame_toolbox.setMinimumSize(QtCore.QSize(0,val))
        #self.frame_toolbox.setMaximumSize(QtCore.QSize(16777215,val))
        #self.tool_container_frame.setFixedWidth(200)
        #self.frame_toolbox.setFixedWidth(200)

    def linkToolBoxBgColor(self,color): 
        self.frame_toolbox.bg_clr=color.name()
        self.frame_toolbox.applyStyle()
        

    def linkToolBoxBrdrColor(self,color):
        self.frame_toolbox.brdr_clr=color.name()
        self.frame_toolbox.applyStyle()

    def linkToolBoxBrdrRadius(self,size):
        self.frame_toolbox.brdr_radius=size
        self.frame_toolbox.applyStyle()

    #panel part

    def linkPanelBgColor(self,color):
        self.Panel.file_tree.bg_clr=color.name()
        self.Panel.file_tree.applyStyle()
        self.Panel.map_tree.bg_clr=color.name()
        self.Panel.map_tree.applyStyle()
    
    def linkPanelToolBarColor(self,color):
        self.Panel.toolbar_file_tree.bg_clr=color.name()
        self.Panel.toolbar_map_tree.bg_clr=color.name()

        self.Panel.toolbar_file_tree.applyStyle()
        self.Panel.toolbar_map_tree.applyStyle()

    def linkPanelToolBarHieght(self,size):
        self.Panel.toolbar_file_tree.h=size
        self.Panel.toolbar_map_tree.h=size
        self.Panel.toolbar_file_tree.setFixedHeight(size)
        self.Panel.toolbar_map_tree.setFixedHeight(size)

    def linkPanelToolButtonSize(self,size):
        #file panel
        self.Panel.add_file_ft_btn.w=size
        self.Panel.add_file_ft_btn.h=size
        self.Panel.add_file_ft_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.add_file_ft_btn.setSizeAsIconSize()

        self.Panel.add_folder_ft_btn.w=size
        self.Panel.add_folder_ft_btn.h=size
        self.Panel.add_folder_ft_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.add_folder_ft_btn.setSizeAsIconSize()

        self.Panel.filter_ft_btn.w=size
        self.Panel.filter_ft_btn.h=size
        self.Panel.filter_ft_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.filter_ft_btn.setSizeAsIconSize()
        
        self.Panel.close_panel_ft_btn.w=size
        self.Panel.close_panel_ft_btn.h=size
        self.Panel.close_panel_ft_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.close_panel_ft_btn.setSizeAsIconSize()


        #symbol panel
        self.Panel.close_panel_mt_btn.w=size
        self.Panel.close_panel_mt_btn.h=size
        self.Panel.close_panel_mt_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.close_panel_mt_btn.setSizeAsIconSize()

        self.Panel.refresh_mt_btn.w=size
        self.Panel.refresh_mt_btn.h=size
        self.Panel.refresh_mt_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.refresh_mt_btn.setSizeAsIconSize()
        
        self.Panel.setting_mt_button.w=size
        self.Panel.setting_mt_button.h=size
        self.Panel.setting_mt_button.setFixedSize(QtCore.QSize(size,size))
        self.Panel.setting_mt_button.setSizeAsIconSize()

        self.Panel.filter_mt_btn.w=size
        self.Panel.filter_mt_btn.h=size
        self.Panel.filter_mt_btn.setFixedSize(QtCore.QSize(size,size))
        self.Panel.filter_mt_btn.setSizeAsIconSize()
        
    

    def linkPanelButtonColor(self,color):
        self.Panel.file_tree.btn_clr=color.name()
        self.Panel.file_tree.applyStyle()
        self.Panel.map_tree.btn_clr=color.name()
        self.Panel.map_tree.applyStyle()
        
    def linkPanelFontColor(self,color):
        self.Panel.file_tree.font_clr=color.name()
        self.Panel.file_tree.applyStyle()
        
        self.Panel.map_tree.font_clr=color.name()
        self.Panel.map_tree.applyStyle()
        

    def linkPanelItemSize(self,size):
        self.Panel.map_tree.font_size=size
        self.Panel.map_tree.item_font.setPointSize(size)
        self.Panel.map_tree.setIconSize(QtCore.QSize(size,size))
        self.Panel.map_tree.setFont(self.Panel.map_tree.item_font)

        self.Panel.file_tree.font_size=size
        self.Panel.file_tree.item_font.setPointSize(size)
        self.Panel.file_tree.setIconSize(QtCore.QSize(size,size))
        self.Panel.file_tree.setFont(self.Panel.file_tree.item_font)


    


    def linkPanelBrdrColor(self,color):
        self.Panel.file_tree.brdr_clr=color.name()
        self.Panel.file_tree.applyStyle()

        self.Panel.map_tree.brdr_clr=color.name()
        self.Panel.map_tree.applyStyle()
        
    def linkPanelBtnBrdrColor(self,color):
        self.Panel.file_tree.btn_brdr_clr=color.name()
        self.Panel.file_tree.applyStyle()

    
        self.Panel.map_tree.btn_brdr_clr=color.name()
        self.Panel.map_tree.applyStyle()
        
    def linkPanelBrdrThink(self,size):
        self.Panel.file_tree.font_size=size

    def linkPanelBtnBrdrThink(self,size):
        self.Panel.file_tree.font_size=size

    def linkPanelBrdrRadius(self,size):
        self.Panel.file_tree.font_size=size
        self.Panel.file_tree.applyStyle()

    def linkPanelBtnRadius(self,size):
        self.Panel.file_tree.font_size=size
        self.Panel.file_tree.applyStyle()

    def linkToolBoxSize(self,size=0):
        self.frame_toolbox.h=size
        self.sizeToolbox(size)


    def linkToolBoxRadius(self,size):

        self.frame_toolbox.brdr_radius=size
        self.frame_toolbox.applyStyle()
        #self.sizeToolbox(size)

    
    def linkToolBoxBrdrThinkness(self,size):
        self.frame_toolbox.brdr_think=size
        self.frame_toolbox.applyStyle()

    def linkToolBoxButtonBrdrColor(self,color):
        self.stylish_t_btn.brdr_clr=color.name()
        self.setPngIconsOnButton()


    def linkToolBoxButtonBrdrThinkness(self,size):
        self.stylish_t_btn.brdr_think=size
        self.setPngIconsOnButton()

    def linkToolBoxButtonBrdrRadius(self,radius):
        self.stylish_t_btn.radius=radius
        self.setPngIconsOnButton()

    def linkToolBoxBrdrRadius(self,size):
        self.frame_toolbox.brdr_radius=size
        self.frame_toolbox.applyStyle()

    def linkToolBoxButtonColor(self,color):
        self.stylish_t_btn.bg_clr=color.name()
        self.setPngIconsOnButton()

    def linkToolBoxButtonSize(self,size=0):
        self.stylish_t_btn.wh=size
        self.frame_toolbox.btn_width=size
        self.sizeIconsAndToolbox(self.stylish_t_btn.wh)
        self.frame_toolbox.updateWidth()

    def linkToolBoxIconSize(self,size=0):
        self.stylish_t_btn.icon_size=size
        self.sizeIconsAndToolbox()

    def linkToolBoxBtnSpacing(self,size):
        self.frame_toolbox.e_spacing=size
        self.frame_toolbox.hlayout.setSpacing(size)
        self.frame_toolbox.setContentsMargins(size,0,size,0)
        self.frame_toolbox.updateWidth()
    #tabbar

    def linkTabbarBgColor(self,color):
        self.Panel.tabbar_panel.bg_clr=color.name()
        self.Panel.tabbar_panel.applyStyle()
        self.Panel.frame_tabbar.bg_clr=color.name()
        self.Panel.frame_tabbar.applyStyle()


    def linkTabbarBrdrColor(self,color):pass
        
    def linkTabBtnBgColor(self,color):
        self.Panel.tabbar_panel.tab_clr=color.name()
        self.Panel.tabbar_panel.applyStyle()
    
    def linkTabBtnBrdrColor(self,color):
        self.Panel.tabbar_panel.tab_brdr=color.name()
        self.Panel.tabbar_panel.applyStyle()
        
    def linkTabBtnWorkingBrdrColor(self,color):
        self.Panel.tabbar_panel.brdr[0]=color.name()
        self.Panel.tabbar_panel.applyStyle()

    def linkTabBtnNonWorkingBrdrColor(self,color):
        self.Panel.tabbar_panel.brdr[1]=color.name()
        self.Panel.tabbar_panel.applyStyle()
    

    def linkTabbarHSize(self,size):
        self.Panel.tabbar_panel.tab_padding_rl=size+2
        self.Panel.tabbar_panel.tab_padding_tb=size

        self.Panel.tabbar_panel.applyStyle()
    
    def linkTabbarFrameHSize(self,size):
        self.Panel.frame_tabbar.h=size
        self.Panel.tabbar_panel.tab_size=size
        self.Panel.tabbar_panel.setFixedHeight(self.Panel.tabbar_panel.tab_size)
        self.Panel.tabbar_panel.setFixedHeight(self.Panel.frame_tabbar.h)

        
    def linkTabBtnRadius(self,size):
        self.Panel.tabbar_panel.tab_radius=size    
        self.Panel.tabbar_panel.applyStyle()
        
    def linkPanelScrollBarColor(self,color):
        self.Panel.map_tree.scroll_bar_clr=color.name()
        self.Panel.map_tree.applyStyle()
        
        self.Panel.file_tree.scroll_bar_clr=color.name()
        self.Panel.file_tree.applyStyle()
    
    def linkPanelScrollHandelColor(self,color):
        
        self.Panel.map_tree.scroll_handel_clr=color.name()
        self.Panel.map_tree.applyStyle()

        self.Panel.file_tree.scroll_handel_clr=color.name()
        self.Panel.file_tree.applyStyle()
    
       
    
    def linkTabBtnHoverColor(self,color):
        self.Panel.tabbar_panel.tab_hover_clr=color.name()
        self.Panel.tabbar_panel.applyStyle()
        
        
    
    def linkTabBtnSelectedColor(self,color):
        self.Panel.tabbar_panel.tab_selected_clr=color.name()
        self.Panel.tabbar_panel.applyStyle()
    
    
    def linkTabBtnFontColor(self,color):
        self.Panel.tabbar_panel.font_clr=color.name()
        self.Panel.tabbar_panel.applyStyle()
