# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:53:41 2022

@author: Drew.Bennett

delegate with chainageWidget.


widgets seem to last until all connected slots do their thing.
setModel data seems to happen before focusLost event and before things connected to valueChanged signal

"""

from . import chainage_widget
from PyQt5.QtWidgets import QStyledItemDelegate

from qgis.core import QgsCoordinateReferenceSystem



class chainageDelegate(QStyledItemDelegate):
    
    
    def __init__(self,parent=None,crs=QgsCoordinateReferenceSystem()):
        super().__init__(parent)
        self.crs = crs
        
    
    def createEditor(self,parent,option,index):
        w = chainage_widget.chainageWidget(parent=parent)
        w.setCrs(self.crs)
        w.setIndex(index)
        
        if isinstance(index.data(),float) or isinstance(index.data(),int):
            w.setValue(index.data())
        
        w.valueChanged.connect(lambda value:setData(index,value))
        return w
    
  
    
def setData(index,value):
    index.model().setData(index,value)
    
    
    
    