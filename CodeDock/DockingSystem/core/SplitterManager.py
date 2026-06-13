from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.DockingSystem.widgets.DockWidget import DockWidget 
from CodeDock.DockingSystem.widgets.DropIndicatorWidget import DropIndicatorWidget 
from CodeDock.DockingSystem.widgets.DropIndicatorWidget import AnimatedSplitter
from CodeDock.DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter
from CodeDock.DockingSystem.Debuger import Debug
#dd
import typing

class SplitterManagerSignals(QtCore.QObject):
    whenAnimationInsertStart=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenAnimationInsertStop=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenAnimationInsertFinish=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenAnimationRemoveStart=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenAnimationRemoveStop=QtCore.pyqtSignal(QtWidgets.QWidget)
    whenAnimationRemoveFinish=QtCore.pyqtSignal(QtWidgets.QWidget)
    
 
class SplitterManager:
    
    splitter_count:int=0
    splitter_buf:set=set()
    is_animating:bool=False
    prev_drop_indicator_widget:typing.Union[DockWidget,None]=None
    #prev_drop_indicator_widget:typing.Union[DropIndicatorWidget,None]=None
    running_animation:typing.Union[QtCore.QVariantAnimation,None]=None
    Signal=SplitterManagerSignals()
    
    def getHorizontalSplitter() -> tuple[DockWidget,AnimatedSplitter]:
             
        container=DockWidget()
        container.mouse_release_event_state=False
        container.mouse_move_event_state=False
        h_splitter=AnimatedSplitter(QtCore.Qt.Orientation.Horizontal)
        container.addWidget(h_splitter)
        h_splitter.container=container
        container.is_container=True
        container.child_splitter=h_splitter

        h_splitter.setContentsMargins(0,0,0,0)

        
        SplitterManager.splitter_buf.add(h_splitter)
        SplitterManager.splitter_count+=1

        container.setObjectName(f"{SplitterManager.splitter_count}")
        Debug.yellow("Horizontal splitter Created : ",SplitterManager.splitter_count)
        
        h_splitter.id_n=SplitterManager.splitter_count

        h_splitter.whenAnimationCreated.connect(SplitterManager.onAnimationCreated)
        h_splitter.whenAnimateStart.connect(SplitterManager.onAnimateStart)
        h_splitter.whenAnimateFinish.connect(SplitterManager.onAnimateFinish)

        return container,h_splitter
        
    
    def getVerticalSplitter() -> tuple[DockWidget,AnimatedSplitter]:

        container=DockWidget()

    
        container.mouse_release_event_state=False
        container.mouse_move_event_state=False
        
        v_splitter=AnimatedSplitter(QtCore.Qt.Orientation.Vertical)

        container.addWidget(v_splitter)
        v_splitter.container=container
        container.is_container=True
        container.child_splitter=v_splitter
        v_splitter.setContentsMargins(0,0,0,0)

        

        SplitterManager.splitter_buf.add(v_splitter)
        SplitterManager.splitter_count+=1
        v_splitter.id_n=SplitterManager.splitter_count
    
        container.setObjectName(f"{SplitterManager.splitter_count}")
    
        Debug.magenta("Vertical splitter Created : ",SplitterManager.splitter_count)

        v_splitter.whenAnimationCreated.connect(SplitterManager.onAnimationCreated)
        v_splitter.whenAnimateStart.connect(SplitterManager.onAnimateStart)
        v_splitter.whenAnimateFinish.connect(SplitterManager.onAnimateFinish)
        
        return container,v_splitter
    
    def tottalSplitter():return SplitterManager.splitter_count,len(SplitterManager.splitter_buf)
    

    def transferDock(
                    dock_widget:typing.Union[DockWidget,DropIndicatorWidget],
                    target_splitter:AnimatedSplitter,
                    index:typing.Union[int,None]
                        ):
        
        dock_widget.setParent(None)
        dock_widget.parent_splitter=target_splitter
        
        if index!=None:


            target_splitter.insertWidget(index,dock_widget)

        else:

            target_splitter.addWidget(dock_widget)



    def removeDockFromSplitter(dock_widget:typing.Union[DockWidget,DropIndicatorWidget]):
        
        splitter:AnimatedSplitter=dock_widget.parent_splitter
        dock_widget.setParent(None)
        total_widgets:int=splitter.count()
        
        if total_widgets==0:
            #self.removeDockFromSplitter(splitter.container)
            splitter.container.setParent(None)
            splitter.container.deleteLater()

        elif total_widgets == 1 and splitter.parent_splitter != None:
            parent_splitter=splitter.parent_splitter
            sizes=parent_splitter.sizes()
            SplitterManager.transferDock(splitter.widget(0),parent_splitter,parent_splitter.indexOf(splitter.container))
            splitter.container.setParent(None)
            splitter.container.deleteLater()

            parent_splitter.setSizes(sizes)
        dock_widget.deleteLater()
        #SplitterManager.target_dock_widget=None

    def removeDropIndicatoreWidget(diw:DropIndicatorWidget):
        #SplitterManager.removeDockFromSplitter(diw)
        SplitterManager.startAnimationRemove(diw.parent_splitter,diw,duration=500)
        #diw.deleteLater()

    def onDockMoveActive(dock_widget:DockWidget):
        
        splitter=dock_widget.parent_splitter
        index=splitter.indexOf(dock_widget)
        sizes=splitter.sizes()

        temp_dock=DropIndicatorWidget()


        temp_dock.setStyleSheet("background-color:#1B1E24")
        #SplitterManager.prev_drop_indicator_widget=temp_dock
        temp_dock.parent_splitter=splitter
        
        dock_widget.setParent(None)
        splitter.insertWidget(index,temp_dock)
        splitter.setSizes(sizes)
        SplitterManager.removeDockFromSplitter(temp_dock)
        #SplitterManager.removeDropIndicatoreWidget(temp_dock)    
        


    def onAnimationCreated(animation:QtCore.QVariantAnimation):
        SplitterManager.running_animation=animation

    def onAnimateStart():
        SplitterManager.removeAnimatingDock()

    def removeAnimatingDock():
        if SplitterManager.is_animating:
            SplitterManager.running_animation.stop()
            if SplitterManager.prev_drop_indicator_widget:

                #SplitterManager.target_dock_widget.setParent(None)
                #SplitterManager.target_dock_widget.deleteLater()
                SplitterManager.removeDockFromSplitter(SplitterManager.prev_drop_indicator_widget)
                SplitterManager.prev_drop_indicator_widget=None
        
        SplitterManager.running_animation=None
        SplitterManager.is_animating=True
        

    def onAnimateFinish():
        SplitterManager.is_animating=False
        #SplitterManager.prev_drop_indicator_widget=None
        SplitterManager.running_animation=None

    def startAnimationInsert(
            splitter:AnimatedSplitter,
            index:int,
            widget:QtWidgets.QWidget,
            widget_size:int=None,
            duration: int = 3000
            ):
        
        if SplitterManager.is_animating:
            SplitterManager.running_animation.stop()
            SplitterManager.running_animation=None
            SplitterManager.is_animating=False

            if SplitterManager.prev_drop_indicator_widget:

                SplitterManager.removeDockFromSplitter(SplitterManager.prev_drop_indicator_widget)
                #SplitterManager.target_dock_widget.setParent(None)
                #SplitterManager.target_dock_widget.deleteLater()
                SplitterManager.prev_drop_indicator_widget=None
                
        #SplitterManager.prev_drop_indicator_widget=widget


        # Get sizes BEFORE inserting widget
        old_sizes = splitter.sizes()
        old_total_sizes = sum(old_sizes)
        
        # Insert widget
        splitter.insertWidget(index, widget)
        index=splitter.indexOf(widget)
        
        
        if widget_size == None:
            new_widget_ratio = 0.25
        else:
            new_widget_ratio = widget_size / old_total_sizes if old_total_sizes > 0 else 0.25
        
        # Calculate target size for new widget
        possible_new_widget_size = old_total_sizes * new_widget_ratio
        new_total_sizes = old_total_sizes + possible_new_widget_size
        
        # Calculate ratio to shrink existing widgets
        ratio = old_total_sizes / new_total_sizes if new_total_sizes > 0 else 1
        
        # Build target sizes list
        target_sizes = []
        for i in range(len(splitter.sizes())):
            if i == index:
                # New widget gets its target size
                target_sizes.append(int(possible_new_widget_size))
            else:
                # Existing widgets shrink proportionally
                old_idx = i if i < index else i - 1
                if old_idx < len(old_sizes):
                    target_sizes.append(int(old_sizes[old_idx] * ratio))
                else:
                    target_sizes.append(0)
        
        #print("old sizes:", old_sizes)
        #print("target sizes:", target_sizes)
        #print("ratio:", ratio)
        
        # Animate the insertion
        splitter.animateInsert(widget,index,target_sizes,duration=duration)

    def startAnimationRemove(self, dock_widget: DockWidget, animate: bool = True, duration: int = 300):
        """Remove widget with optional animation"""
        
        parent_splitter = dock_widget.parent_splitter

        # Get the index of the widget to remove
        
        if not animate:
            # No animation, just remove
            SplitterManager.removeDockFromSplitter(dock_widget)
            SplitterManager.prev_drop_indicator_widget=None
            #dock_widget.setParent(None)
            #dock_widget.deleteLater()
            return
        
        if SplitterManager.is_animating:
            SplitterManager.running_animation.stop()
            SplitterManager.running_animation=None
            SplitterManager.is_animating=False

        #SplitterManager.prev_drop_indicator_widget=dock_widget

        index = parent_splitter.indexOf(dock_widget)
        # Get current sizes
        current_sizes = parent_splitter.sizes()
        removed_widget_size = current_sizes[index]
        
        # Calculate target sizes (redistribute removed widget's space)
        target_sizes = []
        remaining_total = sum(current_sizes) - removed_widget_size
        
        for i in range(len(current_sizes)):
            if i == index:
                target_sizes.append(0)  # Widget being removed shrinks to 0
            else:
                if remaining_total > 0:
                    # Redistribute proportionally
                    proportion = current_sizes[i] / remaining_total
                    target_sizes.append(int((current_sizes[i] + removed_widget_size * proportion)))
                else:
                    target_sizes.append(current_sizes[i])
        
        #print(f"\nRemoving widget at index {index}")
        #print(f"Current sizes: {current_sizes}")
        #print(f"Target sizes: {target_sizes}")
        
        # Animate removal, then delete widget when done
        

        def when_finish():
            SplitterManager.removeDockFromSplitter(dock_widget)
            #dock_widget.setParent(None)
            #dock_widget.deleteLater()
            SplitterManager.running_animation=None
            SplitterManager.is_animating=False
            SplitterManager.prev_drop_indicator_widget=None
            
        parent_splitter.animateRemove(index,dock_widget, target_sizes, duration,when_finish)


