# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 10:05:27 2022

@author: Drew.Bennett



"""

from PyQt5.QtWidgets import QDialog,QFormLayout
from qgis.core import QgsMapLayerProxyModel,QgsFieldProxyModel
from qgis.gui import QgsMapLayerComboBox,QgsFieldComboBox

from route_editor.widgets.field_box import fieldBox
from PyQt5.QtCore import QStringListModel

#FIELDS = ['readingsLayer','startRunCh','endRunCh','runField']


class fieldsDialog(QDialog):
        
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setLayout(QFormLayout(self))
        
        self.runsModel = QStringListModel()
        self.items = {}
        
        self.items['network'] = QgsMapLayerComboBox(self)
        self.items['network'].setFilters(QgsMapLayerProxyModel.LineLayer)
        self.layout().addRow('Layer with network',self.items['network'])
                
        self.items['label'] = fieldBox(parent = self.items['network'],default = 'sec')
        self.items['label'].setFilters(QgsFieldProxyModel.String)
        self.layout().addRow('Field with section label',self.items['label'])
    
        self.items['length'] = fieldBox(parent = self.items['network'],default = 'measLen')
        self.items['length'].setFilters(QgsFieldProxyModel.Numeric)
        self.layout().addRow('Field with section length',self.items['length']) 
  
        self.items['readings'] = QgsMapLayerComboBox(self)
        self.items['readings'].setFilters(QgsMapLayerProxyModel.LineLayer)
        self.layout().addRow('Layer with readings',self.items['readings'])     
      
        self.items['runField'] = fieldBox(parent = self.items['readings'],default = 'run')
        self.items['runField'].setFilters(QgsFieldProxyModel.String)
        self.layout().addRow('Field with run',self.items['runField'])
        self.items['runField'].fieldChanged.connect(self.refreshRuns)
        
        self.items['startRunCh'] = fieldBox(parent = self.items['readings'],default = 's_ch')
        self.items['startRunCh'].setFilters(QgsFieldProxyModel.Numeric)
        self.layout().addRow('Field with start run chainage',self.items['startRunCh'])
        
        self.items['endRunCh'] = fieldBox(parent = self.items['readings'],default = 'e_ch')
        self.items['endRunCh'].setFilters(QgsFieldProxyModel.Numeric)
        self.layout().addRow('Field with end run chainage',self.items['endRunCh'])
        
        self.refreshRuns()
        
        
    
    def refreshRuns(self):
        layer = self.items['runField'].layer()
        field = self.items['runField'].currentField()
        if field and layer is not None:
            oldFilter = layer.subsetString()
            layer.setSubsetString('')
            vals = ['']
            vals += [v for v in layer.uniqueValues(layer.fields().indexFromName(field))]
            self.runsModel.setStringList(sorted(vals))
            layer.setSubsetString(oldFilter)
        else:
            self.runsModel.setStringList([''])
        
        
    #dict like.
    def __getitem__ (self,key):
        w = self.items[key]
        
        if isinstance(w,QgsMapLayerComboBox):
            return w.currentLayer()
        
        if isinstance(w,QgsFieldComboBox):
            return w.currentField()
    
        
        
    def keys(self):
        return self.items.keys()
        
    
    
def test():
    d = fieldsDialog()
    d.show()
    return d
    

    
if __name__=='__console__':
    d = test()