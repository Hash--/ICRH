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
Z_match = 30-0*1j # matching impedance 
Z_load = 0.5 + 30*1j
Pin = 1.5e6 # W

#ideal_bridge = rf.media.Freespace(rf.Frequency(40, 60, 201, 'MHz'))

#dummy_window = rf.Media(rf.Frequency(40, 60, 201, 'MHz'), 0, 0, z0=1)
bridge = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')

idx_f = np.argmin(np.abs(bridge.frequency.f - f_match))

# Characteristic Impedance depends of the prototype number.
# TSproto10: 13.7 Ohm
# TSproto12: 46.7 Ohm
CT = ConjugateT(bridge, impedance_transformer, window)
#CT = ConjugateT(bridge, None, None)

CT.C = [68.77e-12, 77.2158e-12]

sol=CT.match(f_match=f_match, z_load=Z_load, z_match=Z_match)
CT.C = sol.x
print(sol.x*1e12)

figure(1)
clf()
CT.load(Z_load).plot_s_db(show_legend=False)

a_in = sqrt(2*Pin)
a, b = CT._plasma_power_waves([Z_load, Z_load], a_in) 

I_capa = (a-b).T*2*np.sqrt(np.real(CT.get_network().z0[:,1:])) \
        /(CT.get_network().z0[:,1:]+np.conjugate(CT.get_network().z0[:,1:]))
V_capa = (a+b).T*2*np.sqrt(np.real(CT.get_network().z0[:,1:])) \
        /(CT.get_network().z0[:,1:]+np.conjugate(CT.get_network().z0[:,1:]))

print(np.abs(I_capa[idx_f,:])/1e3, 180/pi*np.angle(I_capa[idx_f,:]), np.abs(V_capa[idx_f,:])/1e3)

