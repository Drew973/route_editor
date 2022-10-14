# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:03:32 2022

@author: Drew.Bennett
"""

from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QUndoStack

from . import undoable_sql_table_commands


class undoableSqlTableModel(QSqlTableModel):
    
    
    def __init__(self,db,parent=None):
        super().__init__(db,parent)        
        self.setUndoStack(QUndoStack())
        
    

    def findRow(self,primaryValues):
        for r in range(self.rowcount()):
            if self.primaryValues(r) == primaryValues:
                return r
        return -1



    def setUndoStack(self,undoStack):
        self._undoStack = undoStack



    def undoStack(self):
        return self._undoStack
    
    

    def dropRow(self,row):
        pass
    
    
    
    def rowToDict(self,row):
        rec = self.record(row)
        return {rec.fieldName(i):rec.value(i) for i in range(rec.count())}
       
    
    
    def setData(self, index, value, role=Qt.EditRole,parent=None,description='set data'):
        pass
    
    
    
    def _setData(self,index, value):
        super().setData(index,value)
    
        


    def insertRecord(self,row,record):
        self.undoStack().push(undoable_sql_table_commands.insertRecordCommand(model=self,row=row,record=record))



    def _insertRecord(self,row,record):
        return super().insertRecord(row,record)


    #row int, 
    #data:keyword arguments like columnName=Value. extras ignored
    def _insertRow(self,row=None,**data):
        if row==None:
            row = self.rowCount()
                        
       # self.database().transaction()
        
        rec = self.record()
        
        #remove every field that shouldn't be set by model.
        for i in reversed(range(rec.count())):#count down because removing field will change following indexes.
            fieldName = rec.fieldName(i)
            print(fieldName)
            
            if fieldName in data:
                rec.setValue(i,data[fieldName])
            else:
                rec.remove(i)

       
        if not self.insertRecord(row,rec):
            raise ValueError('could not insert record {}'.format(data))
        
        return self.primaryValues(row)