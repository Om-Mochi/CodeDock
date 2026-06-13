from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.DockingSystem.core.DockZone import DockZone
class DraggableWidget(QtWidgets.QWidget):
    """Widget that can be dragged from toolbar"""
    def __init__(self, color, name, parent=None):
        super().__init__(parent)
        self.color = color
        self.name = name
        self.setFixedSize(80, 60)
        
        # Set background color
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Add label
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(name)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #333; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)
        
        self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)
            self.drag_start_position = event.pos()
    
    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.MouseButton.LeftButton):
            return
        
        # Start drag operation
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.setText(f"{self.color}|{self.name}")
        drag.setMimeData(mime_data)
        
        drag.exec(QtCore.Qt.DropAction.CopyAction)
        self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
    
    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Custom MDI with Draggable Widgets")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create toolbar
        toolbar = QtWidgets.QToolBar("Widget Toolbar")
        #toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #FFFFFF;
                border-bottom: 2px solid #CCCCCC;
                padding: 5px;
            }
            QLabel {
                color: #333;
                font-size: 13px;
            }
        """)
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, toolbar)
        
        # Add instruction label
        instruction = QtWidgets.QLabel("  Drag widgets from toolbar to MDI area ⬇ | Widgets are fixed once dropped | Close with ✕")
        toolbar.addWidget(instruction)
        
        toolbar.addSeparator()
        
        # Add draggable widgets to toolbar with lighter colors
        colors = [
            ("#FFB3BA", "Red"),      # Light Red
            ("#BAE1FF", "Blue"),     # Light Blue
            ("#BAFFC9", "Green"),    # Light Green
            ("#FFD9BA", "Orange"),   # Light Orange
            ("#E0BBE4", "Purple"),   # Light Purple
            ("#B4F8C8", "Mint"),     # Light Mint
            ("#FBE7C6", "Peach"),    # Light Peach
            ("#A0E7E5", "Cyan")      # Light Cyan
        ]
        
        for color, name in colors:
            widget = DraggableWidget(color, name)
            toolbar.addWidget(widget)
            toolbar.addSeparator()
        
        # Create Custom MDI Area
        self.widget=QtWidgets.QWidget()
        #self.custom_mdi = CustomMdiArea()
        self.mycustom_mdi = DockZone()
        self.la=QtWidgets.QHBoxLayout()
        #self.la.addWidget(self.custom_mdi)
        self.la.addWidget(self.mycustom_mdi)
        self.widget.setLayout(self.la)

        self.setCentralWidget(self.widget)

