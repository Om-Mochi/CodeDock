from CodeDock.src.controllers.PathHandler import Path_Handler
from CodeDock.C_Widgets.Custom import Custom
from CodeDock.C_Widgets.CodeArea import MDISubWindow

#from CodeDock.src.controllers.CodeDockMain import Code_Dock_Main
import os

from PyQt6 import QtCore,QtGui
import enum

class ObjectsEnums():
    class Widget(enum.Enum):
        TYPE=enum.auto()
        MAINWINDOW=enum.auto()
        SUBWINDOW=enum.auto()
        VIRTUAL_SPACE=enum.auto()
        DOCK_VIEW=enum.auto()
            
    class MainWindow(enum.Enum):
        GEOMETRY=enum.auto()

    class SubWindow(enum.Enum):
        INDEX=enum.auto()
        TABBAR=enum.auto()
        TITLE=enum.auto()
        GEOMETRY=enum.auto()
        D_PATH=enum.auto()
        O_PATH=enum.auto()
        SCROLL_POS=enum.auto()
        CURSOR_POS=enum.auto()

    class VirtualSpace(enum.Enum):
        INDEX=enum.auto()
        ITEMS=enum.auto()
        TABBAR=enum.auto()
    
    class DockViews(enum.Enum):
        FILET_VIEW=enum.auto()
        SYMBOLT_VIEW=enum.auto()
        MAIN_SPLITTER_SIZE=enum.auto()        
        DOCK_SPLITTER=enum.auto()


