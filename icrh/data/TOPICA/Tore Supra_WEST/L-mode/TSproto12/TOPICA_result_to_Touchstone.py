# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 15:21:32 2014

@author: JH218595
"""
# Import TOPICA Class in my own lib dir before !!
import skrf as rf


F0 = rf.Frequency(start=55, stop=55, npoints=1, unit='MHz')

TOPICA_res = TopicaResult(filename='Zs_TSproto12_55MHz_Profile4.txt', z0=46.7)
TOPICA_res.write_touchstone('TSproto12_55MHz_Profile4',  F0)