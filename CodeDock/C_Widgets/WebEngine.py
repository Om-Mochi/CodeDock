from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QApplication
)


try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except:pass

from PyQt6.QtCore import QUrl,QSize
import sys

from CodeDock.C_Widgets.Custom import Custom

class WebBrowserWidget(Custom.Widget):
    def __init__(self):
        super().__init__()
        
        self.bg_clr="#3c3c3c"
        self.applyStyle()

        # Create widgets
        self.browser = QWebEngineView()
        self.url_bar = Custom.InputBox()

        self.go_button = Custom.PushButton("🔍")
        self.back_button = Custom.PushButton("←")
        self.forward_button = Custom.PushButton("→")
        self.reload_button = Custom.PushButton("⟳")

        self.url_bar.setFixedHeight(20)
        self.go_button.setFixedSize(QSize(20,20))
        self.back_button.setFixedSize(QSize(20,20))
        self.forward_button.setFixedSize(QSize(20,20))
        self.reload_button.setFixedSize(QSize(20,20))
        # Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.reload_button)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.go_button)

        #top_layout.setContentsMargins(0,5,0,0)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.browser)
        self.setLayout(layout)


        layout.setContentsMargins(0,5,0,0)


        # Connections
        self.go_button.clicked.connect(self.load_url)
        self.url_bar.returnPressed.connect(self.load_url)
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.reload_button.clicked.connect(self.browser.reload)
        self.browser.urlChanged.connect(self.update_url_bar)

        # Default
        self.browser.setUrl(QUrl("https://www.google.com"))

    def load_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, qurl: QUrl):
        self.url_bar.setText(qurl.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowserWidget()
    window.setWindowTitle("PyQt6 Custom Web Browser")
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())
