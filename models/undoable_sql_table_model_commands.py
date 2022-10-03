# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:38:56 2022

@author: Drew.Bennett
"""


from PyQt5.QtWidgets import QUndoCommand



#incomplete!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class insertRecordCommand(QUndoCommand):

    
    #function is any function or method.
    #args: arguments to call it with
    def __init__(self,model,row,record,description='insert row',parent=None):
        super().__init__(description,parent)
        self.model = model
        self.row = row
        self.record = record
        


    def redo(self):
        self.result = self.model._insertRecord(self.row,self.record)
        self.pk = self.model.primaryValues(self.row)    



    def undo(self):
       # self.args = self.inverseFunction(self.reverseArgs)
        self.model._deleteRow(self.row)
       