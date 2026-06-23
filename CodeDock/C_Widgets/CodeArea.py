
from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.C_Widgets.Custom import Custom
from CodeDock.src.controllers.PathHandler import Path_Handler
import dataclasses    
import typing
import enum
import math
import abc
#s-dsetee
@dataclasses.dataclass
class RectDT:
    x:int=0
    y:int=0
    #w:int=0
    #h:int=0
                
@dataclasses.dataclass
class CornerDT:
    left:QtCore.QPoint
    right:QtCore.QPoint

@dataclasses.dataclass
class SubWindowSmartSnapGeo:
    top:CornerDT
    bottom:CornerDT
    #ee




class RectangleOverlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setGeometry(parent.rect())
        self.rect_to_draw = None
        self.rect_color=None

    def draw_rectangle(self, x, y, w, h,color=QtGui.QColor(255, 255, 255,150)):
        self.rect_to_draw = QtCore.QRect(x, y, w-2, h-2)
        self.rect_color=color
        self.update()
        
    def remove_rectangle(self):

        self.rect_to_draw = None
        self.update()

    def paintEvent(self, event):
        if not self.rect_to_draw:
            return
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pen = QtGui.QPen(self.rect_color, 3)
        brush=QtGui.QBrush(QtGui.QColor(70,90,90,90))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(self.rect_to_draw)

        
class ProjectDesktop:
    def __init__(self,parent):
        self.project_list=[None]
        self.connect_desk_projects=None
        self.parent_mdi=parent
        self.widget_list=[]
        
        self.total_row=0
        self.total_column=0
        self.current_row=0
        self.current_column=0
        
    def refreshProjectDesk(self):
        for index,project_dt in enumerate(self.project_list):
            project_desk=Custom.RefreshProjectDesk(index,project_dt,self.parent_mdi,self)
            project_desk.setParent(self.parent_ )
            project_desk.connect_desk_projects=self.connect_desk_projects
    
class RefreshProjectDesk(QtWidgets.QWidget):
    
    def __init__(self,index,project_dt,parent=None,manager=None):
        super().__init__(parent)
        self.GRID_SIZE=100
        self.SPACING=50
        
        self.index=index
        self.manager=manager
        self.project_dt=project_dt
        self.connect_desk_projects=None
        self.last_pos=[]
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)  # Space between icon and text

        # Icon part
        self.icon_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self.project_dt[1])
        self.icon_label.setPixmap(pixmap.scaled(64,64,QtCore.Qt.AspectRatioMode.KeepAspectRatio,QtCore.Qt.TransformationMode.SmoothTransformation))
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Text part
        self.text_label= QtWidgets.QLabel(self.project_dt[0])
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("font-size: 12px;")

        # Add to layout
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

        # Optional: Set fixed size
        self.setFixedSize(100,100)
        self._drag_pos = None

        if self.index==0:
            self.move(self.SPACING,self.SPACING)
            self.manager.widget_list.append(self)
        else:
            x,y=self.setProjectIcons()
            self.move(x,y)
            #

    def setProjectIcons(self):

        self.parent=self.parentWidget()
        #def updateTotalRowColumn():
        self.manager.total_column=self.parent.width()//self.GRID_SIZE
        self.manager.total_row=self.parent.height()//self.GRID_SIZE


        #updateTotalRowColumn()  
          
            
        last_widget=self.manager.widget_list[len(self.manager.widget_list)-1]
        
        x,y=self.manager.current_column*self.GRID_SIZE,self.manager.current_row*self.GRID_SIZE

        if self.parent.y()<y:
            self.manager.current_column+=1

        self.manager.current_row=len(self.manager.widget_list)

        return x,y

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_pos = event.position().toPoint()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self._drag_pos:
            self.new_pos=self.mapToParent(event.position().toPoint()-self._drag_pos)
            self.move(self.new_pos)
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, e):
        

        try:
            snapped_x=round(self.new_pos.x()/self.GRID_SIZE)*self.GRID_SIZE
            snapped_y=round(self.new_pos.y()/self.GRID_SIZE)*self.GRID_SIZE
            parent_w=self.parentWidget()
            #print(snapped_x,">","0","\n",snapped_y,">","0","\n",snapped_y,"<",parent_w.height(),"\n",snapped_x,"<",parent_w.width())

            if snapped_x>-150 and snapped_y>-150 and snapped_y<parent_w.height()+150 and snapped_x<parent_w.width()+150:
                self.last_pos=[snapped_x,snapped_y]
                self.manager.widget_list.append([snapped_x,snapped_y])
                self.move(snapped_x, snapped_y)    
            

                for i,widget_pos in enumerate(self.manager.widget_list):
                    if widget_pos==[snapped_x,snapped_y]:
                        self.move(*self.last_pos)

            else:self.move(*self.last_pos)



        except:pass
        
        return super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, a0):
        
        #for index,project_list in enumerate(self.project_list):
        #    if self.text_label.text()==project_list[0]:
        self.connect_desk_projects(self.project_dt[2])            
        return super().mouseDoubleClickEvent(a0)
    
    
#class SubWindowTD(typing.TypedDict):MDISubWindow:'MDISubWindow'
@dataclasses.dataclass
class SubWindowStates:
    subwindow_obj:'MDISubWindow'
    is_activated:bool
    index:int
    
