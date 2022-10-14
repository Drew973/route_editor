# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 07:54:57 2022

@author: Drew.Bennett
"""

import unittest

from route_editor.models import get_db,database_functions

from route_editor import test
from qgis.utils import iface
import os



def fields():
    f = os.path.join(test.layersFolder,'readings.gpkg')
    readingsLayer = iface.addVectorLayer('{f}|layername=readings'.format(f=f), '', 'ogr')
    f = os.path.join(test.layersFolder,'network.gpkg')
    networkLayer = iface.addVectorLayer('{f}|layername=network'.format(f=f), '', 'ogr')
    return {'network':networkLayer,'label':'sec','length':None,'readings':readingsLayer,'startRunCh':'start_run_ch','endRunCh':'end_run_ch','run':'run'}
     
    
    #setUp called before every test method
    
class testFunctions(unittest.TestCase):

  #  def setUp(self):
    #    print('setup')
    #    self.db = get_db.getDb()
    #    database_functions.createReadingsTable(self.db)
    #    database_functions.createRoutesTable(self.db)
    #    self.fields = fields()
        
        
    @classmethod
    def setUpClass(cls):
        cls.db = get_db.getDb()
        database_functions.createReadingsTable(cls.db)
        database_functions.createRoutesTable(cls.db)
        cls.fields = fields()
        
    def testLoadLayer(self):
        f = self.fields
        database_functions.loadReadings(db=self.db,layer=f['readings'],run=f['run'],startRunCh=f['startRunCh'],endRunCh=f['endRunCh'])
        
        
    def testRefit(self):
        f = self.fields
        database_functions.refit(db=self.db,readings=f['readings'],run=f['run'],startRunCh=f['startRunCh'],endRunCh=f['endRunCh'])
        
    
    def test3(self):
        pass
    
    
if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testFunctions)
    unittest.TextTestRunner().run(suite)
   
 
