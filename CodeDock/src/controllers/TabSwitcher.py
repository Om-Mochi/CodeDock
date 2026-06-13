
from PyQt6.QtWidgets import QApplication, QDialog, QTabBar, QVBoxLayout, QWidget, QLabel,QHBoxLayout,QPushButton,QListWidgetItem,QListWidget
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout
)
from PyQt6.QtGui import QPixmap, QMouseEvent, QKeyEvent,QIcon
from PyQt6.QtCore import Qt, QSize, QRect,pyqtSignal,QEvent
import sys
import os


class CTabbar(QTabBar):
    def mouseDoubleClickEvent(self,event):

        #self.connect_on_tabchange(self.tab_bar.currentIndex())
        self.parent().accept()
        return super().mouseDoubleClickEvent(event)

class Tab_V_Switcher(QDialog):
    def __init__(self, screen_size):
        super().__init__(None)
        self.screen_w = screen_size.width()
        self.screen_h = screen_size.height()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)  # Frameless popup
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)  # Transparent background
        #self.setWindowOpacity(0.7)
        #self.setStyleSheet("background-color:black;")
        self.setModal(True)
        
        self.setStyleSheet("""background-color:rgba(0,0,0,100);
                           
                           """)
        self.selected_tab = None
        self.first_index= None
        self.connect_on_tabchange=None
        


        self.tab_bar = CTabbar(self)

        self.tab_bar.currentChanged.connect(self.onTabChange)


        
    def onTabChange(self):
        
        return self.connect_on_tabchange(self.tab_bar.currentIndex())
            #return self.tab_widget.currentIndex()

            #return self.tab_widget.currentIndex()


    def grabAndSet(self, widget_list, dir_path):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # QTabBar for displaying images as tabs
        self.tab_bar.setExpanding(True)  # Make tabs expand to fit width
        self.tab_bar.setIconSize(QSize(0, 0))  # Adjust icon size
        
        self.tab_bar.setShape(QTabBar.Shape.RoundedWest)

        for i, widget in enumerate(widget_list):
            image_path = f"{dir_path}/widget{i}.png"
            widget_pix = widget[0].grab()
            widget_pix.save(image_path)

            
            pixmap = QPixmap(image_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
            #icon = QIcon(pixmap)  # Convert QPixmap to QIcon
            
            # Create a custom tab widget with icon on top and text below
            tab_widget = QWidget()
            tab_layout = QVBoxLayout(tab_widget)
            tab_layout.setSpacing(0)  # No extra spacing
            tab_layout.setContentsMargins(10, 10, 10, 10)  # Remove margins

            icon_label = QLabel()
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label = QLabel(widget[1]) 
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Add icon and text to layout
            label.setStyleSheet("color:#fff34e;font-size:20px;")
            tab_layout.addWidget(icon_label)
            tab_layout.addWidget(label)

            # Add tab without text to avoid side text placement
            index = self.tab_bar.addTab("")
            self.tab_bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, tab_widget)  # Set custom widget

            if self.selected_tab and self.selected_tab == widget[0]:
                #self.first_index=self.tab_bar.currentIndex()
                self.tab_bar.setCurrentIndex(i)

            self.tab_bar.setStyleSheet("""
                QTabBar::tab {
                    padding: 0px;
                    background-color: rgba(0, 0, 0, 0.5);
                    border: none;
                }
                QTabBar::tab:selected {
                    background: rgba(0, 0, 0, 0.5);
                    border: 2px solid #00ffff;
                }
                QTabBar::tab:hover {
                    background: rgba(0, 0, 0, 0.5);
                    border: 2px solid #00ff9d;
                }
            """)

        layout.addWidget(self.tab_bar)
        self.setLayout(layout)
        if len(widget_list) * 200 < self.screen_h:
            self.tab_bar.setFixedSize(300,len(widget_list)*200)
        else:
            self.tab_bar.setFixedSize(300,self.screen_h)
            #self.resize(self.screen_w, self.screen_h)

        self.resize(self.screen_w,self.screen_h)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:  # Select on Enter key
            self.accept()
        elif event.key() == Qt.Key.Key_Escape:
            self.connect_on_tabchange(self.first_index)
            self.reject()
        elif event.key() == Qt.Key.Key_Up:  # Navigate left
            current_index = self.tab_bar.currentIndex()
            self.tab_bar.setCurrentIndex(max(0, current_index - 1))
        elif event.key() == Qt.Key.Key_Down:  # Navigate right
            current_index = self.tab_bar.currentIndex()
            self.tab_bar.setCurrentIndex(min(self.tab_bar.count() - 1, current_index + 1))
        else:
            super().keyPressEvent(event)

    def showSwitcher(self):
        if self.exec() == QDialog.DialogCode.Accepted:pass







