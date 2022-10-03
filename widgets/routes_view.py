# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:32:15 2022

@author: Drew.Bennett
model may have run or not. makes no difference to view.




"""

from PyQt5.QtWidgets import QTableView,QMenu,QAbstractItemView

from PyQt5.QtCore import Qt
# PyQt5.QtGui import QKeySequence


from . import chainage_delegate
from qgis.core import QgsCoordinateReferenceSystem


class routesView(QTableView):
    
    def __init__(self,parent=None,undoStack=None):
        super().__init__(parent)
        self.undoStack = undoStack
        
        self.rowsMenu = QMenu(self)
        self.rowsMenu.setToolTipsVisible(True)

        self.setNetworkModel(None)
        self.setReadingsModel(None)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pt:self.rowsMenu.exec_(self.mapToGlobal(pt)))         

        self.selectOnLayersAct = self.rowsMenu.addAction('select on layers')
        self.selectOnLayersAct.setToolTip('select these rows on network and readings layers.')
        self.selectOnLayersAct.triggered.connect(self.selectOnLayers)

        #selectFromLayersAct = self.rows_menu.addAction('select from layers')
        #selectFromLayersAct.setToolTip('set selected rows from selected features of readings layer.')
  #      self.select_from_layers_act.triggered.connect(self.select_from_layers)

        self.deleteRowsAct = self.rowsMenu.addAction('delete selected rows')
        self.deleteRowsAct.triggered.connect(self.dropSelectedRows)
        
        #create delegates
   #     self.secDelegate = sec_delegate.secDelegate(self)
        self.chainageDelegate = chainage_delegate.chainageDelegate(parent=self,crs = QgsCoordinateReferenceSystem(27700))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)



    def setModel(self,model):
        super().setModel(model)
        self.resizeColumnsToContents()

        self.hideColumn(model.fieldIndex('pk'))
        self.hideColumn(model.fieldIndex('run'))

        if True:
        #    logger.debug('setModel special')
        #    print(model.fieldIndex('pk'))
        #    self.hideColumn(model.fieldIndex('pk'))
        #    self.setItemDelegateForColumn(model.fieldIndex('sec'),self.secDelegate)
            self.setItemDelegateForColumn(model.fieldIndex('start_run_ch'),self.chainageDelegate)    
            self.setItemDelegateForColumn(model.fieldIndex('end_run_ch'),self.chainageDelegate)
            self.setItemDelegateForColumn(model.fieldIndex('start_sec_ch'),self.chainageDelegate)
            self.setItemDelegateForColumn(model.fieldIndex('end_sec_ch'),self.chainageDelegate)    



    def setNetworkModel(self,model):
        self._networkModel = model



    def networkModel(self):
        return self._networkModel



    def readingsModel(self):
        return self._readingsModel

    
    def setReadingsModel(self,model):
        self._readingsModel = model


    #list of row indexes
    def selectedRows(self):
        return [i.row() for i in self.selectionModel().selectedRows()]
    


    def selectedSections(self):
        if self.model() is not None:
            col = self.model().fieldIndex('sec')
            return [i.data() for i in self.selectionModel().selectedRows(col)]
        return []


    def dropSelectedRows(self):
        for r in self.selectedRows():
            self.model().removeRow(r)
        
        
    def selectOnLayers(self):
        self.selectedRows()
        if self.networkModel() is not None:
            self.networkModel().selectOnLayer(self.selectedSections())
        
        
        
        