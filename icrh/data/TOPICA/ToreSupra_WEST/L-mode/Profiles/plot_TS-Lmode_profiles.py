from matplotlib import pylab, mlab, pyplot
from pylab import *
import numpy as np


R1, ne1 = np.loadtxt('TS40574_profil1.txt', unpack=True)
R2, ne2 = np.loadtxt('TS40574_profil2.txt', unpack=True)
R3, ne3 = np.loadtxt('TS40574_profil3.txt', unpack=True)
R4, ne4 = np.loadtxt('TS40574_profil4.txt', unpack=True)
R5, ne5 = np.loadtxt('TS40574_profil5.txt', unpack=True)
R6, ne6 = np.loadtxt('TS40574_profil6.txt', unpack=True)
R7, ne7 = np.loadtxt('TS40574_profil7.txt', unpack=True)
R8, ne8 = np.loadtxt('TS40574_profil8.txt', unpack=True)

# Q2 and Q5: classical antennas. R=3.15 and 3.13
# Q1 : 2007 prototype antenna. R=3.13
R_Q1 = 3.13

Rcutoff = np.array([3.1037,  3.1125,  3.118 ,  3.1242,  3.1294,  3.1368,  3.1417, 3.1481])

figure(1)
clf()
# Cycling the color cycle of the curve, from green (good coupling)
# to red (bad coupling)
# Inspired from http://stackoverflow.com/questions/4805048/how-to-get-different-colored-lines-for-different-plots-in-a-single-figure

colormap = cm.RdYlGn
gca().set_color_cycle([colormap(i) for i in np.linspace(0,0.9, 8)])

plot(R1, ne1/1e18,
     R2, ne2/1e18,
     R3, ne3/1e18,
     R4, ne4/1e18,
     R5, ne5/1e18,
     R6, ne6/1e18,
     R7, ne7/1e18,
     R8, ne8/1e18, lw=2)

axvline(x=R_Q1, color='k', lw=3, ls='--')

xlabel('R [m]', fontsize=14)
ylabel('$n_e$ [$10^{18}$ $m^{-3}$]', fontsize=14)
#set(gca, 'YScale', 'log')
xticks(fontsize=14)
yticks(fontsize=14)
grid(True);

labels=[]
for idx in range(8):
#    labels.append('$R_{cutoff}$='+str(Rcutoff[idx])+' m')
    labels.append('$d_{\mathrm{cutoff}}$='+str((R_Q1-Rcutoff[idx])*100)+' cm')
legend(labels, loc='best')    

annotate('Antenna\nradial location\n R='+str(R_Q1)+' m', (R_Q1, 30), xytext=(3.14, 35), size=16, \
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.2"))
         
savefig('TS40574_density_profiles.png', dpi=300)         