class ImageLabel():
    def __init__(self):
        #super().__init__()
        self.h=190
        self.w=210
        self.radius=8
        self.font_size=12
        self.selected_brdr_thinkess=5
        self.font_clr="white"
        self.brdr_clr="green"
        self.selected_clr="black"

    def getVarDict(self):
        return{
        "h":self.h,
        "w":self.w,
        "radius":self.radius,
        "font_size":self.font_size,
        "selected_brdr_thinkess":self.selected_brdr_thinkess,
        "font_clr":self.font_clr,
        "brdr_clr":self.brdr_clr,
        "selected_clr":self.selected_clr,
        }
    
    def updateVar(self,var_dict):
        self.h=var_dict["h"]
        self.w=var_dict["w"]
        self.radius=var_dict["radius"]
        self.font_size=var_dict["font_size"]
        self.selected_brdr_thinkess=var_dict["selected_brdr_thinkess"]
        self.font_clr=var_dict["font_clr"]
        self.selected_clr=var_dict["selected_clr"]
        self.brdr_clr=var_dict["brdr_clr"]
    
    def addImage(self,path,title,t_icon,index):
        self.container=QWidget()
        self.path = path
        self.index = index
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.container.setFixedSize(self.w,self.h)  # Slightly taller for title

        # --- Image Thumbnail ---
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(self.w, self.h-30)

        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.container.setStyleSheet("background-color:transparent;")

        pixmap = QPixmap(path)
        target_size = QSize(self.w-20, self.h-50)

        if pixmap.width() > target_size.width() or pixmap.height() > target_size.height():
            pixmap = pixmap.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)

        self.image_label.setPixmap(pixmap)
        self.image_label.setStyleSheet(f"border: {self.selected_brdr_thinkess}px solid {self.brdr_clr}; border-radius: {self.radius}px;")

        #self.icon_title_layout=QHBoxLayout()
        #self.icon_label=QLabel()


        self.title_label = QPushButton()
        self.title_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.title_label.setIcon(QIcon(t_icon))
        self.title_label.setIconSize(QSize(self.font_size,self.font_size))
        self.title_label.setText(f"  {title}")

        #self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"background-color:transparent;color: {self.font_clr}; font-size: {self.font_size}px;")

        #self.icon_label.setContentsMargins(0,0,0,0)
        
        # Add widgets to layout

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.title_label)
        return self.container,self.image_label
    
    def set_selected(self, selected,img_widgt,image_label):
        if selected:
            image_label.setStyleSheet(f"border: {self.selected_brdr_thinkess}px solid {self.selected_clr}; border-radius: {self.radius}px;")
        else:
            print("nothing in thi")
            image_label.setStyleSheet(f"border: {self.selected_brdr_thinkess}px solid {self.brdr_clr}; border-radius: {self.radius}px;")

