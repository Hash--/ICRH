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

from matplotlib.pylab import *

f_match = 55e6 # matching frequency
Z_match = 29.74 # matching impedance 


#ideal_bridge = rf.media.Freespace(rf.Frequency(40, 60, 201, 'MHz'))

#dummy_window = rf.Media(rf.Frequency(40, 60, 201, 'MHz'), 0, 0, z0=1)
bridge = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')


## Simple plasma load, two independant impedance 
#Z_simple1 = 1+30*1j
#Z_simple2 = 1+30*1j
## The Z matrix ports indexing follows TOPICA convention, that is indexes strap 1 and 3, and 2 and 4
## create a diagonal Z-matrix
#Z_matrix_simple = np.diag([Z_simple1, Z_simple2, Z_simple1, Z_simple2])
## creating the associated network
#plasma = rf.Network(s=rf.z2s(np.tile(Z_matrix_simple,(len(bridge.frequency),1,1)), z0=[13,13,13,13]))
#plasma.frequency = bridge.frequency
#plasma.z0 = [13.7,13.7,13.7,13.7]
#plasma


def TOPICA_2_network(filename, z0):
    proto9 = TopicaResult(filename, z0)
    # we re-set the characteristic impedance in order to match the bridge characteric impedance
    # TODO: for future TOPICA results, check that the CAD model characteristic impedance is coherent with the bridge model used. 
    proto9.z0 = [z0]*4
    plasma_TOPICA = proto9.to_skrf_network(bridge.frequency, name='plasma')
    return(plasma_TOPICA)

# # RAW data from TOPICA
#plasma = TOPICA_2_network('./data/TOPICA/ToreSupra_WEST/L-mode/TSproto12/Zs_TSproto12_50MHz_Profile1.txt', \
#                            z0=46.7)

# TOPICA matrices corrected from deembedding
plasma = rf.io.hfss_touchstone_2_network('./data/Sparameters/WEST/plasma_from_TOPICA/S_TSproto12_55MHz_Profile8.s4p')
# for compatibility with skrf, copy the Frequency object from Bridge
# and duplicate the S-parameters and z0 idenditically for all the frequencies
plasma.frequency = bridge.frequency
plasma.s = np.tile(plasma.s, (len(plasma.frequency), 1, 1))
plasma.z0 = np.tile(plasma.z0, (len(plasma.frequency),1))

# Characteristic Impedance depends of the prototype number.
# TSproto10: 13.7 Ohm
# TSproto12: 46.7 Ohm
CT1 = ConjugateT(bridge, impedance_transformer, window, capacitor_model='equivalent')
CT2 = ConjugateT(bridge, impedance_transformer, window, capacitor_model='equivalent')

RDL = ResonantDoubleLoop(CT1, CT2, plasma)
a_in = [1,-1]
f_match = 55e6
z_match = [29.74, 29.74]
RDL.match(a_in, f_match, z_match)

figure(2)
clf()
subplot(121)
RDL.get_network().plot_s_db(m=0,n=0)
RDL.get_network().plot_s_db(m=1,n=1)
axis([40,60,-50,0])
legend(('S11', 'S22'),loc='best')

subplot(122)
plot(RDL.get_f()/1e6, 20*np.log10(np.abs(RDL.get_s_active(a_in))))
legend(('Sact1', 'Sact2'),loc='best')
axis([40,60,-50,0])