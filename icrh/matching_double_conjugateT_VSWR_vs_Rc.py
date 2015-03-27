# -*- coding: utf-8 -*-
"""
Created on 27/03/2015

Matching a double conjugate-T and checking the load resilience vs 
the coupling resistance.

@author: J.Hillairet
"""
import skrf as rf
from antenna.conjugate_t import ConjugateT
from antenna.resonant_loop import ResonantDoubleLoop
from antenna.topica import *
from matplotlib.pylab import *

f_match = 55e6 # matching frequency
z_match = [29.74 - 0*1j, 29.74 - 0*1j] # matching impedance target

power_input = [1.5e6, 1.5e6]
phase_input = [0.0, pi]


########
bridge = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.io.hfss_touchstone_2_network(\
        './data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')

idx_f = np.argmin(np.abs(bridge.frequency.f - f_match))

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
plasma = rf.io.hfss_touchstone_2_network(\
    './data/Sparameters/WEST/plasma_from_TOPICA/S_TSproto12_55MHz_Profile8.s4p')
    
#plasma = rf.io.hfss_touchstone_2_network(\
#    './data/Sparameters/WEST/plasma_from_TOPICA/S_TSproto12_55MHz_Hmode_LAD6-5cm.s4p')
    
# for compatibility with skrf, copy the Frequency object from Bridge
# and duplicate the S-parameters and z0 idenditically for all the frequencies
plasma.frequency = bridge.frequency
plasma.s = np.tile(plasma.s, (len(plasma.frequency), 1, 1))
plasma.z0 = np.tile(plasma.z0, (len(plasma.frequency),1))

CT1 = ConjugateT(bridge, impedance_transformer, window)
CT2 = ConjugateT(bridge, impedance_transformer, window)

RDL = ResonantDoubleLoop(CT1, CT2, plasma)

RDL.match(power_input, phase_input, f_match, z_match)

# Get results
act_vswr = RDL.get_vswr_active(power_input, phase_input)
act_S = RDL.get_s_active(power_input, phase_input)
I_plasma, V_plasma = RDL.get_currents_and_voltages(power_input, phase_input)

print(RDL.get_vswr_active(power_input, phase_input)[idx_f])

# Now the antenna has been matched on a specific antenna loading,
# we change this load and look to the VSWR.
VSWR = []
for idx_plasma in range(1,9):
    plasma = rf.io.hfss_touchstone_2_network(\
    './data/Sparameters/WEST/plasma_from_TOPICA/S_TSproto12_55MHz_Profile'+str(idx_plasma)+'.s4p')
    plasma.frequency = bridge.frequency
    plasma.s = np.tile(plasma.s, (len(plasma.frequency), 1, 1))
    plasma.z0 = np.tile(plasma.z0, (len(plasma.frequency),1))

    _RDL = ResonantDoubleLoop(CT1, CT2, plasma)
    VSWR.append(_RDL.get_vswr_active(power_input, phase_input)[idx_f])    

  