# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 12:34:43 2022

@author: Drew.Bennett


definitly need view to have
section,section_start_chainage,section_end_chainage.

may want to map to readings via 1/2 columns with readings chainage/id.


section through QgsFeatureWidget
start+end chainage through chainage delegate.
.gets feature from model. edits chainage though map click and spinbox. have?

"""


from qgis.core import QgsFeature

class routeItem:
       
    
    
    #networkFeature is qgsFeature
    def __init__(self,sectionStartChainage=0,sectionEndChainage=None,networkFeature=QgsFeature(),runStartChainage=None,runEndChainage=None):
        self.setNetworkFeature(networkFeature)

        self.sectionStartChainage = sectionStartChainage
        
        self.setSectionEndChainage(sectionEndChainage)
            
            
        self.runStartChainage = runStartChainage
        self.runEndChainage = runEndChainage
   
        
    
    def setSectionEndChainage(self,chainage):
        if chainage is None:
            f = self.getNetworkFeature()
            
            if f.hasGeometry():
                chainage = f.geometry().length()
            else:    
                chainage = 0
    
        self._sectionEndChainage = chainage
    
    
    
    def getSectionEndChainage(self):
        return self._sectionEndChainage



    def setNetworkFeature(self,feature):
        if not isinstance(feature,QgsFeature):
            raise TypeError('routeItem.setNetworkFeature expected QgsFeature. recieved {} {}'.format(type(feature),feature))
        self._networkFeature = feature



    def getNetworkFeature(self):
        return self._networkFeature


    # higher = worse fit.
    def score(self):
        pass
     
        

    def __getitem__ (self,key):
        if key==0:
            return self.getNetworkFeature()

        if key==1:
            return self.sectionStartChainage 

        
        if key==2:
            return self.getSectionEndChainage()


        if key==3:
            return self.runStartChainage 

        if key==4:
            return self.runEndChainage
        



    def __setitem__(self,key,value):
        if key==0:
            self.setNetworkFeature(value)

        if key==1:
            self.sectionStartChainage = value

        
        if key==2:
            self.setSectionEndChainage(value)


        if key==3:
            self.runStartChainage = value

        if key==4:
            self.runEndChainage = value

        

    def readingsFeatures(self,readingsLayer,startChainageField,endChainageField=None):
        pass
    
    
    
    def readingsRequest(self,readingsLayer,startChainageField,endChainageField=None):
        pass
    
    
    
    def toRteItem(self):
        pass
    
    
    
    def addToSink(self,sink,readingsLayer,startChainageField,endChainageField=None):
        pass
    
    
    property(setNetworkFeature,getNetworkFeature)
    property(setSectionEndChainage,getSectionEndChainage)
