# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:40:35 2022

@author: Drew.Bennett



QDoubleSpinBox with:
    option to display marker on map
    set value from map click



needs model to map double to point. with:

    XYToFloat(index,x,y) method
    point is in self.crs
    
    floatToXY(index,value) method. returns (x,y) in model crs
    floatToXY
    
    
    units for chainage.  
    

"""

from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import QModelIndex


from qgis.gui import QgsMapToolEmitPoint,QgsVertexMarker
from qgis.utils import iface
from qgis.core import QgsCoordinateTransform, QgsProject



class chainageWidget(QDoubleSpinBox):
    
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setIndex(QModelIndex())

        self.tool = QgsMapToolEmitPoint(iface.mapCanvas())
       # self.tool = chainageEmitter()
        
        self.marker = QgsVertexMarker(iface.mapCanvas())
        self.marker.setIconSize(20)
        self.marker.setPenWidth(5)
        self.tool.canvasClicked.connect(self.setFromPoint)
    
        self.valueChanged.connect(self.updateMarker)       
        
        self.setSingleStep(0.001)#1m
        self.setDecimals(3)
        self.updateMarker(self.value())



    '''
    set index (QModelIndex).
    index and it's model is used to convert between points and values
    need index in networkModel for section chainage as depends on section.
    any index for run_chainage as only need run and value.
    '''
    
    def setIndex(self,index):
        self._index = index
        
        if index.model() is not None:
            self.setMinimum(index.model().minValue(index))
            self.setMaximum(index.model().maxValue(index))
            self.updateMarker(self.value())

        

    def getIndex(self):
        return self._index
            
    
    #happens after focusOutEvent
    def setFromPoint(self,point):
        index = self.getIndex()
        m = index.model()
        if m is not None:
            v = m.pointToFloat(pt=point,crs=QgsProject.instance().crs(),index=index)
            if isinstance(v,float):
                self.setValue(v)
        

    def updateMarker(self,val):
        i = self.getIndex()
        m = i.model()
        if m is not None:
            pt,crs = m.floatToPoint(val,i)
            transform = QgsCoordinateTransform(crs,QgsProject.instance().crs(),QgsProject.instance())#transform to project crs
            self.marker.setCenter(transform.transform(pt))#needs to be in project crs


    def focusInEvent(self,event):
        iface.mapCanvas().setMapTool(self.tool)
        self.marker.show()
        super().focusInEvent(event)
    

    #happens before setFromPoint and before delegate destroys widget
    def focusOutEvent(self,event):
       # print(type(event))
        
        #iface.mapCanvas().unsetMapTool(self.tool)
#        print('chainage widget.focusOutEvent')
        self.marker.hide()
        super().focusOutEvent(event)
        
        
    def __del__(self):
        iface.mapCanvas().scene().removeItem(self.marker)


    def deleteLater(self):
        iface.mapCanvas().scene().removeItem(self.marker)
        super().deleteLater()
        