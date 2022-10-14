# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:41:08 2022

@author: Drew.Bennett
"""

from PyQt5.QtSql import QSqlDatabase
from route_editor.models import network_model,routes_model
import os
from route_editor import test
from qgis.utils import iface
import unittest




def fields():
    f = os.path.join(test.layersFolder,'readings.gpkg')
    readingsLayer = iface.addVectorLayer('{f}|layername=readings'.format(f=f), '', 'ogr')
    f = os.path.join(test.layersFolder,'network.gpkg')
    networkLayer = iface.addVectorLayer('{f}|layername=network'.format(f=f), '', 'ogr')
    return {'network':networkLayer,'label':'sec','length':None,'readings':readingsLayer,'startRunCh':'start_run_ch','endRunCh':'end_run_ch','runField':None}
   


def getDb():
    details = {'host':'localhost','database':'A69_hsrr_2022','user':'postgres','password':'pts21'}
    db = QSqlDatabase.addDatabase('QPSQL','routes')
    db.setHostName(details['host'])
    db.setDatabaseName(details['database'])
    db.setUserName(details['user'])
    db.setPassword(details['password'])
    if not db.open():
        raise ValueError('could not open database')
    return db

class testRoutesModel(unittest.TestCase):

    def setUp(self):
        db = getDb()
        m = routes_model.routesModel(db)
        m.setFields(fields())
        m.setTable('hsrr.cateye_routes')
        m.select()
        m.setRun('A69 DBFO EB CL1_slips')
        print(m.rowCount())
        self.model = m
        
    
    def testReadings(self):
        ch = 0
        ind = self.model.index(ch,self.model.fieldIndex('start_run_ch'))
        pt,crs = self.model.floatToPoint(value=0,index=ind)
        ch2 = self.model.pointToFloat(pt=pt,crs=crs,index=ind)
        self.assertTrue(abs(ch2-ch)<0.00001)#some floating point error expected
        
    
    def testFloatToPointNetwork(self):
        self.model.floatToPoint(0,self.model.index(0,self.model.fieldIndex('start_sec_ch')))
    
    
if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testRoutesModel)
    unittest.TextTestRunner().run(suite)
   