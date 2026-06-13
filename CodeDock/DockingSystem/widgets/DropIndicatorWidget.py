
from PyQt6 import QtWidgets,QtCore,QtGui
import typing
from CodeDock.DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter
from CodeDock.DockingSystem.widgets.DockWidget import DockWidget
from CodeDock.DockingSystem.core.SettingsManager import DockWidgetStyle

if typing.TYPE_CHECKING:
    from CodeDock.DockingSystem.core.DockZone import DockZone

class DropIndicatorWidget(QtWidgets.QWidget):

    whenPathUrlDroped=QtCore.pyqtSignal(str)
    whenWidgetDroped=QtCore.pyqtSignal(QtCore.QObject)
    whenMouseEnterWithDrage=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenMouseLeaveWithDrage=QtCore.pyqtSignal(QtWidgets.QWidget)

    #ds
    def __init__(self):
        super().__init__()
        self.setObjectName("DropIndicatorWidget")
        
        self.parent_splitter:AnimatedSplitter=None
        
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet(f"""
             #DropIndicatorWidget{{
                background-color: {DockWidgetStyle.drop_indicator_color};
                border: 2px solid {DockWidgetStyle.drop_indicator_border_color};
                border-radius: 0px;
            }}
        """)
    
    def dragEnterEvent(self, event:QtGui.QDragEnterEvent):
        event.acceptProposedAction()
        self.whenMouseEnterWithDrage.emit(self)
        return super().dragEnterEvent(event)

    def dragLeaveEvent(self, a0):
        self.whenMouseLeaveWithDrage.emit(self)
        return super().dragLeaveEvent(a0)


    def dropEvent(self, event:QtGui.QDropEvent):

        widget = event.source()
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path=url.toLocalFile()
                self.whenPathUrlDroped.emit(file_path)
            event.acceptProposedAction()
        
        
        if widget and isinstance(widget,DockWidget):
            self.whenWidgetDroped.emit(widget)
            event.acceptProposedAction()
        