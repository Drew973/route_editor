# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 07:49:00 2022

@author: Drew.Bennett
"""

from PyQt5.QtCore import QAbstractTableModel ,QModelIndex,Qt


class layerModel(QAbstractTableModel):
    
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setLayer(None)
        
    
    def setLayer(self,layer):
        self._layer = layer
    
    
    def layer(self):
        return self._layer
    
    
    
    #col 0 is feature id.
    #feature ids are 1 indexed
    def data(self,index,role=Qt.EditRole):
        layer = self.layer()
        if layer is not None:
            return layer.getFeature(index.row()+1)[index.column()] #feature ids are 1 indexed.
    
    
    
    def fid(self,index):
        return index.row()
    
    
    
    def fieldIndex(self,name):
        layer = self.layer()
        if layer:
            return layer.fields().indexOf(name)
        
    
    def rowCount(self,parent = QModelIndex()):
        layer = self.layer()
        if layer is None:
            return 0
        else:
            return layer.featureCount()
    
    
    def columnCount(self,parent = QModelIndex()):
        layer = self.layer()
        if layer is None:
            return 0
        else:
            return len(layer.fields())
        
    
    def selectOnLayer(self,indexes):
        if self.layer() is not None:
            self.layer().selectByIds([self.fid(i) for i in indexes])
    
   # bool QAbstractItemModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)
   
   
   # def flags(self,index):
    #   pass
   