# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 07:56:11 2022

@author: Drew.Bennett
"""

from PyQt5.QtSql import QSqlTableModel,QSqlDatabase,QSqlQuery


class queryError(Exception):
    def __init__(self,q):
        message = 'query "%s" failed with "%s"'%(q.lastQuery(),q.lastError().databaseText())
        super().__init__(message)
    



class routesModel(QSqlTableModel):
    
    def __init__(self,db=QSqlDatabase(),parent=None):       
        super().__init__(parent=parent,db=db)
        
        
    def setRun(self,run):
        self._run = run
        self.setFilter("run = '{run}' order by start_run_ch".format(run=run))
        
    def run(self):
        return self._run
        
    def save(self,file):
        pass
    
    
    def load(self,file):
        pass
    
    
    def layer(self):
        pass
    
    
    
    def runQuery(self,query,args={}):
        q = QSqlQuery(self.database())
       
        if not q.prepare(query):
            raise queryError(q)
        
        for k in args:
            q.bindValue(k,args[k])
        
        if not q.exec():
            raise queryError(q)
        
        return q
        
    
    
    def floatToXY(self,value,index):
        
        if index.column() in [self.fieldIndex('start_run_ch'),self.fieldIndex('end_run_ch')]:
            q = self.runQuery('select st_x(hsrr.cateye_ch_to_pt(:ch,:run)),st_y(hsrr.cateye_ch_to_pt(:ch,:run))',
                              {':ch':value,':run':self.run()})
            while q.next():
                return (q.value(0),q.value(1))
                
            
        if index.column() in [self.fieldIndex('start_sec_ch'),self.fieldIndex('end_sec_ch')]:
            sec = self.index(index.row(),self.fieldIndex('sec')).data()
            if sec=='D':
                return(0,0)
            q = self.runQuery('select st_x(hsrr.sec_ch_to_point(:ch,:sec)),st_y(hsrr.sec_ch_to_point(:ch,:sec))',
                              {':ch':value,':sec':sec})
            while q.next():
                return (q.value(0),q.value(1))
        return (0,0)
            
    
    
    def XYToFloat(self,x,y,index):
        
        if index.column() in [self.fieldIndex('start_run_ch'),self.fieldIndex('end_run_ch')]:       
            q = self.runQuery("select hsrr.cateye_ch(:run,:x,:y)",
                              {':x':x,':y':y,':run':self.run()})
            while q.next():
                return (q.value(0))
        
        if index.column() in [self.fieldIndex('start_sec_ch'),self.fieldIndex('end_sec_ch')]:
            
            sec = self.index(index.row(),self.fieldIndex('sec')).data()
            q = self.runQuery("select hsrr.point_to_sec_ch(:x,:y,:sec)",
                              {':x':x,':y':y,':sec':sec})
            while q.next():
                return (q.value(0))        
        
        return 0
    
    
    def minValue(self,index):
        return 0.0
    
    
    def maxValue(self,index):
        return 100.0
    #removeRows(int row, int count, const QModelIndex &parent = QModelIndex())
    
    