from route_editor.models import network_model
import os
from route_editor import test



def testInit():
    f = os.path.join(test.layersFolder,'network.gpkg')
    layer = iface.addVectorLayer('{f}|layername=network'.format(f=f), '', 'ogr')
    fields = {'networkLayer':layer,'labelField':'sec','lengthField':''}
   # crs = QgsCoordinateReferenceSystem("EPSG:27700")
    m = network_model.networkModel(fields)
    p = m.point('0900A69/193',51)
    print(m.chainage('0900A69/193',p,m.crs()))
    

    
if __name__=='__console__':
    testInit()