from CodeDock.DockingSystem.enums.Sides import Sides
from PyQt6 import QtWidgets,QtCore,QtGui
import dataclasses
import typing

from CodeDock.DockingSystem.widgets.AnimatedSplitter import AnimatedSplitter
if typing.TYPE_CHECKING:
    from CodeDock.DockingSystem.core.DockZone import DockZone 

@dataclasses.dataclass
class DockPlacement:
    side:Sides
    prevSide:Sides
    newSplitter:typing.Union[AnimatedSplitter,None]=None
    splitterIndex:int=None
    splitterOn:typing.Union[AnimatedSplitter,None]=None
    splitterContainer:typing.Union[QtWidgets.QWidget,None]=None
    source:typing.Union[QtCore.QObject,None]=None

@dataclasses.dataclass  
class DockWidgetDC:
    widgetType:typing.Union[object,QtWidgets.QWidget,None]
    dockZone:"DockZone"
    isOwnner:bool
