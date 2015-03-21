# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:18:23 2015

Matching a single conjugate-T.


 _ GD
 |
 [Z1]
 |__[C1]__
          |
          |-- Z_T ----[imp transf]----[window]---
  __[C2]__|  
 |
 [Z2]
 |
 - GD


@author: J.Hillairet
"""
import skrf as rf

from antenna.conjugate_t import ConjugateT
from antenna.topica import *

f_match = 55e6 # matching frequency
Z_match = 30+1j*0 # matching impedance 
Z_load = 1 + 30*1j

#ideal_bridge = rf.media.Freespace(rf.Frequency(40, 60, 201, 'MHz'))

#dummy_window = rf.Media(rf.Frequency(40, 60, 201, 'MHz'), 0, 0, z0=1)
bridge = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')

# Characteristic Impedance depends of the prototype number.
# TSproto10: 13.7 Ohm
# TSproto12: 46.7 Ohm
CT = ConjugateT(bridge, impedance_transformer, window)
#CT = ConjugateT(bridge, None, None)


sol=CT.match(C0 = [100e-12, 20e-12], 
             f_match = f_match, 
             z_load = Z_load, 
             z_match = Z_match)
print(sol.x*1e12)

#CT.C = [60e-12, 60e-12]
CT.C = sol.x

CT.load(Z_load).plot_s_db(show_legend=False)
