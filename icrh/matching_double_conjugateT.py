# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17

Matching a double conjugate-T.


 _ GD
 |
 [Z1]
 |__[C1]__
          |
          |-- Z_T ----[imp transf]----[window]--- Gen1
  __[C2]__|  
 |
 [Z2]
 |
 - GD

 _ GD
 |
 [Z3]
 |__[C3]__
          |
          |-- Z_T ----[imp transf]----[window]--- Gen2
  __[C4]__|  
 |
 [Z4]
 |
 - GD


@author: J.Hillairet
"""
import skrf as rf

from antenna.conjugate_t import ConjugateT
from antenna.resonant_loop import ResonantDoubleLoop
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

plasma = TopicaResult('./data/TOPICA/Tore Supra_WEST/L-mode/TSproto12/Zs_TSproto12_50MHz_Profile8.txt', \
                        z0=46.7)

# Characteristic Impedance depends of the prototype number.
# TSproto10: 13.7 Ohm
# TSproto12: 46.7 Ohm
CT1 = ConjugateT(bridge, impedance_transformer, window)
CT2 = ConjugateT(bridge, impedance_transformer, window)

RDL = ResonantDoubleLoop(CT1, CT2, plasma)