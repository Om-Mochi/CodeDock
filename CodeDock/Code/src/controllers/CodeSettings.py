from CodeDock.Code.src.views.CodeUi import Code_Ui
from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.src.controllers.PathHandler import Path_Handler
from CodeDock.C_Widgets.Custom import Custom
#from CodeDock.Code.src.views. import 
class Code_Settings(Code_Ui):
    def __init__(self):
        super().__init__()
        #QtCore.QSize()
        #QtWidgets.QWidget().setGeometry(ax, ay, aw, ah)
        #QtGui.QBitmap(sk)
        self.highlighter=[]
        self.mini_map_highlighter=None
        self.running_textedit_editor:Custom.TextEditor=None
        self.tabbar_widget
 
        self.lsp_server=None    
        self.stylish_t_btn=self.customStyleToolBtn()
        self.style_editor=self.customStyleTextEdit()
        self.style_numpad=self.customStyleTextEdit()
        
        self.style_completer=self.customStyleCompleter()
        self.screen_w=1920
        self.screen_h=1080 
        
        self.Path_h=Path_Handler()
       
        #self.style_numpad.w=65
        
        #self.stylish_t_btn.icon_size=33
                
        #elf.frame_toolbox.w=40
        #self.stylish_t_btn.wh=33
        
        self.tool_container_frame.h=int(self.screen_h/2)

        #self.style_editor.font_size=14
        
        #tabbar
        #self.frame_tabbar.h=45
        #self.tabbar_editor.tab_size=40
        
        #self.setPngIconsOnButton()
        #self.sizeToolbox()
        #self.sizeIconsAndToolbox()

    class customStyleCompleter:
        
        def __init__(self):
            self.bg_clr=None
            self.brdr_clr=None
            self.selecte_item_clr=None
            self.brdr_think=0
            self.text_clr=None
            self.font=None
            self.font_size=12
            self.selecte_text_clr=None
            self.scroll_bar_clr="none"
            self.scroll_handel_clr="none"

        def updateVar(self,var_dict):
            self.bg_clr=var_dict['bg_clr']
            self.brdr_clr=var_dict['brdr_clr']
            self.selecte_item_clr=var_dict['selecte_item_clr']
            self.brdr_think=var_dict['brdr_think']
            self.text_clr=var_dict['text_clr']
            self.font=var_dict['font']
            self.font_size=var_dict['font_size']
            self.selecte_text_clr=var_dict['selecte_text_clr']

        def getVar(self):
            return {
                "bg_clr":self.bg_clr,
                "brdr_clr":self.brdr_clr,
                "selecte_item_clr":self.selecte_item_clr,
                "brdr_think":self.brdr_think,
                "text_clr":self.text_clr,
                "font":self.font,
                "font_size":self.font_size,
                "selecte_text_clr":self.selecte_text_clr,
            }
        
        def applyStyle(self,textedit):    
            textedit.completer.popup().setStyleSheet(f"""
                QListView {{
                    background-color: {self.bg_clr};
                    color: {self.text_clr};
                    border: {self.brdr_think}px solid {self.brdr_clr};
                    padding: 2px;
                    font-family: {self.font};
                    font-size: {self.font_size}px;
                }}
                QListView::item:selected {{
                    background-color: {self.selecte_item_clr};
                    color: {self.selecte_text_clr};
                }}
                QScrollBar::add-line, QScrollBar::sub-line {{
                    border: none; 
                    background: none;
                    
                }}
                QScrollBar:vertical {{
                    background: {self.selecte_item_clr};      /* Scrollbar background */
                    border-radius: 4px;
                    
                    width: 10px;              /* Width of the scrollbar */
                    margin: 0px;               /* No margins */
                }}
                

                QScrollBar:horizontal {{
                    background: {self.selecte_item_clr};  /* Scrollbar background */
                    border-radius: 4px;
                    height: 10px;              /* Scrollbar height */
                    margin: 0px;              /* Margins around scrollbar */
                }}

                QScrollBar::handle:vertical {{
                    background: {self.text_clr};      
                    border-radius: 4px;       /* Rounded handle */
                    min-height: 20px;         /* Minimum height for usability */
                }}
            
                
                QScrollBar::handle:horizontal {{
                    background: {self.text_clr};      /* Scrollbar handle color (green) */
                    border-radius: 4px;       /* Rounded handle corners */
                    min-width: 20px;          /* Minimum handle width */
                }}
            """)

    class customStyleTextEdit:
        def __init__(self):
            self.bg_clr="none"
            self.brdr_clr="none"
            
            self.scroll_bar_clr="none"
            self.scroll_handel_clr="none"
            
            self.brdr_radius=0
            self.brdr_think=0

            self.w=None
            self.font=None
            self.font_size=14
            self.indent_alfa=30
            self.indent_rgba=[255, 255, 255,self.indent_alfa]
            
        def getVarDict(self):
            return {'bg_clr': self.bg_clr, 
                    'brdr_clr': self.brdr_clr, 
                    'scroll_bar_clr': self.scroll_bar_clr, 
                    'scroll_handel_clr': self.scroll_handel_clr, 
                    'brdr_radius': self.brdr_radius, 
                    'brdr_think': self.brdr_think,
                    'w':self.w,
                    'font':self.font,
                    'font_size':self.font_size,
                    'indent_alfa':self.indent_alfa,
                    'indent_rgba':self.indent_rgba
                    }
        
        def updateVar(self,editor,dict):
            editor.bg_clr=dict["bg_clr"]
            editor.brdr_clr=dict["brdr_clr"]
            editor.scroll_bar_clr=dict["scroll_bar_clr"]
            editor.scroll_handel_clr=dict["scroll_handel_clr"]
            editor.brdr_radius=dict["brdr_radius"]
            editor.brdr_think=dict["brdr_think"]
            editor.w=dict["w"]
            editor.font=dict["font"]
            editor.font_size=dict["font_size"]
            editor.indent_alfa=dict["indent_alfa"]
            editor.indent_rgba=dict["indent_rgba"]
                    
        def applyStyle(self,editor):

            
            editor.setStyleSheet(f"""
                QPlainTextEdit {{
                    padding:8px;                                   
                    background-color:{self.bg_clr};
                    border: {self.brdr_think}px solid {self.brdr_clr};    
                    border-radius:{self.brdr_radius};
                    selection-background-color: #cc3333;
                }}
                QScrollBar::add-line, QScrollBar::sub-line {{
                    border: none; 
                    background: none;
                    
                }}
                QScrollBar:vertical {{
                    background: {self.scroll_bar_clr};      /* Scrollbar background */
                    border-radius: 4px;
                    
                    width: 10px;              /* Width of the scrollbar */
                    margin: 0px;               /* No margins */
                }}
                

                QScrollBar:horizontal {{
                    background: {self.scroll_bar_clr};  /* Scrollbar background */
                    border-radius: 4px;
                    height: 10px;              /* Scrollbar height */
                    margin: 0px;              /* Margins around scrollbar */
                }}

                QScrollBar::handle:vertical {{
                    background: {self.scroll_handel_clr};      
                    border-radius: 4px;       /* Rounded handle */
                    min-height: 20px;         /* Minimum height for usability */
                }}
            
                
                QScrollBar::handle:horizontal {{
                    background: {self.scroll_handel_clr};      /* Scrollbar handle color (green) */
                    border-radius: 4px;       /* Rounded handle corners */
                    min-width: 20px;          /* Minimum handle width */
                }}
            
            """)
            editor.numpad_area.bg_clr=self.bg_clr
            editor.update()
    
    
    
    class customStyleToolBtn:
        def __init__(self):

            self.brdr_think=0
            self.brdr_clr=None                  
            self.bg_clr=None
            self.radius=0
            self.hover=None
            self.wh=None
            
            self.icon_size=None

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
        
    
    
        self.long_view_code_btn.setIcon(QtGui.QIcon(self.Path_h.LONG_VIEW_CODE))        
        #self.long_view_code_btn.setFlat(self.tool_btn_brdr)
        #self.long_view_code_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.long_view_code_btn)

        self.zoom_in_btn.setIcon(QtGui.QIcon(self.Path_h.ZOOM_IN_ICON))        
        #self.zoom_in_btn.setFlat(self.tool_btn_brdr)
        #self.zoom_in_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.zoom_in_btn)

        self.zoom_out_btn.setIcon(QtGui.QIcon(self.Path_h.ZOOM_OUT_ICON))        
        #self.zoom_out_btn.setFlat(self.tool_btn_brdr)
        #self.zoom_out_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.zoom_out_btn)

        self.up_arrow_btn.setIcon(QtGui.QIcon(self.Path_h.UP_ARROW_ICON))        
        #self.up_arrow_btn.setFlat(self.tool_btn_brdr)
        #self.up_arrow_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.up_arrow_btn)

        self.down_arrow_btn.setIcon(QtGui.QIcon(self.Path_h.DOWN_ARROW_ICON))        
        #self.down_arrow_btn.setFlat(self.tool_btn_brdr)
        #self.down_arrow_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.down_arrow_btn)


        self.add_subwindow_btn.setIcon(QtGui.QIcon(self.Path_h.ADD_SUBWINDOW_ICON))        
        #self.add_subwindow_btn.setFlat(self.tool_btn_brdr)
        #self.add_subwindow_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.add_subwindow_btn)

        self.web_browser_btn.setIcon(QtGui.QIcon(self.Path_h.WEB_BROWSER_ICON))        
        #self.close_subwindow_btn.setFlat(self.tool_btn_brdr)
        #self.close_subwindow_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.web_browser_btn)

        self.auto_subwindow_arrange_btn.setIcon(QtGui.QIcon(self.Path_h.AUTO_WINDOW_ARRANGE_ICON))        
        #self.auto_subwindow_arrange_btn.setFlat(self.tool_btn_brdr)
        #self.auto_subwindow_arrange_btn.setStyleSheet("border: none;")
        self.stylish_t_btn.applyStyle(self.auto_subwindow_arrange_btn)



    def sizeIconsAndToolbox(self):
        self.long_view_code_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.zoom_in_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.zoom_out_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.up_arrow_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.down_arrow_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.add_subwindow_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.auto_subwindow_arrange_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.web_browser_btn.setIconSize(QtCore.QSize(self.stylish_t_btn.icon_size,self.stylish_t_btn.icon_size))
        self.long_view_code_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.long_view_code_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.zoom_in_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.zoom_in_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.zoom_out_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.zoom_out_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.up_arrow_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.up_arrow_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.down_arrow_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.down_arrow_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.add_subwindow_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.add_subwindow_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.web_browser_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.web_browser_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.auto_subwindow_arrange_btn.setMinimumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))
        self.auto_subwindow_arrange_btn.setMaximumSize(QtCore.QSize(self.stylish_t_btn.wh, self.stylish_t_btn.wh))

    def setToolButtonStyleSheet(self,stylesheet:QtWidgets.QPushButton.styleSheet):
        self.long_view_code_btn.setStyleSheet(stylesheet)
        self.zoom_in_btn.setStyleSheet(stylesheet)
        self.zoom_out_btn.setStyleSheet(stylesheet)
        self.up_arrow_btn.setStyleSheet(stylesheet)
        self.down_arrow_btn.setStyleSheet(stylesheet)
        self.add_subwindow_btn.setStyleSheet(stylesheet)
        self.auto_subwindow_arrange_btn.setStyleSheet(stylesheet)
        self.web_browser_btn.setStyleSheet(stylesheet)
        
    def configCodeEditor(self,fn="JetBrainsMonoNL Nerd Font"):

        #self..setFont(QFont("Ubuntu",12+val))  # Monospace font
        #self.textedit_for_numbers.setFont(QFont("Ubuntu",12+val))
        
        font_editor = QtGui.QFont(fn)
        font_minimap = QtGui.QFont(fn)
        #font_editor.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        #self.setFont(font)

        #font.setPointSize(2+val)
        font_editor.setPointSize(self.style_editor.font_size)
        
        font_minimap.setPointSize(2)
        

        if self.running_textedit_editor!=None:
            #font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
            self.running_textedit_editor.setFont(font_editor)
            #self.sub_numpad_textedit.setFont(font_editor)
            #self.sub_numpad_textedit.setFixedWidth(int(self.style_numpad.w))
            #self.mini_map.map_font=font_minimap
            #self.mini_map.viewport().update()
            self.mini_map.setFont(font_minimap)

    #currently disable 
    def zoomInEditor(self):
        self.editor_font_size=self.editor_font_size+1
        
        self.style_numpad.w=int(self.style_numpad.w+1*(4.5))
        self.configCodeEditor()
    
    def zoomOutEditor(self):
        self.editor_font_size=self.editor_font_size-1

        self.style_numpad.w=int(self.style_numpad.w-1*(4.5))
        self.configCodeEditor()
        
    def setNumpadWidth(self,val=0):
        self.editor_font_size=14+val

        self.style_numpad.w=int(65+val*(2.5))
        self.configCodeEditor()
        #self.sizeCodeEditor_2(val)
        #self.featureLongViewEditor()
    
    def sizeToolbox(self,val=0):
        self.tool_container_frame.setGeometry(QtCore.QRect(0, 0, val,int(self.screen_h/2)))
        self.frame_toolbox.setFixedWidth(val) 
        self.frame_toolbox.setMinimumSize(QtCore.QSize(val,0))
        self.frame_toolbox.setMaximumSize(QtCore.QSize(val,16777215))

    def linkToolBoxBtnSpacing(self,size):
        self.tool_container_frame.h=(8*self.stylish_t_btn.wh)+8*size
        self.tool_container_frame.setFixedHeight(self.tool_container_frame.h)
        

    def linkToolBoxBgColor(self,color):
        self.frame_toolbox.bg_clr=color.name()
        self.frame_toolbox.applyStyle()

    def linkToolBoxButtonBgColor(self,color):
        pass

    def linkToolBoxBrdrColor(self,color):
        self.frame_toolbox.brdr_clr=color.name()
        self.frame_toolbox.applyStyle()

    def linkToolBoxButtonBrdrColor(self,color):
        self.stylish_t_btn.brdr_clr=color.name()
        self.setPngIconsOnButton()


    def linkToolBoxButtonBrdrRadius(self,radius):
        self.stylish_t_btn.radius=radius
        self.setPngIconsOnButton()
    def linkToolBoxButtonBrdrThinkness(self,size):
        self.stylish_t_btn.brdr_think=size
        self.setPngIconsOnButton()


    def linkToolBoxBrdrRadius(self,size):
        self.frame_toolbox.brdr_radius=size
        self.frame_toolbox.applyStyle()

    def linkToolBoxSize(self,size=0):
        self.frame_toolbox.brdr_radius=size
        
        
        self.sizeToolbox(size)

    def linkToolBoxBrdrThinkness(self,size):
        self.frame_toolbox.brdr_think=size
        self.frame_toolbox.applyStyle()
    
    def linkToolBoxButtonColor(self,color):
        self.stylish_t_btn.bg_clr=color.name()
        self.setPngIconsOnButton()

    def linkToolBoxButtonSize(self,size=0):
        self.stylish_t_btn.wh=size
        self.sizeIconsAndToolbox()
        
    def linkToolBoxIconSize(self,size=0):
        self.stylish_t_btn.icon_size=size
        self.sizeIconsAndToolbox()

    #editor

    def linkEditorBrdrThinkness(self,size):
        self.style_editor.brdr_think=size
        self.style_editor.applyStyle(self.running_textedit_editor)

    def linkNumpadBrdrThinkness(self,size):
        self.style_numpad.brdr_think=size
        #self.style_numpad.applyStyle(self.running_textedit_numpad)

    def linkEditorBrdrRadius(self,size):
        self.style_editor.brdr_radius=size
        #self.style_editor.applyStyle(self.running_textedit_editor)

    def linkNumpadBrdrRadius(self,size):
        self.mdi_area.subw_radius=size
        self.mdi_area.applyStyle()


    def linkEditorBgColor(self,color):
        self.style_editor.bg_clr=color.name()
        self.style_editor.applyStyle(self.running_textedit_editor)
        #self.textedit_mini_map.setStyleSheet(f"background-color:{color.name()};font-size:2px;")
        
    def linkEditorBrdrColor(self,color):
        self.style_editor.brdr_clr=color.name()
        self.style_editor.applyStyle(self.running_textedit_editor)

    
    def linkNumpadBgColor(self,color):
        self.style_numpad.bg_clr=color.name()
        #self.style_numpad.applyStyle(self.running_textedit_numpad)
    

    def linkNumpadBrdrColor(self,color):
        self.style_numpad.brdr_clr=color.name()
        #self.style_numpad.applyStyle(self.running_textedit_numpad)
    
    def linkEditorScrollBarColor(self,color):
        self.style_editor.scroll_bar_clr=color.name()
        self.style_editor.applyStyle(self.running_textedit_editor)

    
    def linkEditorScrollHandelColor(self,color):
        self.style_editor.scroll_handel_clr=color.name()
        self.style_editor.applyStyle(self.textedit_code_editor)
    
    def linkEditorFontSize(self,size):
        self.style_editor.font_size=int(size)
        self.configCodeEditor()
        self.running_textedit_editor.updateCompleterFontIconSize()
        #self.style_editor.applyStyle()
    def linkNumpadWidth(self,size):
        self.style_numpad.w=int(size)
        self.configCodeEditor()
    def linkIndentAlfa(self,alfa):
        self.style_editor.indent_alfa=int(alfa)
        self.style_editor.indent_rgba[3]=int(alfa)
        self.textedit_code_editor.indent_rgba=self.style_editor.indent_rgba

        self.textedit_code_editor.update()
    def linkIndentColor(self,color):
        self.style_editor.indent_rgba=[color.red(),color.green(),color.blue(),self.style_editor.indent_alfa]
        self.textedit_code_editor.indent_rgba=self.style_editor.indent_rgba
        self.textedit_code_editor.update()



    
    #mdi & subwindow
    
    def linkMdiBgColor(self,color):
        self.mdi_area.mdi_bg_clr=color.name()
        self.mdi_area.applyStyle()
    
    def linkMdiBrdrColor(self,color):
        self.mdi_area.mdi_brdr_clr=color.name()
        self.mdi_area.applyStyle()

    def linkMdiBrdrThinkness(self,size):
        self.mdi_area.mdi_brdr_think=size
        self.mdi_area.applyStyle()

    def linkSubWindowBgColor(self,color):
        self.mdi_area.subw_bg_clr=color.name()
        self.mdi_area.applyStyle()

    def linkSubWindowBrdrColor(self,color):
        self.mdi_area.subw_brdr_clr=color.name()
        self.mdi_area.applyStyle() 

    def linkSubWindowBrdrThinkness(self,size):
        self.mdi_area.subw_brdr_think=size
        self.mdi_area.applyStyle() 
        
    def linkActiveSubWindowBrdrColor(self,color):
        self.mdi_area.subw_active_brdr_clr=color.name()
        self.mdi_area.applyStyle()

    def linkSubWindowBrdrRadius(self,size):
        self.mdi_area.subw_radius[1]=size
        self.mdi_area.applyStyle()


    def linkDockWidgetTitleBarBrdrRadius(self,size):
        self.mdi_area.subw_radius[0]=size
        self.mdi_area.applyStyle()
    
    def linkSubWindowTitleBarBgColor(self,color):
        self.mdi_area.subw_ttlbr_bg_clr=color.name()
        self.mdi_area.applyStyle()

    def linkActiveSubWindowTitleBarBgColor(self,color):
        self.mdi_area.subw_activated_ttlbr_clr=color.name()
        self.mdi_area.applyStyle()

    def linkSubWindowTitleTextColor(self,color):
        self.mdi_area.subw_ttlbr_text_clr=color.name()
        self.mdi_area.applyStyle()

    def linkSubWindowCloseBtnBgColor(self,color):
        self.mdi_area.subw_close_btn_clr=color.name()
        self.mdi_area.applyStyle()

    def linkSubWindowCloseBtnHoverBgColor(self,color):
        self.mdi_area.subw_close_btn_hover=color.name()
        self.mdi_area.applyStyle()
    
    def linkSubWindowMaximizeBtnBgColor(self,color):
        self.mdi_area.subw_maximize_btn_clr=color.name()
        self.mdi_area.applyStyle()


    def linkSubWindowMaximizeBtnHoverBgColor(self,color):
        self.mdi_area.subw_maximize_btn_hover=color.name()
        self.mdi_area.applyStyle()


    def linkSubWindowBtnsRadius(self,size):
        self.mdi_area.subw_btns_radius=size
        self.mdi_area.applyStyle()

    def linkSubWindowTitlebarHeight(self,size):
        self.mdi_area.ttlbr_hsize=size
        self.mdi_area.applyStyle()

        
    def linkSubWindowTitleFontSize(self,size):
        self.mdi_area.ttlbr_title_font=size
        self.mdi_area.applyStyle()

    def linkSubWindowTitlebarButtonSize(self,size):
        self.mdi_area.ttlbr_btns_size=size
        self.mdi_area.applyStyle()

    def linkSubWindowBorderHover(self,color):
        self.mdi_area.subw_ttlbr_hover=color.name()
        
    #minimap

    def linkMiniMapBgColor(self,color):
        self.mini_map.minimap_bg=color.name()
        self.mini_map.applyMiniMapStyle()
        
    def linkMiniMapViewPortAlfa(self,alfa):
        self.mini_map.vp_rgba[3]=int(alfa)
        self.mini_map.applyViewPortStyle()
    
    def linkMiniMapViewPortColor(self,color):
        #self.textedit_mini_map.minimap_bg=color.name()
        self.mini_map.vp_rgba[0]=color.red()
        self.mini_map.vp_rgba[1]=color.green()
        self.mini_map.vp_rgba[2]=color.blue()
        
        self.mini_map.applyViewPortStyle()
    
    def linkMiniMapVieywPortBorderAlfa(self,alfa):
        self.mini_map.vp_brdr_rgba[3]=int(alfa)
        self.mini_map.applyViewPortBorderStyle()
    
    def linkMiniMapViewPortBorderColor(self,color):
        #self.textedit_mini_map.minimap_bg=color.name()
        self.mini_map.vp_brdr_rgba[0]=color.red()
        self.mini_map.vp_brdr_rgba[1]=color.green()
        self.mini_map.vp_brdr_rgba[2]=color.blue()
        
        self.mini_map.applyViewPortBorderStyle()


    def linkMiniMapViewPortBorderHover(self,color):
        self.mini_map.vp_brdr_hover_rgba[0]=color.red()
        self.mini_map.vp_brdr_hover_rgba[1]=color.green()
        self.mini_map.vp_brdr_hover_rgba[2]=color.blue()
        self.mini_map.applyViewPortBorderStyle()

    
    def linkMiniMapViewPortBorderHoverAlfa(self,alfa):
        self.mini_map.vp_brdr_hover_rgba[3]=int(alfa)
        self.mini_map.applyViewPortBorderStyle()
    

    def linkMiniMapViewPortBorderWidth(self,w):
        self.mini_map.brdr_width=int(w)

    #tabbar

    def linkTabbarBgColor(self,color):
        self.tabbar_editor.bg_clr=color.name()
        self.tabbar_editor.applyStyle()
        self.frame_tabbar.bg_clr=color.name()
        self.frame_tabbar.applyStyle()
        
    def linkTabbarBrdrColor(self,color):pass
        
    def linkTabBtnBgColor(self,color):
        self.tabbar_editor.tab_clr=color.name()
        self.tabbar_editor.applyStyle()
    
    def linkTabBtnBrdrColor(self,color):
        self.tabbar_editor.tab_brdr=color.name()
        self.tabbar_editor.applyStyle()
    

    def linkTabbarHSize(self,size):
        self.tabbar_editor.tab_padding_rl=size+2
        self.tabbar_editor.tab_padding_tb=size
        self.tabbar_editor.tab_h=size
        self.tabbar_editor.applyStyle()
    
    def linkTabbarFrameHSize(self,size):
        self.tabbar_editor.tabbar_h=size
        self.tabbar_editor.setFixedHeight(size)
        self.frame_tabbar.setFixedHeight(size)

    def linkTabBtnRadius(self,size):
        self.tabbar_editor.tab_radius=size
        
        self.tabbar_editor.applyStyle()
        
    def linkTabBtnHoverColor(self,color):
        self.tabbar_editor.tab_hover_clr=color.name()
        self.tabbar_editor.applyStyle()
    
    def linkTabBtnSelectedColor(self,color):
        self.tabbar_editor.tab_selected_clr=color.name()
        self.tabbar_editor.applyStyle()

    def linkTabBtnNonWorkingFontColor(self,color):
        self.tabbar_editor.font_clr=color.name()
        self.tabbar_editor.applyStyle()

    def linkTabBtnWorkingBrdrColor(self,color):
        self.tabbar_editor.brdr[0]=color.name()
        self.tabbar_editor.applyStyle()
    
    def linkTabBtnWorkingFontColor(self,color):
        self.tabbar_editor.selected_font_clr=color.name()
        self.tabbar_editor.applyStyle()
    
    def linkTabBtnNonWorkingBrdrColor(self,color):
        self.tabbar_editor.brdr[1]=color.name()
        self.tabbar_editor.applyStyle()
    
    #completer
    def showCompleterForCustomize(self):
        if not self.running_textedit_editor.completer.popup().isVisible():
            print("show")
            self.running_textedit_editor.completer.popup().show()
            #self.running_textedit_editor.completer.popup().

    def linkCompleterBgColor(self,color):
        self.style_completer.bg_clr=color.name()
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()
            #self.running_textedit_editor.completer.popup().setFocus(no)
    def linkCompleterBrdrColor(self,color):
        self.style_completer.brdr_clr=color.name()
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()

    def linkCompleterTextColor(self,color):
        self.style_completer.text_clr=color.name()
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()

    def linkCompleterSelecteItemColor(self,color):
        self.style_completer.selecte_item_clr=color.name()
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()
    
    def linkCompleterSelecteItemTextColor(self,color):
        self.style_completer.selecte_text_clr=color.name()
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()
    
    def linkCompleterBrdrThinkness(self,size):
        self.style_completer.brdr_think=size
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()

    
    def linkCompleterFontSize(self,size):
        self.style_completer.font_size=size
        self.style_completer.applyStyle(self.running_textedit_editor)
        self.showCompleterForCustomize()

    
    #code themes
    def setSyntaxThemeAndSet(self,highlighters,colors):
        if highlighters!=None:
            for highlighter in highlighters:
                print("aplyy")
                highlighter.colors=colors
                highlighter.setColors()
                highlighter.rehighlight()

    def updateEditorSyntaxTheme(self,highlighters:list[object]=None,key_name=None,color=None):
        print(key_name)

        if highlighters!=None:
            for highlighter in highlighters:
                highlighter.colors[key_name]=color.name()
                highlighter.setColors()
                highlighter.rehighlight()
    
    def updateMinimapSyntaxTheme(self,handler,h_ext,key_name,color):
        print(h_ext,handler.current_minimap_type)
        if handler.current_minimap_highlighter and handler.current_minimap_type==h_ext:
            handler.current_minimap_highlighter.colors[key_name]=color.name()
            handler.current_minimap_highlighter.setColors()
            handler.current_minimap_highlighter.rehighlight()

    def updateOtherSyntaxTheme(self,highlighter=None,key_name=None,color=None):

        if highlighter!=None:
            highlighter.colors[key_name]=color.name()
            highlighter.setColors()
            highlighter.rehighlight()



"""        
    def linkCodeThemeOther(self,key_name=None,color=None,o_highlighter=None):
        with open(self.Path_h.Code.CUSTOM_COLOR_THEME, "r") as file:
            var_dict = file.read()
            var_dict = eval(var_dict.splitlines()[0])

            if key_name!=None:
                var_dict[key_name]=color.name()

                
            self.highlighter[len(self.highlighter)-1].colors=var_dict
            self.highlighter[len(self.highlighter)-1].setColors()
            self.highlighter[len(self.highlighter)-1].rehighlight()
            self.mini_map_highlighter.colors=var_dict
            self.mini_map_highlighter.setColors()
            self.mini_map_highlighter.rehighlight()
            file.close()
            
            if o_highlighter!=None:
                o_highlighter.colors=var_dict
                o_highlighter.setColors()
                o_highlighter.rehighlight()
            
        with open(self.Path_h.Code.CUSTOM_COLOR_THEME, "w") as file:
            file.write(f"{self.highlighter[len(self.highlighter)-1].colors}")        
            file.close()"""
            #self.
    #def linkCodeThemeKeyword(self):...
    