# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 09:50:55 2022

@author: Drew.Bennett



section,start_sec_ch,end_sec_ch,start_run_ch,end_run_ch
"""

from PyQt5.QtWidgets import QUndoStack



class routeModel:
    
    
    def __init__(self,parent):
        super().__init__(parent)
        self.setUndoStack(QUndoStack())
        
        
        
    def setUndoStack(self,undoStack):
        self._undostack = undoStack
    
    
    
    def undoStack(self):
        return self._undostack
    
    
    
    def autofit(self):
        pass
    
    
    
    def saveAsSec(self,path):
        pass
    
    
    
    def saveAsRte(self,path,fields):
        pass
    
    
    
    def saveAsCsv(self,path):
        pass
    
    
    
    #load .sec. clear if row is None.
    def loadSec(self,path,row=None):
        pass
    
    
    
    #load .rte clear if row is None.
    def loadRte(self,path,row=None):
        pass
    
    
    #load .rte clear if row is None.
    def loadCsv(self,path,row=None):
        pass
    
    
    def networkFeature(self,row):
        pass
    
    
    
    def readingsFeatures(self,row):
        pass
    
    
    
    # for points want readings with s_ch<=field<=e_ch
    #all features of readings with range(s_ch-e_ch) overlaps range(s_ch-e_ch)
    
    #interpolate section changes.
    #get part of geometry within chainage range
    def makeFitted(self,featureSink):
        pass
    