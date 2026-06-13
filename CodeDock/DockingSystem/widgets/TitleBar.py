from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.C_Widgets.Custom import Custom
import typing
if typing.TYPE_CHECKING:
    from CodeDock.DockingSystem.widgets.DockWidget import DockWidget



class TitleBar(QtWidgets.QWidget):
    
    whenMouseLeftPressed=QtCore.pyqtSignal()
    whenMouseLeftRelease=QtCore.pyqtSignal()
    whenMouseDrag=QtCore.pyqtSignal()
    
    whenCloseBtnPressed=QtCore.pyqtSignal(QtCore.QObject)
    whenDockToMaximizeBtnPressed=QtCore.pyqtSignal(QtCore.QObject)
    whenMaximizeToDockBtnPressed=QtCore.pyqtSignal(QtCore.QObject)
    whenMiniMizeBtnPressed=QtCore.pyqtSignal(QtCore.QObject)
    whenSplitterLock=QtCore.pyqtSignal()


    whenDockDragActive=QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, parent:"DockWidget"):
        super().__init__(parent)
        
        self.dragging:bool = False
        self.parent:DockWidget=parent
        self.mouse_Lpress_flag:bool=False
        
        self.minimize_button_flag:bool=False

        self._drag_start_pos=None

        self.is_temp_removed=False

        #self.setMouseTracking(True)


        self.setFixedHeight(32)

        self.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Preferred
            )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            background-color:#3F3F3F;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        """)


        self.total_child:int=0
        self.sumeof_child:int=0
        self.child_list:typing.Union[list,None]=None


        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 0, 5, 0)
        
        self.icon_button=QtWidgets.QPushButton()
        self.icon_button.setFixedSize(24, 24)
        

        self.title_label = QtWidgets.QLabel("Untitled")
        self.title_label.setToolTip("Untitled")
        self.title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        #self.block_path_navigation_bar=Custom.BlockPathNevigationBar()
        
        #self.block_path_navigation_bar.bg_clr="black"
        #self.block_path_navigation_bar.applyStyle()
        #self.block_path_navigation_bar.setFixedWidth(400)
        #layout.setSpacing(10)
        self.main_layout.addWidget(self.icon_button)
    
        self.main_layout.addWidget(self.title_label)
        #layout.addSpacerItem(QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum))
        #layout.addWidget(self.block_path_navigation_bar)
        self.main_layout.addStretch()

        
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(lambda:self.whenCloseBtnPressed.emit(self.parent))

        self.maximize_btn_state:bool=False
        self.maximize_button = QtWidgets.QPushButton()
        self.maximize_button.setFixedSize(24, 24)
        
        #self.maximize_button.clicked.connect()
        
        self.minimize_button = QtWidgets.QPushButton()
        self.minimize_button.setFixedSize(24, 24)
        #self.minimize_button.clicked.connect(self.parent_subwindow.minimizeIt)

        self.main_layout.addWidget(self.minimize_button)
        self.main_layout.addWidget(self.maximize_button)
        self.main_layout.addWidget(self.close_button)
        self.setContentsMargins(0,0,0,0)
        self.d_icon = QtGui.QIcon("/home/omx/txtopng")
        

        self.minimize_button.clicked.connect(lambda:self.whenMiniMizeBtnPressed.emit(self.parent))
        self.maximize_button.clicked.connect(self.onMaximizeBtnPressed)
        
        self.close_button.setStyleSheet("background-color:#BF5454;")
        self.maximize_button.setStyleSheet("background-color:#668D4C;")
        self.minimize_button.setStyleSheet("background-color:#ABA457;")

    def onMaximizeBtnPressed(self):
        if self.maximize_btn_state:
            self.maximize_btn_state=False 
            self.whenMaximizeToDockBtnPressed.emit(self.parent)
        else:
            self.maximize_btn_state=True
            self.whenDockToMaximizeBtnPressed.emit(self.parent)
            
    def mouseDoubleClickEvent(self, event):
        self.onMaximizeBtnPressed()
        return super().mouseDoubleClickEvent(event)
    
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.position().toPoint()
            self.mouse_Lpress_flag=True
            self.whenMouseLeftPressed.emit()

        super().mousePressEvent(event)


                
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            
            self.mouse_Lpress_flag=False        
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):

        if not self.mouse_Lpress_flag:
            return

        if (event.position().toPoint() - self._drag_start_pos).manhattanLength() < \
                QtWidgets.QApplication.startDragDistance():
            
            return


        
        #if not self.is_temp_removed:

        self.whenDockDragActive.emit(self.parent)
        
        #self.is_temp_removed=True

        self.start_drag()
        super().mouseMoveEvent(event)



    def start_drag(self):
        drag = QtGui.QDrag(self.parent)
        mime = QtCore.QMimeData()

        mime.setText("DRAG_DOCK_WIDGET")
        drag.setMimeData(mime)

        # 🔹 Get file name
        title = self.title_label.text()

        # 🔹 Get system icon based on file
        icon_provider = QtWidgets.QFileIconProvider()
        file_info = QtCore.QFileInfo(title)
        icon = icon_provider.icon(file_info)

        # 🔹 Font metrics for dynamic width
        font = QtGui.QFont()
        font.setPointSize(10)

        fm = QtGui.QFontMetrics(font)
        text_width = fm.horizontalAdvance(title)

        # 🔹 Dynamic size
        padding = 5
        icon_size = 24
        height = 36

        width = icon_size + text_width + padding * 3

        pm = QtGui.QPixmap(width, height)
        pm.fill(QtCore.Qt.GlobalColor.transparent)

        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # 🔹 Background
        p.setBrush(QtGui.QColor(40, 40, 40, 220))
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.drawRoundedRect(pm.rect(), 8, 8)

        # 🔹 Draw icon
        icon_rect = QtCore.QRect(padding, (height - icon_size)//2, icon_size, icon_size)
        icon.paint(p, icon_rect)

        # 🔹 Draw text
        p.setFont(font)
        p.setPen(QtGui.QColor("white"))

        text_x = padding * 2 + icon_size
        text_y = (height + fm.ascent() - fm.descent()) // 2

        p.drawText(text_x, text_y, title)

        p.end()

        # 🔹 Apply drag preview
        drag.setPixmap(pm)
        drag.setHotSpot(QtCore.QPoint(0, 0))

        #drag.setHotSpot(QtCore.QPoint(0, height // 2))

        drag.exec(QtCore.Qt.DropAction.MoveAction)

    def setCloseBtnIcon(self,icon:QtGui.QIcon):
        self.close_button.setIcon(icon)
    def setMinimizeBtnIcon(self,icon:QtGui.QIcon):
        self.maximize_button.setIcon(icon)
    def setMaximizeBtnIcon(self,icon:QtGui.QIcon):
        self.minimize_button.setIcon(icon)

    def setTitle(self,title:str):
        self.title_label.setText(title)
        
    def maximizeButtonSignal(self):
        if self.minimize_button_flag==False:
            #self.parent_subwindow.showMaximized()
            self.minimize_button_flag=True
        else:
            #self.parent_subwindow.showNormal()
            self.minimize_button_flag=False
    """
    def resizeEvent(self, event):
        fm = self.title_label.fontMetrics()
        elided = fm.elidedText(
            self.title_label.toolTip(),
            QtCore.Qt.TextElideMode.ElideRight,
            self.title_label.width()
            
            )
        print(elided)
        self.title_label.setText(elided)
        return super().resizeEvent(event)
    """

    """
    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = event.size().width()
        print(self.main_layout.children())
        #if self.total_child!=self.main_layout.count():
        self.total_child=self.main_layout.count()
        self.child_list=[self.icon_button,self.title_label,self.minimize_button,self.maximize_button,self.close_button]
        self.sumeof_child=0

        for child in self.child_list:
            self.sumeof_child+=child.width()
        print(self.sumeof_child)
        if self.child_list:
            
            if self.sumeof_child > width-10 :
                self.title_label.setText("...")
                
                self.icon_button.show()
                self.close_button.show()
                self.minimize_button.show()
                self.maximize_button.show()"""

            
  
    def enterEvent(self, event):
        #self.parent_subwindow.parent_mdi.subwindowHover(True,self.parent_subwindow)
        #self.parent.raise_()
        
        return super().enterEvent(event)
    
    def leaveEvent(self, a0):
        #self.parent_subwindow.parent_mdi.subwindowHover(False,self.parent_subwindow)
        #self.parent.lower()
        #self.parent.parent.setWindowRaise()
        return super().leaveEvent(a0)