class WorkSpace_Handler:

    class Store:
        
        class VirtualSpace():
            def __init__(self):
                self.main_virtualspace_buffer=[]
                self.virtual_id=0
                self.s_path=None
            
            def setStorageDir(self,path):
                self.s_path=path

            def createNewVirtualStorageBuffer(self):
                self.virtual_id+=1
                v_buffer={ObjectsEnums.Widget.TYPE:ObjectsEnums.Widget.VIRTUAL_SPACE
                          ,ObjectsEnums.VirtualSpace.INDEX:self.virtual_id,
                          ObjectsEnums.VirtualSpace.ITEMS:[]}
                
                self.main_virtualspace_buffer.append(v_buffer)
                return v_buffer
            
            def getBuffer(self):
                return self.main_virtualspace_buffer
            
            def storeIt(self):

                with open(self.s_path,"w")as file:
                    file.write(f"{self.main_virtualspace_buffer}")
                    file.close()

        class MainWindow:

            def __init__(self):
                self.mainwindow_buffer={}
                
                
            def setObject(self,virtual_buffer,cd_main):
                self.virtual_buffer=virtual_buffer
                self.cd_main=cd_main

                #self.virtual_buffer[ObjectsEnums.VirtualSpace.ITEMS].append(self.mainwindow_buffer)
                
            def storeIt(self):
                self.mainwindow_buffer={
                    

                }
            def getBuffer(self):
                return self.mainwindow_buffer
            

        class DockViews:
            def __init__(self):
                self.dock_view_buffer={}

            def addBuffer(self,virtual_buffer):
                self.virtual_buffer=virtual_buffer

                self.dock_view_buffer[ObjectsEnums.Widget.TYPE]=ObjectsEnums.Widget.DOCK_VIEW
                self.dock_view_buffer[ObjectsEnums.DockViews.FILET_VIEW]={}
                self.dock_view_buffer[ObjectsEnums.DockViews.SYMBOLT_VIEW]={}
                self.virtual_buffer[ObjectsEnums.VirtualSpace.ITEMS].append(self.dock_view_buffer)

                #self.virtual_buffer[]
            def storeIt(self,cd_main):
                self.dock_view_buffer[ObjectsEnums.DockViews.MAIN_SPLITTER_SIZE]=(cd_main.main_splitter.sizes())
                #self.dock_view_buffer[ObjectsEnums.DockViews.DOCK_SPLITTER]=cd_main.Dock.Panel.dock
                #print(cd_main.splitter.sizes())
            def getBuffer(self):return self.dock_view_buffer

        class SubWindow():
            def __init__(self):
                self.subwindow_buffer={}

            def setObjects(self,virtual_buffer:dict,subwindow_index,code_main,subwindow:MDISubWindow,editor:Custom.TextEditor,path_h:Path_Handler):
                self.virtual_buffer=virtual_buffer
                self.subwindow_index=subwindow_index
                self.code_main=code_main
                self.subwindow=subwindow
                self.editor=editor
                self.path_h=path_h

                self.subwindow_buffer[ObjectsEnums.Widget.TYPE]=ObjectsEnums.Widget.SUBWINDOW
                self.subwindow_buffer[ObjectsEnums.SubWindow.INDEX]=subwindow_index
                self.virtual_buffer[ObjectsEnums.VirtualSpace.ITEMS].append(self.subwindow_buffer)
                
                
            def storeBuf(self):
                #title=None,fpath=None,scroll_pos=None,cursor_pos=None
                
                cur,line,col=self.editor.getCurrentLineOrColumnPos()
                
                self.subwindow_buffer[ObjectsEnums.Widget.TYPE]=ObjectsEnums.Widget.SUBWINDOW
                self.subwindow_buffer[ObjectsEnums.SubWindow.INDEX]=self.subwindow_index
                self.subwindow_buffer[ObjectsEnums.SubWindow.TITLE]=self.subwindow.windowTitle()
                self.subwindow_buffer[ObjectsEnums.SubWindow.GEOMETRY]=(self.subwindow.width(),self.subwindow.x(),self.subwindow.height(),self.subwindow.y())
                self.subwindow_buffer[ObjectsEnums.SubWindow.D_PATH]=self.code_main.dummy_codefile_path
                self.subwindow_buffer[ObjectsEnums.SubWindow.O_PATH]=self.code_main.codefile_path
                self.subwindow_buffer[ObjectsEnums.SubWindow.SCROLL_POS]=self.editor.verticalScrollBar().value()
                self.subwindow_buffer[ObjectsEnums.SubWindow.CURSOR_POS]=(line,col)
                print(self.subwindow.windowTitle(),"saved .........")

            def removeBuf(self):
                pass

            def getBuffer(self):
                return self.subwindow_buffer
            
    class ReStore:

        class ReStoreWorkSpace:
            
            def loadAll(cd_main):
                with open(cd_main.Path_h.CodeDock.WORKSPACE,"r")as file:
                    text_data=file.read()
                    file.close()
                workspace_buffer=eval(text_data.splitlines()[0])
                print(workspace_buffer)
                for virtual_s_buffer in workspace_buffer:
                    
                        if virtual_s_buffer[ObjectsEnums.Widget.TYPE]==ObjectsEnums.Widget.VIRTUAL_SPACE:
                            cd_main.virtual_CD.tab_add_btn.click()
                            WorkSpace_Handler.ReStore.virtualSpace(virtual_s_buffer,cd_main)



                        #virtual_space_buffer=virtual_space_buffer[ObjectsEnums.VIRTUAL_SPACE]
                        #if virtual_space_buffer[ObjectsEnums.SUBWINDOW]==ObjectsEnums.SUBWINDOW:
                        #WorkSpace_Handler.ReStore.SubWindow(,cd_main)

        def virtualSpace(virtual_buffer,cd_main):
            
            for v_buff in virtual_buffer[ObjectsEnums.VirtualSpace.ITEMS]:

                if v_buff[ObjectsEnums.Widget.TYPE]==ObjectsEnums.Widget.SUBWINDOW:
                    WorkSpace_Handler.ReStore.SubWindow(v_buff,cd_main)
                
                elif v_buff[ObjectsEnums.Widget.TYPE]==ObjectsEnums.Widget.DOCK_VIEW:
                    WorkSpace_Handler.ReStore.dockView(v_buff,cd_main)
                    


        def dockView(d_buff,cd_main):
            ####
            #cd_main.splitter.setSizes(d_buff[ObjectsEnums.DockViews.MAIN_SPLITTER_SIZE])
            cd_main.main_splitter.setSizes([100,900])

        def SubWindow(swin_buffer,cd_main):

            
            geo=swin_buffer[ObjectsEnums.SubWindow.GEOMETRY]

            cd_main.Code.openUrlSubwindow(swin_buffer[ObjectsEnums.SubWindow.O_PATH])
    
            cd_main.Code.running_subwindow.setGeometry(geo[1],geo[3],geo[0],geo[2])

            cd_main.Code.running_textedit_editor.verticalScrollBar().setValue(swin_buffer[ObjectsEnums.SubWindow.SCROLL_POS])

            cd_main.Code.running_textedit_editor.set_cursor_position(*swin_buffer[ObjectsEnums.SubWindow.CURSOR_POS])

                


            
