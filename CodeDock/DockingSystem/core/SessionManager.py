from PyQt6 import QtCore
import typing

if typing.TYPE_CHECKING:
    from DockingSystem.widgets.DockWidget import DockWidget
    from DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter
    


class SessionManager:
    splitter_buffer=[]


    class Splitter:
        def __init__(self):

            self.save_debouncer=QtCore.QTimer()
            self.save_debouncer.setInterval(300)
            self.save_debouncer.singleShot(True)
            self.save_debouncer.timeout.connect(self._saveSession)

        def saveSession(self):
            ...

        def _saveSession(self):
            ...

        
    class DockWidget:
        def __init__(self):
            pass
        
    class DockZone:
        def __init__(self):
            pass
            
    
    def installSession(session_type:CreateSession):...
    def removeSession(session_type:CreateSession):...
    def saveSession(session_type:CreateSession):...
    def loadSession(session_type:CreateSession):...