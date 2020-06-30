# -*- coding: utf-8 -*-
"""
Generate an equivalent plasma dielectric as eps_r = S - D for a given frequency
"""
#%%
from plasmapy.formulary.dielectric import cold_plasma_permittivity_SDP
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from scipy.constants import pi
#%% Antenna parameters
f0 = 50e6
omega = 2*pi*f0 * u.rad/u.s
Rant = 2.89 * u.m
#○ magnetic field configuration
B0 = 3.6 * u.T
R0 = 2.529 * u.m


#%% Read TOPICA density input files 
R, ne = np.loadtxt('TOPICA_WEST_H-mode_ne_LAD6_Rsep_2.93m.txt', skiprows=3, unpack=True)

# distance form antenna toward plasma
X = Rant.value - R


# generate B profile
B = B0*R0/R 

# generate stix parameters
species = ('e-', 'D+')
ns = (ne, ne)
S, D, P = cold_plasma_permittivity_SDP(B0, species, ns, omega)

eps_r = np.abs(S-D)

#%% plot profiles
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(X, ne)

ax12 = ax1.twinx()
ax12.plot(X, B, color='C2')
ax12.set_ylim(2.5, 4)

ax2.plot(X, eps_r)
ax2.set_xlabel('Rant - R')

[a.axvline(0, color='gray', ls='--') for a in (ax1, ax2)]

#%% export for HFSS
# NB : X must be increasing to fit HFSS setup
np.savetxt('HFSS_epsr_profile_vs_X.tab',  np.flipud(np.vstack([X, eps_r.value]).T), delimiter='\t')

# 
