from PyQt5.QtWidgets import QStyledItemDelegate
from qgis.gui import QgsFeaturePickerWidget
from PyQt5.QtCore import Qt



class featurePickerDelegate(QStyledItemDelegate):
    
    
    def __init__(self,parent=None,displayExpression='',allowNull=True,layer=None):
        super().__init__(parent)
        self.displayExpression = displayExpression
        self.allowNull = allowNull
        self.setLayer(None)
        
        if not isinstance(displayExpression,str):
            raise TypeError('featurePickerDelegate({},{},{},{})'.format(parent,displayExpression,allowNull,layer))
        
        
    def setLayer(self,layer):
        self._layer = layer

    
    def getLayer(self):
        return self._layer



    def createEditor(self,parent=None,option=None,index=None):
        
        w = QgsFeaturePickerWidget(parent)
        
        #if not index is None:
            #w.setLayer(index.model().getNetworkLayer())
          
            
        w.setLayer(self.getLayer())
        
        
        w.setDisplayExpression(self.displayExpression)
        w.setAllowNull(self.allowNull)
        return w
    
    
    
    def setEditorData(self,editor,index):
        f = index.model().data(index,role=Qt.EditRole)
        if f.isValid():
            editor.setFeature(f.id())
        #QgsFeaturePickerWidget.setFeature takes feature id rather than QgsFeature.


    
    def setModelData(self,editor,model,index):
        model.setData(index,editor.feature())
    