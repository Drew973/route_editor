# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 13:53:43 2022

@author: Drew.Bennett
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 11:14:49 2022

@author: Drew.Bennett


interface for network layer
only used by routesModel


"""

from qgis.core import QgsPointXY, QgsCoordinateTransform, QgsProject,QgsGeometry,QgsFeatureRequest
from route_editor.models import database_functions


#check performance with large layer. documentation unclear if QgsFeatureRequest uses spatial indexes.
def nearestFeature(layer,geom,maxDist):
    e = "distance($geometry, geom_from_wkt('{wkt}')) <= {md}".format(wkt=geom.asWkt(),md=maxDist)
    r = QgsFeatureRequest().setFilterExpression(e)
    r = QgsFeatureRequest(r)
    r = r.setLimit(1)
    orderExpression = "distance($geometry, geom_from_wkt('{wkt}'))".format(wkt=geom.asWkt())
    r = r.addOrderBy(orderExpression)
    for f in layer.getFeatures(r):
        return f
        

FIELDS = ['readings','startRunCh','endRunCh','runField']

class readingsModel:
    
    def __init__(self,fields={}):
        
        if not fields:
            fields = {f:None for f in FIELDS}
            
        for f in FIELDS:
            if not f in fields.keys():
                raise KeyError('missing field '+f)
        self.fields = fields
        



    def crs(self):
        if self.fields['readings'] is not None:
            return self.fields['readings'].crs()

    
    def unit(self):
        return self.crs().mapUnits()


    def filterLayer(self,run):
        layer = self.fields['readings']
        if layer and self.fields['runField']:
            layer.setSubsetString('"{runField}"=\'{run}\''.format(run=run,runField=self.fields['runField']))


    #whatever loads layer needs to ensure only 1 point per chainage.
    def feature(self,ch,run=None):
        layer = self.fields['readings']
        startField = self.fields['startRunCh']
        endField = self.fields['endRunCh']
        if startField and endField and layer is not None :
            e = ''
            if self.fields['runField'] and run:
                e += '"{field}"=\'{run}\' and '.format(field=self.fields['runField'],run=run)
            e += '"{sf}"<={ch} and {ch}<="{ef}" and $length>0'.format(sf=startField,ef=endField,ch=ch)
            r = QgsFeatureRequest().setFilterExpression(e)
            for f in layer.getFeatures(r):#get 1st feature
                return f
        
        
    #run chainage to QgsPointXY
    #same units as start_run_ch and end_run_ch.
    
    def point(self,ch,run=None):     
        
        f = self.feature(ch,run)
        startField = self.fields['startRunCh']
        endField = self.fields['endRunCh']
        
        if f:
            geomLen = f.geometry().length()
            frac = (ch-f[startField])/(f[endField]-f[startField])
            dist = geomLen*min(frac,1)
            return f.geometry().interpolate(dist).asPoint()
        
        return QgsPointXY(0,0)


    def selectedCh(self):
        
        startField = self.fields['startRunCh']
        endField = self.fields['endRunCh']
        if startField and endField:
                       
            starts = [f[startField] for f in self.fields['readings'].selectedFeatures()]
            ends = [f[endField] for f in self.fields['readings'].selectedFeatures()]
            
            if starts and ends:
                return (min(starts),min(ends))
            
        return (None,None)       



#QgsFeatureRequest with rectangle?
#create spatial index?

    #QgsPointXY in layer crs to chainage in map units.
    #distance in map units.
    def chainage(self,point,crs=None,run=None,maxDist=250):
        transform = QgsCoordinateTransform(crs,self.crs(),QgsProject.instance())
        p = QgsGeometry().fromPointXY(transform.transform(point))
        startField = self.fields['startRunCh']
        endField = self.fields['endRunCh']
        if startField and endField and self.fields['readings'] is not None:
            f = nearestFeature(self.fields['readings'],p,maxDist)
            if f is not None:
                return f[startField]+(f[endField]-f[startField])*f.geometry().lineLocatePoint(p)/f.geometry().length()
                
    
            
    def loadReadings(self,db):
        database_functions.refit(db=db,readings=self.fields['readings'],startRunCh=self.fields['startRunCh'],endRunCh=self.fields['endRunCh'],run=self.fields['run'])
    
    
    

    def selectOnLayer(self,sections):
        pass
