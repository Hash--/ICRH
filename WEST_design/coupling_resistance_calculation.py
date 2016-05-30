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


Rc_vec = []
for idx in range(1,9):

    #    # TS Classical
    #    fn_TOPICA = './data/TOPICA/ToreSupra_WEST/L-mode/TS_Classical_48MHz/Zs_TS9a_Profile'+str(idx)+'.txt'
    #    z0_TOPICA = 20
    #    length = -(0.149 - 20.6e-3) # m
    #    f = 48e6 # Hz
    
    #    # Proto2007
    #    fn_TOPICA = './data/TOPICA/ToreSupra_WEST/L-mode/TS_Proto2007_48MHz/Zs_TSproto1_Profile'+str(idx)+'.txt'
    #    z0_TOPICA = 23.8
    #    length = -(0.122-25e-3) # m
    #    f = 48e6 # Hz
    
     # WEST Final model
    fn_TOPICA = './data/TOPICA/ToreSupra_WEST/L-mode/TSproto12/Zs_TSproto12_55MHz_Profile'+str(idx)+'.txt'
    z0_TOPICA = 46.7
    length = -(0.1118-50.7e-3) # m 
    f = 55e6 # Hz
    
    #fn_TOPICA = './data/TOPICA/ToreSupra_WEST/H-mode/TSproto12_55MHz/Zs_TSproto12_55MHz_LAD9-5cm.txt'
    #z0_TOPICA = 46.7
    #length = -(0.1118-50.7e-3) # m 
    #f = 55e6 # Hz
    
    # Deembedding TOPICA network by a prescribed length.
    # This length depends of the CAD model sent to Daniele 
    plasma = TopicaResult(fn_TOPICA, z0_TOPICA)
    
    frequency = rf.Frequency(start=f, stop=f, npoints=1, unit='Hz')
    plasma_nwk = plasma.to_skrf_network(skrf_frequency=frequency)
    
    beta=2*pi*f/c
    # Watch out: pay attention the minus sign in the exponential below, to match 
    # the TOPICA time harmonic convention exp(-jwt)
    exp_gamma = np.eye(plasma.s.shape[0])*np.exp(-1j*beta*length)
    
    plasma_nwk_deemb = plasma_nwk.copy()
    plasma_nwk_deemb.s = exp_gamma.dot(plasma_nwk.s.squeeze()).dot(exp_gamma)
    
    #    # Additional renormalisation and deembedding for the Proto2007
    #    plasma_nwk_deemb.s = rf.renormalize_s(plasma_nwk_deemb.s, 23.8, 58.35)
    ##    plasma_nwk_deemb.z0 = 58.35
    #    exp_gamma = np.eye(plasma.s.shape[0])*np.exp(+1j*beta*10e-3)
    #    plasma_nwk_deemb.s = exp_gamma.dot(plasma_nwk.s.squeeze()).dot(exp_gamma)
       
    plasma_z = np.squeeze(plasma_nwk_deemb.z) 
    
    # export the scattering parameters in a s4p file
    plasma_nwk_deemb.write_touchstone(filename='S_TSproto12_55MHz_Hmode_LAD9-5cm',
                                      write_z0=True)
    
    # Prescribed current vector for TOPICA port
    # 2  1
    # 4  3
    # in dipole configuration.                      
    I = np.r_[+1,-1,-1,+1]
#    # in monopole configuration
#    I = np.r_[-1,-1,+1,+1]
    
    #    I = np.r_[0,0,1,-1,-1,1] # classical antenna
    
    # Resulting voltages
    V = plasma_z.dot(I)
    
    # transmitted power
    Pt = np.real(V.T.conj().dot(I))/2
    # Equivalent current
    Is = np.sqrt(np.abs(I).sum() / 4)
    
    # Coupling resistance
    Rc = Pt/(2*Is**2)
    print(Rc)
    Rc_vec.append(Rc)

   