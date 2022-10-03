# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:41:08 2022

@author: Drew.Bennett
"""

from route_editor.models import routes_model
from PyQt5.QtSql import QSqlDatabase


def testInit():
    db = QSqlDatabase.addDatabase('QPSQL','routes')
    details = {'host':'localhost','database':'A69_hsrr_2022','user':'postgres','password':'pts21'}
    db.setHostName(details['host'])
    db.setDatabaseName(details['database'])
    db.setUserName(details['user'])
    db.setPassword(details['password'])

    if not db.open():
        raise ValueError('could not open database')

    m = routes_model.routesModel(db)
    m.setTable('hsrr.cateye_routes')
    m.select()
    
    m.setRun('A69 DBFO EB CL1_slips')
    print(m.rowCount())
    return m
    
    
    
if __name__=='__console__' or __name__=='__main__':
    m = testInit()
    v = QTableView()
    v.setModel(m)
    v.show()
    
    
    
    