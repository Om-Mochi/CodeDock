from PyQt6 import QtWidgets,QtCore,QtGui
from CodeDock.src.controllers.PathHandler import Path_Handler
import typing
import enum

 


class BinarySearch:

    def searchAccurat(lst: typing.List[int,str],target:int) -> int:
        left = 0
        right = len(lst) - 1
        while left <= right:
            mid = (left + right) // 2

            if lst[mid] == target:
                return mid

            if lst[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return
        


    def searchNearestUp(lst: typing.List[int,str],target:int) -> int:...
        

"""

class Position(typing.TypedDict):
    line: int
    character: int


class Range(typing.TypedDict):
    start: Position
    end: Position


class Location(typing.TypedDict):
    range: Range
    uri: str  
"""


class Parent_Dict(typing.TypedDict):
    name:str
    line:int

class Symbol_Dict(typing.TypedDict):

    name: str
    parent:typing.Union[Parent_Dict,None]
    s_line:int
    e_line:int
    s_char:int
    e_char:int
    kind: int
    std_item:QtGui.QStandardItem



class Symbol_Manager:
    from CodeDock.C_Widgets.Custom import Custom

    def __init__(self,editor:Custom.TextEditor,
                 tree_model:Custom.StandardItemModel,
                 path_h:Path_Handler):
        
        self.is_seted=False
        self.editor=editor
        self.tree_model=tree_model
        self.path_h=path_h
        
        self.documet_symbol_list : Symbol_Dict = {}

        self.document_symbols_buffer : Symbol_Dict = {}
        
        self.standard_item_buffer : list[QtGui.QStandardItem] = []
        
        self.symbol_start_lineno_buffer:list[int]=[]
        self.symbol_end_lineno_buffer:list[int]=[] 



    def setSymbols(self,symbol:Symbol_Dict):
        if not self.is_seted:
            self.filterAndSet(symbol)

    def _compare(self,symbols:Symbol_Dict,current_line:int):
        symbols=symbols['result']

        low=0
        high=len(symbols)-1
        last_line=0
        block_symbol_list=[]
        
        while low<=high:
            mid_i=(high+low)//2
            final_lineno=None
            is_end_passed=bool
            final_index=None
            #rev_i=high-low
            
            #ending_line_no=symbols[mid_i]['location']['range']['end']['line']
            
            symbol_line_no:int=symbols[mid_i]['location']['range']['start']['line']
                        
            if current_line==symbol_line_no:                

                final_index=mid_i

                sym_name:str=symbols[mid_i]['name']
                container_name:str=symbols[mid_i]['containerName']
                ending_line_no:int=symbols[mid_i]['location']['range']['end']['line']
                sym_kind:int=symbols[mid_i]['kind']
                
                if container_name!=None:
                    self.document_symbols_buffer
                    self.document_symbols_buffer.insert(mid_i-1,[sym_name,container_name,])

                break
            
            elif current_line > symbol_line_no:
                low=mid_i+1

            elif current_line < symbol_line_no:
                high=mid_i-1
    

    def addSymbolInTreeModel(self,symbol_name:str,symbol_kind:int,item_parent:QtGui.QStandardItem = None) -> QtGui.QStandardItem:
        item=QtGui.QStandardItem()
        item.setIcon(QtGui.QIcon(self.path_h.SYMBOL_KIND_ICONS_LIST[symbol_kind]))
        item.setText(symbol_name)
        item.setEditable(False)


        if item_parent!=None:
            item_parent.appendRow(item)

        else:
            self.tree_model.appendRow(item_parent)

        return item
    
    def filterAndSet(self,symbols:Symbol_Dict):
        
        self.tree_model.clear()

        symbols=symbols['result']
        parent_list=[]
        #parent_list.append([item,name,container_name,line_no,index])
        #print("lenth ",len(symbols))
        #same index(len) every list
        
        parent_item_list:dict[Parent_Dict]={} 



        self.document_symbols_buffer.clear()
        self.symbol_start_lineno_buffer.clear()
        self.symbol_end_lineno_buffer.clear()

        for index,symbol in enumerate(symbols):
            
            sym_name=symbol['name']
            container_name=symbol['containerName']
            s_line=symbol['location']['range']['start']['line']
            e_line=symbol['location']['range']['end']['line']
            s_char=symbol['location']['range']['start']['character']
            e_char=symbol['location']['range']['end']['character']
            
            sym_kind=symbol['kind']

            if sym_kind in self.disable_document_symbol_kind:
                continue
            
            #print(symbol)
            #print(symbol,"\n\n")

            #print(f"{name}-->{container_name} | l:{line_no} k:{kind}","\n\n")

            
            if container_name==None:
                #print(name)

                std_item=self.addSymbolInTreeModel(sym_name,sym_kind,None)

                #parent_list.append([item,name,container_name,line_no,index])
                

                parent_item_list[sym_name]={'name':sym_name,'line':s_line}                

                self.documet_symbol_list={
                    'name':sym_kind,
                    'parent':None,
                    's_line':s_line,
                    'e_line':e_line,
                    's_char':s_char,
                    'e_char':e_char,
                    'std_item':std_item
                    }

                self.document_symbols_buffer[s_line]=self.documet_symbol_list

                #container_name_l.append(container_name)
                continue            
            else:

                item_parent:Parent_Dict=parent_item_list[container_name]

                std_item=self.addSymbolInTreeModel(sym_kind,sym_kind,item_parent['std_item'])                



                parent_item_list[sym_name]={'std_item':std_item,'line':s_line}

                self.documet_symbol_list={
                    'name':sym_kind,
                    'parent':{
                            'name':container_name,
                            'line':item_parent['line'],    
                        },
                    's_line':s_line,
                    'e_line':e_line,
                    's_char':s_char,
                    'e_char':e_char,
                    'std_item':std_item
                    }

                self.document_symbols_buffer[s_line]=self.documet_symbol_list

            
        
    def removeSymbols(self):pass
    def addSymbol(self):pass
    def resetSymbol(self):pass