class MDIArea(QtWidgets.QWidget):
    
    whenWindowActivated=QtCore.pyqtSignal(object)
    whenWindowClose=QtCore.pyqtSignal(object)
    whenWindowMaximized=QtCore.pyqtSignal(object)

    whenAreaResize=QtCore.pyqtSignal()

    whenKey_Ctrl_Tab_Pressed=QtCore.pyqtSignal()
    whenKey_Ctrl_Shift_Tab_Pressed=QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.subwindow_buffer:list[MDISubWindow]=[]
        
        self.subwindow_states:dict[MDISubWindow,SubWindowStates]={}
        
        self.total_minimized_subwindow:int=0
        #key subwindow addr
        self.subwin_smart_snap_geo_buffer:dict[SubWindowSmartSnapGeo]={}
        self.corner_rect:CornerDT=CornerDT(left=RectDT(),right=RectDT)
        self.snap_index=0
        
        self.top_left_buffer=[]
        self.top_right_buffer=[]
        self.bottom_left_buffer=[]
        self.bottom_right_buffer=[]
        
        self.empty_space_buffer={}

        self.activated_subwindow:MDISubWindow=None
        self.organize_flag=False
        self.mdi_bg_clr=None
        
        #self.mdi_radius=[0,0]
        self.mdi_brdr_clr="none"
        self.mdi_brdr_think=0
        self.subw_bg_clr="black"
        self.subw_brdr_clr="red"
        self.subw_radius=[0,0]

        self.subw_brdr_think=2
        self.subw_active_brdr_clr="none"
        #titlebar(subwindow)
        self.subw_ttlbr_bg_clr="none"
        self.subw_activated_ttlbr_clr="none"
        self.subw_ttlbr_text_clr="none"
        self.subw_close_btn_clr="none"
        self.subw_maximize_btn_clr="none"
        self.subw_btns_radius=0
        
        self.subw_ttlbr_hover="none"
        self.subw_maximize_btn_hover="none"
        self.subw_close_btn_hover="none"

        
        self.ttlbr_hsize=32
        self.ttlbr_btns_size=24
        self.ttlbr_title_font=12
        
    
        self.setAcceptDrops(True)
        self.connect_alt_key=None
        self.rectangle_overly=RectangleOverlay(self)

        self.Path_h:Path_Handler
        
    def setPathHandler(self,Path_h:Path_Handler):
        self.Path_h=Path_h

    def calculateEmptySpaceInMdi(self):
        
        mdi_geo=self.geometry()
        print("mdi geo",mdi_geo)

        for subwindow in self.subwindow_buffer:
            if subwindow.isVisible():

                swin_geo=subwindow.geometry()

                print("swindow geo ",subwindow.windowTitle(),swin_geo)

    def resizeEvent(self, a0):
        #self.calculateEmptySpaceInMdi()
        self.rectangle_overly.setGeometry(self.geometry())
        if self.activated_subwindow!=None:
            if self.activated_subwindow.isMaximized():
                self.activated_subwindow.showMaximized()
        return super().resizeEvent(a0)
    
    def tileSubWindows(self):
        self.organize_flag=True
        count = abs(len(self.subwindow_buffer)-self.total_minimized_subwindow)
        
        print("for tile : ",count,"  total : ",len(self.subwindow_buffer)," hidden : ",self.total_minimized_subwindow)
        if count == 0:
            return

        parent_width = self.width()
        parent_height = self.height()
        print("p h:",parent_height)
        print("p w:",parent_width)
        
        # Column-wise layout: determine optimal number of rows
        rows = math.ceil(math.sqrt(count))
        cols = math.ceil(count / rows)

        tile_width = parent_width // cols

        index=0
        hidden=0

        for index, widget in enumerate(self.subwindow_buffer):
            if widget.isHidden():
                hidden+=1        
                continue
            if widget.isVisible():
                
                index=abs(index-hidden)

                col = index // rows
                row_in_col = index % rows

                # Widgets in this column
                if col == cols - 1:
                    # Last column might have fewer items
                    widgets_in_column = count - (cols - 1) * rows
                else:
                    widgets_in_column = rows

                tile_height = parent_height // widgets_in_column

                x = col * tile_width
                y = row_in_col * tile_height

                widget.setGeometry(QtCore.QRect(x+2, y+2, tile_width-4, tile_height-4))
                print(widget.windowTitle()," geo : ",QtCore.QRect(x+2, y+2, tile_width-4, tile_height-4))

    def getVarDict(self):
        return {'mdi_bg_clr':self.mdi_bg_clr,
                'mdi_brdr_clr':self.mdi_brdr_clr,
                'mdi_brdr_think':self.mdi_brdr_think,
                'subw_bg_clr':self.subw_bg_clr,
                'subw_brdr_clr':self.subw_brdr_clr,
                'subw_radius':self.subw_radius,
                'subw_brdr_think':self.subw_brdr_think,
                'subw_active_brdr_clr':self.subw_active_brdr_clr,
                'subw_ttlbr_bg_clr':self.subw_ttlbr_bg_clr,
                'subw_activated_ttlbr_clr':self.subw_activated_ttlbr_clr,
                'subw_ttlbr_text_clr':self.subw_ttlbr_text_clr,
                'subw_close_btn_clr':self.subw_close_btn_clr,
                'subw_maximize_btn_clr':self.subw_maximize_btn_clr,
                'subw_btns_radius':self.subw_btns_radius,
                'subw_maximize_btn_hover':self.subw_maximize_btn_hover,
                'subw_close_btn_hover':self.subw_close_btn_hover,
                "ttlbr_size":self.ttlbr_hsize,
                "ttlbr_btns_size":self.ttlbr_btns_size,
                "ttlbr_title_font":self.ttlbr_title_font,
                "subw_ttlbr_hover":self.subw_ttlbr_hover,
                }
    
    def updateVar(self,MDIArea,dict):
        MDIArea.mdi_bg_clr=dict["mdi_bg_clr"]
        MDIArea.mdi_brdr_clr=dict["mdi_brdr_clr"]
        MDIArea.mdi_brdr_think=dict["mdi_brdr_think"]
        MDIArea.subw_bg_clr=dict["subw_bg_clr"]
        MDIArea.subw_brdr_clr=dict["subw_brdr_clr"]
        MDIArea.subw_radius=dict["subw_radius"]
        MDIArea.subw_brdr_think=dict["subw_brdr_think"]
        MDIArea.subw_active_brdr_clr=dict["subw_active_brdr_clr"]
        MDIArea.subw_ttlbr_bg_clr=dict["subw_ttlbr_bg_clr"]
        MDIArea.subw_activated_ttlbr_clr=dict["subw_activated_ttlbr_clr"]
        MDIArea.subw_ttlbr_text_clr=dict["subw_ttlbr_text_clr"]
        MDIArea.subw_close_btn_clr=dict["subw_close_btn_clr"]
        MDIArea.subw_maximize_btn_clr=dict["subw_maximize_btn_clr"]
        MDIArea.subw_btns_radius=dict["subw_btns_radius"]
        MDIArea.subw_maximize_btn_hover=dict["subw_maximize_btn_hover"]
        MDIArea.subw_close_btn_hover=dict["subw_close_btn_hover"]
        MDIArea.ttlbr_size=dict["ttlbr_size"]
        MDIArea.ttlbr_btns_size=dict["ttlbr_btns_size"]
        MDIArea.ttlbr_title_font=dict["ttlbr_title_font"]
        MDIArea.subw_ttlbr_hover=dict["subw_ttlbr_hover"]

    #change third class code
    def subwindowHover(self,hover_flag,subwindow:'MDISubWindow'):

        if hover_flag==True:
            
            subwindow.border_hover=True
            subwindow.setBorder("left",True)
            subwindow.setBorder("right",True)
            subwindow.setBorder("top",True)
            subwindow.setBorder("bottom",True)
            subwindow.update()

    def applyStyle(self):
        self.setStyleSheet(f"""
                        MDIArea {{
                        background:{self.mdi_bg_clr};
                        border:{self.mdi_brdr_think}px solid {self.mdi_brdr_clr};
                            
                        }}   
        """)

        #self.setWindowActivateStyle(self.activated_subwindow)

    def setSubWindowStyle(self,subwindow:'MDISubWindow'):
        
        subwindow.main_layout.setContentsMargins(
            int(self.subw_brdr_think),
            int(self.subw_brdr_think),
            int(self.subw_brdr_think),
            int(self.subw_brdr_think))

        l_font=QtGui.QFont()
        l_font.setPointSize(self.ttlbr_title_font)
        l_font.setItalic(True)

        #l_font.setBold(True)
        subwindow.titlebar.title_label.setFont(l_font)
        subwindow.titlebar.title_label.setStyleSheet(f"color:{self.subw_ttlbr_text_clr};")
        subwindow.titlebar.setFixedHeight(self.ttlbr_hsize)
        subwindow.titlebar.block_path_navigation_bar.setFixedHeight(self.ttlbr_hsize)
        subwindow.titlebar.block_path_navigation_bar.setBtnFontSize(self.ttlbr_title_font)
        subwindow.titlebar.block_path_navigation_bar.setBtnIconSize(self.ttlbr_title_font)

        
        
        subwindow.titlebar.close_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
        subwindow.titlebar.close_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
        subwindow.titlebar.maximize_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
        subwindow.titlebar.maximize_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
        subwindow.titlebar.minimize_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
        subwindow.titlebar.minimize_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
        subwindow.titlebar.icon_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
        subwindow.titlebar.icon_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
        
        subwindow.titlebar.close_button.setStyleSheet(f"""
            QPushButton{{
                background-color:{self.subw_close_btn_clr};
                border-radius:{self.subw_btns_radius}px;
            }}
            QPushButton:hover{{
                background-color:{self.subw_close_btn_hover};
            }}

        """)

        subwindow.titlebar.minimize_button.setStyleSheet(f"""
            QPushButton{{
                background-color:{self.subw_maximize_btn_clr};
                border-radius:{self.subw_btns_radius}px;
            }}
            QPushButton:hover{{
                background-color:{self.subw_maximize_btn_hover};
            }}

        """)

        subwindow.titlebar.maximize_button.setStyleSheet(f"""
            QPushButton{{
                background-color:{self.subw_maximize_btn_clr};
                border-radius:{self.subw_btns_radius}px;
            }}
            QPushButton:hover{{
                background-color:{self.subw_maximize_btn_hover};
            }}

        """)


    
        subwindow.setStyleSheet(f"""
                    MDISubWindow {{         
                    background-color:{self.subw_bg_clr};
                    border:{self.subw_brdr_think}px solid {self.subw_brdr_clr};
                    border-bottom-left-radius:{self.subw_radius[1]}px;
                    border-bottom-right-radius:{self.subw_radius[1]}px;
                    }}
                """)
        
        subwindow.titlebar.setStyleSheet(f"""
                    background-color:{self.subw_ttlbr_bg_clr};
                    border-top-left-radius: {self.subw_radius[0]}px;
                    border-top-right-radius: {self.subw_radius[0]}px;
                """)



    def setWindowDeActivateStyle(self,subwindow):
        #set deactve theme
 
        subwindow.setStyleSheet(f"""
            MDISubWindow {{         
            background-color:{self.subw_bg_clr};
            border:{self.subw_brdr_think}px solid {self.subw_brdr_clr};
            border-bottom-left-radius:{self.subw_radius[1]}px;
            border-bottom-right-radius:{self.subw_radius[1]}px;
            }}
        """)

        subwindow.titlebar.setStyleSheet(f"""
            background-color:{self.subw_ttlbr_bg_clr};
            border-top-left-radius: {self.subw_radius[0]}px;
            border-top-right-radius: {self.subw_radius[0]}px;
        """)

    def setWindowActivateStyle(self,subwindow):
        subwindow.setStyleSheet(f"""
            MDISubWindow {{
            background-color:{self.subw_bg_clr};
                                
            border:{self.subw_brdr_think}px solid {self.subw_active_brdr_clr};
            border-bottom-left-radius:{self.subw_radius[1]}px;
            border-bottom-right-radius:{self.subw_radius[1]}px;
                                
            }}
        """)
        subwindow.titlebar.setStyleSheet(f"""
            background-color:{self.subw_activated_ttlbr_clr};
            border-top-left-radius: {self.subw_radius[0]}px;
            border-top-right-radius: {self.subw_radius[0]}px;

        """)
    
    def setWindowActivate(self,subwindow):
        print(subwindow.windowTitle()," active by mdi-area")
        subwindow.raise_()
        #self.subwin_states[subwindow].is_activated
        if self.activated_subwindow!=subwindow:
            self.whenWindowActivated.emit(subwindow)
            
            if self.activated_subwindow!=None:   
                print(self.activated_subwindow.windowTitle(),"actvated subinwjiajdfkh ") 
                self.subwindow_states[self.activated_subwindow].is_activated=False
                self.subwindow_states[subwindow].is_activated=True
                self.setWindowDeActivateStyle(self.activated_subwindow)

            else:
                self.subwindow_states[subwindow].is_activated=True
                
            self.setWindowActivateStyle(subwindow)
            self.activated_subwindow=subwindow

    def setWindowRaise(self):
        self.activated_subwindow.raise_()

        """
        for i,subwin in enumerate(self.subwindow_states):
            if subwin[1]==True:
                subwin[0].raise_()
            else:

                subwin[0].lower()
        """
    
    def closeSubWindow(self,subwindow):
        self.subwindow_states.pop(subwindow)
        #self.subwin_smart_snap_geo_buffer.pop(subwindow)
        self.activated_subwindow=None

        if not subwindow.isVisible():
            self.total_minimized_subwindow-=1            
        subwindow.close()
        subwindow.deleteLater()
    


    def subWindowList(self):
        return self.subwindow_buffer
    
    def windowTitle(self,subwindow):
        return subwindow.titlebar.title_label.text()
        

    def overlaySmartSnap(self,subwindow:'MDISubWindow',mouse_pos:QtCore.QPoint=None,reset:bool=False):


        mgeo = self.geometry()

        # Buffers for all candidate snapping lines
        top_buffer: list[CornerDT] = []
        bottom_buffer: list[CornerDT] = []
        left_buffer: list[CornerDT] = []
        right_buffer: list[CornerDT] = []

        # Collect all candidates from other subwindows
        for subwin in self.subwindow_buffer:
            if subwin == subwindow:
                continue

            snap_geo: SubWindowSmartSnapGeo = self.subwin_smart_snap_geo_buffer[subwin]

            # candidates for top/bottom snapping
            top_buffer.append(snap_geo.top)       # top edge
            bottom_buffer.append(snap_geo.bottom) # bottom edge

            # candidates for left/right snapping
            left_buffer.append(snap_geo.top)      # use top corners for x
            right_buffer.append(snap_geo.bottom)  # use bottom corners for x

        # --- Pick the nearest valid snap candidates ---
        final_top = max(
            (c for c in bottom_buffer if mouse_pos.y() > c.left.y()),
            key=lambda c: c.left.y(),
            default=None
        )

        final_bottom = min(
            (c for c in top_buffer if mouse_pos.y() < c.left.y()),
            key=lambda c: c.left.y(),
            default=None
        )

        final_left = max(
            (c for c in left_buffer if mouse_pos.x() > c.right.x()),
            key=lambda c: c.right.x(),
            default=None
        )

        final_right = min(
            (c for c in right_buffer if mouse_pos.x() < c.left.x()),
            key=lambda c: c.left.x(),
            default=None
        )

        # --- Build overlay origin ---
        overlay_origin = QtCore.QPoint()
        if final_top and final_left:
            overlay_origin = QtCore.QPoint(final_left.right.x(), final_top.left.y())
        elif final_top:
            overlay_origin = final_top.left
        elif final_left:
            overlay_origin = final_left.right
        else:
            overlay_origin = QtCore.QPoint(0, 0)

        # --- Build overlay size ---
        overlay_size = QtCore.QSize()
        if final_bottom and final_right:
            overlay_size = QtCore.QSize(
                final_right.left.x() - overlay_origin.x(),
                final_bottom.left.y() - overlay_origin.y()
            )
        elif final_bottom:
            overlay_size = QtCore.QSize(
                mgeo.width() - overlay_origin.x(),
                final_bottom.left.y() - overlay_origin.y()
            )
        elif final_right:
            overlay_size = QtCore.QSize(
                final_right.left.x() - overlay_origin.x(),
                mgeo.height() - overlay_origin.y()
            )
        else:
            overlay_size = QtCore.QSize(
                mgeo.width() - overlay_origin.x(),
                mgeo.height() - overlay_origin.y()
            )

        # --- Debug output ---
        print("Final Snap Lines:")
        print("Top:", final_top)
        print("Bottom:", final_bottom)
        print("Left:", final_left)
        print("Right:", final_right)
        print("Overlay:", overlay_origin.x(), overlay_origin.y(),
            overlay_size.width(), overlay_size.height())
        print("-----------------------------------------------------")

        # --- Draw overlay ---
        self.rectangle_overly.remove_rectangle()
        self.rectangle_overly.draw_rectangle(
            overlay_origin.x(),
            overlay_origin.y(),
            overlay_size.width(),
            overlay_size.height()
        )
        self.raise_()

        """mgeo=self.geometry()
        
        top_buffer:list[CornerDT]=[]
        bottom_buffer:list[CornerDT]=[]
        left_buffer:list[CornerDT]=[]
        right_buffer:list[CornerDT]=[]
        
        
        final_top:CornerDT=None
        final_bottom:CornerDT=None
        final_left:CornerDT=None
        final_right:CornerDT=None

        for index,subwin in enumerate(self.subwindow_buffer):
            
            snap_geo:SubWindowSmartSnapGeo=self.subwin_smart_snap_geo_buffer[subwin]
            
            top=snap_geo.top
            bottom=snap_geo.bottom

            if subwin==subwindow:
                print(subwin.windowTitle(),"is skiped.......")
                continue
            
            #top
            
            top_buffer.append(top)
            bottom_buffer.append(bottom)
            
            print(".............ON Top............")
            if mouse_pos.y() > bottom.left.y():
                
                if final_top!=None:

                    if final_top.left.y() < bottom.left.y():
                        final_top=bottom
                                        
                else:
                    final_top=bottom


                if final_right and final_top:
                        
                    if final_top.left.x()>final_right.left.x():
                        print("final_top : None")
                        final_top=None


                if final_right and  final_top:
                    if final_top.left.y()>final_right.left.y():
                        print("final_right : None")
                        final_right=None
                
                if final_left and final_top:

                    if final_top.left.x()<final_left.right.x():
                        print("final_top : None")
                        final_top=None

                if final_left and final_top:
                    if final_top.left.y()<final_left.right.y():
                        print("final_left : None")
                        final_left=None
                
            
            #bottom
            print(".............ON Bottom............")
            
            if mouse_pos.y() < top.left.y():

                if final_bottom!=None:
                    if final_bottom.left.y() > top.left.y():
                        final_bottom=top
                else:
                    final_bottom=top
                
                if final_left and final_bottom:

                    if final_bottom.right.x()<final_left.right.x():
                        print("final_bttom : None")
                        
                        final_bottom=None


                if final_right and final_bottom:
                    if final_bottom.right.x()>final_right.right.x():
                        print("final_right : None")
                        final_right=None

            

            #left
            print(".............ON Left............")
            
            if mouse_pos.x() > top.right.x():
                
                if final_left!=None:
                    if final_left.left.x() < top.left.x():
                        final_left=top


                else:
                    final_left=top
            
                if final_top:

                    if final_top.left.x()<final_left.right.x():
                        print("final_top : None")
                        final_top=None

                if final_top and final_left:
                    if final_top.left.y()<final_left.right.y():
                        print("final_left : None")
                        final_left=None
                
                if final_bottom and final_left:

                    if final_bottom.right.x()<final_left.right.x():
                        print("final_bttom : None")
                        
                        final_bottom=None

            
            #right
            print(".............ON Right............")

            if mouse_pos.x() < bottom.left.x():
                if final_right!=None:
                    if final_right.right.x() > bottom.right.x():
                        final_right=bottom
                    
                else:
                    final_right=bottom

                if final_top:
                        
                    if final_top.left.x()>final_right.left.x():
                        print("final_top : None")
                        final_top=None


                if final_top:
                    if final_top.left.y()>final_right.left.y():
                        print("final_right : None")
                        final_right=None
                            
                if final_bottom and final_right:
                    if final_bottom.right.x()>final_right.right.x():
                        print("final_bottom : None")
                        final_right=None






        #final_top = max(top_buffer, key=lambda c: c.left.y(), default=None)
        #final_bottom = min(bottom_buffer, key=lambda c: c.left.y(), default=None)
        #final_left = max(left_buffer, key=lambda c: c.right.x(), default=None)
        #final_right = min(right_buffer, key=lambda c: c.left.x(), default=None)
        #print(final_bottom,final_left,"khskdhwukfgieuw uiqh iuqegfuilg")

        overlay_origin=QtCore.QPoint()s
        overlay_size=QtCore.QSize()

        print(final_top)
        print(final_bottom)
        print(final_left)
        print(final_right)
        print("-----------------------------------------------------")
        
        if final_top and final_left:
            
            if final_top.left.x() < final_left.right.x():
                overlay_origin.setX(final_left.right.x())
                print("set X: final_left.right : ",final_left.right.x())
            else:
                overlay_origin.setX(final_top.left.x())
                print("e set X: final_top.left : ",final_top.left.x())
        
            if final_top.left.y() < final_left.right.y():
                overlay_origin.setY(final_left.right.y())
                print("set Y: final_left.right : ",final_left.right.y())

            else:
                overlay_origin.setY(final_top.left.y())
                print("e set Y: final_top.left : ",final_top.left.y())
        
        elif final_top:
            overlay_origin.setX(final_top.left.x())
            overlay_origin.setY(final_top.left.y())
            print("None set XY: final_top.left : ",final_top)

        elif final_left:

            overlay_origin.setX(final_left.right.x())
            overlay_origin.setY(final_left.right.y())
            print("None set XY: final_left.right : ",final_left)


        if final_bottom and final_right:
            if final_bottom.right.x() > final_right.left.x():
                overlay_size.setWidth(final_right.left.x()-overlay_origin.x())
                print("set Width: final_right.left X - origin X: ",final_right.left.x()-overlay_origin.x())

            else:
                overlay_size.setWidth(final_bottom.right.x()-overlay_origin.x())
                print("E set Width: final_bottom.right X - origin X: ",final_bottom.right.x()-overlay_origin.x())

            if final_bottom.right.y() > final_right.left.y():
                overlay_size.setHeight(final_right.left.y()-overlay_origin.y())
                print("set Height: final_right.left Y - origin Y: ",final_right.left.y()-overlay_origin.y())

            else:
                overlay_size.setHeight(final_bottom.right.y()-overlay_origin.y())
                print("E set Height: final_bottom.right Y - origin Y: ",final_bottom.right.y()-overlay_origin.y())

        elif final_bottom:
            overlay_size.setWidth(final_bottom.right.x()-overlay_origin.x())
            overlay_size.setHeight(final_bottom.right.y()-overlay_origin.y())
            print("None set XY: final_bottom.right - origin.XY: ",final_bottom.right.x()-overlay_origin.x(), final_bottom.right.y()-overlay_origin.y())

        elif final_right:
            overlay_size.setWidth(final_right.left.x()-overlay_origin.x())
            overlay_size.setHeight(final_right.left.y()-overlay_origin.y())
            print("None set XY: final_right.left - origin.XY: ",final_right.left.x()-overlay_origin.x(),final_right.left.y()-overlay_origin.y())

        else:
            overlay_size.setWidth(self.rect().bottomRight().x()-overlay_origin.x())
            overlay_size.setHeight(self.rect().bottomRight().y()-overlay_origin.y())
            
        #print(self.subwin_smart_snap_geo_buffer)

        #test left origin
        self.rectangle_overly.remove_rectangle()
        
        
        print("final : ",overlay_origin.x(),overlay_origin.y(),overlay_size.width(),overlay_size.height())
        
        self.rectangle_overly.draw_rectangle(overlay_origin.x(),overlay_origin.y(),overlay_size.width(),overlay_size.height())
        self.raise_()
        """
            
        """top_left_X = 2
        top_left_Y = ssnap_geo.top.left.y()
        width      = ssnap_geo.bottom.left.x() - top_left_X-2
        height     = ssnap_geo.bottom.left.y() - top_left_Y-2

        top_left_X = ssnap_geo.bottom.left.x()
        top_left_Y = ssnap_geo.bottom.left.y()
        width      = ssnap_geo.bottom.right.x() - top_left_X
        height     = ssnap_geo.bottom.right.y() - top_left_Y

        top_left_X = ssnap_geo.top.right.x()
        top_left_Y = ssnap_geo.top.right.y()
        width      = top_left_X - ssnap_geo.bottom.left.x()
        height     = top_left_Y - ssnap_geo.bottom.left.y()
        """

        #print(self.subwindow_buffer[self.snap_index].setGeometry(top_left_X,top_left_Y,width,height))

        """
            origin_lx=2-ssnap_geo.top.left.x()
            origin_ly=2-ssnap_geo.top.left.y()

            top_rx=mgeo.width()-ssnap_geo.top.right.x()
            top_ry=mgeo.height()-ssnap_geo.top.right.y()
            


            top_rx=mgeo.width()-ssnap_geo.top.right.x()
            top_ry=mgeo.height()-ssnap_geo.top.right.y()
            
            """



    def updateSubWindowSmartSpanGeoBuffer(self,subwindow:"MDISubWindow"):
        
        subwindow_geo_list:SubWindowSmartSnapGeo=SubWindowSmartSnapGeo(top=CornerDT(QtCore.QPoint,QtCore.QPoint),bottom=CornerDT(QtCore.QPoint,QtCore.QPoint))


        sgeo=subwindow.geometry()
        mdi_geo=self.geometry()
        
        subwindow_geo_list.top.left=sgeo.topLeft()
        subwindow_geo_list.top.right=sgeo.topRight()
        subwindow_geo_list.bottom.left=sgeo.bottomLeft()
        subwindow_geo_list.bottom.right=sgeo.bottomRight()

        subwindow_geo_list.title=subwindow.windowTitle()
        self.subwin_smart_snap_geo_buffer[subwindow]=subwindow_geo_list
        
        
        
        #self.top_left_buffer.append(sgeo.topLeft())
        #self.top_right_buffer.append(sgeo.topRight())
        #self.bottom_left_buffer.append(sgeo.bottomLeft())
        #self.bottom_right_buffer.append(sgeo.bottomRight())

        #print(self.subwin_smart_snap_geo_bufferpr)
        print(sgeo.topLeft(),sgeo.topRight(),sgeo.bottomLeft(),sgeo.bottomRight())
        


    def addSubWindow(self,subwindow:'MDISubWindow'):
        subwindow.setParent(self)
        subwindow.parent=self
        self.subwindow_buffer.append(subwindow)
        self.subwindow_states[subwindow]=SubWindowStates(subwindow_obj=subwindow,is_activated=False,index=len(self.subwindow_buffer)-1)

        self.setSubWindowStyle(subwindow)
        self.setWindowActivate(subwindow)

    def linkDropUrls(self,link):
        self.link=link
    
    def dragEnterEvent(self,event:QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self,event:QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():  # Accept valid file URLs
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self,event:QtGui.QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path=url.toLocalFile()
                self.link(file_path)  # Open a subwindow with the file
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
    
    def keyPressEvent(self, event):
            
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key()==QtCore.Qt.Key.Key_Q:
            self.whenKey_Ctrl_Tab_Pressed.emit()
        if (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier and
            event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier and
            event.key() == QtCore.Qt.Key.Key_Q):
            self.whenKey_Ctrl_Shift_Tab_Pressed.emit()

 
        
        else:   
            super().keyPressEvent(event)




class MDISubWindow(QtWidgets.QWidget):
    whenResize=QtCore.pyqtSignal()
    whenMove=QtCore.pyqtSignal()

    class TitleBar(QtWidgets.QWidget):
        def __init__(self, parent:'MDISubWindow'):
            super().__init__(parent)
            self.parent_subwindow = parent
            
            self.dragging = False
            self.mouse_press_flag:bool=False
            self.offset = QtCore.QPoint()
            self.active_signal=None
            self.minimize_button_flag=False
            self.cusror_detect=False
            self.e_spacing=2
            
            self.last_pos=[]
            
            self.setFixedHeight(32)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

            self.setStyleSheet("""
                background-color:#3F3F3F;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            """)

            layout = QtWidgets.QHBoxLayout(self)
            layout.setContentsMargins(10, 0, 5, 0)

            self.icon_button=QtWidgets.QPushButton()
            self.icon_button.setFixedSize(24, 24)
            

            self.title_label = QtWidgets.QLabel("Untitled")
            self.title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
            
            self.block_path_navigation_bar=Custom.BlockPathNevigationBar()
            
            #self.block_path_navigation_bar.bg_clr="black"
            #self.block_path_navigation_bar.applyStyle()
            #self.block_path_navigation_bar.setFixedWidth(400)
            #layout.setSpacing(10)
            layout.addWidget(self.icon_button)
        
            layout.addWidget(self.title_label)
            layout.addSpacerItem(QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum))
            layout.addWidget(self.block_path_navigation_bar)
            layout.addStretch()

            
            self.close_button = QtWidgets.QPushButton()
            self.close_button.setIcon(QtGui.QIcon(parent.parent_mdi.Path_h.CLOSE_ICON))

            self.close_button.setFixedSize(24, 24)

            self.close_button.clicked.connect(self.sendCloseSignalToParent)

            self.maximize_button = QtWidgets.QPushButton()
            self.maximize_button.setIcon(QtGui.QIcon(self.parent_subwindow.parent_mdi.Path_h.MAXIMIZE_ICON))
            self.maximize_button.setFixedSize(24, 24)
            
            self.maximize_button.clicked.connect(self.maximizeButtonSignal)

            self.minimize_button = QtWidgets.QPushButton()
            self.minimize_button.setIcon(QtGui.QIcon(self.parent_subwindow.parent_mdi.Path_h.MINIMIZE_ICON))
            self.minimize_button.setFixedSize(24, 24)
            self.minimize_button.clicked.connect(self.parent_subwindow.minimizeIt)

            layout.addWidget(self.minimize_button)
            layout.addWidget(self.maximize_button)
            layout.addWidget(self.close_button)
            self.setContentsMargins(0,0,0,0)

    
            self.smooth_drag = True 
            self.smooth_factor = 0.3 
            self.target_pos = QtCore.QPoint(0, 0)
            self.e_spacing = 2  

            self.smooth_drage_timer= QtCore.QTimer()
            self.smooth_drage_timer.timeout.connect(self.updatePosition)

            self.smart_snap_debouncer=QtCore.QTimer()
            self.smart_snap_debouncer.setInterval(300)
            self.smart_snap_debouncer.setSingleShot(True)
            
            self.smart_snap_debouncer.timeout.connect(lambda:
                                                      self.parent_subwindow.parent.overlaySmartSnap(
                                                          self.parent_subwindow,
                                                          self.parent_subwindow.parent.mapFromGlobal(
                                                              QtGui.QCursor.pos()
                                                              )
                                                          ))

        def sendCloseSignalToParent(self):
            self.parent_subwindow.is_closing=True
            
            self.parent_subwindow.closeWindow()

        
        def maximizeButtonSignal(self):
            if self.minimize_button_flag==False:
                self.parent_subwindow.showMaximized()
                self.minimize_button_flag=True
            else:
                self.parent_subwindow.showNormal()
                self.minimize_button_flag=False


        def setSmoothDrag(self, enabled=True, smooth_factor=0.3):
            """Enable/disable smooth dragging
            
            Args:
                enabled (bool): True to enable smooth dragging, False to disable
                smooth_factor (float): Smoothness factor (0.1 = very smooth, 0.8 = less smooth)
            """
            self.smooth_drag = enabled
            self.smooth_factor = smooth_factor

        def mousePressEvent(self, event):
            self.parent_subwindow.parent_mdi.subwindowHover(True, self.parent_subwindow)
            
            self.parent_subwindow.raise_()
            
            self.parent_subwindow.parent_mdi.setWindowActivate(self.parent_subwindow)
            self.mouse_press_flag = True

            if self.parent_subwindow.isMaximized() == True:
                self.parent_subwindow.maximize_flag = True

            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.dragging = True
                self.offset = event.globalPosition().toPoint() - self.parent_subwindow.pos()
                # Store the target position for smooth movement
                self.target_pos = self.parent_subwindow.pos()
                
                # Only start timer if smooth dragging is enabled
                if self.smooth_drag and not self.smooth_drage_timer.isActive():
                    self.smooth_drage_timer.start(16)

        def mouseMoveEvent(self, event):
            if self.dragging:
                if self.smooth_drag:
                    # Store target position for smooth movement
                    self.target_pos = event.globalPosition().toPoint() - self.offset
                else:
                    # Direct movement without smoothing
                    pos = event.globalPosition().toPoint() - self.offset
                    self.move_window_directly(pos)

        def move_window_directly(self, pos):
            """Move window directly without smoothing (used when smooth_drag is False)"""
            self.parent_subwindow.maximize_flag = False   
            self.parent_subwindow.parent_mdi.subwindowHover(True, self.parent_subwindow)
            self.parent_subwindow.raise_()
            
            global_cur = QtGui.QCursor().pos()
            gx, gy = self.parent_subwindow.parent_mdi.mapFromGlobal(global_cur).x(), self.parent_subwindow.parent_mdi.mapFromGlobal(global_cur).y()

            if gx > 0 and gy > 0 and gx < self.parent_subwindow.parent_mdi.size().width() and gy < self.parent_subwindow.parent_mdi.size().height():
                self.parent_subwindow.move(pos)
                self.last_pos = [pos.x(), pos.y()]
                self.parent_subwindow.saveLastGeo(x=pos.x(), y=pos.y())

            # left
            elif gx < 0 and gy > 0 and gy < self.parent_subwindow.parent_mdi.size().height():
                self.parent_subwindow.move(self.last_pos[0], pos.y() + 1)
                self.last_pos = [self.last_pos[0], pos.y() + 1]
                self.parent_subwindow.saveLastGeo(x=pos.x(), y=pos.y() + 1)

            # right
            elif gy > 0 and gx > self.parent_subwindow.parent_mdi.size().width() and gy < self.parent_subwindow.parent_mdi.size().height():
                self.parent_subwindow.move(self.last_pos[0], pos.y() + 1)
                self.last_pos = [self.last_pos[0], pos.y() + 1]
                self.parent_subwindow.saveLastGeo(x=pos.x(), y=pos.y() + 1)
            
            # top
            elif gy < 0 and gx > 0 and gx < self.parent_subwindow.parent_mdi.size().width():
                self.parent_subwindow.move(pos.x() + 1, 0)
                self.last_pos = [pos.x() + 1, 0]
                self.parent_subwindow.saveLastGeo(x=pos.x() + 1, y=0)

            # bottom
            elif gx > 0 and gy > self.parent_subwindow.parent_mdi.size().height() and gx < self.parent_subwindow.parent_mdi.size().width():
                self.parent_subwindow.move(pos.x() + 1, self.last_pos[1])
                self.last_pos = [pos.x() + 1, self.last_pos[1]]
                self.parent_subwindow.saveLastGeo(x=pos.x() + 1, y=pos.y())

            # Update overlay
            self.update_overlay()

        def updatePosition(self):
            # Only run smooth movement if smooth_drag is enabled
            if not self.dragging or not self.smooth_drag:
                return
                
            self.parent_subwindow.maximize_flag = False   
            self.parent_subwindow.parent_mdi.subwindowHover(True, self.parent_subwindow)
            self.parent_subwindow.raise_()
            
            # Use target_pos for smooth movement
            pos = self.target_pos
            
            global_cur = QtGui.QCursor().pos()
            gx, gy = self.parent_subwindow.parent_mdi.mapFromGlobal(global_cur).x(), self.parent_subwindow.parent_mdi.mapFromGlobal(global_cur).y()

            # Get current position for smooth interpolation
            current_pos = self.parent_subwindow.pos()
            
            # Calculate smooth movement (interpolate between current and target)
            new_x = int(current_pos.x() + (pos.x() - current_pos.x()) * self.smooth_factor)
            new_y = int(current_pos.y() + (pos.y() - current_pos.y()) * self.smooth_factor)
            
            #new_x = int(current_pos.x() + (pos.x() - current_pos.x()))
            #new_y = int(current_pos.y() + (pos.y() - current_pos.y()))
            smooth_pos = QtCore.QPoint(new_x, new_y)

            if gx > 0 and gy > 0 and gx < self.parent_subwindow.parent_mdi.size().width() and gy < self.parent_subwindow.parent_mdi.size().height():
                self.parent_subwindow.move(smooth_pos)
                self.last_pos = [smooth_pos.x(), smooth_pos.y()]
                self.parent_subwindow.saveLastGeo(x=smooth_pos.x(), y=smooth_pos.y())

            # left
            elif gx < 0 and gy > 0 and gy < self.parent_subwindow.parent_mdi.size().height():
                self.parent_subwindow.move(self.last_pos[0], smooth_pos.y() + 1)
                self.last_pos = [self.last_pos[0], smooth_pos.y() + 1]
                self.parent_subwindow.saveLastGeo(x=smooth_pos.x(), y=smooth_pos.y() + 1)

            # right
            elif gy > 0 and gx > self.parent_subwindow.parent_mdi.size().width() and gy < self.parent_subwindow.parent_mdi.size().height():
                self.parent_subwindow.move(self.last_pos[0], smooth_pos.y() + 1)
                self.last_pos = [self.last_pos[0], smooth_pos.y() + 1]
                self.parent_subwindow.saveLastGeo(x=smooth_pos.x(), y=smooth_pos.y() + 1)
            
            # top
            elif gy < 0 and gx > 0 and gx < self.parent_subwindow.parent_mdi.size().width():
                self.parent_subwindow.move(smooth_pos.x() + 1, 0)
                self.last_pos = [smooth_pos.x() + 1, 0]
                self.parent_subwindow.saveLastGeo(x=smooth_pos.x() + 1, y=0)

            # bottom
            elif gx > 0 and gy > self.parent_subwindow.parent_mdi.size().height() and gx < self.parent_subwindow.parent_mdi.size().width():
                self.parent_subwindow.move(smooth_pos.x() + 1, self.last_pos[1])
                self.last_pos = [smooth_pos.x() + 1, self.last_pos[1]]
                self.parent_subwindow.saveLastGeo(x=smooth_pos.x() + 1, y=smooth_pos.y())

            # Update overlay
            self.update_overlay()

        def update_overlay(self):
            global_pos = QtGui.QCursor.pos()
            x, y = self.parent_subwindow.parent_mdi.mapFromGlobal(global_pos).x(), self.parent_subwindow.parent_mdi.mapFromGlobal(global_pos).y()
            w, h = self.parent_subwindow.parent_mdi.width(), self.parent_subwindow.parent_mdi.height()

            if 10 < x and w - 10 > x and 0 > y:
                # Top edge - maximize
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle(0, 0, w, h)
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            # Left edge
            elif 10 < y and h - 10 > y and 0 > x:
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle(self.e_spacing,
                                        self.e_spacing,
                                        (w//2)-(self.e_spacing*2),
                                        h-(self.e_spacing*2))
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            # Right edge
            elif 10 < y and h - 10 > y and w < x:
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle((w//2)+self.e_spacing,
                                        self.e_spacing,
                                        (w//2)-(self.e_spacing*2),
                                        h-(self.e_spacing*2))
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            # Top left corner
            elif 10 > x and 10 > y:
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle(self.e_spacing,
                                        self.e_spacing,
                                        (w//2)-(self.e_spacing*2),
                                        (h//2)-(self.e_spacing*2))
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            # Top right corner
            elif w - 10 < x and 10 > y:
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle((w//2)+self.e_spacing,
                                        self.e_spacing,
                                        (w//2)-(self.e_spacing*2),
                                        (h//2)-(self.e_spacing*2))
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            # Bottom right corner
            elif h - 10 < y and w - 10 < x:
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle((w//2)+self.e_spacing,
                                        (h//2)+self.e_spacing,
                                        (w//2)-(self.e_spacing*2),
                                        (h//2)-(self.e_spacing*2))
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            # Bottom left corner
            elif h - 10 < y and 10 > x:
                self.parent_subwindow.parent_mdi.rectangle_overly.draw_rectangle(self.e_spacing,
                                        (h//2)+self.e_spacing,
                                        (w//2)-(self.e_spacing*2),
                                        (h//2)-(self.e_spacing*2))
                self.parent_subwindow.parent_mdi.rectangle_overly.raise_()
            else:
                self.parent_subwindow.parent_mdi.rectangle_overly.remove_rectangle()

        def mouseReleaseEvent(self, event):
            self.parent_subwindow.parent_mdi.updateSubWindowSmartSpanGeoBuffer(self.parent_subwindow)
            
            self.dragging = False
            # Stop the smooth drag timer when mouse is released (only if it was running)
            if self.smooth_drage_timer.isActive():
                self.smooth_drage_timer.stop()
            
            self.parent_subwindow.parent_mdi.rectangle_overly.remove_rectangle()
            super().mouseReleaseEvent(event)
            
            # Rest of your mouseReleaseEvent code remains the same...
            global_pos = QtGui.QCursor.pos()
            x, y = self.parent_subwindow.parent_mdi.mapFromGlobal(global_pos).x(), self.parent_subwindow.parent_mdi.mapFromGlobal(global_pos).y()
            w, h = self.parent_subwindow.parent_mdi.width(), self.parent_subwindow.parent_mdi.height()

            if self.mouse_press_flag == True:
                if self.parent_subwindow.isMaximized() == True and self.parent_subwindow.maximize_flag == True:
                    if 100 < y:
                        self.parent_subwindow.showNormal()
                        self.parent_subwindow.maximize_flag = False
            if self.parent_subwindow.isMaximized == False:
                self.parent_subwindow.maximize_flag = False
            self.mouse_press_flag = False

            # Your snap-to-edge logic remains the same...
            if 10 < x and w - 10 > x and 0 > y:
                self.parent_subwindow.showMaximized()
            elif 10 < y and h - 10 > y and 0 > x:
                self.parent_subwindow.setGeometry(self.e_spacing, self.e_spacing, (w//2)-(self.e_spacing*2), h-(self.e_spacing*2))
                self.parent_subwindow.saveLastGeo()
            elif 10 < y and h - 10 > y and w < x:
                self.parent_subwindow.setGeometry((w//2)+self.e_spacing, self.e_spacing, (w//2)-(self.e_spacing*2), h-(self.e_spacing*2))
                self.parent_subwindow.saveLastGeo()
            elif 10 > x and 10 > y:
                self.parent_subwindow.setGeometry(self.e_spacing, self.e_spacing, (w//2)-(self.e_spacing*2), (h//2)-(self.e_spacing*2))
                self.parent_subwindow.saveLastGeo()
            elif w - 10 < x and 10 > y:
                self.parent_subwindow.setGeometry((w//2)+self.e_spacing, self.e_spacing, (w//2)-(self.e_spacing*2), (h//2)-(self.e_spacing*2))
                self.parent_subwindow.saveLastGeo()
            elif h - 10 < y and w - 10 < x:
                self.parent_subwindow.setGeometry((w//2)+self.e_spacing, (h//2)+self.e_spacing, (w//2)-(self.e_spacing*2), (h//2)-(self.e_spacing*2))
                self.parent_subwindow.saveLastGeo()
            elif h - 10 < y and 10 > x:
                self.parent_subwindow.setGeometry(self.e_spacing, (h//2)+self.e_spacing, (w//2)-(self.e_spacing*2), (h//2)-(self.e_spacing*2))
                self.parent_subwindow.saveLastGeo()

        def enterEvent(self, event):
            self.parent_subwindow.parent_mdi.subwindowHover(True,self.parent_subwindow)
            #self.parent.raise_()
            
            return super().enterEvent(event)
        
        def leaveEvent(self, a0):
            self.parent_subwindow.parent_mdi.subwindowHover(False,self.parent_subwindow)
            #self.parent.lower()
            #self.parent.parent.setWindowRaise()
            return super().leaveEvent(a0)

    
    def __init__(self, parent:MDIArea=None,transparent=False):
        super().__init__(parent)
        #self.setMinimumSize(150, 150)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setMouseTracking(True)

        self.parent_mdi=parent
        
        self.is_closing = False
        #self.transparent_flag=transparent
        self.resize_margin = 6
        self.original_geometry = None
        self.past_geometry=self.geometry()
        self.mouse_press_flag=False
        self.maximize_flag=False

    
        self.normal_flag=True
        self.widgets=[]

        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        #self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.titlebar = self.TitleBar(self)
        #self.titlebar.active_signal=self.parent.whenWindowActivated

        self.main_layout.addWidget(self.titlebar)

        self.resize_handles = {key: False for key in [
            'top', 'bottom', 'left', 'right',
            'top-left', 'top-right', 'bottom-left', 'bottom-right'
        ]}

        self.resize_debouncer=Custom.Debouncer(300)
        self.resize_debouncer.timeout.connect(self.subWindowResizeTasks)

        self.move_debouncer=Custom.Debouncer(300)
        self.move_debouncer.timeout.connect(self.whenMove.emit)
        
        self.border_hover_debouncer=Custom.Debouncer(200)
        self.border_hover_debouncer.timeout.connect(lambda:self.borderHoverAndSetCursor(self.mouse_move_event_pos))

        self.border_hover_unset_debouncer=Custom.Debouncer(200)
        self.border_hover_unset_debouncer.timeout.connect(lambda:(self.unsetCursor(),self.unsetBorderHover()))

        self.mouse_move_event_pos=None

        self.border_hover:bool=False
        
        self.borders = {
            "left":  False,
            "right": False,
            "top":   False,
            "bottom":False,
        }
        
    def keyPressEvent(self, event):

        print(self.titlebar.dragging)
        if event.modifiers()==QtCore.Qt.KeyboardModifier.ControlModifier and event.key()==QtCore.Qt.Key.Key_Up:
            print("change........ ")        
            #if self.titlebar:

            #self.parent.overlaySmartSnap(self,False)
        
        elif event.modifiers()==QtCore.Qt.KeyboardModifier.ControlModifier :
            #print("ok1")        
            #if self.titlebar.dragging:
            print("desable smart snapp")        
            #self.parent.overlaySmartSnap(self,True)
            #self.titlebar.smart_snap_debouncer.start()

        return super().keyPressEvent(event)

    def saveLastGeo(self, x=None, y=None, w=None, h=None):
        if x is None:
            x = self.x()
        if y is None:
            y = self.y()
        if w is None:
            w = self.width()
        if h is None:
            h = self.height()

        self.past_geometry = QtCore.QRect(x, y, w, h)


    def setWidget(self,widget):
        #local_layout=QtWidgets.QVBoxLayout()
        #local_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(widget)
        self.widgets.append(widget)
        
    def childWidget(self):
        return self.widgets[0]
        
    def setWindowTitle(self, title):
        self.titlebar.title_label.setText(title)

    def windowTitle(self):
        return self.titlebar.title_label.text()

    def setWindowIcon(self,icon_path):
        self.titlebar.icon_button.setIcon(QtGui.QIcon(icon_path))

    def closeWindow(self):
        self.parent_mdi.whenWindowClose.emit(self)

        #self.parent_mdi.closeSubWindow(self)
        pass
    
    def minimizeIt(self):
        if self.isVisible():    
            self.parent_mdi.total_minimized_subwindow+=1
            self.hide()

    def showMaximized(self):
        self.maximize_flag=True
        self.parent_mdi.organize_flag=False
        self.setGeometry(0,0,self.parent_mdi.size().width(),self.parent_mdi.size().height())
        self.raise_()
        
    def isMaximized(self):  
        return self.maximize_flag
    
    def showNormal(self):
        self.maximize_flag=False
        self.setGeometry(self.past_geometry)
        self.raise_()
    
    def mousePressEvent(self, event):
        
        self.mouse_press_flag=True

        self.parent_mdi.setWindowActivate(self)

        if any(self.resize_handles.values()):
            self.original_geometry = self.geometry()
            self.start_mouse_pos = event.globalPosition().toPoint()
        else:
            self.raise_()
        self.past_geometry=self.geometry()

        
    def borderHoverAndSetCursor(self,m_pos):
        if not self.original_geometry:
            self.update_resize_cursor(m_pos)
            return

    
    def mouseMoveEvent(self, event):
        
        self.mouse_move_event_pos=event.pos()

        #self.border_hover=True
        self.border_hover_debouncer.start()
        #self.border_hover=False
        #self.borderHoverAndSetCursor(event.pos())

        if event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.original_geometry:
            self.parent_mdi.organize_flag=False
            current_pos = event.globalPosition().toPoint()
            dx = current_pos.x() - self.start_mouse_pos.x()
            dy = current_pos.y() - self.start_mouse_pos.y()
            
            geo = self.original_geometry
            
            new_x, new_y = geo.x(), geo.y()
            new_w, new_h = geo.width(), geo.height()

            if self.resize_handles['right']:
                new_w = max(self.minimumWidth(), geo.width() + dx)

            if self.resize_handles['bottom']:
                new_h = max(self.minimumHeight(), geo.height() + dy)

            if self.resize_handles['left']:
                new_x = geo.x() + dx
                new_w = max(self.minimumWidth(), geo.width() - dx)

            if self.resize_handles['top']:
                new_y = geo.y() + dy
                new_h = max(self.minimumHeight(), geo.height() - dy)
            
            if self.resize_handles['top-left']:
                new_x = geo.x() + dx
                new_y = geo.y() + dy
                new_w = max(self.minimumWidth(), geo.width() - dx)
                new_h = max(self.minimumHeight(), geo.height() - dy)

            if self.resize_handles['top-right']:
                new_y = geo.y() + dy
                new_w = max(self.minimumWidth(), geo.width() + dx)
                new_h = max(self.minimumHeight(), geo.height() - dy)

            if self.resize_handles['bottom-left']:
                new_x = geo.x() + dx
                new_w = max(self.minimumWidth(), geo.width() - dx)
                new_h = max(self.minimumHeight(), geo.height() + dy)

            if self.resize_handles['bottom-right']:
                new_w = max(self.minimumWidth(), geo.width() + dx)
                new_h = max(self.minimumHeight(), geo.height() + dy)

            #local_x,local_y=self.parent.mapFromGlobal(current_pos).x(),self.parent.mapFromGlobal(current_pos).y()
            parent_rect = self.parent_mdi.rect()

            new_x = max(0, min(new_x, parent_rect.width() - new_w))
            new_y = max(0, min(new_y, parent_rect.height() - new_h))

            # Clamp size
            new_w = min(new_w, parent_rect.width() - new_x)
            new_h = min(new_h, parent_rect.height() - new_y)

            self.setGeometry(new_x, new_y, new_w, new_h)
            #print(self.parent.mapFromParent(current_pos))

            #print(local_x, local_y, self.parent.x() , self.y())

            self.past_geometry=self.geometry()

    def mouseReleaseEvent(self, event):
        self.mouse_press_flag=False
        self.original_geometry = None
        self.resize_handles = {key: False for key in self.resize_handles}
        self.unsetCursor()
        self.unsetBorderHover()

    def update_resize_cursor(self, pos):
        rect = self.rect()
        top = pos.y() <= self.resize_margin
        bottom = pos.y() >= rect.height() - self.resize_margin
        left = pos.x() <= self.resize_margin
        right = pos.x() >= rect.width() - self.resize_margin

        self.resize_handles = {key: False for key in self.resize_handles}


        if top and left:
            self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
            self.resize_handles['top-left'] = True
            self.border_hover=True
            self.setBorder("top",True)
            self.setBorder("left",True)
            
        elif top and right:
            self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
            self.resize_handles['top-right'] = True
            
            
            self.border_hover=True
            self.setBorder("right",True)
            self.setBorder("top",True)
            
        
        elif bottom and left:
            self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
            self.resize_handles['bottom-left'] = True

            self.border_hover=True
            self.setBorder("left",True)
            self.setBorder("bottom",True)
            

        elif bottom and right:

            self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
            self.resize_handles['bottom-right'] = True
            self.border_hover=True
            self.setBorder("bottom",True)
            self.setBorder("right",True)
        
        elif top:
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            self.resize_handles['top'] = True
            self.border_hover=True
            self.setBorder("top",True)
            

        elif bottom:

            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            self.resize_handles['bottom'] = True
            self.border_hover=True
            self.setBorder("bottom",True)
            
        elif left:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            self.resize_handles['left'] = True
            self.border_hover=True
            self.setBorder("left",True)

        elif right:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            self.resize_handles['right'] = True
            self.border_hover=True
            self.setBorder("right",True)
        else:
            self.unsetCursor()
            self.unsetBorderHover()

        self.update()

    def setBorder(self, side: str, enabled: bool):
        """Enable/disable a border on a given side (left, right, top, bottom)."""
        if side in self.borders:
            self.borders[side]=enabled
            #self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.border_hover:
            painter = QtGui.QPainter(self)
            rect = self.rect()

            for side, enabled in self.borders.items():
                
                if not enabled:
                    continue
                
                width=int(self.parent_mdi.subw_brdr_think)+1
                """if side=="left" and self.geometry().x()<2:
                    pen = QtGui.QPen(QtGui.QColor("#3FA48F"),width)
                    
                else:pass"""
                pen = QtGui.QPen(QtGui.QColor(self.parent_mdi.subw_ttlbr_hover),width)
                painter.setPen(pen)

                if side == "left":
                    painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
                elif side == "right":
                    painter.drawLine(rect.right()-width//2, rect.top(), rect.right()-width//2, rect.bottom())

                elif side == "top":
                    painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())

                elif side == "bottom":
                    painter.drawLine(rect.left(), rect.bottom()-width//2, rect.right(), rect.bottom()-width//2)


    def unsetBorderHover(self):

        self.border_hover=False
        self.borders['left']=False
        self.borders['right']=False
        self.borders['top']=False
        self.borders['bottom']=False
        self.update()


    def leaveEvent(self, a0):
        if not self.is_closing:
            self.border_hover_debouncer.stop()
            self.border_hover_unset_debouncer.start()

        #self.unsetBorderHover()
        return super().leaveEvent(a0)
    
    def moveEvent(self, a0):
        self.move_debouncer.start() 
        return super().moveEvent(a0)

    def subWindowResizeTasks(self):
        
        self.maximize_flag=False
        self.parent_mdi.organize_flag=False
        #self.parent.tileSubWindows()
        self.whenResize.emit()
        
    def resizeEvent(self, a0):
        self.resize_debouncer.start()
        return super().resizeEvent(a0)
    
class RefrenceManager(QtCore.QObject):
    whenItemSelect=QtCore.pyqtSignal(str,int)
    whenGoButtonClick=QtCore.pyqtSignal(str,int)
    def __init__(self,textedit):
        super().__init__()

        self.textedit:Custom.TextEditor=textedit
        
        self.container=QtWidgets.QWidget()
        self.container_layout=QtWidgets.QHBoxLayout()
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container.setLayout(self.container_layout)
        
        self.refrence_container=Custom.Widget()
        self.refrence_container_layout=QtWidgets.QVBoxLayout()
        self.refrence_container.setLayout(self.refrence_container_layout)
        self.refrence_container_layout.setContentsMargins(0,0,0,0)
        self.splitter=QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        self.splitter.addWidget(self.textedit)
        self.splitter.addWidget(self.refrence_container)
        self.splitter.setSizes([200,200])

        self.item_bgcolor="none"
        self.item_selected_clr="rgba(0,0,0,50)"
        self.splitter.setStyleSheet("background-color:black;")
        self.refrence_container.setStyleSheet("background-color:#BF5454;")

        self.last_selected_widget=None
        
        self.container_layout.addWidget(self.splitter)



        self.tree_view=QtWidgets.QTreeWidget()
        self.tree_view.setAnimated(False)
        self.tree_view.setUniformRowHeights(True)
        #self.tree_view.setObjectName("TreeView")
        self.tree_view.setStyleSheet(f"""
            QTreeView::item:selected {{
                                     
                background-color:{self.item_selected_clr};
                border-left:3px solid #00eaff;
                color: #3E4451;                /* selection text color */
            
            }}
        """)


        self.refrence_container_layout.addWidget(self.tree_view)
        self.item_widget_dict={}

        #self.tree_view.setHeaderHidden(True)
        # connect selection change
        self.tree_view.itemSelectionChanged.connect(self.onItemSelected)

    def addFileRefrenceGroup(self,file_name,path,refrences):
        container=QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        fname_label = QtWidgets.QLabel(file_name)
        fname_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        fname_label.setWordWrap(False)  # Optional, prevents wrapping
        fname_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(fname_label, stretch=1)  # Give it flexible space

        ln_label=QtWidgets.QLabel("---")
        #ln_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        ln_label.setWordWrap(False) #Optional,prevents wrapping
        #ln_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(ln_label)  # Give it flexible space

        go_btn = Custom.PushButton()
        go_btn.setText(" Go ")
        go_btn.bg_clr = "#FF8848"
        go_btn.text_clr = "black"
        go_btn.hover_clr = "#247163"
        go_btn.applyStyle()
        go_btn.setFixedWidth(60)
        layout.addWidget(go_btn)
        
        go_btn.clicked.connect(lambda:self.onItemSelected(True))

        container.setLayout(layout) 

        file_item=QtWidgets.QTreeWidgetItem(self.tree_view)
        file_item.setText(0,file_name)
        file_item.setToolTip(0,path)
        self.tree_view.setItemWidget(file_item,0,container)

        for refrence in refrences:
            if type(refrence)!=list:
                continue
            
            refrence_item=QtWidgets.QTreeWidgetItem(file_item)
            
            item_widget=RefrenceItemWidget(refrence[0],refrence[1])
            
            self.tree_view.setItemWidget(refrence_item,0,item_widget)
            #self.item_widget_dict[refrence_item]=item_widget

    def onItemSelected(self,go_btn_signal=False):
        selected_items = self.tree_view.selectedItems()
        if selected_items:
            item=selected_items[0]
            
            widget=self.tree_view.itemWidget(item,0)
            
            if item.parent()!=None:
                p_widget=self.tree_view.itemWidget(item.parent(),0)
                p_widget.children()[2].setText(widget.children()[1].text())
                
                if go_btn_signal==True:
                    self.whenGoButtonClick.emit(item.parent().toolTip(0),int(widget.children()[1].text()))

                #print(item.parent().toolTip(0),widget.children()[1].text())
                self.whenItemSelect.emit(item.parent().toolTip(0),int(widget.children()[1].text()))
            
            if self.last_selected_widget:

                self.last_selected_widget.setStyleSheet(f"background-color:{self.item_bgcolor};")
            
            if widget:
                self.last_selected_widget=widget
                widget.setFocus()
                widget.setStyleSheet(f"background-color:{self.item_selected_clr};")
                
                                                
class RefrenceItemWidget(QtWidgets.QWidget):
    whenGoButtonPressed = QtCore.pyqtSignal()

    def __init__(self, r_text, line):
        super().__init__()

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        # Line number label
        line_no_label = QtWidgets.QLabel(f"{line+1}")
        line_no_label.setFixedWidth(50)
        line_no_label.setStyleSheet("color:white;")
        line_no_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(line_no_label)

        # Reference text label
        refrence_label = QtWidgets.QLabel(r_text)
        refrence_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        refrence_label.setWordWrap(False)  # Optional, prevents wrapping
        refrence_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(refrence_label, stretch=1)  # Give it flexible space

        # Go button
        #go_btn = Custom.PushButton()
        #go_btn.setText(" Go ")
        #go_btn.bg_clr = "#FF8848"
        #go_btn.text_clr = "black"
        #go_btn.hover_clr = "#247163"
        #go_btn.applyStyle()
        #go_btn.setFixedWidth(60)
        #layout.addWidget(go_btn)

        self.setLayout(layout)


    def focusInEvent(self, a0):
        return super().focusInEvent(a0)
    
    def focusOutEvent(self, a0):
        return super().focusOutEvent(a0)