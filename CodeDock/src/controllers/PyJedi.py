from PyQt6 import QtWidgets, QtGui, QtCore
import sys


class CustomTabBar(QtWidgets.QTabBar):

    tabMinimizeRequested = QtCore.pyqtSignal(int)
    tabCloseRequestedEx = QtCore.pyqtSignal(int)

    def addCustomTab(self, icon: QtGui.QIcon, title: str):
        index = self.addTab(icon, title)

        # ----- Right side widget (minimize + close)
        rightWidget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(rightWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        btnMin = QtWidgets.QToolButton()
        btnMin.setText("−")
        btnMin.setAutoRaise(True)

        btnClose = QtWidgets.QToolButton()
        btnClose.setText("✕")
        btnClose.setAutoRaise(True)

        layout.addWidget(btnMin)
        layout.addWidget(btnClose)

        self.setTabButton(index, QtWidgets.QTabBar.ButtonPosition.RightSide, rightWidget)

        # connect signals
        btnMin.clicked.connect(lambda _, i=index: self.tabMinimizeRequested.emit(i))
        btnClose.clicked.connect(lambda _, i=index: self.tabCloseRequestedEx.emit(i))

        return index


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        # replace tabbar
        bar = CustomTabBar()
        self.tabs.setTabBar(bar)
        bar.setMovable(True)
        # signals
        bar.tabMinimizeRequested.connect(self.onMinimizeTab)
        bar.tabCloseRequestedEx.connect(self.onCloseTab)

        # add tabs
        for i in range(5):
            w = QtWidgets.QTextEdit()
            self.tabs.addTab(w, "")
            bar.setTabText(i, "")  # important (avoid duplicate text)
            bar.setTabIcon(i, QtGui.QIcon.fromTheme("text-x-python"))

            bar.addCustomTab(QtGui.QIcon.fromTheme("text-x-python"), f"File {i}.py")

    def onMinimizeTab(self, index):
        print("minimize tab:", index)
        self.tabs.widget(index).hide()

    def onCloseTab(self, index):
        print("close tab:", index)
        self.tabs.removeTab(index)


app = QtWidgets.QApplication(sys.argv)
w = Window()
w.resize(800, 500)
w.show()
sys.exit(app.exec())