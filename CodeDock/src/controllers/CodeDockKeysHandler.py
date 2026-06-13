from PyQt6.QtCore import QObject, QEvent, Qt

class Code_Dock_Key_Handler(QObject):
    def __init__(self, mainwin):
        super().__init__()
        self.mainwin = mainwin  # Reference to main window
        self.mainwin.installEventFilter(self)  # Install event filter

    def eventFilter(self, obj, event):
        if obj == self.mainwin and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_N and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                
                return True  # Stop further processing
        return super().eventFilter(obj, event)  # Default processing
