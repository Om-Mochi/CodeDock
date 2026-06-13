from PyQt6 import QtCore,QtGui,QtWidgets
import sys
import logging
from CodeDock.src.controllers.CodeDockMain import Code_Dock_Main
def main():
    app=QtWidgets.QApplication(sys.argv)
    font=QtGui.QFont("JetBrainsMonoNL Nerd Font")
    
    GLOBAL_STYLESHEET = """
    * {
    }
    """
    app.setStyleSheet(GLOBAL_STYLESHEET)
    cd=Code_Dock_Main(app)
    app.setFont(font)
    sys.exit(app.exec())

main()
