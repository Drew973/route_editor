# -*- coding: utf-8 -*-
"""
Created on Fri May  6 08:25:54 2022

@author: Drew.Bennett
"""

from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox

from qgis.gui import QgsMapLayerComboBox,QgsFieldComboBox 
from qgis.core import QgsMapLayerProxyModel



class layersDialog(QDialog):
    
    
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.setLayout(QFormLayout())
        
        #network
        self.networkBox = QgsMapLayerComboBox(self)
        self.networkBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        
        self.layout().addRow('Layer with network',self.networkBox)
        
        #label field
        self.labelBox = QgsFieldComboBox(self)
        self.labelBox.setAllowEmptyFieldName(True)
        self.addFieldWidget(self.labelBox,self.networkBox,'Field with label')

        #readings
        self.readingsBox = QgsMapLayerComboBox(self)
        self.readingsBox.setAllowEmptyLayer(True)
        self.layout().addRow('Layer with readings.',self.readingsBox)

        #start chainage field
        self.startChainageBox = QgsFieldComboBox(self)
        #self.startChainageBox.setAllowEmptyFieldName(True)
        self.addFieldWidget(self.startChainageBox,self.readingsBox,'Field with start run chainage')

        #end chainage field
        self.endChainageBox = QgsFieldComboBox(self)
        self.endChainageBox.setAllowEmptyFieldName(True)
        self.addFieldWidget(self.endChainageBox,self.readingsBox,'Field with end run chainage')
        
        self.box = QDialogButtonBox(QDialogButtonBox.Close,parent=self)
        self.box.accepted.connect(self.accept)
        self.box.rejected.connect(self.reject)
        
        self.layout().addWidget(self.box)
        
        
        
    #connect layerChanged signal of parent QGSMapLayerComboBox 
    #then adds to layout.
    def addFieldWidget(self,fieldBox,parent,label=''):
        parent.layerChanged.connect(fieldBox.setLayer)
        fieldBox.setLayer(parent.currentLayer())
        self.layout().addRow(label,fieldBox)





if __name__=='__main__' or __name__=='__console__':
    d = layersDialog()
    d.show()