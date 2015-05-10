# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 22:20:59 2013

@author: hash
"""


from numpy import *
from scipy.constants import epsilon_0, mu_0, c, pi
from matplotlib.pylab import *



## WEST ICRH Two step transformer
##
## Plot the reflection coefficient (S11) in dB vs frequency
## of the WEST ICRH two step transformer
##
## JH 07/06/2013
def coaxial_characteristic_impedance(Dint,Dout, epsilon_r=1, mu_r=1):
    Z0 = sqrt(mu_0*mu_r/(epsilon_0*epsilon_r))
    Zc = Z0*log(Dout/Dint)/(2.*pi)
    return Zc 

def transfer_maxtrix(V0, I0, Z0, gamma, L):
    V = cosh(gamma*L)*V0 + Z0*sinh(gamma*L)*I0
    I = sinh(gamma*L)/Z0*V0 + cosh(gamma*L)*I0
    return V,I

# Frequency Sweep & Constants
f = arange(40e6,60e6,101)

beta = 2.*pi*f/c


# Cicuit definition
Source_Z = 30 # Ohm
Source_P = 1.5e6 # W

Load_Z = 3 #

Stage1_Dint = 140e-3# ASIPP final diameter 
Stage1_Dout = 153e-3# ASIPP final diameter 
Stage1_L = 1.5 # lambda/4 @ 50MHz
Stage1_eps_r = 1

Stage2_Dint = 114e-3# ASIPP final diameter 
Stage2_Dout = 153e-3# ASIPP final diameter 
Stage2_L = 1.5
Stage2_eps_r = 1

Stage1_Zc = coaxial_characteristic_impedance(Stage1_Dint, Stage1_Dout)
Stage2_Zc = coaxial_characteristic_impedance(Stage2_Dint, Stage2_Dout)

# Calculating impedance as seen from the source
# we start from the load and go toward the source
Z1 = Stage1_Zc * (Load_Z + 1j*Stage1_Zc*tan(beta*Stage1_L))/(Stage1_Zc+1j*Load_Z*tan(beta*Stage1_L))
Z2 = Stage2_Zc * (Z1 + 1j*Stage2_Zc*tan(beta*Stage2_L))/(Stage2_Zc+1j*Z1*tan(beta*Stage2_L))

# reflection coefficient as seen from the 30 Ohm feeder
Gamma2 = (Z2 - Source_Z)/(Z2 + Source_Z)
VSWR = (1.+abs(Gamma2))/(1.-abs(Gamma2))

# Plot Designer solution for comparison
f_designer, S11dB_designer = loadtxt( \
    'data/Sparameters/WEST/Designer_TwoStepImpedance_S11dB.csv', \
    skiprows=1, delimiter=',', unpack=True)

figure(1)
clf()
plot(f/1e6, 20*np.log10(abs(Gamma2)), \
     f_designer, S11dB_designer, linewidth=2) 
xlabel('f [MHz]')
ylabel('|$\Gamma$| [dB]')
legend(('TL theory','Ansoft Designer'))
grid()


# Calculating Voltage and Current on the Circuit
# here we start from the source where we knows the input voltage and
# current and go toward the load
f = 60e6
# copper conductivity
sigma = 4.4e7#5.8e7 # S/m
# standing wave ratio
SWR = 1

beta = 2*pi*f/c

# Voltage and current as 30 Ohm feeder
V0 = sqrt(2*Source_P*Source_Z*SWR)
I0 = sqrt(2*Source_P/Source_Z*SWR)

# from source to Stage2
l2 = linspace(0,Stage2_L,num=101)

V2 = zeros_like(l2,dtype=complex) # pay attention to define as complex !
I2 = zeros_like(l2,dtype=complex)

for idx, l2_val in enumerate(l2):
   V2[idx], I2[idx] = transfer_maxtrix(V0, I0, Stage2_Zc, 1j*beta, -l2_val)

# from Stage2 to Stage1
l1 = linspace(0,Stage1_L,101)

V1 = zeros_like(l1, dtype='complex') # same remark than for V2,I2 !
I1 = zeros_like(l1, dtype='complex')

for idx, l1_val in enumerate(l1):
   V1[idx], I1[idx] = transfer_maxtrix(V2[-1], I2[-1], Stage1_Zc, 1j*beta, -l1_val)
   
fig2=figure(2)
fig2.clear()

ax1=subplot(3,1,1)
title('f='+str(f/1e6)+' MHz')
plot(l2, abs(V2)/1e3, 'k', l2[-1]+l1, abs(V1)/1e3, 'k', lw=2)
#xlabel('L [m]')
ylabel('V [kV]')
grid(True)

ax2=subplot(3,1,2, sharex=ax1) 
plot(l2, abs(I2)/1e3, 'k', l2[-1]+l1, abs(I1)/1e3, 'k', lw=2)
#xlabel('L [m]')
ylabel('I [kA]')
grid(True)

# Calculates the loss on the conductors

# surface resistance in [Ohm/square]
Rs = sqrt(2.*pi*f*mu_0/(2.*sigma))
# Power loss density in W/m^2
P_l1_inner = Rs * abs(I1)**2 / 2 / (pi*Stage1_Dint)**2
P_l1_outer = Rs * abs(I1)**2 / 2 / (pi*Stage1_Dout)**2

P_l2_inner = Rs * abs(I2)**2 / 2 / (pi*Stage2_Dint)**2
P_l2_outer = Rs * abs(I2)**2 / 2 / (pi*Stage2_Dout)**2

#fig3 = figure(3)
#fig3.clear()
#subplot(2,1,1)
#plot( append(l2, l1+l2[-1]), append(P_l2_inner, P_l1_inner),  
#      append(l2, l1+l2[-1]), append(P_l2_outer, P_l1_outer),
#      linewidth=2 )
#grid(True)
#title('f='+str(f/1e6)+' MHz')
#xlabel('L [m]')
#ylabel('Loss Density [$W/m$]')
      
ax3=subplot(3,1,3, sharex=ax1)
plot( append(l2, l1+l2[-1]), append(P_l2_inner, P_l1_inner)/(2.*pi*Stage2_Dint/2)/1e3, '-',  
      append(l2, l1+l2[-1]), append(P_l2_outer, P_l1_outer)/(2.*pi*Stage2_Dout/2)/1e3, '--', 
      linewidth=2 )
grid(True)
xlabel('L [m]')
ylabel('Loss Density [$kW/m^2$]')
legend(('Inner Conductor', 'Outer Conductor'), loc='best')      
savefig('WEST_ICRH_Impedance_transformer_{}MHz_{}MSpermeter.png'.format(f/1e6, sigma/1e6), dpi=300)