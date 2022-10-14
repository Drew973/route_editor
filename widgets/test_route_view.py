# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:41:08 2022
@author: Drew.Bennett
"""
from route_editor.models import test_routes_model
from route_editor.widgets import route_view


if __name__=='__console__' or __name__=='__main__':
    m = test_routes_model.testRoutesInit()
    v = route_view.routeView()
    v.setModel(m)
    v.show()
    