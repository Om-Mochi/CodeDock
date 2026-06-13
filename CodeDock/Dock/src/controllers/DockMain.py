from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.Dock.src.controllers.DockSettings import Dock_Settings

class Dock_Main(Dock_Settings):
    def __init__(self):
        super().__init__()
        
        #self.Panel.Fpaths=self.Path_h
        self.layout_main_tree.addWidget(self.Panel)
        self.layout_main_tree.setContentsMargins(0,0,0,0)
        self.components_parent=[0,None]
        self.components_child=[0,None]

        self.Panel.map_tree.clicked.connect(self.onMapItemsClicked)
        self.connect_map_items=lambda x:...
    def removeComponents(self):
        layout=self.layout_code_components_map
        for i in reversed(range(layout.count())):
            widget=layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
            else:...

        self.tool_container_frame

    def resetComponents(self,scode):
        pass
        """if isCodeComponents(scode[1]):
            self.setComponents(scode)"""


    def onMapItemsClicked(self,index):
        items_lineno=self.Panel.map_model.itemFromIndex(index)
        #self.jumpComponentsInEditor(int(components.toolTip()))
        self.connect_map_items(items_lineno.toolTip().split('-'))


    def setCodeTagsOnModel(self,code_tags):
        #code_components : [lineno,type,t_tab,name,pattern,member]
        
        block_buffer=[]
        s_item_buffer=[]
        for index,code_tag in enumerate(code_tags,0):
            block_i=code_tag[1]
    
            if block_i==0:
                parent=QtGui.QStandardItem()
                parent.setText(code_tag[4])
                parent.setEditable(False)
                parent.setToolTip(f"{code_tag[0]}-{code_tag[3]}")
                self.Panel.map_model.appendRow(parent)
                
                block_buffer.clear()
                s_item_buffer.clear()
                block_buffer.append(block_i)
                s_item_buffer.append(parent)
            
            else:
                child=QtGui.QStandardItem()
                child.setText(code_tag[4])
                child.setEditable(False)
                child.setToolTip(f"{code_tag[0]}-{code_tag[3]}")

                if block_i in block_buffer:
                    block_buffer.pop(block_i)
                    s_item_buffer.pop(block_i)
                block_buffer.insert(block_i,block_i)

                s_item_buffer.insert(block_i,child)
                s_item_buffer[block_i-1].appendRow(child)
        self.Panel.map_tree.expandAll()
