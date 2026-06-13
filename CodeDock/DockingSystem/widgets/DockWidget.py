from PyQt6 import QtWidgets,QtCore,QtGui
import typing

from CodeDock.DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter
from CodeDock.DockingSystem.widgets.TitleBar import TitleBar
from CodeDock.DockingSystem.core.SettingsManager import DockWidgetStyle
from CodeDock.DockingSystem.Debuger import Debug
from CodeDock.C_Widgets.Custom import Custom
if typing.TYPE_CHECKING:
    from CodeDock.DockingSystem.core.DockZone import DockZone

class DockWidget(QtWidgets.QWidget):
    #signals    
    whenMouseDrag=QtCore.pyqtSignal(QtCore.QRect,QtCore.QPoint,QtWidgets.QWidget,object)
    whenMouseLeftRelease=QtCore.pyqtSignal(QtWidgets.QWidget)
    when_Ctrl_MovementsKeyPressed=QtCore.pyqtSignal(QtCore.Qt.Key,QtWidgets.QWidget)
    whenPathUrlDroped=QtCore.pyqtSignal(str)
    whenWidgetDroped=QtCore.pyqtSignal(QtCore.QObject)
    whenMouseLeftClick=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenFocusIn=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenMouseEnterWithDrage=QtCore.pyqtSignal(QtWidgets.QWidget,AnimatedSplitter)
    whenMouseLeaveWithDrage=QtCore.pyqtSignal(QtWidgets.QWidget,AnimatedSplitter)
    
    whenDockMoveActive=QtCore.pyqtSignal(QtWidgets.QWidget)
    def __init__(self):
        super().__init__()
        self.setObjectName("DockWidget")
        self.parent_dock_zone:typing.Union[DockZone,None]=None
        self.vlayout=QtWidgets.QVBoxLayout()
        self.parent_splitter:AnimatedSplitter=None

    
        self.is_container:bool=False
        self.child_splitter:typing.Union[AnimatedSplitter,None]=None


        self.setLayout(self.vlayout)
        self.setAcceptDrops(True)
        self.mouse_move_event_state:bool=True
        self.mouse_release_event_state:bool=True
        self.is_mouse_inside:bool=False
        self.mouse_drag_event_state:bool=False
  
        
                    #self.setAutoFillBackground(True)
        self.text_editor:Custom.TextEditor=None
        self.titlebar_total_child:int=0
        self.titlebar_sumeof_child:int=0
        self.titlebar_child_list:typing.Union[list,None]=None

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.vlayout.setSpacing(0)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )


        self._drag_pos=None
        self._source_widget=None

        self.drop_area_debouncer=QtCore.QTimer()
        self.drop_area_debouncer.setInterval(300)
        self.drop_area_debouncer.setSingleShot(True)
        self.drop_area_debouncer.timeout.connect(self.onItemDrag)

    def initTitlebar(self):
        self.title_bar=TitleBar(self)
        
        self.vlayout.addWidget(self.title_bar)
        
        self.title_bar.whenDockDragActive.connect(lambda x:self.whenDockMoveActive.emit(x))
        #self.title_bar.whenCloseBtnPressed.connect()
        #self.title_bar.whenMaximizeBtnPressed.connect()
        #self.title_bar.whenMiniMizeBtnPressed.connect()
        #self.title_bar.whenMouseLeftPressed.connect()
        #self.title_bar.whenMouseLeftRelease.connect()
        #self.title_bar.whenMouseDrag.connect()
    

    def setTitle(self,title:str):
        self.title_bar.setTitle(title)
        self.title_bar.setToolTip(title)
    def title(self)->str:
        return self.title_bar.title_label.text()
    



    def getSplitterIndex(self)->int:
        return self.parent_splitter.indexOf(self)
    
    def setParentSplitter(self,splitter:AnimatedSplitter):
        self.parent_splitter=splitter

    def addWidget(self,widget:QtWidgets.QWidget):
        if widget:
            widget.setParent(self)
        self.vlayout.addWidget(widget)
    
    def mousePressEvent(self, a0:QtGui.QMouseEvent):
        
        if a0.button()==QtCore.Qt.MouseButton.LeftButton:    
            self.whenMouseLeftClick.emit(self)
        return super().mousePressEvent(a0)

    def onFocusInWidgets(self,widget):
        self.whenFocusIn.emit(self)
        

    def mouseReleaseEvent(self, a0):
        #if self.mouse_drag_event_state:
            #self.whenMouseRelease.emit(self)
        self.mouse_drag_event_state=False

        return super().mouseReleaseEvent(a0)
    
    def dragEnterEvent(self, event:QtGui.QDragEnterEvent):
        #print("drag enter :",self.objectName())

        #QtWidgets.QApplication.instance().installEventFilter(self)

        event.acceptProposedAction()
        return super().dragEnterEvent(event)

    def dragLeaveEvent(self, a0):
        self.mouse_drag_event_state=False
        #QtWidgets.QApplication.instance().removeEventFilter(self)

        return super().dragLeaveEvent(a0)


    def dragMoveEvent(self, event:QtGui.QDragMoveEvent):
        if not self.mouse_drag_event_state:
            self.mouse_drag_event_state=True
        pos = event.position().toPoint()

        widget=event.source()
        self._drag_pos=pos
        self._source_widget=widget

        self.drop_area_debouncer.start()
        #self.onItemDrag()
        return super().dragMoveEvent(event)

    def onItemDrag(self):
        if self._source_widget and isinstance(self._source_widget,DockWidget):
            self.whenMouseDrag.emit(self.rect(),self._drag_pos,self,self._source_widget)
        else:
            self.whenMouseDrag.emit(self.rect(),self._drag_pos,self,None)
        

    def dropEvent(self, event:QtGui.QDropEvent):
        self.whenMouseLeftRelease.emit(self)
        
        widget = event.source()
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path=url.toLocalFile()
                self.whenPathUrlDroped.emit(file_path)
            event.acceptProposedAction()
            
        
        if widget and isinstance(widget,DockWidget):
            self.whenWidgetDroped.emit(widget)
            event.acceptProposedAction()

        try:
            self.title_bar.mouse_Lpress_flag=False
        except:pass
    

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier and event.modifiers() & QtCore.Qt.KeyboardModifier.AltModifier:

            if event.key() == QtCore.Qt.Key.Key_Up:
                self.when_Ctrl_MovementsKeyPressed.emit(QtCore.Qt.Key.Key_Up, self)
                event.accept()
                return

            elif event.key() == QtCore.Qt.Key.Key_Down:
                
                self.when_Ctrl_MovementsKeyPressed.emit(QtCore.Qt.Key.Key_Down, self)
                event.accept()
                return

            elif event.key() == QtCore.Qt.Key.Key_Left:
                self.when_Ctrl_MovementsKeyPressed.emit(QtCore.Qt.Key.Key_Left, self)
                event.accept()
                return

            elif event.key() == QtCore.Qt.Key.Key_Right:
                self.when_Ctrl_MovementsKeyPressed.emit(QtCore.Qt.Key.Key_Right, self)
                event.accept()
                return

        super().keyPressEvent(event)



    def setDockIcon(self,icon:QtGui.QIcon):
        self.title_bar.icon_button.setIcon(icon)


        #return super().resizeEvent(event)


    def focusInEvent(self, a0):
        print("fcus in..........\n\n\n\n")
        DockWidgetStyle.setActivatedStyleSheet(self)
        return super().focusInEvent(a0)
    
    def focusOutEvent(self, a0):
        DockWidgetStyle.setDeActivatedStyleSheet(self)
        return super().focusOutEvent(a0)
    