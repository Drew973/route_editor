# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 07:54:30 2022

@author: Drew.Bennett
"""

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import QVariant


from qgis.core import QgsFeature,QgsProject,QgsVectorLayer,QgsField



def createRoutesTable(db):
    q='''
    create table if not exists routes
    (
    pk serial,
    sec text,
    start_sec_ch NUMERIC,
    end_sec_ch NUMERIC,
    run text,
    start_run_ch NUMERIC,
    end_run_ch NUMERIC
    )
    '''
    
    e = db.exec(q).lastError()
    
    if e.isValid():
        print(e.text())
  
        
       

def createReadingsTable(db):
    q = '''
    create table if not exists readings
    (
    fid int,
    run text,
    s_ch NUMERIC,
    e_ch NUMERIC
    )
    '''
    db.exec(q)
    
    
    
    
    
def createNetworkTable(db):
     q = '''
     create table if not exists network
     (
     sec text primary key,
     s_ch NUMERIC,
     e_ch NUMERIC
     )
     '''
     db.exec(q)
     
     
    
    #sink:QgsFeatureSink
def refit(db,readings,startRunCh,endRunCh,run='',sink=None):
    
    loadReadings(db,layer = readings, run = run, startRunCh = startRunCh, endRunCh = endRunCh)
    
    if sink is None:
        sink = QgsVectorLayer("Linestring?", "fitted", "memory")
        sink.setCrs(readings.crs())
        
        
        pr = sink.dataProvider()
        pr.addAttributes(readings.fields())
        
        pr.addAttributes([
                          QgsField("sec",  QVariant.String),
                          QgsField("startSecCh", QVariant.Double),
                          QgsField("endSecCh", QVariant.Double),
                          ])
        sink.updateFields()
        
        QgsProject.instance().addMapLayer(sink)
    
    if isinstance(sink,QgsVectorLayer):
        sink = sink.dataProvider()
    
    query = '''
    select 
    fid
    ,sec
    ,max(start_sec_ch,start_sec_ch+(s_ch-start_run_ch)*(end_sec_ch-start_sec_ch)/(end_run_ch-start_run_ch)) as s
    ,min(end_sec_ch,start_sec_ch+(e_ch-start_run_ch)*(end_sec_ch-start_sec_ch)/(end_run_ch-start_run_ch)) as e
    ,max(start_run_ch,s_ch) as start_run_ch
    ,min(end_run_ch,e_ch) as end_run_ch
    from readings inner join routes 
    on routes.run=readings.run and s_ch<end_run_ch and e_ch>start_run_ch and end_run_ch>start_run_ch
    '''
 
    q = db.exec(query)
    features = []
    
    fields = readings.fields().names()
    
    while q.next():
        readingFeat = readings.getFeature(q.value(0))
        
        f = QgsFeature(sink.fields())
        
        for field in fields:
            f[field] = readingFeat[field]
        
        f['sec'] = q.value(1)
        f['startSecCh'] = q.value(2)
        f['endSecCh'] = q.value(3)
        
        f.setGeometry(readingFeat.geometry())
        features.append(f)
    
    print(sink.addFeatures(features))
    
    
    
def loadReadings(db,layer,run,startRunCh,endRunCh):
    db.exec('delete from readings')
    q = QSqlQuery(db)
    q.prepare('insert into readings(fid,run,s_ch,e_ch) values(:fid,:run,:s_ch,:e_ch)')
    
    #test performance. is execBatch() worthwhile?
    
    for f in layer.getFeatures():
        q.bindValue(':fid',f.id())
        q.bindValue(':run',f[run])
        q.bindValue(':s_ch',f[startRunCh])
        q.bindValue(':e_ch',f[endRunCh])
        r = q.exec()
    
    


