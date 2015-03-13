from matplotlib import pylab, mlab, pyplot
from pylab import *
import numpy as np
from scipy.io import loadmat


data=loadmat('scan_profile_2007_Q1_Q2_Q5_hybrid_COMSOL_2D_3D_150213.mat')

# Q2 and Q5: classical antennas. R=3.15 and 3.13
# Q1 : 2007 prototype antenna. R=3.13

RQ1 = np.squeeze(data['RQ1'])
RQ2 = np.squeeze(data['RQ2'])
RQ5 = np.squeeze(data['RQ5'])

ne_cutoff = np.squeeze(data['ne_cutoff'])
Rcutoff = np.squeeze(data['Rcutoff'])

RcQ1 = np.squeeze(data['RcQ1'])
RcQ2 = np.squeeze(data['RcQ2'])
RcQ5 = np.squeeze(data['RcQ5'])

figure(1)

plot((RQ2 - Rcutoff)*1e3, RcQ2, lw=2)

xlabel('$R_{ant}$-$R_{cutoff}$ [mm]', fontsize=16)
ylabel('$R_c$ [$\Omega$/m]', fontsize=16)
#set(gca, 'YScale', 'log')
xticks(fontsize=14)
yticks(fontsize=14)
grid(True);