# -*- coding: utf-8 -*-
"""
Created on Thu May  5 07:49:13 2022

@author: Drew.Bennett
"""

from PyQt5.QtWidgets import QTableView

from route_editor import feature_picker_delegate



class routeView(QTableView):
    
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setNetworkLayer(None)
        self.setLabelField(None)
        self.setReadingsLayer(None)

        
        
    def setNetworkLayer(self,layer):
        self._networkLayer = layer
        self.updateSecDelegate()
        
        
        
    def getNetworkLayer(self):
        return self._networkLayer
    
    
    
    def updateSecDelegate(self):
        f = self.getLabelField()
        if f is None:
            f = ''
        
        d = feature_picker_delegate.featurePickerDelegate(parent=self,displayExpression=f,layer=self.getNetworkLayer())
        self.setItemDelegateForColumn(0,d)



    def setReadingsLayer(self,layer):
        self._readingsLayer = layer
        self.updateSecDelegate()
    

    
    def getReadingsLayer(self):
        return self._readings_layer
    
    
    
    def setLabelField(self,field):
        if not self.model() is None:
            self.model().setLabelField(field)
            self.updateSecDelegate()
    
    
    
    def getLabelField(self):
        if not self.model() is None:
            return self.model().getLabelField()
       
    
    
    def setStartChainageField(self,field):
        self._startChainageField = field
        
        
        
    def getStartChainageField(self):
        return self._startChainageField
        
    
    
    def setEndChainageField(self,field):
        self._endChainageField = field
        
        
        
    def getEndChainageField(self):
        return self._endChainageField
    