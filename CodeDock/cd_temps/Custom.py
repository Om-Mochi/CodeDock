from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.src.controllers.PathHandler import Path_Handler
#from CodeDock.C_Widgets.FuzzyProxyModel import FuzzyProxyModel,HighlightDelegate
import typing
import enum
import re
import math
import time

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed = None
        
    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time
        return self.elapsed

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.elapsed = None

    def report(self, label: str = "Time taken"):
        if self.elapsed is not None:
            print(f"{label}: {self.elapsed:.6f} seconds")
        else:
            print("Timer has not been stopped yet.")

time_tracker=TimeTracker()

class Custom:

    class MainWindow(QtWidgets.QWidget):
        whenResize=QtCore.pyqtSignal(object)
        
        #keys signals
        when_Ctrl_pressed=QtCore.pyqtSignal()
        when_Ctrl_release=QtCore.pyqtSignal()
        when_Ctrl_w_pressed=QtCore.pyqtSignal()
        when_Ctrl_f_pressed=QtCore.pyqtSignal()
        when_Ctrl_g_pressed=QtCore.pyqtSignal()
        when_Ctrl_l_pressed=QtCore.pyqtSignal()
        when_Ctrl_n_pressed=QtCore.pyqtSignal()
        when_Esc_pressed=QtCore.pyqtSignal()
        when_Ctrl_t_pressed=QtCore.pyqtSignal()



        class TitleBar(QtWidgets.QWidget):

            def __init__(self, parent:"Custom.MainWindow"):
                super().__init__(parent)
                self.mainwindow_parent = parent
                self.dragging = False
                self.offset = QtCore.QPoint()
                self.active_signal=None
                self.minimize_button_flag=False
                self.cusror_detect=False
                self.e_spacing=8
                self.connect_virtual_button=lambda x:...                
                self.virtual_desk_list=[]
                self.virtual_tab_list=[]
                self.last_pos=[]
                
                self.setFixedHeight(32)
                
                self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

                self.setStyleSheet("""
                    background-color:#3F3F3F;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                """)
                self.h_layout = QtWidgets.QHBoxLayout(self)
                self.h_layout.setContentsMargins(5, 0, 5, 0)
                self.h_layout.setSpacing(self.e_spacing)
                self.icon_button=QtWidgets.QPushButton()
                self.icon_button.setFixedSize(34, 28)
                self.icon_button.setIconSize(QtCore.QSize(20,20))

                self.title_label = QtWidgets.QLabel("CodeDock")
                self.title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
                

                self.close_button = QtWidgets.QPushButton()
                self.close_button.setFixedSize(24, 24)

                self.close_button.clicked.connect(self.mainwindow_parent.closeWindow)

                self.maximize_button = QtWidgets.QPushButton()
                self.maximize_button.setFixedSize(24, 24)
                
                self.maximize_button.clicked.connect(self.maximizeButtonSignal)

                self.minimize_button = QtWidgets.QPushButton()
                self.minimize_button.setFixedSize(24,24)
                self.minimize_button.clicked.connect(self.mainwindow_parent.showMinimized)

                self.bars_container=QtWidgets.QWidget()
                self.bars_layout=QtWidgets.QHBoxLayout()
                self.bars_container.setLayout(self.bars_layout)
                self.bars_layout.setContentsMargins(0,0,0,0)

                #self.virtual_container.setStyleSheet("background:#0D1115")
                self.h_layout.insertWidget(0,self.title_label)
                self.h_layout.insertStretch(1)
                
                self.h_layout.insertWidget(2,self.bars_container)
                self.h_layout.insertSpacing(3,10)
                self.h_layout.insertWidget(4,self.minimize_button)
                self.h_layout.insertWidget(5,self.maximize_button)
                self.h_layout.insertWidget(6,self.close_button)
                

            def maximizeButtonSignal(self):
                if self.minimize_button_flag==False:
                    self.mainwindow_parent.showMaximize()
                    self.minimize_button_flag=True
                else:
                    self.mainwindow_parent.showWindowNormal()
                    self.minimize_button_flag=False

            def mouseDoubleClickEvent(self, a0):
                self.maximizeButtonSignal()
                return super().mouseDoubleClickEvent(a0)
            
            def mousePressEvent(self, event):
                
                if event.button() == QtCore.Qt.MouseButton.LeftButton and not self.mainwindow_parent.maximize_flag:
                    self.startPos:QtCore.QPoint = event.globalPosition().toPoint()
                    
            def mouseMoveEvent(self, event):
                if event.buttons() == QtCore.Qt.MouseButton.LeftButton and not self.mainwindow_parent.maximize_flag:
                    delta = event.globalPosition().toPoint() - self.startPos
                    print(self.mainwindow_parent.pos() + delta)
                    self.mainwindow_parent.move(self.mainwindow_parent.pos() + delta)
                    self.startPos = event.globalPosition().toPoint()

                if self.mainwindow_parent.maximize_flag and event.globalPosition().toPoint().y:
                    print(self.startPos.y())
                    self.mainwindow_parent.showWindowNormal()
                    self.mainwindow_parent.maximize_flag=False
                    


            def mouseReleaseEvent(self, event):
                self.dragging = False

                super().mouseReleaseEvent(event)
                        
                x=QtGui.QCursor.pos().x()
                y=QtGui.QCursor.pos().y()
                w=self.mainwindow_parent.screenGeo.width()
                h=self.mainwindow_parent.screenGeo.height()
                
                if self.mainwindow_parent.mouse_press_flag==True:
                    if self.mainwindow_parent.isMaximized()==True and self.mainwindow_parent.maximize_flag==True:
                        self.mainwindow_parent.showWindowNormal()
                        self.mainwindow_parent.maximize_flag=False
                    if self.mainwindow_parent.isMaximized==False:
                        self.mainwindow_parent.maximize_flag=False
                        self.mainwindow_parent.mouse_press_flag=False



                #top edge
                if 10<x and w-10>x and 0>=y:
                    #self.setGeometry(0,0,w,h)


                    if self.minimize_button_flag==False:
                        self.mainwindow_parent.showMaximize()
                        self.minimize_button_flag=True
                    else:
                        self.mainwindow_parent.showWindowNormal()
                        self.minimize_button_flag=False

                    
                #top left
                elif 10<y and h-10>y and 3>=x:
                    
                    self.mainwindow_parent.setGeometry(self.e_spacing,
                                            self.e_spacing,
                                            (w//2)-(self.e_spacing*2),
                                            h-(self.e_spacing*2))
                    self.mainwindow_parent.saveLastGeo()
                #rigth edge
                elif 10<y and h-10>y and w-3<=x:
                    
                    self.mainwindow_parent.setGeometry((w//2)+self.e_spacing,
                                            self.e_spacing,
                                            (w//2)-(self.e_spacing*2),
                                            h-(self.e_spacing*2))
                    self.mainwindow_parent.saveLastGeo()
                #top rigth edge 
                elif 10>x and 10>y :
                    
                    self.mainwindow_parent.setGeometry(self.e_spacing,
                                            self.e_spacing,
                                            (w//2)-(self.e_spacing*2),
                                            (h//2)-(self.e_spacing*2))
                    self.mainwindow_parent.saveLastGeo()
                #top left edge
                elif w-10<x and 10>y:
                    
                    self.mainwindow_parent.setGeometry((w//2)+self.e_spacing,
                                            self.e_spacing,
                                            (w//2)-(self.e_spacing*2),
                                            (h//2)-(self.e_spacing*2))
                    self.mainwindow_parent.saveLastGeo()
                #bottom rigth edge 
                elif h-10<y and w-10<x:
                    
                    self.mainwindow_parent.setGeometry((w//2)+self.e_spacing,
                                            (h//2)+self.e_spacing,
                                            (w//2)-(self.e_spacing*2),
                                            (h//2)-(self.e_spacing*2))
                    self.mainwindow_parent.saveLastGeo()
                #bottom left edge
                elif h-10<y and 10>x:
                    
                    self.mainwindow_parent.setGeometry(self.e_spacing,
                                            (h//2)+self.e_spacing,
                                            (w//2)-(self.e_spacing*2),
                                            (h//2)-(self.e_spacing*2))
                    self.mainwindow_parent.saveLastGeo()

            def enterEvent(self, event):
                self.mainwindow_parent.subwindowHover(True)
                self.mainwindow_parent.raise_()            
                return super().enterEvent(event)

            def leaveEvent(self, a0):
                self.mainwindow_parent.subwindowHover(False)
                #self.parent.lower()
                #self.parent.parent.setWindowRaise()
                return super().leaveEvent(a0)

        
        def __init__(self):
            super().__init__()
            #self.setMinimumSize(150, 150)
            self.setObjectName("MainWindow")
            self.window_brdr_color="none"
            self.window_brdr_think=1
            self.btn_radius=[0,0]
            
            self.ttlbr_bg_clr="#608180"            
            self.ttlbr_text_clr="none"
            self.close_btn_clr="none"
            self.maximize_btn_clr="none"
            self.btns_radius=0
            self.ttlbr_hover="gray"
            self.maximize_btn_hover="green"
            self.close_btn_hover="red"
            self.ttlbr_hsize=32
            self.ttlbr_btns_size=24
            self.ttlbr_title_font=12
            self.ttlbr_icon_size=24


            self.screenGeo=QtGui.QGuiApplication.primaryScreen().geometry()
            
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
            #self.parent=parent
            self.past_geometry=self.geometry()
            self.mouse_press_flag=False
            self.maximize_flage=False

            self.maximize_flag=False
            self.normal_flag=True
            self.widgets=[]
            #self.setMinimumSize(100, 100)  # Allow resizing

            
            self.main_layout = QtWidgets.QVBoxLayout(self)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setSpacing(0)

            self.titlebar = self.TitleBar(self)
            #self.titlebar.active_signal=self.parent.whenWindowActivated

            self.main_layout.addWidget(self.titlebar)

            self.resize_handles = {key: False for key in [
                'top', 'bottom', 'left', 'right',
                'top-left', 'top-right', 'bottom-left', 'bottom-right'
            ]}
            self.resize_margin = 6
            self.original_geometry = None
            self.applyStyle()
            self.applyWindowStyle()
            #self.setStyleSheet("border:2px solid red;")

        
        def getVarDict(self):
            return {
                    'window_brdr_color':self.window_brdr_color,
                    'window_brdr_think':self.window_brdr_think,
                    'ttlbr_bg_clr':self.ttlbr_bg_clr,
                    'ttlbr_text_clr':self.ttlbr_text_clr,
                    'close_btn_clr':self.close_btn_clr,
                    'maximize_btn_clr':self.maximize_btn_clr,
                    'btns_radius':self.btns_radius,
                    'maximize_btn_hover':self.maximize_btn_hover,
                    'close_btn_hover':self.close_btn_hover,
                    "ttlbr_size":self.ttlbr_hsize,
                    "ttlbr_btns_size":self.ttlbr_btns_size,
                    "ttlbr_title_font":self.ttlbr_title_font,
                    "ttlbr_hover":self.ttlbr_hover,
                    }
        


        

        def subwindowHover(self,hover_flag):
            if hover_flag==True:
                self.setStyleSheet(f"""
                    MainWindow {{
                    background-color:#242424;
                    border:{self.window_brdr_think}px solid {self.ttlbr_hover};
                    }}
                """)

                self.titlebar.setStyleSheet(f"""                        
                        background-color:{self.ttlbr_hover};
                        
                        border-top-left-radius: {self.btn_radius[0]}px;
                        border-top-right-radius: {self.btn_radius[0]}px;
                """)

            else:pass
                #self.applyStyle()

        def applyWindowStyle(self):
            self.setStyleSheet(f"""
                MainWindow{{                  
                background-color:#242424;
                border:{self.window_brdr_think}px solid {self.window_brdr_color};
            }}
            """)
        

        def applyStyle(self):

            self.main_layout.setContentsMargins(int(self.window_brdr_think),
                                                            int(self.window_brdr_think),
                                                            int(self.window_brdr_think),
                                                            int(self.window_brdr_think))

            self.titlebar.title_label.setStyleSheet(f"color:{self.ttlbr_text_clr};font-size:{self.ttlbr_title_font}px")
            self.titlebar.setFixedHeight(self.ttlbr_hsize)
            self.titlebar.close_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
            self.titlebar.close_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
            self.titlebar.maximize_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
            self.titlebar.maximize_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
            self.titlebar.minimize_button.setFixedSize(QtCore.QSize(self.ttlbr_btns_size,self.ttlbr_btns_size))
            self.titlebar.minimize_button.setIconSize(QtCore.QSize(self.ttlbr_btns_size-5,self.ttlbr_btns_size-5))
            
            #self.titlebar.icon_button.setFixedSize(QtCore.QSize(self.ttlbr_icon_size,self.ttlbr_icon_size))
            #self.titlebar.icon_button.setIconSize(QtCore.QSize(self.ttlbr_icon_size-5,self.ttlbr_icon_size-5))
            
            
            self.titlebar.close_button.setStyleSheet(f"""
                QPushButton{{
                    background-color:{self.close_btn_clr};
                    border-radius:{self.btns_radius}px;
                }}
                QPushButton:hover{{
                    background-color:{self.close_btn_hover};
                }}

            """)

            
            self.titlebar.minimize_button.setStyleSheet(f"""
                QPushButton{{
                    background-color:{self.maximize_btn_clr};
                    border-radius:{self.btns_radius}px;
                }}
                QPushButton:hover{{
                    background-color:{self.maximize_btn_hover};
                }}

            """)
            
            self.titlebar.maximize_button.setStyleSheet(f"""
                QPushButton{{
                    background-color:{self.maximize_btn_clr};
                    border-radius:{self.btns_radius}px;
                }}
                QPushButton:hover{{
                    background-color:{self.maximize_btn_hover};
                }}

            """)
            

            self.titlebar.setStyleSheet(f"""
                background-color:{self.ttlbr_bg_clr};
                
                border-top-left-radius: {self.btn_radius[0]}px;
                border-top-right-radius: {self.btn_radius[0]}px;
            """)
            
       
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

        def setWindowActivate(self):
            self.raise_()

        def closeWindow(self):
            #self.when.emit(self)        
            self.close()

        def showMaximize(self):
            self.maximize_flag=True
            self.showMaximized()
            #self.setGeometry(0,0,self.screenGeo.width(),self.screenGeo.height())
            self.raise_()
            
        def isMaximized(self):
            return self.maximize_flag
        
        def showWindowNormal(self):
            self.maximize_flag=False

            self.showNormal()
            #self.setGeometry(self.past_geometry)
            self.raise_()
            
        def keyReleaseEvent(self, event):
            if event.key() == QtCore.Qt.Key.Key_Control:
                print("released")
                self.when_Ctrl_release.emit()
            return super().keyReleaseEvent(event)
        
        def keyPressEvent(self,event):
            if event.key() == QtCore.Qt.Key.Key_Control:
                self.when_Ctrl_pressed.emit()
                
            if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_G:
                self.when_Ctrl_g_pressed.emit()
            if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_F:
                self.when_Ctrl_f_pressed.emit()
            
            if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_W:
                self.when_Ctrl_w_pressed.emit()
                
            if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_N:
                self.when_Ctrl_n_pressed.emit()
                
            if event.key()==QtCore.Qt.Key.Key_Escape:
                self.when_Esc_pressed.emit()
            
            if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_L:
                self.when_Ctrl_l_pressed.emit()
                
            
            if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_T:
                self.when_Ctrl_t_pressed.emit()
                
            else:
            
                super().keyPressEvent(event)
        
        def mousePressEvent(self, event):
            self.setWindowActivate()
            self.update_resize_cursor(event.pos())
            if any(self.resize_handles.values()):
                self.original_geometry = self.geometry()
                self.start_mouse_pos = event.globalPosition().toPoint()
            else:
                self.raise_()
            self.past_geometry=self.geometry()

        def mouseMoveEvent(self, event):
            if not self.original_geometry:
                self.update_resize_cursor(event.pos())
                return

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
            parent_rect =QtCore.QRect(self.screenGeo.x(),self.screenGeo.y(),self.screenGeo.width(),self.screenGeo.height())
            

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
            self.original_geometry = None
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

        def update_resize_cursor(self, pos):
            margin = self.resize_margin
            x, y = pos.x(), pos.y()
            w, h = self.width(), self.height()

            self.resize_handles = {
                'top': y < margin,
                'bottom': y > h - margin,
                'left': x < margin,
                'right': x > w - margin,
                'top-left': x < margin and y < margin,
                'top-right': x > w - margin and y < margin,
                'bottom-left': x < margin and y > h - margin,
                'bottom-right': x > w - margin and y > h - margin,
            }

            # Change cursor shape
            if self.resize_handles['top-left'] or self.resize_handles['bottom-right']:
                self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
            elif self.resize_handles['top-right'] or self.resize_handles['bottom-left']:
                self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
            elif self.resize_handles['top'] or self.resize_handles['bottom']:
                self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            elif self.resize_handles['left'] or self.resize_handles['right']:
                self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            else:
                self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)


        def resizeEvent(self, a0):
            #self.parent.tileSubWindows()
            self.whenResize.emit(True)
            
            return super().resizeEvent(a0)
            
    class DockWidget(QtWidgets.QDockWidget):
        def __init__(self):
            super().__init__()

    class NestedMainWindow(QtWidgets.QMainWindow):
        
        def __init__(self,parent=None):
            super().__init__(parent)
            
            self.setWindowFlags(QtCore.Qt.WindowType.Widget)  
            self.setDockNestingEnabled(True)

            

    class ElidedLabel(QtWidgets.QLabel):
        def __init__(self, text="", parent=None):
            super().__init__(parent)
            self._full_text = text
            self.setText(text)
            
        def setText(self, text):
            self._full_text = text
            super().setText(text)

        def resizeEvent(self, event):
            fm = self.fontMetrics()
            elided = fm.elidedText(
                self._full_text,
                QtCore.Qt.TextElideMode.ElideRight,
                self.width()
            )
            super().setText(elided)
            super().resizeEvent(event)

    class Widget(QtWidgets.QWidget):
        def __init__(self,parent=None):
            super().__init__(parent)
            self.bg_clr="black"
            self.brdr_clr="none"
            self.brdr_think=0
            self.brdr_radius=0
            
            #adv    

            self.w=None
            self.h=None

        def getVarDict(self):
            return {
                "bg_clr":self.bg_clr,
                "brdr_clr":self.brdr_clr,
                "brdr_think":self.brdr_think,
                "brdr_radius":self.brdr_radius,
                "w":self.w,
                "h":self.h,
            }
    
        def updateVar(self,widget:object,dict:dict):
            widget.bg_clr=dict["bg_clr"]
            widget.brdr_clr=dict["brdr_clr"]
            widget.brdr_think=dict["brdr_think"]
            widget.brdr_radius=dict["brdr_radius"]
            widget.w=dict["w"]
            widget.h=dict["h"]
            widget.applyStyle()

        def applyStyle(self):
            #self.setFixedSize(self.w,self.h)

            self.setStyleSheet(f"""
            Widget{{
                background-color:{self.bg_clr};
                border:{self.brdr_think}px solid {self.brdr_clr};
                border-radius:{self.brdr_radius};
                               
            }}
            """)

    class PopupBox(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent, QtCore.Qt.WindowType.Popup)

            self.setWindowFlags(
                QtCore.Qt.WindowType.Popup |
                QtCore.Qt.WindowType.FramelessWindowHint
            )
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            
        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

            # Draw semi-transparent background
            rect = self.rect()
            color = QtGui.QColor(30, 30, 30, 235)  # dark gray with alpha
            painter.setBrush(color)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 0, 0)


    class SmartToolBar(QtWidgets.QFrame):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,  # can shrink/grow
            QtWidgets.QSizePolicy.Policy.Fixed
        )
            self.setFixedHeight(32)
            self.hlayout = QtWidgets.QHBoxLayout(self)
            self.hlayout.setContentsMargins(2, 0, 2, 0)
            self.hlayout.setSpacing(2)
            self.hlayout.addStretch()

            self._buttons: list[QtWidgets.QPushButton] = []
            self.btn_width = 32
            self.e_spacing = 2
            self._total_visible_buttons = 0

            # Debounce timer — only update after resize settles
            self._resize_timer = QtCore.QTimer(self)
            self._resize_timer.setSingleShot(True)
            self._resize_timer.setInterval(300)  # ms, tune between 16–50
            self._resize_timer.timeout.connect(self.updateButtons)
            
            self.bg_clr=...
            self.brdr_clr=...
            self.brdr_think=0
            self.brdr_radius=0
            self.w=None
            self.h=None
        
        def updateWidth(self):
            print(len(self._buttons),self.btn_width,self.e_spacing)
            btn_len=len(self._buttons)
            self.setMaximumWidth((btn_len*self.btn_width)+(self.e_spacing+1)*btn_len)

        def getVarDict(self):
            return {
                "bg_clr":self.bg_clr,
                "brdr_clr":self.brdr_clr,
                "brdr_think":self.brdr_think,
                "brdr_radius":self.brdr_radius,
                "w":self.w,
                "h":self.h,
                "spacing":self.e_spacing
            }

        def updateVar(self,dict:dict):
            self.bg_clr=dict["bg_clr"]
            self.brdr_clr=dict["brdr_clr"]
            self.brdr_think=dict["brdr_think"]
            self.brdr_radius=dict["brdr_radius"]
            self.w=dict["w"]
            self.h=dict["h"]
            #self.e_spacing=dict["spacing"]

        def applyStyle(self):
            print(self.bg_clr)
            self.setStyleSheet(f"""
            QFrame{{
                background-color:{self.bg_clr};
                border:{self.brdr_think}px solid {self.brdr_clr};
                border-radius:{self.brdr_radius}px;
                               
            }}
            """)

        def addToolButton(self, button: QtWidgets.QPushButton):
            self.btn_width = button.width()
            button.setFixedSize(self.btn_width, self.btn_width)
            button.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Fixed,
                QtWidgets.QSizePolicy.Policy.Fixed
            )
            self.hlayout.insertWidget(self.hlayout.count() - 1, button)
            self._buttons.append(button)
            self._total_visible_buttons += 1
            self.updateButtons()
            self.updateWidth()
        def resizeEvent(self, event):
            super().resizeEvent(event)
            # Restart timer on every resize — fires once when dragging stops
            self._resize_timer.start()

        def updateButtons(self):
            if not self._buttons:
                return

            margins = self.hlayout.contentsMargins()
            available = self.width() - margins.left() - margins.right()
            slot_width = self.btn_width + self.e_spacing
            max_visible = max(0, available // slot_width)

            # Block signals during batch visibility changes to avoid mid-loop repaints
            for i, btn in enumerate(self._buttons):
                should_show = i < max_visible
                if btn.isVisible() != should_show:
                    btn.blockSignals(True)
                    btn.setVisible(should_show)
                    btn.blockSignals(False)
                    self._total_visible_buttons += 1 if should_show else -1

                    
    class Frame(QtWidgets.QFrame):
        def __init__(self,parent=None):
            super().__init__(parent)
            self.bg_clr=...
            self.brdr_clr=...
            self.brdr_think=0
            self.brdr_radius=0
            self.w=None
            self.h=None

        def updateVar(self,frame:object,dict:dict):
            frame.bg_clr=dict["bg_clr"]
            frame.brdr_clr=dict["brdr_clr"]
            frame.brdr_think=dict["brdr_think"]
            frame.brdr_radius=dict["brdr_radius"]
            frame.w=dict["w"]
            frame.h=dict["h"]

        def applyStyle(self):
            self.setStyleSheet(f"""
            QFrame{{
                background-color:{self.bg_clr};
                border:{self.brdr_think}px solid {self.brdr_clr};
                border-radius:{self.brdr_radius}px;
                               
            }}
            """)

    
    class ToolBar(Frame):
        def __init__(self):
            super().__init__()
            #self.h=80
            #self.applyStyle()

            self.tool_btn_list=[]
            self.on_off_flag_button_list=[]

            self.main_layout=QtWidgets.QHBoxLayout()
            self.main_layout.setContentsMargins(0,0,0,0)
            self.setLayout(self.main_layout)

            self.layout_left_h=QtWidgets.QHBoxLayout()
            self.layout_left_h.setContentsMargins(10,3,3,3)
            self.main_layout.addLayout(self.layout_left_h)

            self.layout_right_h=QtWidgets.QHBoxLayout()
            self.layout_right_h.setContentsMargins(3,3,10,3)
            self.main_layout.addLayout(self.layout_right_h)

            self.tool_btn_style=Custom.PushButton()

        def applyToolButtonStyle(self):
            for tl_btn in self.tool_btn_list:

                tl_btn.bg_clr=self.tool_btn_style.bg_clr
                tl_btn.brdr_clr=self.tool_btn_style.brdr_clr
                tl_btn.hover_clr=self.tool_btn_style.hover_clr
                tl_btn.pressed_clr=self.tool_btn_style.pressed_clr
                tl_btn.brdr_radius=self.tool_btn_style.brdr_radius
                tl_btn.brdr_think=self.tool_btn_style.brdr_think    
                tl_btn.applyStyle()

        def addToolButton(self,text=None,icon=(None,0,0),parent=None):
            btn=Custom.PushButton()
            
            if text!=None:btn.setText(text)
            if icon!=None:
                btn.setIcon(QtGui.QIcon(icon[0]))
                btn.setIconSize(QtCore.QSize(icon[1],icon[2]))
                btn.h=icon[1]+2
                btn.w=icon[2]+2
                
            if parent!=None:...

            self.layout_right_h.addWidget(btn,alignment=QtCore.Qt.AlignmentFlag.AlignRight)
            self.tool_btn_list.append(btn)
            container_layout=QtWidgets.QGridLayout()
            
            btn.clicked.connect(lambda:self.whenToolButtonClicked(btn,container_layout))

            return btn,container_layout
        
        def addOnOffFlagButton(self,text,layout=None,pos=0):
            label=QtWidgets.QLabel(text)
            btn=Custom.PushButton()
            btn.setCheckable(True)

            btn.setFixedWidth(60)
            btn.bg_clr="#67B95F"
            btn.brdr_radius=2
            btn.setText("On")
            btn.text_clr="black"
            btn.setChecked(True)
            btn.clicked.connect(lambda:self.whenOnOffFlagButtonClicked(btn))
            btn.applyStyle()
            layout.addWidget(label,pos,0)
            layout.addWidget(btn,pos,1)
                        
        def whenOnOffFlagButtonClicked(self,btn):
            if btn.isChecked():
                btn.bg_clr="#67B95F"
                btn.setText("On")
                btn.applyStyle()
            else:
                btn.bg_clr="#D37E46"
                btn.setText("Off")
                btn.applyStyle()

        def whenToolButtonClicked(self,btn,layout):
            popup=Custom.PopupBox(self)
            #p_layout=QtWidgets.QGridLayout()
            popup.setLayout(layout)
            btn_pos=self.mapToGlobal(self.rect().bottomLeft())
            popup.move(btn_pos)
            popup.show()


    class BlockPathNevigationBar(Widget):
        def __init__(self):
            super().__init__()
            self.btn_obj_buffer:list[list[Custom.PushButton,Custom.PushButton]]=[]
            
            self.block_holder=QtWidgets.QHBoxLayout()
            self.block_holder.setContentsMargins(0,0,0,0)
            self.setLayout(self.block_holder)
            self.btn_font=QtGui.QFont()

        def setBlockSymbols(self,symbol_list):
            self._removeBlocksButton()
            len_s=len(symbol_list)-1
            for i,symbol in enumerate(symbol_list[::-1]):
                
                self._addBlockButton(symbol[0],len_s,i,symbol[1])

        def _removeBlocksButton(self):
            for i,btn in enumerate(self.btn_obj_buffer):
                btn[0].deleteLater()
                if btn[1]!=None:
                    btn[1].deleteLater()
            self.btn_obj_buffer.clear()
            
        def _addBlockButton(self,symbol_name,len_s,index,icon):
            btn=Custom.PushButton()
            arw_btn=Custom.PushButton()
            
            btn.setText(f" {symbol_name} ")
            btn.setFixedHeight(self.height())
            btn.setFont(self.btn_font)
            btn.setIcon(QtGui.QIcon(icon))
            self.block_holder.addWidget(btn)
            
            if len_s!=index:
                arw_btn.setIcon(
                    QtWidgets.QApplication.style().standardIcon(
                        QtWidgets.QStyle.StandardPixmap.SP_ArrowRight
                    )
                )
                self.block_holder.addWidget(arw_btn)
                self.btn_obj_buffer.append([btn,arw_btn])
            
            else:
                self.btn_obj_buffer.append([btn,None])

        def setBtnIconSize(self,size):
            for i,btn in enumerate(self.btn_obj_buffer):
                btn[0].setIconSize(QtCore.QSize(size,size))
                
                if btn[1]!=None:
                    btn[1].setIconSize(QtCore.QSize(size,size))
                    btn[1].setFixedWidth(size+5)
        
        def setBtnFontSize(self,size):

            for btn in self.btn_obj_buffer:
                self.btn_font.setPointSize(size)
                btn[0].setFont(self.btn_font)

        def resizeEvent(self, a0):
            for btn in self.btn_obj_buffer:
                btn[0].setFixedHeight(self.height())
                if btn[1]!=None :
                    btn[1].setFixedHeight(self.height())
        
            return super().resizeEvent(a0)
        
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
                project_desk.setParent(self.parent_mdi)
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
            
        
    class ImageViewer(QtWidgets.QWidget):
        def __init__(self, image_path: str):
            super().__init__()
            self.setStyleSheet("background-color:#171819;")
            self.setMinimumSize(200, 200)
            self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)  # needed for key events

            self.image = QtGui.QPixmap(image_path)
            self.scale_factor = 1.0
            self.offset = QtCore.QPoint(0, 0)  # pan offset

            # drag state
            self._drag_start = None
            self._offset_at_drag_start = None

            iw, ih = self.image.width(), self.image.height()
            self.half_size = QtCore.QSize(iw // 2, ih // 2)
            self.resize(self.half_size)
            self.scale_factor = self.half_size.width() / iw

        # ── rendering ──────────────────────────────────────────────────────────────
        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            if not self.image.isNull():
                scaled_img = self.image.scaled(
                    self.image.size() * self.scale_factor,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
                # centre + apply pan offset
                x = (self.width() - scaled_img.width()) // 2 + self.offset.x()
                y = (self.height() - scaled_img.height()) // 2 + self.offset.y()
                painter.drawPixmap(x, y, scaled_img)

        # ── zoom (Ctrl + scroll) ───────────────────────────────────────────────────
        def wheelEvent(self, event: QtGui.QWheelEvent):
            if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
                angle = event.angleDelta().y()
                step = 0.1
                if angle > 0:
                    self.scale_factor *= (1 + step)
                else:
                    self.scale_factor /= (1 + step)
                self.scale_factor = max(0.1, min(self.scale_factor, 10.0))
                self.update()

        # ── mouse drag ─────────────────────────────────────────────────────────────
        def mousePressEvent(self, event: QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self._drag_start = event.position().toPoint()
                self._offset_at_drag_start = QtCore.QPoint(self.offset)
                self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

        def mouseMoveEvent(self, event: QtGui.QMouseEvent):
            if self._drag_start is not None:
                delta = event.position().toPoint() - self._drag_start
                self.offset = self._offset_at_drag_start + delta
                self.update()

        def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self._drag_start = None
                self._offset_at_drag_start = None
                self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

        # ── arrow-key pan ──────────────────────────────────────────────────────────
        def keyPressEvent(self, event: QtGui.QKeyEvent):
            step = 20  # pixels per key press (hold Shift for 5×)
            if event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier:
                step *= 5

            key = event.key()
            if key == QtCore.Qt.Key.Key_Left:
                self.offset += QtCore.QPoint(-step, 0)
            elif key == QtCore.Qt.Key.Key_Right:
                self.offset += QtCore.QPoint(step, 0)
            elif key == QtCore.Qt.Key.Key_Up:
                self.offset += QtCore.QPoint(0, -step)
            elif key == QtCore.Qt.Key.Key_Down:
                self.offset += QtCore.QPoint(0, step)
            else:
                super().keyPressEvent(event)
                return
            self.update()

        # ── reset pan (double-click) ───────────────────────────────────────────────
        def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.offset = QtCore.QPoint(0, 0)
                self.update()



    class RectangleOverlay(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
                        
            self.setGeometry(parent.rect())
            self.rect_to_draw = None
            self.rect_color=None

        def draw_rectangle(self, x, y, w, h,color=QtGui.QColor(255, 255, 255)):
            self.rect_to_draw = QtCore.QRect(x, y, w, h)
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
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.drawRect(self.rect_to_draw)


    class TextEditMinimap(QtWidgets.QPlainTextEdit):
        """ Minimap with a fixed viewport height and overlay for the visible area. """
        def __init__(self):
            super().__init__()
            self.editor:Custom.TextEditor = None
            self.subwindow= None
            self.dragging = False  # Track if the viewport is being dragged
            self.last_scroll_state=None
            self.ignore_sync = False  # Prevent unwanted sync loop

            self.minimap_bg = "#000000"
            self.brdr_width = 2
            self.vp_rgba =[0,0,0,80]
            self.vp_brdr_rgba=[142,167,163,255]
            self.vp_brdr_hover_rgba=[217,255,252,255]

            self.applyViewPortStyle()
            self.applyViewPortBorderStyle()
            self.applyMiniMapStyle()
            self.viewport_clr = QtGui.QColor(*self.vp_rgba)
            self.viewport_brdr_clr = QtGui.QColor(*self.vp_brdr_rgba)
            self.viewport_brdr_hover= QtGui.QColor(*self.vp_brdr_hover_rgba)


            #self.setReadOnly(True)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  
            
            self.map_font=QtGui.QFont("JetBrainsMonoNL Nerd Font", 2)
            self.setFont(self.map_font)  
            self.setFixedWidth(110)  
            self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
            #self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            #self.setTabChangesFocus(False)

            # Connect minimap scroll to editor scroll
            self.verticalScrollBar().valueChanged.connect(self.sync_editor_scroll)
            
        def getVarDict(self):
            return {
                'minimap_bg':self.minimap_bg,
                'vp_rgba':self.vp_rgba,
                'vp_brdr_rgba':self.vp_brdr_rgba,
                'vp_brdr_hover_rgba':self.vp_brdr_hover_rgba,
                'brdr_width':self.brdr_width,
            }
        
        def updateVar(self,TextEditMinimap,dict):
            TextEditMinimap.minimap_bg=dict["minimap_bg"]
            TextEditMinimap.vp_rgba=dict["vp_rgba"]
            TextEditMinimap.vp_brdr_rgba=dict["vp_brdr_rgba"]
            TextEditMinimap.vp_brdr_hover_rgba=dict["vp_brdr_hover_rgba"]
            TextEditMinimap.brdr_width=dict["brdr_width"]

        def applyViewPortStyle(self):
            if self.editor!=None and self.subwindow!=None:
                self.viewport_clr = QtGui.QColor(*self.vp_rgba)
                self.viewport().update()

        def applyViewPortBorderStyle(self):
            if self.editor!=None and self.subwindow!=None:
                self.viewport_brdr_clr = QtGui.QColor(*self.vp_brdr_rgba)
                self.viewport_brdr_hover= QtGui.QColor(*self.vp_brdr_hover_rgba)
                self.viewport().update()

        def applyMiniMapStyle(self):
            self.setStyleSheet(f"background-color:{self.minimap_bg};")
        def sync_minimap_to_editor_scroll(self):
            if self.editor is None:
                return
            editor_scroll = self.editor.verticalScrollBar()
            minimap_scroll = self.verticalScrollBar()

            scale_factor = minimap_scroll.maximum() / max(1, editor_scroll.maximum())
            minimap_scroll.setValue(int(editor_scroll.value() * scale_factor))
            self.viewport().update()
            
        def paintEvent(self, event):

            if self.editor!=None and self.subwindow!=None:
                #self.setStyleSheet("background-color:white;")
                #original_font = self.document().defaultFont()

                # Temporarily override document font to 4px only for this paint
                
                # Restore original font so main editor is not affected
                #self.document().setDefaultFont(self.map_font)

                super().paintEvent(event)
                
                #self.document().setDefaultFont(original_font)
                painter_viewport = QtGui.QPainter(self.viewport())
                painter_lborder = QtGui.QPainter(self.viewport())
                try:
                    editor_scroll = self.editor.verticalScrollBar()
                except:
                    self.editor=None
                    
                # Get total lines in editor
                total_lines = self.editor.blockCount()
                visible_lines = self.editor.viewport().height() / self.editor.fontMetrics().height()

                # Calculate overlay position and height


                font_metric=QtGui.QFontMetrics(self.font())
                line_height=font_metric.lineSpacing()  # Includes line spacing

                # Calculate the height of 20 visible lines
                
                self.viewport_height=int(line_height*visible_lines)


                scale_factor = self.editor.height() / total_lines
                self.viewport_y = int(editor_scroll.value() * scale_factor)
                #self.viewport_height = max(1, int(visible_lines*scale_factor))
                # Draw the overlay
                    
                painter_viewport.fillRect(QtCore.QRect(0, self.viewport_y, self.viewport().width(), self.viewport_height), self.viewport_clr)
                
                if self.dragging==True:
                    #painter_lborder=QtGui.QPainter(self.viewport())

                    painter_lborder.fillRect(QtCore.QRect(0, self.viewport_y,self.brdr_width,self.viewport_height),self.viewport_brdr_hover)
                else:
                    painter_lborder.fillRect(QtCore.QRect(0, self.viewport_y,self.brdr_width,self.viewport_height),self.viewport_brdr_clr)
                painter_viewport.end()
            else:pass

        def mouseReleaseEvent(self, event):
            """ Stops dragging when mouse button is released. """
            self.dragging = False
            self.viewport().update()

        def mousePressEvent(self, event):
            """ Detects when the viewport is clicked and starts dragging. """
            if self.editor is None:
                return

            click_y = event.position().y()
            if self.viewport_y <= click_y <= self.viewport_y + self.viewport_height:
                self.dragging = True
            else:
                # Move viewport immediately to follow cursor
                self.set_viewport_position(click_y)

            event.accept()

        def mouseMoveEvent(self, event):

            """ Moves the viewport to follow the cursor position. """
            if self.dragging and self.editor is not None:
                self.set_viewport_position(event.position().y())

        def set_viewport_position(self, cursor_y):
            """ Moves the viewport directly to the cursor position in the minimap. """
            minimap_scroll = self.verticalScrollBar()
            editor_scroll = self.editor.verticalScrollBar()
            
            #print("m scroll :",minimap_scroll.value())
            # Calculate the new scroll position based on cursor position
            #total_lines = max(1, self.editor.blockCount())
            minimap_height = self.height()
            scale_factor = (editor_scroll.maximum()) / max(1, minimap_scroll.maximum())

            # Calculate target position
            new_scroll_value = int((cursor_y / minimap_height) * minimap_scroll.maximum())

            # Apply to minimap and editor
            if self.editor.verticalScrollBar().maximum()!=int(scale_factor):    

                minimap_scroll.setValue(new_scroll_value)
                editor_scroll.setValue(int(new_scroll_value * scale_factor))
            #print("new scrol :",new_scroll_value)
            self.viewport().update()  # Refresh the viewport

        def sync_editor_scroll(self, value):
            if self.editor is not None and self.subwindow is not None:
                if self.ignore_sync:
                    return

                editor_scroll = self.editor.verticalScrollBar()
                minimap_scroll = self.verticalScrollBar()
                    
                self.ignore_sync = True
                editor_scroll.valueChanged.disconnect(self.sync_minimap_scroll)

                scale_factor = editor_scroll.maximum() / max(1, minimap_scroll.maximum())
                if self.editor.verticalScrollBar().maximum()!=int(scale_factor):    
                    editor_scroll.setValue(int(value*scale_factor))
                editor_scroll.valueChanged.connect(self.sync_minimap_scroll)
                self.ignore_sync = False

                self.viewport().update()

        def sync_minimap_scroll(self, value):
            try:
                if self.editor is not None and self.subwindow is not None:
                    if self.ignore_sync:
                        return
            
                    editor_scroll = self.editor.verticalScrollBar()
                    #print("scroll")
                    minimap_scroll = self.verticalScrollBar()

                    self.ignore_sync = True
                    minimap_scroll.valueChanged.disconnect(self.sync_editor_scroll)

                    scale_factor = minimap_scroll.maximum() / max(1, editor_scroll.maximum())
                    if self.editor.verticalScrollBar().maximum()!=int(scale_factor):    
                        minimap_scroll.setValue(int(value * scale_factor))
                    
                    minimap_scroll.valueChanged.connect(self.sync_editor_scroll)
                    self.ignore_sync = False

                    self.viewport().update()
            except:pass


        def ensureCursorVisible(self):
            pass

        def simulateKeys(self, key, modifiers=QtCore.Qt.KeyboardModifier.NoModifier):
            press_event=QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, key, modifiers)
            release_event = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyRelease, key, modifiers)
            QtWidgets.QApplication.postEvent(self, press_event)
            QtWidgets.QApplication.postEvent(self, release_event)


        def trigger_ctrl_c(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_C,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )
        
        def trigger_ctrl_v(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_V,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )

        def trigger_ctrl_a(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_A,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )

        def trigger_ctrl_z(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Z,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )


        def trigger_ctrl_shift_z(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Z,
                QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.ShiftModifier 
            )


        def trigger_enter(self):
            cursor=self.textCursor()
            current_line = cursor.block().text()
            leading_spaces = len(current_line) - len(current_line.lstrip(' '))
            cursor.insertText("\n" + " " * leading_spaces)

        def trigger_ctrl_backspace(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Backspace,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )


        def trigger_delete(self):
            self.simulateKeys(QtCore.Qt.Key.Key_Delete)
            
            """self.simulateKeys(
                QtCore.Qt.Key.Key_Delete,
                QtCore.Qt.KeyboardModifier.NoModifier
            )
        """
        def trigger_Shift_Tab(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Delete,
                QtCore.Qt.KeyboardModifier.ShiftModifier
            )


        def trigger_Tab(self):

            cur=self.textCursor()
            cur.insertText(" "*4)


            """         self.simulateKeys(
                QtCore.QEvent.Type.KeyPress,
                QtCore.Qt.Key.Key_Tab,
                QtCore.Qt.KeyboardModifier.NoModifier
            )
            QtWidgets.QApplication.postEvent(self, event)

            """        
        def trigger_PageUp(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_PageUp,
                QtCore.Qt.KeyboardModifier.NoModifier
            )

        def trigger_PageDown(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_PageDown,
                QtCore.Qt.KeyboardModifier.NoModifier
            )

        def trigger_Shift_PageUp(self):
            self.simulateKeys(
                QtCore.QEvent.Type.KeyPress,
                QtCore.Qt.Key.Key_PageUp,
                QtCore.Qt.KeyboardModifier.ShiftModifier
            )


        def trigger_Shift_PageDown(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_PageDown,
                QtCore.Qt.KeyboardModifier.ShiftModifier
            )
            
        def trigger_Up(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Up,
                QtCore.Qt.KeyboardModifier.NoModifier
            )

        def trigger_Down(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Down,
                QtCore.Qt.KeyboardModifier.NoModifier
            )
            
        def trigger_Left(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Left,
                QtCore.Qt.KeyboardModifier.NoModifier
            )
            
        def trigger_Right(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Right,
                QtCore.Qt.KeyboardModifier.NoModifier
            )
            
        def trigger_Ctrl_Up(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Up,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )
            
        def trigger_Ctrl_Down(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Down,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )
            

        def trigger_Ctrl_Left(self):
            self.simulateKeys(
                QtCore.Qt.Key.Key_Left,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )
            
        def trigger_Ctrl_Right(self):
        
            self.simulateKeys(
                QtCore.Qt.Key.Key_Right,
                QtCore.Qt.KeyboardModifier.ControlModifier
            )
            
        def trigger_backspace(self):
            #self.trigger_ctrl_a()
            self.simulateKeys(QtCore.Qt.Key.Key_Backspace)
            #self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            
        def setChar(self, char):
            self.cursor2.insertText(char)

        def setCursorPosition(self, line, column):
            
            block = self.document().findBlockByNumber(line)
            pos = block.position() + column
            self.cursor2 = self.textCursor()
            self.cursor2.setPosition(pos)
            self.setTextCursor(self.cursor2)

        def setSelection(self, start, end):
            cursor = self.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)


    class LineNumberArea(QtWidgets.QWidget):
        def __init__(self, editor:"Custom.TextEditor"):

            super().__init__(editor)
            
            self.editor = editor
            self.bg_clr="#000000"
            self.editor.viewport().installEventFilter(self)
            self.editor.blockCountChanged.connect(self.update_width)
            self.editor.updateRequest.connect(self.update_area)

            self.breakpoints = set()
            self.error_lines = set()

            self.breakpoint_icon = QtGui.QPixmap(editor.Path_h.BREAKPOINT_ICON)
            self.error_icon = QtGui.QPixmap(editor.Path_h.WARNING_ICON)
            self.set_errors({10,15})
            self.update_width(0)
            self.editor.cursorPositionChanged.connect(self.update)


        def update_width(self, _):
            digits = len(str(self.editor.blockCount()))
            width = 40 + self.fontMetrics().horizontalAdvance("9") * digits
            self.editor.setViewportMargins(width, 0, 0, 0)
            self.setFixedWidth(width)

        def update_area(self, rect, dy):
            if dy:
                self.scroll(0, dy)
            else:
                self.update(0, rect.y(), self.width(), rect.height())

            if rect.contains(self.editor.viewport().rect()):
                self.update_width(0)

        def resizeUpdate(self, event):
            cr = self.editor.contentsRect()
            self.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.width(), cr.height()))

        def eventFilter(self, obj, event):
            if event.type() == QtCore.QEvent.Type.Paint:
                self.update()
            return super().eventFilter(obj, event)

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.fillRect(event.rect(), QtGui.QColor(self.bg_clr))

            block = self.editor.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = self.editor.contentOffset()
            top = self.editor.blockBoundingGeometry(block).translated(offset).top()

            font_metrics = self.editor.fontMetrics()
            line_height = font_metrics.height()

            icon_size = 12
            
            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible():
                    line_num = block_number + 1
                    rect_top = int(top)

                    # Center icon vertically in the line
                    icon_y = rect_top + int((line_height - icon_size) / 2)
                    icon_x = 4

                    # Draw error or breakpoint icons
                    if line_num in self.error_lines:
                        painter.drawPixmap(icon_x, icon_y, icon_size, icon_size, self.error_icon)
                    elif line_num in self.breakpoints:
                        painter.drawPixmap(icon_x, icon_y, icon_size, icon_size, self.breakpoint_icon)

                    # Draw line number text
                    text_x = icon_x + icon_size + 4  # Leave space after icon
                    cursor_block_number = self.editor.textCursor().blockNumber() + 1

                    # Decide color based on cursor position
                    if line_num == cursor_block_number:
                        painter.setPen(QtGui.QColor("#7EA0A0"))  # Green color for active line
                    else:
                        painter.setPen(QtGui.QColor("#4B4B4B"))  # Normal color

                    painter.setFont(self.editor.font())
                    painter.drawText(-10, rect_top, self.width() - 4, line_height,
                        QtCore.Qt.AlignmentFlag.AlignRight, str(line_num))

                # Move to next block
                top += self.editor.blockBoundingRect(block).height()
                block = block.next()
                block_number += 1

            painter.end()

        def toggle_breakpoint(self, line: int):
            if line in self.breakpoints:
                self.breakpoints.remove(line)
            else:
                self.breakpoints.add(line)
            self.update()

        def set_errors(self, lines: set):
            self.error_lines = lines
            self.update()


        def mousePressEvent(self, event: QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                # Calculate which line was clicked
                y = event.position().y()
                block = self.editor.firstVisibleBlock()
                top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
                bottom = top + self.editor.blockBoundingRect(block).height()
                line = block.blockNumber()

                while block.isValid() and top <= y:
                    if block.isVisible() and bottom >= y:
                        self.toggle_breakpoint(line + 1)
                        break
                    block = block.next()
                    top = bottom
                    bottom = top + self.editor.blockBoundingRect(block).height()
                    line += 1


    class TextEditor(QtWidgets.QPlainTextEdit):
    
        whenTextCursorHover=QtCore.pyqtSignal(list)
        whenMouseCursorTextMatch=QtCore.pyqtSignal(str,int,int,QtCore.QPoint)
        whenMouseCursorNoTextMatch=QtCore.pyqtSignal()
        whenMouseCursorLeaveHover=QtCore.pyqtSignal()
        whenGoToDefinitionRequest=QtCore.pyqtSignal(str,int,int,QtCore.QPoint)
        

        whenFocusIn=QtCore.pyqtSignal(object)
        whenMouseEnter=QtCore.pyqtSignal()
        #whenMouseLeftClick=QtCore.pyqtSignal(QtGui.QMouseEvent)
        when_Key_SHIFT_F12_Pressed=QtCore.pyqtSignal()
        whenOnlyAplphaNemuricKeyPressed=QtCore.pyqtSignal(str)

        getCursorPosition = QtCore.pyqtSignal(object, int, int)
        when_Key_Ctrl_BackSpace_Pressed = QtCore.pyqtSignal()
        when_Key_Ctrl_BackSpace_Pressed_V2 = QtCore.pyqtSignal(int,int,int,int,str)

        when_Key_BackSpace_Pressed = QtCore.pyqtSignal()
        getCharWhenType = QtCore.pyqtSignal(str)
        whenLinePosChangeGetLineNo=QtCore.pyqtSignal(int)
        selectionChanged = QtCore.pyqtSignal(int, int)  # New signal

        when_Key_Ctrl_c_pressed = QtCore.pyqtSignal()
        when_Key_Ctrl_v_pressed = QtCore.pyqtSignal()
        when_Key_Ctrl_a_pressed = QtCore.pyqtSignal()
        when_Key_Ctrl_shift_z_pressed = QtCore.pyqtSignal()
        when_Key_Ctrl_z_pressed = QtCore.pyqtSignal()
        when_Key_Ctrl_s_pressed=QtCore.pyqtSignal()

        when_Key_delete_pressed = QtCore.pyqtSignal()
        when_Key_Shift_delete_pressed = QtCore.pyqtSignal()

        when_Key_Tab_pressed = QtCore.pyqtSignal()
        when_Key_Shift_Tab_pressed = QtCore.pyqtSignal()

        when_Key_Enter_pressed = QtCore.pyqtSignal()


        when_Key_Up_pressed= QtCore.pyqtSignal()
        when_Key_Down_pressed= QtCore.pyqtSignal()
        when_Key_Left_pressed= QtCore.pyqtSignal()
        when_Key_Right_pressed= QtCore.pyqtSignal()

        when_Key_PageUp_pressed=QtCore.pyqtSignal()
        when_Key_PageDown_pressed=QtCore.pyqtSignal()
        when_Key_Shift_PageUp_pressed=QtCore.pyqtSignal()
        when_Key_Shift_PageDown_pressed=QtCore.pyqtSignal()
            

        when_Key_Ctrl_Up_pressed= QtCore.pyqtSignal()
        when_Key_Ctrl_Down_pressed= QtCore.pyqtSignal()
        when_Key_Ctrl_Left_pressed= QtCore.pyqtSignal()
        when_Key_Ctrl_Right_pressed= QtCore.pyqtSignal()

        notifyOnKeyStrock=QtCore.pyqtSignal()
        whenCompletionInsert=QtCore.pyqtSignal(int,int,int,int,str)
        whenAutoPair=QtCore.pyqtSignal(int,int,int,int,str)
        when_Key_Enter_Pressed_V2=QtCore.pyqtSignal(int,int,int,int,str)


        def __init__(self,parent=None,path_h:Path_Handler=None,transparent=False):
            super().__init__(parent)

            if transparent:
                self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)


            self.Path_h=path_h
            self.dock_parent=parent
            self.tansparent_flag=transparent
            self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
            #self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
            self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            self.setTabChangesFocus(False)

            self.syntax_pairs = {
                '(': ')',
                '[': ']',
                '{': '}',
                '"': '"',
                "'": "'",
                '`': '`',
            }

            self.closers = {v for v in self.syntax_pairs.values()}

            #self.setFont(QtGui.QFont("Courier New"))
            font = QtGui.QFont("JetBrainsMonoNL Nerd Font")
            font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
            self.setFont(font)

            #font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
            #self.setAcceptDrops(True)

            self.indent_rgba=[255, 255, 255,30]

            self.link_url=None
            self.last_completion=None
            self.connect_completion=lambda:...
            """            
            self.completer = QtWidgets.QCompleter(self)
            self.completer.setWidget(self)
            self.completer.popup().setUniformItemSizes(True)
            self.completer.activated.connect(self.insert_completion)

            # model setup
            self.completer_model = QtGui.QStandardItemModel(self)
            self.proxy_model = FuzzyProxyModel(self)
            self.proxy_model.setSourceModel(self.completer_model)
            self.completer.setModel(self.proxy_model)
            #self.delegate = HighlightDelegate(self.completer.popup())
            #self.completer.popup().setItemDelegate(self.delegate)

            # shortcut references
            self.popup = self.completer.popup()

            # connect text change
            self.textChanged.connect(self.update)

            self.completer_popup_pos = None
            """
            self.completer = QtWidgets.QCompleter(self)
            self.completer.setWidget(self)
            self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive) 
            self.completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)  
            self.completer.popup().setUniformItemSizes(True)  
            self.completer.activated.connect(self.insertCompletion)

            self.proxy_model = QtCore.QSortFilterProxyModel(self)
            #self.proxy_model=FuzzyProxyModelCompleter(self)
            self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)  
            self.completer.setModel(self.proxy_model)
            self.textChanged.connect(self.update)
            self.popup=self.completer.popup()
            
            self.completer_popup_pos=None
            self.completer_model=QtGui.QStandardItemModel(self)
            self.proxy_model.setSourceModel(self.completer_model)
            
            self.prev_hover_text_lineno:int=None
            self.prev_hover_text_colno:int=None
            self.setMouseTracking(True)
            #self.cursorPositionChanged.connect(self.onTextCursorMove)

            self.hover_text_debouncer = QtCore.QTimer()
            self.hover_text_debouncer.setInterval(600)
            self.hover_text_debouncer.setSingleShot(True)
            
            self.hover_timer_t = QtCore.QTimer()
            self.hover_timer_t.setInterval(100)
            self.hover_timer_t.setSingleShot(True)



            
            self.last_word = ""

            self.last_cursor = None
            self.last_line_no=0

            self.highlight_format = QtGui.QTextCharFormat()
            self.highlight_format.setBackground(QtGui.QColor("#5A5A48"))  # Light yellow
            self.highlighted_selections = []
            
            self.hover_text_debouncer.timeout.connect(self.handleMouseCursorHover)
            self.hover_timer_t.timeout.connect(self.handleTextCursorHover)
            
            self.numpad_area = Custom.LineNumberArea(self)
            
            self.cursorPositionChanged.connect(self.highlight_current_line)
            self.highlight_current_line()  # Initialize once

            self.current_match_format = QtGui.QTextCharFormat()
            self.current_match_format.setBackground(QtGui.QColor("#503939"))

            self._last_find_word = ""
            self._find_results: list[QtGui.QTextCursor] = []
            self._find_index = -1
    
            #self.textChanged.connect(self.onTextChanged)
            self.cursorPositionChanged.connect(self.sync_selection)
            self.cursorPositionChanged.connect(self.onCursorPositionChanged)        
            self.ctrl_hold_flag=False
            self.shift_hold_flag=False
            self.alt_hold_flag=False

            self.setAcceptDrops(False)
            self.updateCompleterFontIconSize()    
        def updateCompleterFontIconSize(self):
            self.completer.popup().setFont(self.font())
            self.completer.popup().setIconSize(QtCore.QSize(self.font().pointSize()+5,self.font().pointSize()+5))

        def sendAutoPairDetails(self, start_cursor, end_cursor, new_text):
            """Print info in LSP didChange-style format"""
            start_line = start_cursor.blockNumber()
            start_col = start_cursor.positionInBlock()
            end_line = end_cursor.blockNumber()
            end_col = end_cursor.positionInBlock()
            self.whenAutoPair.emit(start_line,start_col,end_line,end_col,new_text)


        def _handle_opening(self, ch):
            end = self.syntax_pairs[ch]
            cur = self.textCursor()
            if cur.hasSelection():
                sel = cur.selectedText()
                start = cur.selectionStart()
                endpos = cur.selectionEnd()

                cur.insertText(f"{ch}{sel}{end}")

                # log change: replacement with wrapped text
                start_cur = self.textCursor()
                start_cur.setPosition(start)
                end_cur = self.textCursor()
                end_cur.setPosition(start + len(sel) + 2)  # opener + closer
                self.sendAutoPairDetails(start_cur, end_cur, f"{ch}{sel}{end}")

                cur.setPosition(start + 1)
                cur.setPosition(start + 1 + len(sel), QtGui.QTextCursor.MoveMode.KeepAnchor)
                self.setTextCursor(cur)


                return
            
            # no selection → insert pair
            start_pos = cur.position()
            cur.insertText(ch + end)

            start_cur = self.textCursor()
            start_cur.setPosition(start_pos)
            end_cur = self.textCursor()
            end_cur.setPosition(start_pos + 2)
            self.sendAutoPairDetails(start_cur, end_cur, ch + end)

            cur.movePosition(QtGui.QTextCursor.MoveOperation.Left)
            self.setTextCursor(cur)

        def _handle_closing(self, ch):
            # If next char is the same closer, just skip over it
            if self._next_char() == ch:
                c = self.textCursor()
                c.movePosition(QtGui.QTextCursor.MoveOperation.Right)
                self.setTextCursor(c)
            else:
                super().insertPlainText(ch)
        def _handle_backspace(self) -> bool:
            c = self.textCursor()
            if c.hasSelection():
                return False
            prev_ch = self._prev_char()
            next_ch = self._next_char()
            if prev_ch and prev_ch in self.syntax_pairs and self.syntax_pairs[prev_ch] == next_ch:
                # delete both
                start_pos = c.position() - 1
                c.beginEditBlock()
                c.movePosition(QtGui.QTextCursor.MoveOperation.Left, QtGui.QTextCursor.MoveMode.KeepAnchor)
                c.deleteChar()
                c.deleteChar()
                c.endEditBlock()

                start_cur = self.textCursor()
                start_cur.setPosition(start_pos)
                end_cur = self.textCursor()
                end_cur.setPosition(start_pos + 2)
                self.sendAutoPairDetails(start_cur, end_cur, "")  # deletion
                return True
            return False
        
        def _next_char(self):
            c = self.textCursor()
            c.movePosition(QtGui.QTextCursor.MoveOperation.Right, QtGui.QTextCursor.MoveMode.KeepAnchor)
            return c.selectedText()

        def _prev_char(self):
            c = self.textCursor()
            c.movePosition(QtGui.QTextCursor.MoveOperation.Left, QtGui.QTextCursor.MoveMode.KeepAnchor)
            return c.selectedText()

        def _handle_return(self) -> bool:
            c = self.textCursor()
            prev = self._prev_char()
            nxt = self._next_char()
            indent = self._indent_of_line_before()
            # { | } pattern
            if prev == '{' and nxt == '}':
                c.beginEditBlock()
                super().insertPlainText('\n' + indent + '    ')
                # create the closing line
                closing_indent = indent
                super().insertPlainText('\n' + closing_indent)
                # move cursor back to the indented empty line
                c.movePosition(QtGui.QTextCursor.MoveOperation.Up)
                c.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine)
                c.endEditBlock()
                self.setTextCursor(c)
                return True
            # Normal newline: keep same indent
            line_before = self._current_line_text_before_cursor()
            base_indent = line_before[:len(line_before) - len(line_before.lstrip())]
            super().insertPlainText('\n' + base_indent)
            return True
        

        def _current_line_text_before_cursor(self):
            c = self.textCursor()
            col = c.positionInBlock()
            block_text = c.block().text()
            return block_text[:col]

        def _indent_of_line_before(self):
            c = self.textCursor()
            block = c.block().previous()
            if not block.isValid():
                return ""
            text = block.text()
            return text[:len(text) - len(text.lstrip())]
        
        def onCursorPositionChanged(self):
            cur,l,c=self.getCurrentLineOrColumnPos()
            self.getCursorPosition.emit(cur,l,c)
            if l!=self.last_line_no:
                self.last_line_no=l
                self.whenLinePosChangeGetLineNo.emit(l)

        def set_cursor_position(self, line, column,highlight=False):
            doc = self.document()
            
            block_count = doc.blockCount()
            line = max(0, min(line, block_count - 1))
            
            block = doc.findBlockByNumber(line)
            
            column = max(0, min(column, block.length() - 1))

            pos = block.position() + column
            
            cursor = QtGui.QTextCursor(doc)
            cursor.setPosition(pos)
            self.setTextCursor(cursor)
            self.centerCursor()
            self.setFocus()

            if highlight:
                # Move to word under cursor
                cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
                word = cursor.selectedText()

                if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                    self.blockSignals(True)
                    fmt = QtGui.QTextCharFormat()
                    fmt.setBackground(QtGui.QColor("#502929"))  # Deep red background

                    cursor.setCharFormat(fmt)
                    self.setTextCursor(cursor)  # So the user sees the selected highlight
                    self.blockSignals(False)

        def on_find_text_changed(self, text):
            self._last_find_word = ""  # Reset to re-find
            self._find_index = -1
            self._find_results = []
            self.highlight_matching_words(text)
        
        def on_find_enter(self):
            text = self.find_input.text()
            self.find_word_and_focus(text)

            
        def find_word_and_focus(self, word: str):
            
            if word != self._last_find_word:
                self._find_results = self.find_matching_words(word)
                self._find_index = -1
                self._last_find_word = word

            if not self._find_results:
                return

            self._find_index += 1
            if self._find_index >= len(self._find_results):
                self._find_index = 0

            current_cursor = self._find_results[self._find_index]
            self.setTextCursor(current_cursor)
            self.moveCursor(QtGui.QTextCursor.MoveOperation.NoMove) 
            self.ensureCursorVisible()
            self.highlight_matching_words(word, current_cursor)

            return self._find_index+1,len(self._find_results)



        def goToLine(self,line_number,set_cursor=False):


            line_number = max(1, line_number)
            doc = self.document()
            block = doc.findBlockByNumber(line_number - 1)

            if not block.isValid():
                return

            cursor = QtGui.QTextCursor(block)
            
            if set_cursor==True:
                self.setTextCursor(cursor)
                self.setFocus()
            
            else:
                self.setTextCursor(cursor)
            
            
            self.centerCursor()

        def findWords(self,word):
            #cusrors=self.find_matching_words(word)
            cursor=self.highlight_matching_words(word)

            

        def highlight_current_line(self):
            extra_selections = []

            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor(0,0,0,30)  
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

            self.setExtraSelections(extra_selections)

        def resizeEvent(self, e):
            self.numpad_area.resizeUpdate(e)
            return super().resizeEvent(e)
        
        def mouseMoveEvent(self, event):

            self.mouse_pos = event.pos()
            self.hover_text_debouncer.start()
            super().mouseMoveEvent(event)


        def focusInEvent(self, e):
            if not self.completer.popup().isVisible():
                self.whenFocusIn.emit(self)
                

            return super().focusInEvent(e)  
        
        def getCurrentLineOrColumnPos(self):
            cursor=self.textCursor()
            
            l=cursor.blockNumber()         
            c=cursor.positionInBlock()
            #self.getCursorPosition.emit(cursor,l,c)
            return cursor,l,c

        def getTextInRange(self, start_line: int, start_col: int, end_line: int, end_col: int) -> str:
            """
            Return text between (start_line, start_col) and (end_line, end_col).
            Lines are 0-based (like blockNumber).
            """
            doc = self.document()
            start_block = doc.findBlockByNumber(start_line)
            end_block = doc.findBlockByNumber(end_line)

            if not start_block.isValid() or not end_block.isValid():
                return ""

            cursor = self.textCursor()
            cursor.setPosition(start_block.position() + start_col)
            cursor.setPosition(end_block.position() + end_col, cursor.MoveMode.KeepAnchor)

            return cursor.selectedText()

        def getLineByNumber(self,line_number):
            block=self.document().findBlockByNumber(line_number)
            if block.isValid():
                return block.text()
            return None

        def getWordUnderCursor(self):
            cursor=self.textCursor()
            cursor.select(cursor.SelectionType.WordUnderCursor)
            return cursor.selectedText(),cursor

        def onTextCursorMove(self):
            
            self.hover_timer_t.start()
            
        def handleTextCursorHover(self):
            word,cursor=self.getWordUnderCursor()
            if not word:
                self.clear_highlighted_words()
                return
            """if word==self.last_word:
                return
            """
            self.last_word = word
            self.clear_highlighted_words()
           
            self.highlight_matching_words(word)
        
            #line = self.textCursor().blockNumber()
            #char = self.textCursor().columnNumber()

        def getWordUnderCursorDetail(self):
            cursor = self.textCursor()
            cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
            word=cursor.selectedText()
            if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                start_cursor = QtGui.QTextCursor(cursor)
                start_cursor.setPosition(cursor.selectionStart())

                # Get the block (line) and column (position in block) of the word start
                line_number = start_cursor.blockNumber()
                column_number = start_cursor.positionInBlock()

                # Optional: get global screen position of the word's start (for popup)
                word_rect = self.cursorRect(start_cursor)
                global_pos = self.mapToGlobal(word_rect.bottomLeft())

                # Emit word, global_pos, line, and column
                
                #self.whenMouseCursorHover.emit(word,line_number,column_number,global_pos)

            return word,line_number,column_number,global_pos
        
        def goToDefinition(self):
            word,line,column,pos=self.getWordUnderCursorDetail()
            self.whenGoToDefinitionRequest.emit(word,line,column,pos)
            
        def handleMouseCursorHover(self):

            if not hasattr(self, "mouse_pos") or self.mouse_pos is None:
                return
            
            cursor = self.cursorForPosition(self.mouse_pos)
            cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText()

            if not word:
                self.clear_highlight()
                self.whenMouseCursorLeaveHover.emit()
                return 
            """if word==self.last_word:
                return"""
            
            self.last_word = word
            self.clear_highlight()
            
            if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                start_cursor = QtGui.QTextCursor(cursor)
                start_cursor.setPosition(cursor.selectionStart())

                # Get the block (line) and column (position in block) of the word start
                line_number = start_cursor.blockNumber()
                column_number = start_cursor.positionInBlock()
                self.hover_text_debouncer.setInterval(600)

                if self.prev_hover_text_colno==column_number and self.prev_hover_text_lineno==line_number:
                    return

                self.prev_hover_text_lineno=line_number
                self.prev_hover_text_colno=column_number
                # Optional: get global screen position of the word's start (for popup)
                word_rect = self.cursorRect(start_cursor)
                global_pos = self.mapToGlobal(word_rect.bottomLeft())

                # Emit word, global_pos, line, and column
                self.whenMouseCursorTextMatch.emit(word,line_number,column_number,global_pos)

                self.highlight_cursor(cursor)
                #self.viewport().update()
            else:
                
                self.whenMouseCursorNoTextMatch.emit()
                self.hover_text_debouncer.setInterval(600)
                self.prev_hover_text_lineno=None
                self.prev_hover_text_colno=None
                
                print("kjdakjdhadjsda")
            
            # Simulated hover content (replace with LSP hover request):

            #QToolTip.showText(self.mapToGlobal(self.mouse_pos), hover_text)

        def highlight_cursor(self, cursor):
            
            self.blockSignals(True)
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QtGui.QColor("#502929")) 
            
            cursor.setCharFormat(fmt)
            self.last_cursor = cursor

            self.blockSignals(False)

        def clear_highlight(self,cursor=None):
            if cursor==None:
                cursor=self.last_cursor
                
            self.blockSignals(True)
            
            if cursor:
                fmt = QtGui.QTextCharFormat()
                fmt.setBackground(QtGui.QColor("transparent"))
                cursor.setCharFormat(fmt)
                cursor = None
            self.blockSignals(False)
            
        def find_matching_words(self, word: str):
            cursors = []
            if not word:
                return cursors

            pattern = r'\b' + re.escape(word)
            text = self.toPlainText()
            for match in re.finditer(pattern, text):
                cursor = QtGui.QTextCursor(self.document())
                cursor.setPosition(match.start())
                cursor.setPosition(match.end(), QtGui.QTextCursor.MoveMode.KeepAnchor)
                cursors.append(cursor)
            return cursors
        
        def highlight_matching_words(self, word: str, current_cursor: QtGui.QTextCursor = None):
            self.clear_highlighted_words()
            if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                return

            cursors = self.find_matching_words(word)
            selections = []

            for cursor in cursors:
                selection = QtWidgets.QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format = self.highlight_format  # green
                selections.append(selection)

            if current_cursor:
                current_selection = QtWidgets.QTextEdit.ExtraSelection()
                current_selection.cursor = current_cursor
                current_selection.format = self.current_match_format  # red
                selections.append(current_selection)

            self.highlighted_selections = selections
            self.setExtraSelections(selections)
        
        def clear_highlighted_words(self):
            self.blockSignals(True)
            self.setExtraSelections([])
            self.highlighted_selections.clear()
            self.highlight_current_line()
            self.blockSignals(False)

        def paintEvent(self, event):
            super().paintEvent(event)

            painter = QtGui.QPainter(self.viewport())
            painter.setPen(QtGui.QColor(*self.indent_rgba))

            font_metrics = QtGui.QFontMetrics(self.font())
            char_width = font_metrics.horizontalAdvance(' ')

            block = self.firstVisibleBlock()
            offset = self.contentOffset()
            scroll_x = self.horizontalScrollBar().value()  # <-- This is the fix

            visible_blocks = 0
            max_blocks = 100  # Limit for performance

            while block.isValid() and visible_blocks < max_blocks:
                text = block.text()
                indent_level = (len(text) - len(text.lstrip())) // 4

                if indent_level > 0:
                    rect = self.blockBoundingGeometry(block).translated(offset)
                    for i in range(indent_level):
                        x_pos = i * char_width * 4 - scroll_x  # Adjust x with horizontal scroll
                        painter.drawLine(x_pos, int(rect.top()), x_pos, int(rect.bottom()))

                block = block.next()
                visible_blocks += 1

            painter.end()

                    
        def dragEnterEvent(self,event:QtGui.QDragEnterEvent):
            
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
                
            elif event.mimeData().hasText():
                event.acceptProposedAction()
                
            
            else:
                event.ignore()

        def dragMoveEvent(self,event:QtGui.QDragEnterEvent):
            event.acceptProposedAction()

        def dropEvent(self,event:QtGui.QDropEvent):
            
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    file_path=url.toLocalFile()
                    self.link_url(file_path)

                    with open(file_path,'r')as file:
                        self.setPlainText(file.read())
                        file.close()

                event.acceptProposedAction()
            
            elif event.mimeData().hasText():    
                dropped_text=event.mimeData().text()
                self.insertPlainText(dropped_text)
                event.acceptProposedAction()
        
            else:
                super().dropEvent(event)
        
        def insertCompletion(self,completion:str):
            self.last_completion=completion
            self.connect_completion()
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.StartOfWord,cursor.MoveMode.KeepAnchor)
            s_col=cursor.columnNumber()
            if completion.startswith(" "):
                completion=completion[1:]
                cursor.insertText(completion)
                e_col=cursor.columnNumber()-2
            else:
                cursor.insertText(completion)
                e_col=cursor.columnNumber()-1
                
            print(cursor.columnNumber())
            self.whenCompletionInsert.emit(cursor.blockNumber(),s_col,cursor.blockNumber(),e_col,completion)

            self.setTextCursor(cursor)
            
        def keyPressEvent(self, event:QtGui.QKeyEvent):
        
            
            if self.completer.popup().isVisible():
                # If the completer popup is open, handle special keys
                if event.key() in (QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Return):
                    # Get the current item from the popup
                    current_index = self.completer.popup().currentIndex()
                    if current_index.isValid():
                        completion = current_index.data()
                        self.insertCompletion(completion)
                        self.completer_model.clear()
                        self.notifyOnKeyStrock.emit()
                          # Insert the selected completion
                    self.completer.popup().hide()  # Close the popup
                    return  # Consume the event to prevent default behavior
                elif event.key() == QtCore.Qt.Key.Key_Escape:
                    self.completer.popup().hide()  # Close the popup
                    return
                elif event.key() in (QtCore.Qt.Key.Key_Up, QtCore.Qt.Key.Key_Down):
                    # Allow navigation within the popup
                    return super().keyPressEvent(event)


            

            if event.key() in (
                QtCore.Qt.Key.Key_Up,
                QtCore.Qt.Key.Key_Down,
                QtCore.Qt.Key.Key_Left,
                QtCore.Qt.Key.Key_Right
                ):

                self.onTextCursorMove()
                #self.highlight_current_line()
            else:
                self.clear_highlighted_words()


            if event.key()==QtCore.Qt.Key.Key_F12:
                self.goToDefinition()
            if event.modifiers()==QtCore.Qt.KeyboardModifier.ShiftModifier and event.key()==QtCore.Qt.Key.Key_F12:
                self.when_Key_SHIFT_F12_Pressed.emit()



            ##############################################################################
            cur, l, c = self.getCurrentLineOrColumnPos()
            char = event.text()

            if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):

                self.getCursorPosition.emit(cur,l,c)
                self.when_Key_Enter_pressed.emit()

                cursor=self.textCursor()
                current_line = cursor.block().text()
                
                leading_spaces = len(current_line) - len(current_line.lstrip(' '))
                cursor.insertText("\n" + " " * leading_spaces)
                self.ensureCursorVisible()
                line=cursor.blockNumber()
                col=cursor.columnNumber()
                self.when_Key_Enter_Pressed_V2.emit(line,col,line,col,"\n" + " " * leading_spaces)
                return
            if event.modifiers()==QtCore.Qt.KeyboardModifier.ControlModifier:
                if self.ctrl_hold_flag==False:
                    self.ctrl_hold_flag=True
            else:
                if self.ctrl_hold_flag==True:
                    self.ctrl_hold_flag=False

            if event.modifiers()==QtCore.Qt.KeyboardModifier.ShiftModifier:
                if self.shift_hold_flag==False:
                    self.shift_hold_flag=True
            else:
                if self.shift_hold_flag==True:
                    self.shift_hold_flag=False

            if event.modifiers()==QtCore.Qt.KeyboardModifier.AltModifier:
                if self.alt_hold_flag==False:
                    self.alt_hold_flag=True
            else:
                if self.alt_hold_flag==True:
                    self.alt_hold_flag=False

        
            if event.key() == QtCore.Qt.Key.Key_Backspace and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                cur=self.textCursor()
                e_line=cur.blockNumber()
                e_col=cur.columnNumber()
                super().keyPressEvent(event)

                self.when_Key_Ctrl_BackSpace_Pressed.emit()
                self.when_Key_Ctrl_BackSpace_Pressed_V2.emit(cur.blockNumber(),cur.columnNumber(),e_line,e_col,"")
                self.notifyOnKeyStrock.emit()
                    
                return

            elif event.key() == QtCore.Qt.Key.Key_Backspace:
                self.when_Key_BackSpace_Pressed.emit()
            
            elif event.key() == QtCore.Qt.Key.Key_C and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.when_Key_Ctrl_c_pressed.emit()

            elif event.key() == QtCore.Qt.Key.Key_V and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.when_Key_Ctrl_v_pressed.emit()
            
            elif event.key() == QtCore.Qt.Key.Key_A and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.when_Key_Ctrl_a_pressed.emit()

            elif event.key() == QtCore.Qt.Key.Key_Z and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.when_Key_Ctrl_z_pressed.emit()
            
            elif event.key() == QtCore.Qt.Key.Key_Z and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
                self.when_Key_Ctrl_Shift_z_pressed.emit()
            
            elif event.key() == QtCore.Qt.Key.Key_S and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
                self.when_Key_Ctrl_s_pressed.emit()
            
            elif event.key() == QtCore.Qt.Key.Key_Delete:
                if self.shift_hold_flag:
                    self.when_Key_Shift_delete_pressed.emit()
                else:
                    self.when_Key_delete_pressed.emit()
            
            elif event.key() == QtCore.Qt.Key.Key_Tab:
                if self.shift_hold_flag:
                    self.when_Key_Shift_Tab_pressed.emit()
                    return
                else:
                    self.getCursorPosition.emit(cur, l, c)
                    self.when_Key_Tab_pressed.emit()
                    cursor_pos=self.textCursor()
                    cursor_pos.insertText(" " * 4)
                    #self.target.setCursorPosition(cursor_pos + 4)
                    #self.ensureCursorVisible()
                    return
            
            

            elif event.key() == QtCore.Qt.Key.Key_PageUp:
                if self.shift_hold_flag:
                    self.when_Key_Shift_PageUp_pressed.emit()
                else:
                    self.when_Key_PageUp_pressed.emit()


            elif event.key() == QtCore.Qt.Key.Key_PageDown:
                if self.shift_hold_flag:
                    self.when_Key_Shift_PageDown_pressed.emit()
                else:
                    
                    self.when_Key_PageDown_pressed.emit()


            elif event.key() == QtCore.Qt.Key.Key_Up and event.modifiers()!=QtCore.Qt.KeyboardModifier.ShiftModifier:
                if self.ctrl_hold_flag:
                    self.when_Key_Ctrl_Up_pressed.emit()
                    #self.highlight_current_line()
                else:
                    self.when_Key_Up_pressed.emit()

            
            elif event.key() == QtCore.Qt.Key.Key_Down and event.modifiers()!=QtCore.Qt.KeyboardModifier.ShiftModifier:
                if self.ctrl_hold_flag:
                    self.when_Key_Ctrl_Down_pressed.emit()
                else:
                    self.when_Key_Down_pressed.emit()


            elif event.key() == QtCore.Qt.Key.Key_Left and event.modifiers()!=QtCore.Qt.KeyboardModifier.ShiftModifier:
                if self.ctrl_hold_flag:
                    self.when_Key_Ctrl_Left_pressed.emit()
                else:
                    self.when_Key_Left_pressed.emit()
            
            
            elif event.key() == QtCore.Qt.Key.Key_Right and event.modifiers()!=QtCore.Qt.KeyboardModifier.ShiftModifier:
                if self.ctrl_hold_flag:
                    self.when_Key_Ctrl_Right_pressed.emit()
                else:
                    self.when_Key_Right_pressed.emit()
            
            
                """
            elif event.key() in (QtCore.Qt.Key.Key_Up,
                            QtCore.Qt.Key.Key_Down,
                            QtCore.Qt.Key.Key_Left,
                            QtCore.Qt.Key.Key_Right) and event.modifiers()!=QtCore.Qt.KeyboardModifier.ShiftModifier:
                cur, l, c = self.getCurrentLineOrColumnNumber()
                self.takeEachWord.emit(cur, l, c)
            """
                

            elif char:
                self.getCursorPosition.emit(cur, l, c)
                self.getCharWhenType.emit(char)
                self.getCursorPosition.emit(cur, l, c)

            t_charecter = event.text()
            key = event.key()
            modifiers = event.modifiers()

            # Let Ctrl/Alt shortcuts pass through untouched 

            if modifiers & (QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.AltModifier):
                return super().keyPressEvent(event)

            if t_charecter in self.syntax_pairs:
                self._handle_opening(t_charecter)
                return

            if t_charecter in self.closers:
                self._handle_closing(t_charecter)
                return

            if key == QtCore.Qt.Key.Key_Backspace:
                if self._handle_backspace():
                    return

            if key in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                if self._handle_return():
                    return
                
            super().keyPressEvent(event)

            self.notifyOnKeyStrock.emit()
            
            if t_charecter and key!=QtCore.Qt.Key.Key_Backspace:
                print(f"'{t_charecter}' - char")
                self.whenOnlyAplphaNemuricKeyPressed.emit(t_charecter)

            elif t_charecter and key==QtCore.Qt.Key.Key_Backspace:
                print(f"'{t_charecter}' - char")
                self.whenOnlyAplphaNemuricKeyPressed.emit(t_charecter)
                

        def sync_selection(self):
            cursor = self.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                self.selectionChanged.emit(start, end)


        def onTextChanged(self,completion_len):
            cursor = self.textCursor()
            cursor.select(cursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText().strip()

            print("word ",word)
            
            if True:
                self.proxy_model.setFilterFixedString(word)
                #self.completer.setCompletionPrefix(word)
                
                rect = self.cursorRect()
                #global_pos = self.mapToGlobal(rect.bottomRight())
                #global_pos.setX(global_pos.x() + 85)  
                #global_pos.setY(global_pos.y() + 10)  
                rect = self.cursorRect()
                rect.translate(85, 10)
                #print("on txt chae ",self.completer_popup_pos) 
                
                """popup_width = (
                    self.completer.popup().sizeHintForColumn(0) +
                    self.completer.popup().verticalScrollBar().sizeHint().width()
                )
                """
                popup=self.completer.popup()
                
                if completion_len>=12:
                    
                    self.completer.popup().setFixedHeight(300)
                    
                else:
                    size_h=popup.sizeHintForRow(0)
                    self.completer.popup().setFixedHeight((size_h+3)*completion_len)
                    
                    #print("less", size_h, completion_len,(size_h+5)*completion_len)

                self.completer.popup().setFixedWidth(300)
                #popup.setMaximumWidth(500)
                self.completer.complete(rect)
                #self.completer.popup().move(global_pos)
                #self.completer_popup_pos=global_pos
                #self.completer.popup().show()
            """else:
                if self.completer.popup().isVisible():
                    
                    self.completer.popup().hide()
"""

        def enterEvent(self, event):
            self.whenMouseEnter.emit()
            return super().enterEvent(event)


        def setCompletions(self,completion_result,wich_lsp):
            time_tracker.start()
            if len(completion_result)!=0:
                self.completer_model.clear()


            print("cccccccc seteddd d d d d d d")
            for completion in completion_result:
                
                #suggestions.append((item.get("label"),item.get("kind")))
                #print("compl -----  \n\n",completion)    

                item = QtGui.QStandardItem()
                if wich_lsp=="py":
                    item.setText(completion.get("insertText",""))
                else:
                    item.setText(completion.get("filterText",""))

                kind_icon = self.Path_h.COMPLITION_KIND_INCONS_LIST.get(completion.get("kind"), self.Path_h.COMPLITION_KIND_INCONS_LIST[0])
                item.setIcon(QtGui.QIcon(kind_icon))
                self.completer_model.appendRow(item)

            if self.completer_model.rowCount() > 0:
                first_index = self.completer_model.index(0, 0)
                self.popup.setCurrentIndex(first_index)

            #self.proxy_model.setSourceModel(self.completer_model)
            #self.completer.popup().move(self.completer_popup_pos)
            
            time_tracker.stop()

            #size=self.completer.popup().sizeHintForRow(0)
            #print(size,"size")
            #self.completer.popup().setFixedHeight(self.completer_model.rowCount()*size)
            #time_tracker.report("compliter time : ")
            #self.onTextChanged()
            """first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)
            first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)
            first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)
            first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)"""
            
        #def con(self,fl):print(fl)

    class TextEditStyleSheetManager(QtWidgets.QPlainTextEdit):
        def __init__(self):
            super().__init__()
            self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

            #self.highlighter = ColorBasedHashHighlighter(self.document())
            self.hex_pattern = re.compile(r"#([0-9a-fA-F]{6})")
            self.color_dialog=QtWidgets.QColorDialog()    
            self.tag_cursor=None
            self.tag_full_pos=None
            
        def mousePressEvent(self, event: QtGui.QMouseEvent):
            super().mousePressEvent(event)  # keep default behavior
            cursor = self.cursorForPosition(event.position().toPoint())
            block = cursor.block()
            block_pos = block.position()
            text = block.text()
            click_pos = cursor.position() - block_pos

            for match in self.hex_pattern.finditer(text):
                hash_pos_in_block = match.start()
                full_pos = block_pos + hash_pos_in_block

                # Check if the click is exactly on '#'
                if full_pos == cursor.position():
                    old_code = match.group(0)
                    color = QtGui.QColor(old_code)
                    self.tag_cursor=cursor
                    self.tag_full_pos=full_pos

                    #new_color = QColorDialog.getColor(color, self)

                    new_color=self.color_dialog.setCurrentColor(color)
                    self.color_dialog.currentColorChanged.connect(self.changeColor)
                    self.color_dialog.show()
                    
                    # stop after first replacement

        def changeColor(self,new_color):
            if new_color.isValid():
                self.tag_cursor.setPosition(self.tag_full_pos)
                self.tag_cursor.setPosition(self.tag_full_pos + 7, QtGui.QTextCursor.MoveMode.KeepAnchor)
                self.tag_cursor.insertText(new_color.name())
                return  
            
        def wheelEvent(self, event: QtGui.QWheelEvent):
            cursor = self.cursorForPosition(self.mapFromGlobal(self.cursor().pos()))
            cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText()

            # Find number within the word
            match = re.search(r"\d+", word)
            if match:
                number = int(match.group())
                delta = 1 if event.angleDelta().y() > 0 else -1
                new_number = max(0, number + delta)

                # Replace only the number in the word
                start = match.start()
                end = match.end()
                new_word = word[:start] + str(new_number) + word[end:]
                #print(new_number)
                cursor.insertText(new_word)
            else:
                super().wheelEvent(event)


    class TextEditPopup(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent, QtCore.Qt.WindowType.ToolTip)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)
            self.setWindowFlags(QtCore.Qt.WindowType.ToolTip)

            self.popup_text_edit = QtWidgets.QTextEdit()
            self.popup_text_edit.setReadOnly(True)
            self.popup_text_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.popup_text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.popup_text_edit.setWordWrapMode(QtGui.QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
            self.popup_text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #3B3B3B;
                    border-bottom: 1px solid #ffdba2;
                    border-radius: 0px;
                }
            """)
            self.popup_text_edit.setFont(QtGui.QFont("JetBrainsMonoNL Nerd Font",12))            
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(self.popup_text_edit)
            layout.setContentsMargins(0, 0, 0, 0)

            # Optional: drop shadow like VS Code
            #effect = QtWidgets.QGraphicsDropShadowEffect(self)
            #effect.setBlurRadius(10)
            #effect.setOffset(0, 3)
            #effect.setColor(QtGui.QColor(0, 0, 0, 160))
            #self.setGraphicsEffect(effect)

    class PopupSignature(TextEditPopup):
        def __init__(self, parent=None):
            from CodeDock.Code.src.controllers.CodePadHighlighter import SignatureHighlighter,PythonHighlighter
            super().__init__()            

            self.highlighter=SignatureHighlighter(self.popup_text_edit.document())

        def setSignature(self, sig_response: dict, editor: QtWidgets.QTextEdit):
            result = sig_response.get("result", {})
            signatures = result.get("signatures", [])
            if not signatures:
                return

            sig_index = result.get("activeSignature", 0)
            param_index = result.get("activeParameter", 0)

            if not (0 <= sig_index < len(signatures)):
                return

            signature = signatures[sig_index]
            label = signature.get("label", "")
            sig_doc = signature.get("documentation", {}).get("value", "")
            params = signature.get("parameters", [])

            # Only show current signature's label and doc (like VS Code)
            combined = label.strip()
            if sig_doc:
                sig_doc = sig_doc.replace("```", "").strip()
                combined += "\n\n" + sig_doc

            self.popup_text_edit.setPlainText(combined)


            # Highlight only the active param
            if 0 <= param_index < len(params):
                param_label = params[param_index].get("label", "")
                self.highlighter.set_active_param(param_label)
            else:
            
                self.highlighter.set_active_param(None)

            self.auto_size()


            
            # Position above cursor
            cursor_rect = editor.cursorRect()
            global_cursor_pos = editor.mapToGlobal(cursor_rect.topLeft())
            popup_height=self.height()
            # Optional offsets (adjust as needed)
            global_cursor_pos.setX(global_cursor_pos.x() + 80)

            global_cursor_pos.setY(abs(global_cursor_pos.y()-popup_height))

            self.move(global_cursor_pos)
            self.show()

        def auto_size(self):
            font_matrix=QtGui.QFontMetrics(self.popup_text_edit.font())

            lines=self.popup_text_edit.toPlainText().splitlines()
            # Find the width of the longest line
            widest_width=max(font_matrix.horizontalAdvance(line) for line in lines)
            #font_matrix.horizontalAdvance(self.popup_text_edit.toPlainText())
            text_hight=font_matrix.lineSpacing()*len(lines)
            #doc = self.popup_text_edit.document()
            #doc.setTextWidth(500)  # max width
            #size = doc.size().toSize()
            if len(lines)<=3:

                self.setFixedWidth(widest_width+30)  # cap height
                self.setFixedHeight(text_hight-10)
            else:
                self.setFixedWidth(widest_width+30)  # cap height
                self.setFixedHeight(text_hight+30)


        
    class PopupHover(TextEditPopup):
        def __init__(self, parent=None):
            super().__init__()
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)
            l_n=None

        def show_popup(self,text,pos:QtCore.QPoint):
            self.popup_text_edit.setPlainText(text)
            #cursor_pos = text_edit.mapToGlobal(text_edit.cursorRect().bottomRight())
        
            font_matrix=QtGui.QFontMetrics(self.popup_text_edit.font())


            
            lines=self.popup_text_edit.toPlainText().splitlines()
            # Find the width of the longest line
            widest_width=max(font_matrix.horizontalAdvance(line) for line in lines)
            #font_matrix.horizontalAdvance(self.popup_text_edit.toPlainText())
            text_hight=font_matrix.lineSpacing()*len(lines)
            #doc = self.popup_text_edit.document()
            #doc.setTextWidth(500)  # max width
            #size = doc.size().toSize()
            if len(lines)<=3:

                self.setFixedWidth(widest_width+25)  # cap height
                self.setFixedHeight(text_hight-10)
            else:
                self.setFixedWidth(widest_width+25)  # cap height
                self.setFixedHeight(text_hight+10)

            
            popup_height=self.height()
            # Optional offsets (adjust as needed)
            pos.setX(pos.x() + 80)

            pos.setY(abs(pos.y()-popup_height)-10)

            self.move(pos)
            self.show()



    class TabBar(QtWidgets.QTabBar):
        whenDoubleClick=QtCore.pyqtSignal(int)
        def __init__(self,parent=None):
            super().__init__(parent)
            self.setMovable(True)

            self.bg_clr="#3B515D"
            self.brdr_clr="none"
            self.tab_clr="#3B515D"
            self.tab_brdr_size=1
            self.brdr=["green","red"]
            self.tab_hover_clr="#767677"
            self.tab_selected_clr="#141618"
            self.font_clr="#52B7EC"
            self.selected_font_clr="#000000"
            self.tab_brdr=None
            self.font=None        
            self.tab_radius=0
            self.tab_padding_tb=4
            self.tab_padding_rl=6
            self.tab_size_flag=False
            self.tab_w=60
            self.tab_h=30

            self.tabbar_h=28

            self.setIconSize(QtCore.QSize(14,14))
            #self.setTabsClosable(True)
            #self.setMouseTracking(True)

            self.tab_hover_index=None

        def mouseMoveEvent(self, event):
            index = self.tabAt(event.pos())
            
            if self.tab_hover_index!=index:
                self.tab_hover_index=index
 

            super().mouseMoveEvent(event)

        def hoverCloseBtn(self):
            for i in range(self.count()):
                btn = self.tabButton(i, QtWidgets.QTabBar.ButtonPosition.RightSide)
                if btn:
                    btn.setVisible(i == self.tab_hover_index)
        
        def leaveEvent(self, event):
            pass
            #self.tab_hover_index = -1
            #self.hoverCloseBtn()
            #super().leaveEvent(event)


        def getVarDict(self):
            return {'bg_clr':self.bg_clr,
                    'brdr_clr':self.brdr_clr,
                    'tab_clr': self.tab_clr,
                    'tab_brdr_clr': self.brdr, 
                    'tab_hover_clr': self.tab_hover_clr, 
                    'tab_selected_clr': self.tab_selected_clr,
                    'selected_font_clr':self.selected_font_clr,
                    'font_clr': self.font_clr, 
                    'tab_brdr': self.tab_brdr, 
                    'font': self.font, 
                    'tab_radius': self.tab_radius, 
                    'tab_padding_tb': self.tab_padding_tb, 
                    'tab_padding_rl': self.tab_padding_rl,
                    'tab_size_flag':self.tab_size_flag,
                    'tab_w':self.tab_w,
                    'tab_h':self.tab_h,
                    'tabbar_h':self.tabbar_h
                    }

        def tabSizeHint(self, index):
            if self.tab_size_flag==True:

                return QtCore.QSize(self.tab_w,self.tab_h)
            else:return super().tabSizeHint(index)

        def updateVar(self,obj,dict):
            
            obj.bg_clr=dict["bg_clr"]
            obj.brdr_clr=dict["brdr_clr"]
            obj.tab_clr=dict["tab_clr"]
            obj.tab_brdr_clr=dict["tab_brdr_clr"]
            obj.tab_hover_clr=dict["tab_hover_clr"]
            obj.tab_selected_clr=dict["tab_selected_clr"]
            #obj.selected_font_clr=dict["selected_font_clr"]
            obj.font_clr=dict["font_clr"]
            obj.tab_brdr=dict["tab_brdr"]
            obj.font=dict["font"]
            obj.tab_radius=dict["tab_radius"]
            obj.tab_padding_tb=dict["tab_padding_tb"]
            obj.tab_padding_rl=dict["tab_padding_rl"]
            #obj.tab_size_flag=dict["tab_size_flag"]
            #obj.tab_w=dict["tab_w"]
            #obj.tab_h=dict["tab_h"]
            obj.applyStyle()
            obj.update()

        def applyStyle(self):
            
            self.setStyleSheet(f"""
                            
                QTabWidget {{
                    border: 0px solid {self.brdr_clr};
                    background-color: {self.bg_clr};
                }}
                QTabBar::tab {{
                    background: {self.tab_clr};
                    color: {self.font_clr};
                    font-size:14px;
                    border-bottom: {self.tab_brdr_size}px solid {self.brdr[1]};                    
                    border-radius: {self.tab_radius};
                    padding: {self.tab_padding_tb}px {self.tab_padding_rl}px;
                    margin-right: 2px;
                }}
                QTabBar::tab:selected {{
                    background: {self.tab_selected_clr};
                    border-bottom: {self.tab_brdr_size}px solid {self.brdr[0]};
                    color:{self.selected_font_clr};
                    
                }}
                QTabBar::tab:hover {{
                    background: {self.tab_hover_clr};
                }}
                
            """)
            
        
        def mouseDoubleClickEvent(self, event):
            """Handle double-click events."""
            tab_index=self.tabAt(event.position().toPoint())
            self.whenDoubleClick.emit(tab_index)


    class TreeView(QtWidgets.QTreeView):
        def __init__(self, parent=None):
            super().__init__()
            self.bg_clr=None
            self.brdr_clr=None
            self.btn_clr=None
            self.font_clr='#ffffff'
            self.btn_brdr_clr=None
            self.btn_hover=None

            self.font_size=14
            self.brdr_think=0
            self.brdr_radius=0
            self.btn_brdr_think=0
            self.btn_brdr_radius=0

            self.cr_path=None
            self.od_path=None

            self.scroll_bar_clr="blue"
            self.scroll_handel_clr="yellow"
            
            self.connect_url_droper=lambda:...
            self.item_font = QtGui.QFont()
            self.item_font.setPointSize(self.font_size)  # Set font size
            self.setFont(self.item_font)
            self.setIconSize(QtCore.QSize(self.font_size,self.font_size))
            #self.setIconSize(QtCore.QSize(14, 4))
            self.header().setHidden(True)

        

        def getVarDict(self):
            return {'bg_clr':self.bg_clr,
                    'brdr_clr':self.brdr_clr,
                    'btn_clr':self.btn_clr,
                    'font_clr':self.font_clr,
                    'font_size':self.font_size,
                    'btn_brdr_clr':self.btn_brdr_clr,
                    'btn_hover':self.btn_hover,
                    'scroll_bar_clr':self.scroll_bar_clr,
                    'scroll_handel_clr':self.scroll_handel_clr
                    }
        def updateVar(self,TreeView,dict):
            TreeView.bg_clr=dict["bg_clr"]
            TreeView.brdr_clr=dict["brdr_clr"]
            TreeView.btn_clr=dict["btn_clr"]
            TreeView.font_clr=dict["font_clr"]
            TreeView.font_size=dict["font_size"]
            TreeView.btn_brdr_clr=dict["btn_brdr_clr"]
            TreeView.btn_hover=dict["btn_hover"]
            TreeView.scroll_bar_clr=dict["scroll_bar_clr"]
            TreeView.scroll_handel_clr=dict["scroll_handel_clr"]
            
        def dragEnterEvent(self, event):
            if event.mimeData().hasUrls():  # Ensure dragged item has URLs
                event.acceptProposedAction()
            else:
                event.ignore()

        def dragMoveEvent(self, event):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
            else:
                event.ignore()
        def dropEvent(self, event):
            mime_data = event.mimeData()
            if mime_data.hasUrls():
                urls = mime_data.urls()
                for url in urls:
                    folder_path = url.toLocalFile()
                    if folder_path:  # Ensure a valid local path is retrieved
                        #print(f"Dropped folder: {folder_path}")  # Debugging output
                        #self.model().setRootPath(folder_path)  # Set new root path
                        #self.setRootIndex(self.model().index(folder_path))  # Update view
                        self.connect_url_droper(folder_path)
                        event.acceptProposedAction()
                        return  # Stop processing after first valid folder drop
            event.ignore()  # If no valid folder is found

        
        def applyStyle(self):
            
                
            self.setStyleSheet(f"""
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
                QTreeView {{
                    background-color: {self.bg_clr};  /* Dark background */
                    color: {self.font_clr};            /* Light text */
                    border: {self.brdr_think}px solid {self.brdr_clr};
                    border-radius: {self.brdr_radius};

                }}
                QTreeView::item {{
                    background-color: {self.btn_clr};  /* Set the background color */
                    border: {self.btn_brdr_think}px solid {self.btn_brdr_clr};
                    border-radius:{self.btn_brdr_radius};     /* Optional: Add borders */
                    
                }}
                QTreeView::item:hover {{
                    background-color: #4c566a; /* Highlight on hover */
                }}
                QTreeView::item:selected {{
                    background-color: #88c0d0; /* Highlight selected item */
                    color: none;
                }}
            
                
                QTreeView::branch:has-children:!has-siblings:closed,
                QTreeView::branch:closed:has-children:has-siblings {{
                    border-image: none;
                    image: url('{self.cr_path}'); /* Path to custom closed arrow image */
                }}

                QTreeView::branch:open:has-children:!has-siblings,
                QTreeView::branch:open:has-children:has-siblings  {{
                    border-image: none;
                    image: url('{self.od_path}'); /* Path to custom open arrow image */
                }}
                                QScrollBar::add-line, QScrollBar::sub-line {{
                    border: none; 
                    background: none;
                    
                }}
                
                                                        
        """)
            

    class StandardItemModel(QtGui.QStandardItemModel):
        def __init__(self,parent=None):
            super().__init__()


    class FileSystemModel(QtGui.QFileSystemModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.f_icons={}

        def data(self, index, role):
            if role==QtCore.Qt.ItemDataRole.DecorationRole:
                file_path=self.filePath(index)
                extension=file_path[file_path.rfind("."):]
                #if self.isDir(index):
                    #return QtGui.QIcon(self.f_icons['folder'])
                if extension in self.f_icons:
                    self.f_icons[extension]
                    return QtGui.QIcon(self.f_icons[extension])
                
            return super().data(index,role)
        
    class FuzzyFilterProxyModel(QtCore.QSortFilterProxyModel):
        def __init__(self, parent=None):
            super().__init__(parent)
            self._pattern = ""

        def fuzzy_match_score(self,word, pattern):
            
            pattern = '.*?'.join(map(re.escape, pattern))
            regex = re.compile(pattern, re.IGNORECASE)
            match = regex.search(word)
            if match:
                return len(match.group())
            return float('inf')

        def setFilterFixedString(self, pattern):
            self._pattern = pattern
            self.invalidateFilter()

        def filterAcceptsRow(self, source_row, source_parent):
            if not self._pattern:
                return True

            index = self.sourceModel().index(source_row, 0, source_parent)
            text = index.data(QtCore.Qt.ItemDataRole.DisplayRole)
            return self.fuzzy_match_score(text, self._pattern) != float('inf')

        def lessThan(self, left, right):
            left_text = left.data()
            right_text = right.data()
            return self.fuzzy_match_score(left_text, self._pattern) < self.fuzzy_match_score(right_text, self._pattern)

    class InputBox(QtWidgets.QLineEdit):
        def __init__(self):
            super().__init__()
            self.bg_clr="none"
            self.text_clr="none"
            self.brdr_clr="none"
            self.hover_clr="none"
            self.focus_in_clr="none"
            self.brdr_think=1
            self.brdr_radius=0
            self.font_size=14
            
            self.w=100
            self.h=40
            
        def applyStyle(self):
            self.setStyleSheet(f"""
                    QLineEdit {{
                        border: {self.brdr_think}px solid {self.brdr_clr};
                        border-radius: {self.brdr_radius}px;
                        background-color: {self.bg_clr};
                        color: {self.text_clr};
                        font-size: {self.font_size}px;
                    }}

                    QLineEdit:hover {{
                        border: {self.brdr_think}px solid {self.hover_clr};
                    }}

                    QLineEdit:focus {{
                        border: {self.brdr_think}px solid {self.focus_in_clr};
                        
                    }}
                               
                """)
            
        def updateVar(self,dict):
            self.bg_clr=dict["bg_clr"]
            self.text_clr=dict["text_clr"]
            self.brdr_clr=dict["brdr_clr"]
            self.hover_clr=dict["hover_clr"]
            self.focus_in_clr=dict["focus_in_clr"]
            self.brdr_think=dict["brdr_think"]
            self.brdr_radius=dict["brdr_radius"]
            self.font_size=dict["font_size"]

    class FindInputBox(InputBox):
        def __init__(self):
            super().__init__()
            self.brdr_clr="#478D76"
            self.focus_in_clr="#32A160"
            self.text_clr="#ffffff"
            self.applyStyle()

            self.setFixedWidth(150)
            
        def keyPressEvent(self, event):
            if event.key()==QtCore.Qt.Key.Key_Return:
                
                pass
            if event.modifiers()==QtCore.Qt.KeyboardModifier.ShiftModifier and event.key()==QtCore.Qt.Key.Key_Return:
                
                pass
            
            else:
                return super().keyPressEvent(event)
             
        
        

    class FindInputBar(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.layout=QtWidgets.QHBoxLayout()
            self.find_input_box=Custom.FindInputBox()
            self.find_input_box.setPlaceholderText(" find")
            self.find_input_box.setFixedWidth(150)
            
            self.find_filter_btn=Custom.PushButton()
            self.find_filter_btn.setText("A-a")
            
            
            self.spin_box=QtWidgets.QSpinBox()
            self.spin_box.setButtonSymbols(QtWidgets.QSpinBox.ButtonSymbols.NoButtons)

            self.out_of_label=QtWidgets.QLabel(self)

            self.find_up=Custom.PushButton()
            self.find_up.setText("<")

            self.find_down=Custom.PushButton()
            self.find_down.setText(">")

            self.layout.addWidget(self.find_input_box)
            self.layout.addWidget(self.find_filter_btn)
            self.layout.addWidget(self.spin_box)
            self.layout.addWidget(self.out_of_label)
            self.layout.addWidget(self.find_up)
            self.layout.addWidget(self.find_down)

            self.setLayout(self.layout)

            self.layout.setContentsMargins(0,0,0,0) 
            
        
        


    #Testing
    class GoToInputBar(InputBox):
        
        when_Esc_KeyPressed=QtCore.pyqtSignal()

        def __init__(self):
            super().__init__()
            #self.bg_clr="#339285"
            self.brdr_clr="#478D76"
            self.focus_in_clr="#32A160"
            self.text_clr="#ffffff"
            self.applyStyle()
            self.setPlaceholderText("Go To")
            self.setFixedWidth(100)
        
        def focusOutEvent(self, a0):
            self.hide()
            return super().focusOutEvent(a0)
        def focusInEvent(self, a0):
            self.show()
            return super().focusInEvent(a0)
        
        def keyPressEvent(self, a0):
            if a0.key()==QtCore.Qt.Key.Key_Escape:
                self.when_Esc_KeyPressed.emit()

            else:
                return super().keyPressEvent(a0)



    class PushButton(QtWidgets.QPushButton):
        whenCursorEnter=QtCore.pyqtSignal()
        whenCursorLeave=QtCore.pyqtSignal()

        def __init__(self,parent=None):
            super().__init__(parent)
            self.bg_clr="none"
            self.text_clr="none"
            self.brdr_clr="none"
            self.hover_clr="#464E53"
            self.pressed_clr="#1E252F"
            
           
            self.brdr_radius=0
            self.brdr_think=0
            self.applyStyle()

            self.h=10
            self.w=10

        def getVarDict(self):
            return{
                "bg_clr":self.bg_clr,
                "brdr_clr":self.brdr_clr,
                "hover_clr":self.hover_clr,
                "pressed_clr":self.pressed_clr,
                "brdr_radius":self.brdr_radius,
                "brdr_think":self.brdr_think,
                "text_clr":self.text_clr,
                "h":self.h,
                "w":self.w
            }
        
        def updateVar(self,PushButton,dict):
            PushButton.bg_clr=dict["bg_clr"]
            PushButton.brdr_clr=dict["brdr_clr"]
            PushButton.hover_clr=dict["hover_clr"]
            PushButton.pressed_clr=dict["pressed_clr"]
            PushButton.brdr_radius=dict["brdr_radius"]
            PushButton.brdr_think=dict["brdr_think"]
            PushButton.text_clr=dict["text_clr"]
            
        def applyStyle(self):
            
            self.setStyleSheet(f"""
                QPushButton {{
                    border: {self.brdr_think}px solid {self.brdr_clr};
                    background-color: {self.bg_clr}; /* Green background */
                    border-radius: {self.brdr_radius}px; /* Radius = half of the width/height */
                    color:{self.text_clr};
                }}
                QPushButton:hover {{
                    background-color: {self.hover_clr}; /* Slightly lighter green on hover */
                }}
                QPushButton:pressed {{
                    background-color: {self.pressed_clr}; /* Darker green on press */
                }}
            """)

        def enterEvent(self, event):
            self.whenCursorEnter.emit()
            self.iconHover(hover=True)
            return super().enterEvent(event)
        def leaveEvent(self, a0):
            self.whenCursorLeave.emit()
            self.iconHover(hover=False)
            
            return super().leaveEvent(a0)
        
        def setSizeAsIconSize(self):
            self.setIconSize(QtCore.QSize(self.width()-2,self.height()-2))
        
        def iconHover(self,hover,hover_size=2):
            if self.icon():
                if hover==True:
                    self.setIconSize(QtCore.QSize(self.iconSize().width()+hover_size,self.iconSize().height()+hover_size))
                else:
                    self.setIconSize(QtCore.QSize(self.iconSize().width()-hover_size,self.iconSize().height()-hover_size))

    class Splitter(QtWidgets.QSplitter):
        whenReSize=QtCore.pyqtSignal()
        def __init__(self,parent=None):
            super().__init__(parent)

        def resizeEvent(self, a0):
            self.whenReSize.emit()
            return super().resizeEvent(a0)
    


        
    class Debouncer(QtCore.QObject):

        timeout = QtCore.pyqtSignal(object) 

        def __init__(self, delay_ms=300, parent=None):
            super().__init__(parent)
            self.delay = delay_ms
            self.timer = QtCore.QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self._on_timeout)
            self.last_arg = None
        
        def start(self, arg=None):
            self.last_arg = arg
            self.timer.start(self.delay)

        def stop(self):
            self.timer.stop()
            self.last_arg = None

        def _on_timeout(self):
            self.timeout.emit(self.last_arg)
            self.last_arg = None