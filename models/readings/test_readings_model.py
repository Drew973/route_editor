# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 15:27:53 2022

@author: Drew.Bennett
"""
from qgis.utils import iface
from route_editor.models import readings_model
from route_editor import test
import os


def testInit():
    f = os.path.join(test.layersFolder,'readings.gpkg')
    layer = iface.addVectorLayer('{f}|layername=readings'.format(f=f), '', 'ogr')
    fields = {'readingsLayer':layer,'runField':'run','startRunCh':'start_run_ch','endRunCh':'end_run_ch'}
   # crs = QgsCoordinateReferenceSystem("EPSG:27700")
    m = readings_model.readingsModel(fields)
    p = m.point(3.0)
    

    
if __name__=='__console__':
    testInit()