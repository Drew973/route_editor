# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 09:21:26 2022

@author: Drew.Bennett


model to handle everything view needs.
network model and readings model only to be used by routesModel


actions:
    
    insert selected feature:
        insert selected section at selected row. If readings selected set start and end runChainage.
        order by hidden row(int) column.
        
    
    insert dummy
    
    
    open: rte,sec,csv
    
    insert file
    
    save

    

methods:
    
    floatToXY :required by chainageDelegate
    XYToFloat :required by chainageDelegate
    selectOnLayers(rows): required by view.
    selectedRows(): required by view.

"""
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
from PyQt5.QtCore import Qt
from qgis.core import QgsPointXY,QgsCoordinateReferenceSystem,QgsUnitTypes

from route_editor.models.network import network_model
from route_editor.models.readings import readings_model

#from route_editor.models.routes import functions
#from .. import database_functions
from route_editor.models import database_functions


class routesModel(QSqlTableModel):

    def __init__(self,db=QSqlDatabase(),parent=None):
        database_functions.createRoutesTable(db)
        
        super().__init__(parent=parent,db=db)      
        self.setFields()
        
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
       # self.setSort(self.fieldIndex('sort_col'),Qt.AscendingOrder)
        self.setTable('routes')
        self.setRun('')
    
        
    def setRun(self,run):
        self._run = run
        if run:
            self.setFilter("run = '{run}'".format(run=run))
        else:
            self.setFilter('')
        self.setSort(self.fieldIndex('start_run_ch'),Qt.AscendingOrder)
        self.select()
        
        
    #set layers and fields. Using dialog with QgsMapLayerComboBox,QgsFieldCombobox and __getitem__ method avoids
    #'wrapped c++ object has been deleted...' error when something deletes layer.
    def setFields(self,fields = {}):
        self.networkModel = network_model.networkModel(fields)
        self.readingsModel = readings_model.readingsModel(fields)
        self.fields = fields
        
        
        
    def autofit(self):
        self.networkModel.loadNetwork()
        
        
        
        
    def refit(self):
        readings = self.readingsModel.fields['readings']
        if readings is not None:
            self.readingsModel.loadReadings()
            database_functions.refit(db=self.database(),readings=readings)
        #readings,startRunCh,endRunCh,run=''
    
    
    #unit used for chainage columns.
    def unit(self):
        return QgsUnitTypes.DistanceKilometers
        
    
    def filterLayer(self):
        self.readingsModel.filterLayer(self.run())
    
    
    def run(self):
        return self._run
    
    
    def openFile(self,file):
        pass
    
    
    def insertFile(self,file):
        pass
    
    
    def sec(self,row):
        return self.index(row,self.fieldIndex('sec')).data()
    
    
    
   # def units(self,index)
    
    
    #return (QgsPointXY,crs)
    def floatToPoint(self,value,index):
        if index.column() in [self.fieldIndex('start_sec_ch'),self.fieldIndex('end_sec_ch')]:
            return (self.networkModel.point(sec=self.sec(index.row()),ch=value),self.networkModel.crs())

        if index.column() in [self.fieldIndex('start_run_ch'),self.fieldIndex('end_run_ch')]:
            return (self.readingsModel.point(ch=value,run=self.run()),self.readingsModel.crs())

        return (QgsPointXY(0,0),QgsCoordinateReferenceSystem())
    
    
    #QgsPointXY,QgsCoordinateReferenceSystem,QModelIndex
    
    # for readings ch in same units as start_run_ch and end_run_ch  
    #for network sec_ch in units of meas_len where specified or in map units.
    
    def pointToFloat(self,pt,crs,index):
        if index.column() in [self.fieldIndex('start_sec_ch'),self.fieldIndex('end_sec_ch')]:
            return self.networkModel.chainage(sec=self.sec(index.row()),point=pt,crs=crs)

        if index.column() in [self.fieldIndex('start_run_ch'),self.fieldIndex('end_run_ch')]:
            return self.readingsModel.chainage(run=self.run(),point=pt,crs=crs)
            
        return 0.0


    def minValue(self,index):
        return 0.0
    
    
    def maxValue(self,index):
        return 100.0
    
    
    #rows selected on layers
    def selectedRows(self):
        pass


    def selectOnLayers(self,rows):
        self.networkModel.selectOnLayer([self.sec(r) for r in rows])
        zoomToSelectedMultilayer([self.networkModel.fields['network'],self.readingsModel.fields['readings']])
        
        
    #find position to insert new row
    #1 where rowCount=0.    
    def newRowPos(self,startRunCh):
        r = 1
        col = self.fieldIndex('start_run_ch')
        for r in range(self.rowCount()+1):
            v = self.index(r,col).data()
            if isinstance(v,float):
                if v >startRunCh:
                    return r        
        return r
        
    
    
    
    #insert selected section. full section length. 
    #run chainages at min and max selected.   
    def insertSelected(self):
        
        f = self.networkModel.selectedFeature()
        startRunCh,endRunCh = self.readingsModel.selectedCh()       
                
        if f:
            self.insertRow(
                row = self.newRowPos(startRunCh),
                sec = f[self.networkModel.fields['label']],
                start_sec_ch = 0,
                end_sec_ch = f[self.networkModel.fields['length']],
                start_run_ch = startRunCh,
                end_run_ch = endRunCh,
                run = self.run()
                       )
        
        
        
    def insertRow(self,row=None,**data):
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
        
        return row
        
       
        
       
        
from qgis.utils import iface
from qgis.core import QgsRectangle        
#zoom to selected features on multiple layers.
#zooms out slightly (scale)
def zoomToSelectedMultilayer(layers,scale=1.1):
    layers = [layer for layer in layers if hasattr(layer,'boundingBoxOfSelected')]
    
    extent = QgsRectangle()
    
    for layer in layers:
        extent.combineExtentWith(layer.boundingBoxOfSelected())#in layer crs or project crs?
        
    if extent.area()>0:
        extent.scale(scale)
        iface.mapCanvas().setExtent(extent)
        iface.mapCanvas().refresh()        
        