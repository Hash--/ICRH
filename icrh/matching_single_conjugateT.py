# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:18:23 2015

Matching a single conjugate-T.


 _
 |
 Z1
 |__C1__
        |___ Z_T
  __C2__|  
 |
 Z2
 |
 -

@author: J.Hillairet
"""
import skrf as rf

from antenna.conjugate_t import ConjugateT
from antenna.topica import *

f_match = 48e6 # matching frequency
Z_match = [30+1j*0] # matching impedance 
Z_load = 1 + 30*1j

plasma_profile_nb = 8 # 1 to 8

#ideal_bridge = rf.media.Freespace(rf.Frequency(40, 60, 201, 'MHz'))

bridge = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')

filename = './data/TOPICA/Tore Supra_WEST/L-mode/TSproto12/Zs_TSproto12_'\
                +str(int(f_match/1e6))+'MHz_Profile'+str(int(plasma_profile_nb))+'.txt'
                
# Characteristic Impedance depends of the prototype number.
# TSproto10: 13.7 Ohm
# TSproto12: 46.7 Ohm
CT = ConjugateT(bridge, impedance_transformer, window)
sol=CT.match(C0=[100e-12, 20e-12], f_match=f_match, z_load=Z_load)

CT.set_capacitors(sol.x)
CT.load(Z_load).plot_s_db(show_legend=False)
