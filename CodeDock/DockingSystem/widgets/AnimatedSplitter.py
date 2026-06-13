
from PyQt6 import QtWidgets,QtCore,QtGui
import typing


if typing.TYPE_CHECKING:
    from CodeDock.DockingSystem.widgets.DockWidget import DockWidget

class SplitterHandle(QtWidgets.QSplitterHandle):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.splitter = parent


    

    """    
    def paintEvent(self, event):/*
        painter = QtGui.QPainter(self)
        print("paint event runnin.......")
        #painter.fillRect(self.rect(), QtGui.QColor("#2c88bd"))

        # draw 3 dots
        painter.setBrush(QtGui.QColor("#f5f5f5"))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        cx = self.width() // 2
        cy = self.height() // 2

        for offset in (-6, 0, 6):
            painter.drawEllipse(cx-2, cy+offset-2, 4, 4)
    """

    def mousePressEvent(self, event):
        index = self.splitter.indexOf(self)
        self.splitter._onHandlePressed(index)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.splitter._onHandleReleased()
        super().mouseReleaseEvent(event)


class AnimatedSplitter(QtWidgets.QSplitter):
    """Splitter with smooth size animation"""
    whenAnimationCreated=QtCore.pyqtSignal(QtCore.QVariantAnimation)
    whenAnimateStart=QtCore.pyqtSignal()
    whenAnimateFinish=QtCore.pyqtSignal()

    whenAnimateRemoveFinish=QtCore.pyqtSignal()
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.animation = None
        self.id_n:int=None
        self._is_animating:bool=False
        self._target_dock_widget:typing.Union[DockWidget,None]=None
        
        self.parent_splitter:typing.Union[AnimatedSplitter,None]=None
        self.container:DockWidget=None
        
        self.setChildrenCollapsible(False)
    
    def getContainer(self):
        return self.container
    
    def getContainerIndex(self)->int:
        return self.parent_splitter.indexOf(self.container)

    def getParentSplitter(self)->"AnimatedSplitter":
        return self.parent_splitter

    def setParentSplitter(self,parent_splitter):
        self.parent_splitter=parent_splitter
        self.container.parent_splitter=parent_splitter

    def createHandle(self):
        return SplitterHandle(self.orientation(), self)

    def _onHandlePressed(self, handle_index):
        # handle_index controls widgets (handle_index-1) and handle_index
        left = handle_index - 1
        right = handle_index

        # Lock all widgets
        for i in range(self.count()):
            self.setStretchFactor(i, 0)

        # Unlock only adjacent widgets
        if 0 <= left < self.count():
            self.setStretchFactor(left, 1)

        if 0 <= right < self.count():
            self.setStretchFactor(right, 1)

    def _onHandleReleased(self):
        # Restore default behavior``
        for i in range(self.count()):
            self.setStretchFactor(i, 1)


    def animateInsert(self,dock_Widget, index,target_sizes, duration=400):
        """Animate widgeoot insertion to target sizes"""
        
        # Get current sizes
        start_sizes = self.sizes().copy()
        
        # Set new widget to 0 initially
        start_sizes[index] = 0
        self.setSizes(start_sizes)
        
        self.whenAnimateStart.emit()
        
    
        # Create animation from 0.0 to 1.0 (progress)
        self.animation = QtCore.QVariantAnimation(self)
        self.whenAnimationCreated.emit(self.animation)
        self.animation.setDuration(duration)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        # Update function - interpolate all sizes
        def update_size(progress):
            interpolated_sizes = []
            for i in range(len(start_sizes)):
                start_val = start_sizes[i]
                target_val = target_sizes[i]
                current_val = start_val + (target_val - start_val) * progress
                interpolated_sizes.append(int(current_val))
            self.setSizes(interpolated_sizes)
        
        self.animation.valueChanged.connect(update_size)
        self.animation.finished.connect(lambda:self.whenAnimateFinish.emit())

        self.animation.start()
        

    def animateRemove(self, index,dock_widget, target_sizes, duration=300,callback=None):
        """Animate widget removal to target sizes"""
        
        # Get current sizes
        start_sizes = self.sizes().copy()
        
        self.whenAnimateStart.emit()
        # Stop any existing animation

        self.animation = QtCore.QVariantAnimation(self)
        self.whenAnimationCreated.emit(self.animation)
        self.animation.setDuration(duration)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InExpo)  # InCubic for removal
        
        # Update function - interpolate all sizes
        def update_size(progress):
            interpolated_sizes = []
            for i in range(len(start_sizes)):
                start_val = start_sizes[i]
                target_val = target_sizes[i]
                current_val = start_val + (target_val - start_val) * progress
                interpolated_sizes.append(int(current_val))
            self.setSizes(interpolated_sizes)
        
        self.animation.valueChanged.connect(update_size)
        
        
        self.animation.finished.connect(callback)
        self.animation.finished.connect(lambda:self.whenAnimateFinish.emit())

        self.animation.start()  