from __future__ import annotations
from PyQt6 import QtCore,QtWidgets,QtGui
import typing

if typing.TYPE_CHECKING:
    from CodeDock.DockingSystem.widgets.DockWidget import DockWidget
    from CodeDock.DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter

class TextEditThemeUpdateSignal(QtCore.QObject):
    whenUpdateDock=QtCore.pyqtSignal(QtCore.QObject)
    
class DockWidgetStyle:

    border_thickness='1'
    border_color="#4C4C4C"
    border_radius='0'
    activated_border_color="#6A9DA0"
    titlebar_bg_color="#4C4C4C"
    titlebar_activated_bg_color="#6A9DA0"
    title_text_color='red'
    close_button_color="#834343"
    maximize_button_color="#606549"
    minimize_button_color="#676C52"
    controll_button_hover_color="#927500"
    

    title_text_font=12
    #title_text_font_size=12
    titlebar_hsize=20
    controll_button_size=15
    controll_button_radius=0

    dock_widget_list:typing.Union[set,None]=()

    drop_indicator_color="#2B2B2B"
    drop_indicator_border_color="#4D4D4D"
    
    textEditThemeUpdate=TextEditThemeUpdateSignal()


    def getVarDict()->dict:
        return {
            "border_thickness":DockWidgetStyle.border_thickness,
            "border_color":DockWidgetStyle.border_color,
            "border_radius":DockWidgetStyle.border_radius,
            "activated_border_color":DockWidgetStyle.activated_border_color,
            "titlebar_bg_color":DockWidgetStyle.titlebar_bg_color,
            "titlebar_activated_bg_color":DockWidgetStyle.titlebar_activated_bg_color,
            "title_text_color":DockWidgetStyle.title_text_color,
            "title_text_font":DockWidgetStyle.title_text_font,
            "close_button_color":DockWidgetStyle.close_button_color,
            "maximize_button_color":DockWidgetStyle.maximize_button_color,
            "minimize_button_color":DockWidgetStyle.minimize_button_color,
            "controll_button_size":DockWidgetStyle.controll_button_size,
            "titlebar_hsize":DockWidgetStyle.titlebar_hsize,
            "controll_button_hover_color":DockWidgetStyle.controll_button_hover_color,
            "controll_button_radius":DockWidgetStyle.controll_button_radius

        }

    def updateVar(vdict):
        DockWidgetStyle.border_thickness=vdict["border_thickness"]
        DockWidgetStyle.border_color=vdict["border_color"]
        DockWidgetStyle.border_radius=vdict["border_radius"]
        DockWidgetStyle.activated_border_color=vdict["activated_border_color"]
        DockWidgetStyle.titlebar_bg_color=vdict["titlebar_bg_color"]
        DockWidgetStyle.titlebar_activated_bg_color=vdict["titlebar_activated_bg_color"]
        DockWidgetStyle.title_text_color=vdict["title_text_color"]
        DockWidgetStyle.title_text_font=vdict["title_text_font"]
        DockWidgetStyle.close_button_color=vdict["close_button_color"]
        DockWidgetStyle.maximize_button_color=vdict["maximize_button_color"]
        DockWidgetStyle.minimize_button_color=vdict["minimize_button_color"]
        DockWidgetStyle.controll_button_size=vdict["controll_button_size"]
        DockWidgetStyle.titlebar_hsize=vdict["titlebar_hsize"]
        DockWidgetStyle.controll_button_hover_color=vdict["controll_button_hover_color"]
        DockWidgetStyle.controll_button_radius=vdict["controll_button_radius"]



    def setDeActivatedStyleSheet(dock_widget:typing.Union[DockWidget]):
        
        dock_widget.setStyleSheet(f"""
            DockWidget {{        
            border:{DockWidgetStyle.border_thickness}px solid {DockWidgetStyle.border_color};
            border-bottom-left-radius:{DockWidgetStyle.border_radius}px;
            border-bottom-right-radius:{DockWidgetStyle.border_radius}px;
            }}
        """)


        dock_widget.title_bar.setStyleSheet(f"""
            background-color:{DockWidgetStyle.titlebar_bg_color};
            border-top-left-radius: {DockWidgetStyle.border_radius}px;
            border-top-right-radius: {DockWidgetStyle.border_radius}px;
        """)

    def setActivatedStyleSheet(dock_widget:"DockWidget"):
        
        dock_widget.setStyleSheet(f"""
            DockWidget {{        
            border:{DockWidgetStyle.border_thickness}px solid {DockWidgetStyle.activated_border_color};
            border-bottom-left-radius:{DockWidgetStyle.border_radius}px;
            border-bottom-right-radius:{DockWidgetStyle.border_radius}px;
            }}
        """)
        
        dock_widget.title_bar.setStyleSheet(f"""
            background-color:{DockWidgetStyle.titlebar_activated_bg_color};
            border-top-left-radius: {DockWidgetStyle.border_radius}px;
            border-top-right-radius: {DockWidgetStyle.border_radius}px;
        """)

    def setOtherStyles(dock_widget:typing.Union[DockWidget]):
        
        DockWidgetStyle.drop_indicator_color=DockWidgetStyle.titlebar_bg_color
        DockWidgetStyle.drop_indicator_border_color=DockWidgetStyle.titlebar_activated_bg_color

        dock_widget.vlayout.setContentsMargins(
            int(int(DockWidgetStyle.border_thickness)),
            int(int(DockWidgetStyle.border_thickness)),
            int(int(DockWidgetStyle.border_thickness)),
            int(int(DockWidgetStyle.border_thickness)))

        l_font=QtGui.QFont()
        l_font.setPointSize(DockWidgetStyle.title_text_font)
        l_font.setItalic(True)

        #l_font.setBold(True)
        dock_widget.title_bar.title_label.setFont(l_font)
        dock_widget.title_bar.title_label.setStyleSheet(f"color:{DockWidgetStyle.title_text_color};")
        dock_widget.title_bar.setFixedHeight(DockWidgetStyle.titlebar_hsize)

        #dock_widget.title_bar.block_path_navigation_bar.setFixedHeight(dock_widget.ttlbr_hsize)
        #dock_widget.title_bar.block_path_navigation_bar.setBtnFontSize(dock_widget.ttlbr_title_font)
        #dock_widget.title_bar.block_path_navigation_bar.setBtnIconSize(dock_widget.ttlbr_title_font)

        dock_widget.title_bar.close_button.setFixedSize(QtCore.QSize(DockWidgetStyle.controll_button_size,DockWidgetStyle.controll_button_size))
        dock_widget.title_bar.close_button.setIconSize(QtCore.QSize(DockWidgetStyle.controll_button_size-5,DockWidgetStyle.controll_button_size-5))
        dock_widget.title_bar.maximize_button.setFixedSize(QtCore.QSize(DockWidgetStyle.controll_button_size,DockWidgetStyle.controll_button_size))
        dock_widget.title_bar.maximize_button.setIconSize(QtCore.QSize(DockWidgetStyle.controll_button_size-5,DockWidgetStyle.controll_button_size-5))
        dock_widget.title_bar.minimize_button.setFixedSize(QtCore.QSize(DockWidgetStyle.controll_button_size,DockWidgetStyle.controll_button_size))
        dock_widget.title_bar.minimize_button.setIconSize(QtCore.QSize(DockWidgetStyle.controll_button_size-5,DockWidgetStyle.controll_button_size-5))
        dock_widget.title_bar.icon_button.setFixedSize(QtCore.QSize(DockWidgetStyle.controll_button_size,DockWidgetStyle.controll_button_size))
        dock_widget.title_bar.icon_button.setIconSize(QtCore.QSize(DockWidgetStyle.controll_button_size-5,DockWidgetStyle.controll_button_size-5))

    
        dock_widget.title_bar.close_button.setStyleSheet(f"""
            QPushButton{{
                background-color:{DockWidgetStyle.close_button_color};
                border-radius:{DockWidgetStyle.controll_button_radius}px;
            }}
            QPushButton:hover{{
                background-color:{DockWidgetStyle.controll_button_hover_color};
            }}

        """)

        dock_widget.title_bar.minimize_button.setStyleSheet(f"""
            QPushButton{{
                background-color:{DockWidgetStyle.minimize_button_color};
                border-radius:{DockWidgetStyle.controll_button_radius}px;
            }}
            QPushButton:hover{{
                background-color:{DockWidgetStyle.controll_button_hover_color};
            }}

        """)

        dock_widget.title_bar.maximize_button.setStyleSheet(f"""
            QPushButton{{
                background-color:{DockWidgetStyle.maximize_button_color};
                border-radius:{DockWidgetStyle.controll_button_radius}px;
            }}
            QPushButton:hover{{
                background-color:{DockWidgetStyle.controll_button_hover_color};
            }}

        """)


    def updateAllStyle(theme_dict:dict=None,dock_list:typing.Union[set[DockWidget],None]=None):

        if dock_list:
            DockWidgetStyle.dock_widget_list=dock_list
        if not theme_dict:
            theme_dict=DockWidgetStyle.getVarDict()

        DockWidgetStyle.updateVar(theme_dict)
        print(dock_list)
        for dock in DockWidgetStyle.dock_widget_list:
            dock:DockWidget
            DockWidgetStyle.setActivatedStyleSheet(dock)
            DockWidgetStyle.setDeActivatedStyleSheet(dock)
            DockWidgetStyle.setOtherStyles(dock)
            print(dock.isVisible() and dock.text_editor)
            if dock.isVisible() and dock.text_editor:
                
                DockWidgetStyle.textEditThemeUpdate.whenUpdateDock.emit(dock.text_editor)
            
            


    def copyDockList(dock_widget_list:typing.Union[set[DockWidget],None]):
        DockWidgetStyle.dock_widget_list=dock_widget_list


    def setBorderColor(color):
        DockWidgetStyle.border_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setBorderThickness(size):
        DockWidgetStyle.border_thickness=size
        DockWidgetStyle.updateAllStyle() 
        
    def setActiveBorderColor(color):
        DockWidgetStyle.activated_border_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setBorderRadius(size):
        DockWidgetStyle.border_radius=size
        DockWidgetStyle.updateAllStyle()


    def setTitleBarBgColor(color):
        DockWidgetStyle.titlebar_bg_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setActiveTitleBarBgColor(color):
        DockWidgetStyle.titlebar_activated_bg_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setTitleTextColor(color):
        DockWidgetStyle.title_text_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setCloseBtnBgColor(color):
        DockWidgetStyle.close_button_color=color.name()
        DockWidgetStyle.updateAllStyle()

    
    def setMaximizeBtnBgColor(color):
        DockWidgetStyle.maximize_button_color=color.name()
        DockWidgetStyle.updateAllStyle()


    def setMinimizeBtnBgColor(color):
        DockWidgetStyle.minimize_button_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setControllBtnHoverColor(color):
        DockWidgetStyle.controll_button_hover_color=color.name()
        DockWidgetStyle.updateAllStyle()

    def setControllBtnsRadius(size):
        DockWidgetStyle.controll_button_radius=size
        DockWidgetStyle.updateAllStyle()

    def setTitlebarHeight(size):
        DockWidgetStyle.titlebar_hsize=size
        DockWidgetStyle.updateAllStyle()

        
    def setTitleFontSize(size):
        DockWidgetStyle.title_text_font=size
        DockWidgetStyle.updateAllStyle()

    def setControllButtonSize(size):
        DockWidgetStyle.controll_button_size=size
        DockWidgetStyle.updateAllStyle()