class Ui_Tab_Switcher(QWidget):
    whenTabSelected=pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.image_labeler=ImageLabel()

        self.image_paths=[]
        self.widget_list=[]
        self.dir_path=[]
        self.index = 0
        self.columns = 6  # items per row        
        self.img_spacing=20
        self.bg_clr=[30,30,30,200]
        self.margin=40
        self.brdr_radius=20

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_widgets = []
        self.image_labels=[]

        self.wrapper = QWidget()
        self.wrapper.setLayout(self.grid_layout)
        self.wrapper.setStyleSheet("background-color: rgba(30, 30, 30, 200); border-radius: 20px;")

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.addWidget(self.wrapper)
        

        self.adjustSize()
        self.resize(0,0)

    def getVarDict(self):

        return {
            "index":self.index,
            "columns":self.columns,
            "img_spacing":self.img_spacing,
            "bg_clr":self.bg_clr,
            "margin":self.margin,
            "brdr_radius":self.brdr_radius,
            "image_labes":self.image_labeler.getVarDict()
        }
    
    def updateVar(self,var_dict):
        self.index=var_dict["index"]
        self.columns=var_dict["columns"]
        self.img_spacing=var_dict["img_spacing"]
        self.bg_clr=var_dict["bg_clr"]
        self.margin=var_dict["margin"]
        self.brdr_radius=var_dict["brdr_radius"]
        
        self.image_labeler.updateVar(var_dict=var_dict["image_labes"])
        self.applyStyle()
        
    def resetImageLabels(self):
        self.setImage(self.image_paths)

    def applyStyle(self):
        self.wrapper.setStyleSheet(
            f"background-color: rgba{self.bg_clr[0],self.bg_clr[1],self.bg_clr[2],self.bg_clr[3]}; border-radius: {self.brdr_radius}px;")
    
    def setItemPerRow(self,val):
        #self.margin=val
        #self.setContentsMargins(self.margin,self.margin,self.margin,self.margin)
        self.columns=val
        self.close()
        self.setImage(self.image_paths)
        self.show()

    def setImageSpacing(self,val):
        self.img_spacing=val
        self.grid_layout.setSpacing(self.img_spacing)
    
    def setMargin(self,val):
        self.margin=val
        self.setContentsMargins(val,val,val,val)
        
    def setBgColor(self,color):
        self.bg_clr=[color.red(),color.green(),color.blue(),self.bg_clr[3]]
        self.applyStyle()

    def setBgAlfa(self,val):
        self.bg_clr[3]=val
        self.applyStyle()

    def setBrdrRadius(self,val):
        self.brdr_radius=val
        self.applyStyle()

    def setImageHight(self,val):
        self.image_labeler.h=val
        self.close()
        self.resetImageLabels()
        self.show()

    def setImageWidth(self,val):
        
        self.image_labeler.w=val
        self.close()
        self.resetImageLabels()
        self.show()
    
    def setImageBorderColor(self,color):
        self.image_labeler.brdr_clr=color.name()
        self.resetImageLabels()

    def setImageSelectedColor(self,color):
        self.image_labeler.selected_clr=color.name()
        self.resetImageLabels()

    def setImageSelectedBrdrThinkness(self,val):
        self.image_labeler.selected_brdr_thinkess=val
        self.resetImageLabels()

    def setImageBrdrRadius(self,val):
        self.image_labeler.radius=val
        self.resetImageLabels()
    
    def setImageTitleFontColor(self,color):
        self.image_labeler.font_clr=color.name()
        self.resetImageLabels()
    
    def setImageTitileFontSize(self,val):
        self.image_labeler.font_size=val
        
        self.resetImageLabels()


    def setImage(self,image_paths):
        
        for image_widget in self.image_widgets:
            image_widget.deleteLater()
        
        self.image_widgets.clear()
        self.image_labels.clear()
        
        for i, path in enumerate(image_paths):
            image_widget,image_label = self.image_labeler.addImage(path[0],path[1],path[2], i)
            image_widget.mousePressEvent = self.label_clicked  # assign custom click handler
            self.image_widgets.append(image_widget)
            self.image_labels.append(image_label)
            row = i // self.columns
            col = i % self.columns
            self.grid_layout.addWidget(image_widget, row, col)

        self.image_labeler.set_selected(True,self.image_widgets[self.index],image_label)
        self.adjustSize()
        self.updateGeometry()
        

    def grabAndSet(self, widget_list=[], dir_path=[]):
        #self.widget_list=[widget_list]
        #self.dir_path=dir_path
        self.image_paths.clear()
        for imgae_idget in self.image_widgets:
            imgae_idget.deleteLater()
        
        self.image_widgets.clear()
        self.image_labels.clear()
        
        for i, widget in enumerate(widget_list):
            image_path = f"{dir_path}/widget{i}.png"
            widget_pix = widget[0].grab()
            widget_pix.save(image_path)
            self.image_paths.append([image_path,widget[1],widget[2]])
            imgae_idget,image_label = self.image_labeler.addImage(image_path,widget[1],widget[2],i)
            imgae_idget.mousePressEvent = self.label_clicked  # assign custom click handler
            self.image_widgets.append(imgae_idget)
            self.image_labels.append(image_label)
            row = i // self.columns
            col = i % self.columns
            self.grid_layout.addWidget(imgae_idget, row, col)

        self.image_labeler.set_selected(True,self.image_widgets[self.index],image_label)


        self.adjustSize()
        self.grid_layout.update()
        self.updateGeometry()



    def label_clicked(self, event: QMouseEvent):
        clicked_label = self.sender()
        print(clicked_label)
        self.set_selected_index(clicked_label.index)

    def set_selected_index(self, new_index):
        if 0 <= new_index < len(self.image_widgets):
            self.image_labeler.set_selected(False,self.image_widgets[self.index],self.image_labels[self.index])
            self.index = new_index
            self.image_labeler.set_selected(True,self.image_widgets[self.index],self.image_labels[self.index])

    def keyPressEvent(self, event: QKeyEvent):

        cols = self.columns
        rows = (len(self.image_widgets) + cols - 1) // cols

        row = self.index // cols
        col = self.index % cols

        if event.key() == Qt.Key.Key_Right:
            col = (col + 1) % cols
        elif event.key() == Qt.Key.Key_Left:
            col = (col - 1 + cols) % cols
        elif event.key() == Qt.Key.Key_Down:
            row = (row + 1) % rows
        elif event.key() == Qt.Key.Key_Up:
            row = (row - 1 + rows) % rows
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Escape):
            print(self.image_paths[self.index])
            self.whenTabSelected.emit(self.index)
            self.close()
            return

        new_index = row * cols + col
        if new_index >= len(self.image_widgets):
            new_index = self.index  # keep previous if overflow
        self.set_selected_index(new_index)
