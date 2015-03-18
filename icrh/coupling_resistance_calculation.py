# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 15:44:45 2015

This script evaluates the coupling resistance from the definition given
in Walid's paper (FED2015). 

@author: JH218595
"""

from antenna.topica import TopicaResult    
import numpy as np
import skrf as rf
from scipy.constants import c, pi

#
# TOPICA impedance matrix
#

## TS Classical
#fn_TOPICA = './data/TOPICA/ToreSupra_WEST/L-mode/TS_Classical_48MHz/Zs_TS9a_Profile1.txt'
#z0_TOPICA = 20
#length = 0.149 # m
#f = 48e6 # Hz

## Proto2007
#fn_TOPICA = './data/TOPICA/ToreSupra_WEST/L-mode/TS_Proto2007_48MHz/Zs_TSproto1_Profile1.txt'
#z0_TOPICA = 23.8
#length = 0.122 # m
#f = 48e6 # Hz

# WEST Final model
fn_TOPICA = './data/TOPICA/ToreSupra_WEST/L-mode/TSproto12/Zs_TSproto12_48MHz_Profile1.txt'
z0_TOPICA = 46.7
length = 0#0.1118 # m
f = 48e6 # Hz


# Deembedding TOPICA network by a prescribed length.
# This length depends of the CAD model sent to Daniele 
plasma = TopicaResult(fn_TOPICA, z0_TOPICA)

frequency = rf.Frequency(start=f, stop=f, npoints=1, unit='Hz')
plasma_nwk = plasma.to_skrf_network(skrf_frequency=frequency)

beta=2*pi*f/c
exp_gamma = np.eye(plasma.s.shape[0])*np.exp(1j*beta*length)

plasma_nwk_deemb = plasma_nwk.copy()
plasma_nwk_deemb.s = exp_gamma.dot(plasma_nwk.s.squeeze()).dot(exp_gamma)
plasma_z = np.squeeze(plasma_nwk_deemb.z) 

# Prescribed current vector for TOPICA port
# 2  1
# 4  3
# in dipole configuration.                      
I = np.r_[+1,-1,-1,+1]
#I = np.r_[0,0,1,-1,-1,1] # classical antenna

# Resulting voltages
V = plasma_z.dot(I)

# transmitted power
Pt = np.real(V.T.conj().dot(I))/2
# Equivalent current
Is = np.sqrt(np.abs(I).sum() / 4)

# Coupling resistance
Rc = Pt/(2*Is**2)
print(Rc)