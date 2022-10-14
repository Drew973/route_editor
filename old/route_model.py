# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:35:35 2022

@author: Drew.Bennett
"""

from PyQt5.QtCore import QAbstractTableModel,QModelIndex
from PyQt5.QtCore import Qt

from route_editor import route_item
from qgis.core import QgsFeature



class routeModel(QAbstractTableModel):
    
    
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.items = []
        self.columns = ['section','start_section_chainage','end_section_chainage','start_run_chainage','end_run_chainage']        
        self.setLabelField(None)
        
        
        
    def setLabelField(self,field):
        self._labelField = field
        self.dataChanged.emit(self.index(0,0),self.index(self.rowCount(),self.columnCount()))
        
        
        
    def getLabelField(self):
        return self._labelField
        
        
    
    def flags(self,index):
        return Qt.ItemIsEditable|Qt.ItemIsEnabled


        
    def data(self,index,role=Qt.DisplayRole):
        
        i = self.items[index.row()]
        col = index.column()
        
        
        if not i is None:
            
            
            if col == 0:
                f = i.getNetworkFeature()
                
                
                if role == Qt.EditRole:
                    return f

                
                if role==Qt.DisplayRole:
                    if f.isValid():
                        field = self.getLabelField()
                        if field:
                            return f[field]
                        else:
                            return f.id()
                    else:
                        return ''
                
               
            if role==Qt.DisplayRole:
                return i[col]
        
        
        
    def setData(self,index,value, role = Qt.EditRole):
        
        if role == Qt.EditRole:
        
            
            col = index.column()
        
            i = self.items[index.row()]
        
        
            print(index.row(),col,value)
            
            if col==0:
                i.setNetworkFeature(value)
            else:            
                i[col] = value
                
            return True
        
        
        
    def rowCount(self,parent=None):
        return len(self.items)
        
    
    
    def columnCount(self,parent=None):
        return 5
    
    
    
    #int section, Qt::Orientation orientation, int role = Qt::DisplayRole
    def headerData(self,section,orientation,role = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]

    

    def insert(self,row=0,sectionStartChainage=0,sectionEndChainage=None,networkFeature=QgsFeature(),runStartChainage=None,runEndChainage=None):
        item = route_item.routeItem(sectionStartChainage,sectionEndChainage,networkFeature,runStartChainage,runEndChainage)
        self.beginInsertRows(QModelIndex(),row,row)
        self.items.insert(row,item)
        self.endInsertRows()
        
        
    def insertDummy(self,row,runStartChainage=None,runEndChainage=None):
        self.insert(row=row,runStartChainage=runStartChainage,runEndChainage=runEndChainage)
        
  #  def insert(self,item,i=-1):
     #   self.beginInsertRows(QModelIndex(),i,i)
    #    self.items.insert(i,item)
    #    self.endInsertRows()
        
        
        
    property(getLabelField,setLabelField)