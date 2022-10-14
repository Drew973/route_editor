# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:26:33 2022

@author: Drew.Bennett
"""

from PyQt5.QtSql import QSqlDatabase
import os




from route_editor import test

def getDb():
   # db = QSqlDatabase.addDatabase("QSQLITE",'routes')
    db = QSqlDatabase.addDatabase("QSPATIALITE",'routes')

    dbFile = os.path.join(os.path.dirname(test.__file__),'test.db')
    print(dbFile)
    db.setDatabaseName(dbFile)
    if not db.open():
        raise ValueError('could not open database')
    return db