from PyQt6.QtCore import Qt, QSize, QEvent, pyqtSignal
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout,
    QListWidget, QListWidgetItem
)
import sys


class BasicTabSwitcher(QDialog):
    whenTabSelected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(10, 10, 10, 10)

        self.current_row_i = 0
        self.last_row_i = 0

    def applyStyle(self):
        self.setStyleSheet("background-color:red;")
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                font-size: 14px;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item {
                border-left: 3px solid #7b6a63;
                padding: 2px 5px;
            }
            QListWidget::item:selected {
                background-color: #555;
                border-left: 3px solid #ffdcce;
                padding: 6px 10px;
            }
        """)

    def setTabsItems(self, tabs=[]):
        try:
            self.list_widget.deleteLater()
            print("deleted old list")
        except:
            pass

        self.list_widget = QListWidget()
        self.vlayout.addWidget(self.list_widget)

        for i, tab in enumerate(tabs):
            item = QListWidgetItem(QIcon(tab[2]), tab[1])
            self.list_widget.addItem(item)

        self.list_widget.setIconSize(QSize(14, 14))
        self.applyStyle()

        self.current_row_i = 0
        self.last_row_i = 0
        self.list_widget.currentRowChanged.connect(self.onCurrentRowChange)

        # install event filter for wrap-around
        self.list_widget.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.list_widget and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Down:
                if self.list_widget.currentRow() == self.list_widget.count() - 1:
                    self.setCurrentRow(0)
                    return True
            elif event.key() == Qt.Key.Key_Up:
                if self.list_widget.currentRow() == 0:
                    self.setCurrentRow(self.list_widget.count() - 1)
                    return True
        return super().eventFilter(source, event)

    def onCurrentRowChange(self, i):
        self.last_row_i = i

    def setCurrentRow(self, index):
        self.last_row_i = index
        self.list_widget.setCurrentRow(index)
    def keyReleaseEvent(self, event):
        
        if event.key() == Qt.Key.Key_Control:
            # Close only when Ctrl is released
            self.accept()
            self.get_selected_tab()
        elif event.key() == Qt.Key.Key_Tab:
            # Ignore Tab release (do nothing)
            pass
        else:
            super().keyReleaseEvent(event)

    def keyPressEvent(self, event):
        print(event.modifiers(),event.key())
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        elif event.key() == Qt.Key.Key_Return:
            self.get_selected_tab()
            self.accept()
        elif (event.modifiers() & Qt.KeyboardModifier.ControlModifier) and \
             (event.key() == Qt.Key.Key_Tab):
            press_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
            release_event = QKeyEvent(QEvent.Type.KeyRelease, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier)
            QApplication.postEvent(self.list_widget, press_event)
            QApplication.postEvent(self.list_widget, release_event)

        elif (event.modifiers() & Qt.KeyboardModifier.ControlModifier) | \
             (event.modifiers() & Qt.KeyboardModifier.ShiftModifier) and \
             (event.key() == Qt.Key.Key_Tab):
            
            press_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier)
            release_event = QKeyEvent(QEvent.Type.KeyRelease, Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier)
            QApplication.postEvent(self.list_widget, press_event)
            QApplication.postEvent(self.list_widget, release_event)
        else:
            super().keyPressEvent(event)

    def get_selected_tab(self):
        row = self.list_widget.currentRow()
        print("Selected tab:", row)
        self.whenTabSelected.emit(row)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Change this to your actual image directory
    test_folder = "D:\Linux\projects\CodeBookN\CodeDock\src\controllers\TabSwitcher.py"
    image_list = [
        os.path.join(test_folder, f)
        for f in os.listdir(test_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not image_list:
        print("No images found.")
        sys.exit(1)

    switcher = Ui_Tab_Switcher()
    switcher.setImage(image_list)
    switcher.show()

    sys.exit(app.exec())
