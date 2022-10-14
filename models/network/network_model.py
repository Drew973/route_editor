
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 11:14:49 2022

@author: Drew.Bennett


interface for network layer
only used by routesModel


"""

from qgis.core import QgsFeatureRequest
from qgis.core import QgsPointXY, QgsCoordinateTransform, QgsProject,QgsGeometry


FIELDS = ['network','label','length']

class networkModel:
    
    
    def __init__(self,fields={}):
        
        if not fields:
            fields = {f:None for f in FIELDS}
        for f in FIELDS:
            if not f in fields.keys():
                raise KeyError('missing field '+f)
        self.fields = fields        
        


    def crs(self):
        if self.fields['network'] is not None:
            return self.fields['network'].crs()

    
    def unit(self):
        return self.crs().mapUnits()

    
    def selectedFeature(self):
        for f in self.fields['network'].selectedFeatures():
            return f


    def feature(self,sec):
        layer = self.fields['network']
        sf = self.fields['label']
        if sf and layer is not None:
            r = QgsFeatureRequest()#only getting subset of attributes would be more efficient...
            r.setFilterExpression('"{field}"=\'{sec}\''.format(field=sf,sec=sec))
            for f in layer.getFeatures(r):#get 1st feature
                return f
        
        
    #section chainage (in units of length field) to QgsPointXY
    def point(self,sec,ch):        
        f = self.feature(sec)
        lf = self.fields['length']
        if f and lf:
            geomLen = f.geometry().length()
            p = f.geometry().interpolate(min(geomLen*ch/f[lf],geomLen))
            if not  p.isNull():
                return p.asPoint()
        return QgsPointXY(0,0)


    #QgsPointXY in layer crs to chainage (in units of length field).
    def chainage(self,sec,point,crs):
        transform = QgsCoordinateTransform(crs,self.crs(),QgsProject.instance())
        p = QgsGeometry().fromPointXY(transform.transform(point))
        f = self.feature(sec)
        lf = self.fields['length']
        if f and lf:
            return f[lf]*f.geometry().lineLocatePoint(p)/f.geometry().length()           


    def selectOnLayer(self,sections):
        sf = self.fields['label']
        layer = self.fields['network']
        if sf and layer:
            # "section" in ('a','b')
            s = ','.join(["'{sec}'".format(sec=sec) for sec in sections])
            e = '"{field}" in ({sects})'.format(field=sf,sects=s)
            layer.selectByExpression(e)
