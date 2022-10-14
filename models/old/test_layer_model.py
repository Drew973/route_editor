from route_editor.models import layer_model
import os
from route_editor import test



def testInit():
    m = layer_model.layerModel()
    
    f = os.path.join(test.layersFolder,'network.gpkg')
    layer = iface.addVectorLayer('{f}|layername=network'.format(f=f), '', 'ogr')
    m.setLayer(layer)
    
    print(m.rowCount())
    print(m.columnCount())

    print(m.index(0,0).data())
   # print(layer.getFeature(1)[0])
    
if __name__=='__console__':
    testInit()