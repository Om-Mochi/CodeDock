from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.DockingSystem.core.SplitterManager import SplitterManager
from CodeDock.DockingSystem.widgets.DockWidget import DockWidget
from CodeDock.DockingSystem.widgets.DropIndicatorWidget import DropIndicatorWidget 
from CodeDock.DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter
from CodeDock.DockingSystem.core.States import DockPlacement
from CodeDock.DockingSystem.enums.Sides import Sides
from CodeDock.DockingSystem.core.SettingsManager import DockWidgetStyle
from CodeDock.DockingSystem.Debuger import Debug
#from CodeDock.DockingSystem.core.SessionManager import SessionManager

import typing
import functools

class DockZone(QtWidgets.QFrame):

    whenPathUrlDroped=QtCore.pyqtSignal(str,DockWidget)
    whenWidgetDroped=QtCore.pyqtSignal(QtCore.QObject)
    whenMouseReleaseWithDrop=QtCore.pyqtSignal(DockWidget)
    whenDockActivated=QtCore.pyqtSignal(DockWidget)
    whenDockClose=QtCore.pyqtSignal(DockWidget)
    whenKey_Ctrl_Shift_Tab_Pressed=QtCore.pyqtSignal()
    whenKey_Ctrl_Tab_Pressed=QtCore.pyqtSignal()
   
    def __init__(self):
        super().__init__()
        self.whenDockClose.connect
        self.setContentsMargins(0,0,0,0)
        self.setAcceptDrops(True)
        #SplitterManager=SplitterManager()
        self.dock_zone_list:set[DockZone]=set()        
        self.dock_widgets_list:set[DockWidget]=set()

        self.activated_dock_widget:typing.Union[DockWidget,None]=None
        #self.prev_activated_dock_widget:typing.Union[DockWidget,None]=None

        self.prev_temp_splitter:typing.Union[None,AnimatedSplitter]=None
        self.prev_hosted_dock:typing.Union[None,DockWidget]=None
        #SplitterManager.prev_drop_indicator_widget:typing.Union[None,DropIndicatorWidget]=None
        #SplitterManager.prev_drop_indicator_widget_list:list[DropIndicatorWidget]=None
        #self.dock_placement.prevSide:typing.Union[Sides,None]=None
        self.parent_zone:typing.Union[DockZone,None]=None
        
        self.is_any_dock_maximized:bool=False
        self.is_hidden:bool=True
        self._is_mouseL_pressed:bool=False
        
        self.cur_dock_widget:DockWidget=None
        self.prev_stretched_dock_widget:DockWidget=None
        self.stretch:typing.Union[int,None]=None
        self.prev_key_type:QtCore.Qt.Key=None


        self.main_layout=QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.maximize_container=QtWidgets.QWidget()
        self.maximize_container_layout=QtWidgets.QVBoxLayout()
        self.maximize_container.setLayout(self.maximize_container_layout)
        self.maximize_container.setContentsMargins(0,0,0,0)
        self.maximize_container_layout.setContentsMargins(0,0,0,0)

        self.main_layout.addWidget(self.maximize_container)
        self.maximize_container.hide()
        self.maximized_dock:typing.Union[DockWidget,None]=None
        self.maximized_dock_splitter:AnimatedSplitter
        self.maximized_dock_splitter_index:int
        self.maximized_dock_splitter_sizes:list[int]=[]

        self.root_splitter:AnimatedSplitter
        self.main_container:DockWidget
        self.main_container,self.root_splitter=SplitterManager.getHorizontalSplitter()
        self.main_layout.addWidget(self.main_container)
        
        #self.owner_dock=None
        #self.main_splitter.setStyleSheet("border:2px solid #FFFFFF")
        self.setAutoFillBackground(True)

        #self.prev_dock_widget:DockWidget=None
        
        self.dock_placement:DockPlacement=DockPlacement(
                            side=None,
                            prevSide=None,
                            newSplitter=None,
                            splitterIndex=None,
                            splitterOn=None,
                            splitterContainer=None,
                            source=None
                                                        )
        
        self.labl_i=0
        self.setObjectName("MainDockZone")
        self.setStyleSheet("""
            MainDockZone {
                background-color: #1F1F1F;
                border:2px solid #5C705C;
            }
        """)
        self.max_btn=None
        self.min_btn=None
        self.close_btn=None

    def setPathH(self,Path_h):
        self.min_btn=QtGui.QIcon(Path_h.MINIMIZE_ICON)
        self.max_btn=QtGui.QIcon(Path_h.MAXIMIZE_ICON)
        self.close_btn=QtGui.QIcon(Path_h.CLOSE_ICON)
            
    #def geSelf(self)->'DockZone':return self

    def detectZone(self):
        
        ...

    def _createInnerDockZone(self):

        inner_dock_zone=DockZone()
        inner_dock_zone.parent_zone=self
        self.dock_zone_list.add(inner_dock_zone)
    
    def setDropIndicatorWidget(
            self,widget:typing.Union[QtCore.QObject,None]=None,
            splitter:typing.Union[AnimatedSplitter,None]=None,
            splitter_index:int=None,
            ) -> DropIndicatorWidget:
        
        indicator_widget=DropIndicatorWidget()
        
        indicator_widget.whenWidgetDroped.connect(self.createAndSetDockWidget)
        indicator_widget.whenPathUrlDroped.connect(self.onPathUrlDropped)
        indicator_widget.whenMouseLeaveWithDrage.connect(SplitterManager.removeDropIndicatoreWidget)


        if splitter:
            #container,splitter=SplitterManager.getVerticalSplitter()
            #splitter_on.insertWidget(dock_widget,splitter_in_index)
            #splitter_in.insertWidget(splitter_container,splitter_in_index)
                        
            SplitterManager.startAnimationInsert(splitter,splitter_index,indicator_widget)
            SplitterManager.prev_drop_indicator_widget=indicator_widget
            
            indicator_widget.parent_splitter=splitter
            
        else:
            #print(self.RED+" heree eeeee... . ... .. .. .. . . "+self.RESET)
            self.root_splitter.addWidget(indicator_widget)
            indicator_widget.setParent(self.root_splitter)
            indicator_widget.parent_splitter=self.root_splitter
        
            #dock_widget.whenPathUrlDroped.connect(lambda s:self.whenWidgetDroped.emit(s,self.cur_dock_widget))
        return indicator_widget
    

    def addDockWidget(
            self,widget:typing.Union[QtCore.QObject,None],
            splitter:typing.Union[AnimatedSplitter,None]=None,
            splitter_index:int=None,
            source=None,
            duration=300
            ) -> DockWidget:
        
    
        if source==None:
            dock_widget=DockWidget()
            self.dock_widgets_list.add(dock_widget)

            dock_widget.initTitlebar()
            dock_widget.title_bar.close_button.setIcon(self.close_btn)
            dock_widget.title_bar.maximize_button.setIcon(self.max_btn)
            dock_widget.title_bar.minimize_button.setIcon(self.min_btn)


            dock_widget.addWidget(widget)
            
            if widget:
                widget.setParent(dock_widget)
            
            self.cur_dock_widget=dock_widget
            dock_widget.whenMouseDrag.connect(self.calCenterZone)
            dock_widget.when_Ctrl_MovementsKeyPressed.connect(self.dynamicDockResize)
            #dock_widget.whenMouseEnterWithDrage.connect(self.handleMouseDrageFlage)
            dock_widget.whenWidgetDroped.connect(self.createAndSetDockWidget)
            dock_widget.whenPathUrlDroped.connect(self.onPathUrlDropped)
            dock_widget.whenMouseLeftClick.connect(self.setActivatDock)
            dock_widget.whenFocusIn.connect(self.setActivatDock)
            dock_widget.title_bar.whenDockToMaximizeBtnPressed.connect(self.setDockToMaximize)
            dock_widget.title_bar.whenMaximizeToDockBtnPressed.connect(self.setMaximizedToDock)
            dock_widget.title_bar.whenDockDragActive.connect(lambda dock:SplitterManager.onDockMoveActive(dock))
            dock_widget.title_bar.whenCloseBtnPressed.connect(self.onDockCloseSignal)
            dock_widget.title_bar.whenMiniMizeBtnPressed.connect(self.onDockMinimizeSignal)


            #dock_widget.title_bar.whenMiniMizeBtnPressed.connect(self.setMaximizedToDock)

            
            #dock_widget.whenWidgetDroped.connect(lambda s:self.whenPathUrlDroped.emit(s,self.cur_dock_widget))


        else:
            dock_widget=source
            
        #if not is_temp and source==None:

        #dock_widget.setObjectName("DockWidget")
        #dock_widget.enableStyleSheet()
            

        if splitter:
            #container,splitter=SplitterManager.getVerticalSplitter()
            #splitter_on.insertWidget(dock_widget,splitter_in_index)
            #splitter_in.insertWidget(splitter_container,splitter_in_index)
            
            SplitterManager.startAnimationInsert(splitter=splitter,index=splitter_index,widget=dock_widget,duration=duration)
            dock_widget.parent_splitter=splitter
            
        else:
            if self.activated_dock_widget:
                splitter=self.activated_dock_widget.parent_splitter
            else:splitter=self.root_splitter
            splitter.addWidget(dock_widget)
            dock_widget.setParent(splitter)
            dock_widget.parent_splitter=splitter
                    
        DockWidgetStyle.setDeActivatedStyleSheet(dock_widget)
        DockWidgetStyle.setOtherStyles(dock_widget)

        self.setActivatDock(dock_widget)
            #dock_widget.whenPathUrlDroped.connect(lambda s:self.whenWidgetDroped.emit(s,self.cur_dock_widget))
        return dock_widget
    


    def onPathUrlDropped(self,url):

        self.createAndSetDockWidget(None)
        
        if (
            self.dock_placement.side!=Sides.NONE
            and self.dock_placement.side!=Sides.CENTER
            ):
            self.whenPathUrlDroped.emit(url,self.cur_dock_widget)

    def setActivatDock(self,dock_widget:DockWidget):

        if self.activated_dock_widget==None:
            self.activated_dock_widget=dock_widget
            DockWidgetStyle.setActivatedStyleSheet(dock_widget)
            return

        if self.activated_dock_widget!=dock_widget:
            DockWidgetStyle.setDeActivatedStyleSheet(self.activated_dock_widget)
            DockWidgetStyle.setActivatedStyleSheet(dock_widget)
            self.activated_dock_widget=dock_widget
            self.whenDockActivated.emit(dock_widget)

        
    def dynamicDockResize(self,key_type:QtCore.Qt.Key,dock_widget:DockWidget):
        
        if self.prev_stretched_dock_widget==dock_widget:
            
            if self.prev_key_type==key_type:
                self.stretch+=1
            else:
                self.prev_key_type=key_type
                self.stretch=1

            if key_type==QtCore.Qt.Key.Key_Up:
                self.reduceDockSizeUpward(self.stretch,dock_widget)
            
            elif key_type==QtCore.Qt.Key.Key_Down:

                self.expandDockSizeDownward(self.stretch,dock_widget)

            elif key_type==QtCore.Qt.Key.Key_Left:
                self.reduceDockSizeLeftward(self.stretch,dock_widget)
            elif key_type==QtCore.Qt.Key.Key_Right:
                self.expandDockSizeRightward(self.stretch,dock_widget)
                
            
        self.prev_stretched_dock_widget=dock_widget


    #def _expandDockSize(self,host_splitter,)

    def expandDockSizeDownward(self,strock_count:int,dock_widget:DockWidget):        
        
        splitter=dock_widget.parent_splitter
        parent_splitter=splitter.parent_splitter
        dock_index=splitter.indexOf(dock_widget)

        splitter_widget_max=splitter.count()-1 
        
        if parent_splitter==None:
            return
        if parent_splitter.parent_splitter==None:
            return


        if  0 == dock_index or splitter_widget_max == dock_index:

            #if splitter widgets are more than 2
            if splitter_widget_max >= 2:
                Debug.red("splitter max ")
                h_splitter:AnimatedSplitter
                container,h_splitter=SplitterManager.getHorizontalSplitter()
                
                container_index=parent_splitter.indexOf(splitter.container)
                print(dock_widget.title())
                dock_widget.setParent(None)
                print(dock_widget.title())
                
                splitter.container.setParent(None)

                parent_splitter.insertWidget(container_index,container)
                
                h_splitter.setParentSplitter(parent_splitter)                
                splitter.setParentSplitter(h_splitter)
                
                if dock_index==0:
                    h_splitter.addWidget(dock_widget)
                    h_splitter.addWidget(splitter.container)
                    dock_widget.setParentSplitter(h_splitter)
                    dock_index=0
                else:

                    h_splitter.addWidget(splitter.container)    
                    h_splitter.addWidget(dock_widget)
                    dock_widget.setParentSplitter(h_splitter)
                    dock_index=1

                splitter=h_splitter


            else:pass
            
            neighbor_dock:DockWidget
            neighbor_dock=splitter.widget(1-dock_index)
            
            #if parent_splitter.count() == 1:pass
            
            if (neighbor_dock.is_container 
                and neighbor_dock.child_splitter.orientation()==QtCore.Qt.Orientation.Horizontal
                or not neighbor_dock.is_container
                ):
                v_splitter:AnimatedSplitter
                vcontainer,v_splitter=SplitterManager.getVerticalSplitter()
                
                splitter_sizes=splitter.sizes()
                Debug.green(splitter.sizes())
                
                neighbor_dock.setParent(None)
                splitter.insertWidget(1-dock_index,vcontainer)
                v_splitter.setParentSplitter(splitter)
                v_splitter.addWidget(neighbor_dock)
                splitter.setSizes(splitter_sizes)
                neighbor_dock.parent_splitter=v_splitter
                
                splitter_container_index=parent_splitter.indexOf(splitter.container)            
                splitter_container_index+=1

                if splitter_container_index < parent_splitter.count():
                    parent_dock_widget=parent_splitter.widget(splitter_container_index)
                    parent_splitter_sizes:list=parent_splitter.sizes()
                    dock_widget_hieght=parent_splitter_sizes[splitter_container_index]
                    container_hieght=parent_splitter_sizes[splitter_container_index-1]
                    
                    v_splitter.addWidget(parent_dock_widget)
                    v_splitter.setSizes([container_hieght, dock_widget_hieght])
                    Debug.blue(v_splitter.sizes())
                    parent_splitter_sizes.pop(splitter_container_index)
                    parent_splitter_sizes[splitter_container_index-1]=dock_widget_hieght+container_hieght
                    parent_splitter.setSizes(parent_splitter_sizes)
                    Debug.blue(parent_splitter.sizes())
                    parent_dock_widget.parent_splitter=v_splitter

                    if splitter_container_index == parent_splitter.count():
                        s_parent_splitter=parent_splitter.parent_splitter                 
                         
                        if splitter_container_index > 1:
                            return
                        
                        if s_parent_splitter==None:
                            
                            splitter.container.setParent(None)
                            parent_splitter.container.setParent(None)
                            parent_splitter.container.deleteLater()
                            self.main_layout.addWidget(splitter.container)
                            self.root_splitter=splitter
                            splitter.parent_splitter=None
                            return
                        

                        container_index=s_parent_splitter.indexOf(parent_splitter.container)
                        
                        dock_widget.setParent(None)
                        v_splitter.container.setParent(None)
                        splitter.container.setParent(None)


                        if dock_index==0:
                            s_parent_splitter.insertWidget(container_index,dock_widget)
                            s_parent_splitter.insertWidget(container_index + 1,v_splitter.container)
                            
                            v_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)
                        else:
                            s_parent_splitter.insertWidget(container_index,v_splitter.container)
                            s_parent_splitter.insertWidget(container_index + 1,dock_widget)
                            
                            v_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)

                        splitter.container.deleteLater()
                        parent_splitter.container.setParent(None)
                        parent_splitter.container.deleteLater()
                        dock_widget.setFocus()
                        self.setActivatDock(dock_widget)
            elif (neighbor_dock.is_container 
                and neighbor_dock.child_splitter.orientation()==QtCore.Qt.Orientation.Vertical
                ):

                splitter_container_index=parent_splitter.indexOf(splitter.container)            
                splitter_container_index+=1


                if splitter_container_index < parent_splitter.count():
                    v_splitter=neighbor_dock.child_splitter
                    v_splitter_sizes:list=v_splitter.sizes()
                    parent_dock_widget=parent_splitter.widget(splitter_container_index)
                    parent_splitter_sizes:list=parent_splitter.sizes()
                    dock_widget_hieght=parent_splitter_sizes[splitter_container_index]
                    container_hieght=parent_splitter_sizes[splitter_container_index-1]
                    
                    v_splitter.addWidget(parent_dock_widget)
                    v_splitter_sizes.append(dock_widget_hieght)
                    v_splitter.setSizes(v_splitter_sizes)

                    parent_splitter_sizes.pop(splitter_container_index)
                    parent_splitter_sizes[splitter_container_index-1]=dock_widget_hieght+container_hieght
                    parent_splitter.setSizes(parent_splitter_sizes)
                    parent_dock_widget.parent_splitter=v_splitter

                    if splitter_container_index == parent_splitter.count():
                        s_parent_splitter=parent_splitter.parent_splitter        

                        #if index not 0
                        if splitter_container_index > 1:
                           
                            return
                         
                        if s_parent_splitter==None:
                            splitter.container.setParent(None)
                            parent_splitter.container.setParent(None)
                            parent_splitter.container.deleteLater()
                            self.main_layout.addWidget(splitter.container)
                            self.root_splitter=splitter
                            splitter.parent_splitter=None
                            return
                        

                        container_index=s_parent_splitter.indexOf(parent_splitter.container)
                        p_slitter_sizes=splitter.sizes()

                        s_splitter_sizes=s_parent_splitter.sizes()
                        dock_widget.setParent(None)
                        neighbor_dock.setParent(None)
                        splitter.container.setParent(None)

                        if dock_index==0:
                            s_parent_splitter.insertWidget(container_index,dock_widget)
                            s_parent_splitter.insertWidget(container_index + 1,neighbor_dock)

                            v_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)
                        else:
                            s_parent_splitter.insertWidget(container_index,neighbor_dock)
                            s_parent_splitter.insertWidget(container_index + 1,dock_widget)
                            
                            v_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)


                        s_splitter_sizes.pop(container_index)
                        s_parent_splitter.setSizes(s_splitter_sizes+p_slitter_sizes)

                        splitter.container.deleteLater()
                        parent_splitter.container.setParent(None)
                        parent_splitter.container.deleteLater()
                        dock_widget.setFocus()
                        self.setActivatDock(dock_widget)
        else:pass


    def expandDockSizeRightward(self,strock_count:int,dock_widget:DockWidget):        

        splitter=dock_widget.parent_splitter
        parent_splitter=splitter.parent_splitter
        dock_index=splitter.indexOf(dock_widget)
        
        if parent_splitter==None:
            return


        splitter_widget_max=splitter.count()-1 

        if  0 == dock_index or splitter_widget_max == dock_index:

            #if splitter widgets are more than 2
            if splitter_widget_max >= 2:
                
                h_splitter:AnimatedSplitter
                container,h_splitter=SplitterManager.getVerticalSplitter()
                
                container_index=parent_splitter.indexOf(splitter.container)
                splitter.container.setParent(None)

                parent_splitter.insertWidget(container_index,container)
                
                h_splitter.setParentSplitter(parent_splitter)
                splitter.setParentSplitter(h_splitter)
                

                dock_widget.setParent(None)

                if dock_index==0:
                    h_splitter.addWidget(dock_widget)
                    h_splitter.addWidget(splitter.container)
                    dock_widget.setParentSplitter(h_splitter)
                    dock_index=0
                else:
                    h_splitter.addWidget(splitter.container)
                    h_splitter.addWidget(dock_widget)
                    dock_widget.setParentSplitter(h_splitter)
                    dock_index=1

                splitter=h_splitter

            else:pass
            
            neighbor_dock:DockWidget
            neighbor_dock=splitter.widget(1-dock_index)
            
            #if parent_splitter.count() == 1:pass

            if (neighbor_dock.is_container 
                and neighbor_dock.child_splitter.orientation()==QtCore.Qt.Orientation.Vertical
                or not neighbor_dock.is_container
                ):
                h_splitter:AnimatedSplitter
                vcontainer,h_splitter=SplitterManager.getHorizontalSplitter()

                splitter_sizes=splitter.sizes()

                neighbor_dock.setParent(None)
                splitter.insertWidget(1-dock_index,vcontainer)
                h_splitter.setParentSplitter(splitter)
                h_splitter.addWidget(neighbor_dock)
                neighbor_dock.parent_splitter=h_splitter
                splitter.setSizes(splitter_sizes)

                splitter_container_index=parent_splitter.indexOf(splitter.container)            
                splitter_container_index+=1

                if splitter_container_index < parent_splitter.count():
                    
                    parent_dock_widget=parent_splitter.widget(splitter_container_index)
                    parent_splitter_sizes:list=parent_splitter.sizes()
                    dock_widget_hieght=parent_splitter_sizes[splitter_container_index]
                    container_hieght=parent_splitter_sizes[splitter_container_index-1]
                    
                    h_splitter.addWidget(parent_dock_widget)
                    h_splitter.setSizes([container_hieght, dock_widget_hieght])
                    parent_splitter_sizes.pop(splitter_container_index)
                    parent_splitter_sizes[splitter_container_index-1]=dock_widget_hieght+container_hieght
                    parent_splitter.setSizes(parent_splitter_sizes)
                    parent_dock_widget.parent_splitter=h_splitter

                    if splitter_container_index == parent_splitter.count():
                        s_parent_splitter=parent_splitter.parent_splitter
                        
                        if splitter_container_index > 1:
                            return

                        if s_parent_splitter==None:
                            splitter.container.setParent(None)
                            parent_splitter.container.setParent(None)
                            parent_splitter.container.deleteLater()
                            self.main_layout.addWidget(splitter.container)
                            self.root_splitter=splitter
                            splitter.parent_splitter=None
                            return
                        
                        container_index=s_parent_splitter.indexOf(parent_splitter.container)
                        dock_widget.setParent(None)
                        h_splitter.container.setParent(None)
                        splitter.container.setParent(None)


                        if dock_index==0:
                            s_parent_splitter.insertWidget(container_index,dock_widget)
                            s_parent_splitter.insertWidget(container_index + 1,h_splitter.container)
                            
                            h_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)
                        else:
                            s_parent_splitter.insertWidget(container_index,h_splitter.container)
                            s_parent_splitter.insertWidget(container_index + 1,dock_widget)
                            
                            h_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)

                        splitter.container.deleteLater()
                        parent_splitter.container.setParent(None)
                        parent_splitter.container.deleteLater()
                        dock_widget.setFocus()
                        self.setActivatDock(dock_widget)
            elif (neighbor_dock.is_container 
                and neighbor_dock.child_splitter.orientation()==QtCore.Qt.Orientation.Horizontal
                ):

                splitter_container_index=parent_splitter.indexOf(splitter.container)            
                splitter_container_index+=1


                if splitter_container_index < parent_splitter.count():
                    h_splitter=neighbor_dock.child_splitter
                    h_splitter_sizes:list=h_splitter.sizes()
                    parent_dock_widget=parent_splitter.widget(splitter_container_index)
                    parent_splitter_sizes:list=parent_splitter.sizes()
                    dock_widget_hieght=parent_splitter_sizes[splitter_container_index]
                    container_hieght=parent_splitter_sizes[splitter_container_index-1]
                    
                    h_splitter.addWidget(parent_dock_widget)
                    h_splitter_sizes.append(dock_widget_hieght)
                    h_splitter.setSizes(h_splitter_sizes)

                    parent_splitter_sizes.pop(splitter_container_index)
                    parent_splitter_sizes[splitter_container_index-1]=dock_widget_hieght+container_hieght
                    parent_splitter.setSizes(parent_splitter_sizes)
                    parent_dock_widget.parent_splitter=h_splitter

                    if splitter_container_index == parent_splitter.count():
                        s_parent_splitter=parent_splitter.parent_splitter                        
                        
                        if splitter_container_index > 1:
                            return

                        if s_parent_splitter==None:
                            splitter.container.setParent(None)
                            parent_splitter.container.setParent(None)
                            parent_splitter.container.deleteLater()
                            self.main_layout.addWidget(splitter.container)
                            self.root_splitter=splitter
                            splitter.parent_splitter=None
                            return
                        
                        container_index=s_parent_splitter.indexOf(parent_splitter.container)
                        p_slitter_sizes=splitter.sizes()

                        s_splitter_sizes=s_parent_splitter.sizes()
                        dock_widget.setParent(None)
                        neighbor_dock.setParent(None)
                        splitter.container.setParent(None)

                        if dock_index==0:
                            s_parent_splitter.insertWidget(container_index,dock_widget)
                            s_parent_splitter.insertWidget(container_index + 1,neighbor_dock)
                            
                            h_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)
                        else:
                            s_parent_splitter.insertWidget(container_index,neighbor_dock)
                            s_parent_splitter.insertWidget(container_index + 1,dock_widget)
                            
                            h_splitter.setParentSplitter(s_parent_splitter)
                            dock_widget.setParentSplitter(s_parent_splitter)


                        s_splitter_sizes.pop(container_index)
                        s_parent_splitter.setSizes(s_splitter_sizes+p_slitter_sizes)

                        splitter.container.deleteLater()
                        parent_splitter.container.setParent(None)
                        parent_splitter.container.deleteLater()
                        dock_widget.setFocus()
                        self.setActivatDock(dock_widget)

    def reduceDockSizeUpward(self, strock_count: int, dock_widget: DockWidget):        
        splitter=dock_widget.parent_splitter
        parent_splitter=splitter.parent_splitter
        dock_index=splitter.indexOf(dock_widget)
        splitter_widget_max=splitter.count()-1 

        #if splitter_widget_max > 2:
        neighbor_dock=splitter.widget(dock_index-1)
        neighbor_dock_index=dock_index-1


        
        neighbor_dock:DockWidget
        if neighbor_dock.is_container!=True:
            
            return
        
        neighbor_splitter=neighbor_dock.child_splitter
        print(splitter_widget_max)
        if parent_splitter==None or splitter_widget_max>=2:

            v_container,new_v_splitter=SplitterManager.getVerticalSplitter()
            h_container,new_h_splitter=SplitterManager.getHorizontalSplitter()
            
            v_container:DockWidget
            new_h_splitter:AnimatedSplitter
            h_container:DockWidget
            new_v_splitter:AnimatedSplitter

            splitter_sizes=splitter.sizes()
            neighbor_dock.setParent(None)
            splitter.insertWidget(neighbor_dock_index,v_container)
            
            new_v_splitter.setParentSplitter(splitter)
            
            new_v_splitter.addWidget(h_container)
            new_h_splitter.setParentSplitter(new_v_splitter)
            
            new_h_splitter.addWidget(neighbor_dock)
            neighbor_splitter.setParentSplitter(new_h_splitter)

            dock_widget.setParent(None)
            new_h_splitter.addWidget(dock_widget)
            dock_widget.setParentSplitter(new_h_splitter)

            dock_size=splitter_sizes.pop(dock_index)
            new_h_splitter.setSizes([splitter_sizes[neighbor_dock_index],dock_size])
            splitter_sizes[neighbor_dock_index]+=dock_size
            splitter.setSizes(splitter_sizes)
            
            dock_widget.setFocus()
            self.setActivatDock(dock_widget)
            self.reduceDockSizeUpward(0,dock_widget)

        elif parent_splitter.orientation() == QtCore.Qt.Orientation.Vertical:
            neighbor_splitter_max=neighbor_splitter.count()-1

            if neighbor_splitter_max == 0:
                return
            
            target_dock_widget=neighbor_splitter.widget(neighbor_splitter_max)
            target_dock_widget:DockWidget
            
            splitter_container_index=parent_splitter.indexOf(splitter.container)

            neighbor_splitter_sizes=neighbor_splitter.sizes()
            parent_splitter_sizes=parent_splitter.sizes()


            splitter_container_sizes=parent_splitter_sizes.pop(splitter_container_index)

            target_dock_widget.setParent(None)
            parent_splitter.insertWidget(splitter_container_index+1,target_dock_widget)
            target_dock_widget.setParentSplitter(parent_splitter)

            target_widget_size=neighbor_splitter_sizes.pop(neighbor_splitter_max)
            parent_splitter_sizes.insert(neighbor_dock_index,splitter_container_sizes-target_widget_size)
            parent_splitter_sizes.insert(neighbor_dock_index+1,target_widget_size)
            parent_splitter.setSizes(parent_splitter_sizes)
            neighbor_splitter.setSizes(neighbor_splitter_sizes)

            dock_widget.setFocus()
            self.setActivatDock(dock_widget)
    
    def reduceDockSizeLeftward(self,strock_count:int,dock_widget:DockWidget):        
        ...

    def createAndSetDockWidget(self,widget:DockWidget):
        
        if SplitterManager.prev_drop_indicator_widget!=None: 
            if (
                self.dock_placement.side!=Sides.NONE
                and self.dock_placement.side!=Sides.CENTER
                ):
                
                splitter=SplitterManager.prev_drop_indicator_widget.parent_splitter
                index=splitter.indexOf(SplitterManager.prev_drop_indicator_widget)
                
                self.removeDock(SplitterManager.prev_drop_indicator_widget)
            
                SplitterManager.prev_drop_indicator_widget=None
                self.dock_placement.prevSide=None
    

                dock_widget=self.addDockWidget(
                                    widget=None,
                                    splitter=splitter,
                                    splitter_index=index,
                                    source=self.dock_placement.source,
                                    duration=100
                                    )
                
                self.whenMouseReleaseWithDrop.emit(dock_widget)
        
    def createDockPlacement(self,host_widget:DockWidget,source=None):
        
        if self.dock_placement.side!=Sides.NONE and self.dock_placement.side!=Sides.CENTER:
            
        
            #SplitterManager.removeAnimatingDock()
            if SplitterManager.prev_drop_indicator_widget:
                SplitterManager.removeDockFromSplitter(SplitterManager.prev_drop_indicator_widget)
                SplitterManager.prev_drop_indicator_widget=None
            parent_splitter=host_widget.parent_splitter
            #print("on create final dock space",parent_splitter,"\n",widget.objectName())    
            splitter_index=parent_splitter.indexOf(host_widget)


            if self.dock_placement.side == Sides.TOP or self.dock_placement.side == Sides.BOTTOM:
                
                if parent_splitter.orientation()==QtCore.Qt.Orientation.Vertical:

                    self.dock_placement.newSplitter=parent_splitter
                    
                    if self.dock_placement.side == Sides.TOP:
                        self.dock_placement.splitterIndex=splitter_index

                    elif self.dock_placement.side == Sides.BOTTOM:
                        self.dock_placement.splitterIndex=splitter_index+1
                    
                    #self.prev_temp_splitter=None
                
                elif parent_splitter.orientation()==QtCore.Qt.Orientation.Horizontal:
                                    
                    parent_splitter_sizes=parent_splitter.sizes()                    
                
                    host_widget.setParent(None)
                    container,new_splitter=SplitterManager.getVerticalSplitter()
                    
                    self.prev_temp_splitter=new_splitter
                    

                    #SplitterManager.insertWidget(parent_splitter,splitter_index,container,container_size)
                    parent_splitter.insertWidget(splitter_index,container)
                    parent_splitter.setSizes(parent_splitter_sizes)

                    new_splitter.addWidget(host_widget)
                    host_widget.parent_splitter=new_splitter
                    self.dock_placement.splitterContainer=container
                    self.dock_placement.newSplitter=new_splitter
                    new_splitter.parent_splitter=parent_splitter

                    if self.dock_placement.side == Sides.TOP:
                        self.dock_placement.splitterIndex=0

                    elif self.dock_placement.side == Sides.BOTTOM:
                        self.dock_placement.splitterIndex=1


                               
            elif self.dock_placement.side == Sides.LEFT or self.dock_placement.side == Sides.RIGHT:
                
                if parent_splitter.orientation()==QtCore.Qt.Orientation.Horizontal:
                
                    self.dock_placement.newSplitter=parent_splitter

                    if self.dock_placement.side == Sides.LEFT:
                        self.dock_placement.splitterIndex=splitter_index

                    elif self.dock_placement.side == Sides.RIGHT:
                        self.dock_placement.splitterIndex=splitter_index+1

                    #self.prev_temp_splitter=None

                elif parent_splitter.orientation()==QtCore.Qt.Orientation.Vertical:

                
                    parent_splitter_sizes=parent_splitter.sizes()                    
                
                    host_widget.setParent(None)
                    container,new_splitter=SplitterManager.getHorizontalSplitter()
                    
                    self.prev_temp_splitter=new_splitter
                    

                    #SplitterManager.insertWidget(parent_splitter,splitter_index,container,container_size)
                    parent_splitter.insertWidget(splitter_index,container)
                    parent_splitter.setSizes(parent_splitter_sizes)

                    new_splitter.addWidget(host_widget)
                    host_widget.parent_splitter=new_splitter
                    self.dock_placement.splitterContainer=container
                    self.dock_placement.newSplitter=new_splitter
                    new_splitter.parent_splitter=parent_splitter

                    if self.dock_placement.side == Sides.LEFT:
                        self.dock_placement.splitterIndex=0

                    elif self.dock_placement.side == Sides.RIGHT:
                        self.dock_placement.splitterIndex=1
                        

                    
                        
            #print(self.final_dock_widget)
            #print(parent_splitter.sizes())


            self.dock_placement.prevSide=self.dock_placement.side   



            """
            if splitter_index>0:
                if self.final_dock_widget.side == Sides.TOP or self.final_dock_widget.side == Sides.BOTTOM:
                    lb.setGeometry(0,0,widget.width(),widget.height()//2)
                else:
                    lb.setGeometry(0,0,widget.width()//2,widget.height())
                """


            dock_widget=self.setDropIndicatorWidget(
                                widget=None,
                                splitter=self.dock_placement.newSplitter,
                                splitter_index=self.dock_placement.splitterIndex
                                )            
            

    def calCenterZone(self,dw_rect:QtCore.QRect,mouse_pos:QtCore.QPoint,host_widget:DockWidget,source=None):
        #print(mouse_pos)
        if host_widget==self.maximized_dock:
            self.setMaximizedToDock(host_widget)
            return
        width=dw_rect.width()
        height=dw_rect.height()
    
        mouse_x=mouse_pos.x()
        mouse_y=mouse_pos.y()
        
        zone_w=width//2
        zone_h=height//2
        
        zone_top=dw_rect.x() + (width - zone_w) // 2
        zone_left=dw_rect.y() + (height - zone_h) // 2
        zone_bottom=zone_top+zone_w
        zone_right=zone_left+zone_h

        
        """print("\n\n")
        print(mouse_y,"y < top",zone_top)
        print(mouse_x,"x < left",zone_left)
        print(mouse_y,"y > bott",zone_bottom)
        print(mouse_x,"x > righ",zone_right)"""


        if self.prev_hosted_dock!=host_widget:
            self.dock_placement.side=Sides.NONE
                

        if  (mouse_x < zone_top and mouse_y < zone_left or 
             mouse_x < zone_top and mouse_y > zone_right or 
             mouse_x > zone_bottom and mouse_y < zone_left or 
             mouse_x > zone_bottom and mouse_y >zone_right):
            #ingone 4 side corners    
            pass
        
        elif mouse_y<zone_left:
                
            if self.dock_placement.side != Sides.TOP:
                self.dock_placement.side=Sides.TOP
                self.dock_placement.source=source


                if SplitterManager.prev_drop_indicator_widget!=None:
                    #SplitterManager.startAnimationRemove(host_widget.parent_splitter,SplitterManager.prev_drop_indicator_widget,duration=200)
                    
                    #self.dock_placement.prevSide=Sides.NONE
                    #SplitterManager.prev_drop_indicator_widget=None
                    pass
                self.createDockPlacement(host_widget,source=source)
                self.prev_hosted_dock=host_widget

        elif mouse_x<zone_top:
            if self.dock_placement.side != Sides.LEFT:    
                self.dock_placement.side=Sides.LEFT
                self.dock_placement.source=source       
         

                if SplitterManager.prev_drop_indicator_widget!=None:
                    
                    #SplitterManager.startAnimationRemove(host_widget.parent_splitter,SplitterManager.prev_drop_indicator_widget,duration=200)
                    
                    #self.dock_placement.prevSide=Sides.NONE
                    #SplitterManager.prev_drop_indicator_widget=None
                    pass
                self.createDockPlacement(host_widget,source=source)
                self.prev_hosted_dock=host_widget


        elif mouse_y>zone_right:
            if self.dock_placement.side != Sides.BOTTOM:
                self.dock_placement.side=Sides.BOTTOM
                self.dock_placement.source=source

  
                if SplitterManager.prev_drop_indicator_widget!=None:
                    
                    #SplitterManager.startAnimationRemove(host_widget.parent_splitter,SplitterManager.prev_drop_indicator_widget,duration=200)
                
                    #self.dock_placement.prevSide=Sides.NONE
                    #SplitterManager.prev_drop_indicator_widget=None
                    pass

                self.createDockPlacement(host_widget,source=source)
                self.prev_hosted_dock=host_widget


        elif mouse_x>zone_bottom:
            if self.dock_placement.side != Sides.RIGHT:
                self.dock_placement.side=Sides.RIGHT
                self.dock_placement.source=source


                if SplitterManager.prev_drop_indicator_widget!=None:
                    
                    #SplitterManager.startAnimationRemove(host_widget.parent_splitter,SplitterManager.prev_drop_indicator_widget,duration=200)
                
                    #self.dock_placement.prevSide=Sides.NONE
                    #SplitterManager.prev_drop_indicator_widget=None
                    pass
                                      
                self.createDockPlacement(host_widget,source=source)
                self.prev_hosted_dock=host_widget

        else:
            
            if self.dock_placement.side != Sides.CENTER:
                self.dock_placement.side=Sides.CENTER
                #self.prev_hosted_widget=host_widget

                #if self.dock_placement.prevSide != Sides.NONE and SplitterManager.prev_drop_indicator_widget!=None:                
                if SplitterManager.prev_drop_indicator_widget!=None and not SplitterManager.is_animating:                
                
                    #SplitterManager.startAnimationRemove(host_widget.parent_splitter,SplitterManager.prev_drop_indicator_widget,duration=200)
                    SplitterManager.removeDropIndicatoreWidget(SplitterManager.prev_drop_indicator_widget)
                    self.dock_placement.prevSide=Sides.NONE
                    self.dock_placement.side=Sides.NONE
                    #SplitterManager.prev_drop_indicator_widget=None
                    pass
            pass
            #print("on elese")
            #self.final_dock_widget=FinalDockWidget(None,None,None,None,None)

        #print("tottal splitter :",SplitterManager.tottalSplitter())


        #print(self.final_dock_widget)
    def onDockMinimizeSignal(self,dock_widget:DockWidget):
        if self.is_any_dock_maximized:
            self.maximize_container.hide()
            self.main_container.show()
            self.is_any_dock_maximized=False
        dock_widget.hide()
    
    def onDockCloseSignal(self,dock_widget:DockWidget):
        self.whenDockClose.emit(dock_widget)
        SplitterManager.removeDockFromSplitter(dock_widget)
    def onTabClose(self,dock_widget):
        SplitterManager.removeDockFromSplitter(dock_widget)

    def setDockToMaximize(self,dockwidget:DockWidget=None):

        if self.is_any_dock_maximized:
            self.setMaximizedToDock(self.maximized_dock)

        if dockwidget!=self.maximized_dock:    
            self.maximized_dock=dockwidget
            self.maximized_dock_splitter=dockwidget.parent_splitter
            self.maximized_dock_splitter_index=dockwidget.getSplitterIndex()
            self.maximized_dock_splitter_sizes=dockwidget.parent_splitter.sizes()
            self.maximize_container_layout.addWidget(dockwidget)
            self.maximize_container.show()
            self.main_container.hide()
            self.is_any_dock_maximized=True
        #dockwidget.show()


    def setMaximizedToDock(self,dockwidget:DockWidget=None):

        if dockwidget==self.maximized_dock:
            self.maximized_dock=None
            self.maximized_dock_splitter.insertWidget(self.maximized_dock_splitter_index,dockwidget)
            self.maximized_dock_splitter.setSizes(self.maximized_dock_splitter_sizes)
            self.maximize_container.hide()
            self.main_container.show()
            self.is_any_dock_maximized=False
            

    def updateAllDockTheme(self,theme_dict:dict):

        DockWidgetStyle.updateVar(theme_dict)
        DockWidgetStyle.updateAllStyle(theme_dict,self.dock_widgets_list)

    def handleMouseDrageFlage(self,dock_widget:DockWidget,zone_splitter:AnimatedSplitter,splitter_index:int):
        if self.prev_dock_widget!=None:
            self.prev_dock_widget.is_mouse_inside=False
            self.prev_dock_widget=dock_widget


    def removeContainer(self,container:QtWidgets.QWidget):
        container.setParent(None)
        container.deleteLater()
    
    def removeParent(self,widget):
        widget.setParent(None)
    
    def removeDock(self,dock_widget:DockWidget):
        
        #parent_splitter=dock_widget.parent_splitter
        dock_widget.setParent(None)
        dock_widget.deleteLater()
        try:
            print("\ndock removed..... :- ",dock_widget.title())
        except:...

    
    def mousePressEvent(self, event:QtGui.QMouseEvent):
        if event.button()==QtCore.Qt.MouseButton.LeftButton: 
            self._is_mouseL_pressed=True

        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button()==QtCore.Qt.MouseButton.LeftButton:
            self._is_mouseL_pressed=False
        return super().mouseReleaseEvent(event)

    
    def dragEnterEvent(self,event:QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event:QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event:QtGui.QDropEvent):
        widget = event.source()
        
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path=url.toLocalFile()
            
                #if self.dock_placement.side!=Sides.NONE or self.dock_placement.side!=Sides.CENTER:
                
                #self.whenPathUrlDroped.emit(file_path)
            event.acceptProposedAction()

        elif widget:
            self.whenWidgetDroped.emit(widget)
            event.acceptProposedAction()

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_Q:
            self.whenKey_Ctrl_Tab_Pressed.emit()

        if (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier and
            event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier and
            event.key() == QtCore.Qt.Key.Key_Q):
            self.whenKey_Ctrl_Shift_Tab_Pressed.emit()
        return super().keyPressEvent(event)               

 


        """if event.mimeData().hasText():
            # Parse color and name from mime data
            data = event.mimeData().text().split('|')
            color, name = data
            
            # Create fixed widget at drop position
            #widget = FixedWidget(color, f"{name} #Test", self)
            
            # Position at drop location
            #pos = event.position().toPoint()
            self.addDockWidget(QtWidgets.QLabel("0"))
            event.acceptProposedAction()
            """



    def enterEvent(self, event):
        return super().enterEvent(event)
    
    def leaveEvent(self, a0):
        return super().leaveEvent(a0)
