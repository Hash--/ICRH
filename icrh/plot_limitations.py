# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:39:58 2015

In this script we plot the maximum coupled power limits vs coupling resistance.
The limitations come from the maximum current permitted in capacitors and the 
maximum voltage. In fact, all the limits are due to the current limits only. 

@author: hash
"""
import pandas as pd
from matplotlib.pylab import *
from scipy.optimize import curve_fit

# open the excel sheet with pandas
# The data comes from the final antenna model made with Designer
data = pd.read_excel(io='./data/TOPICA/ToreSupra_WEST/WEST_ICRH_Compilation_resultats_designer.xlsx')

#The information we want to plot correspond to the coupling resistance 
#and the maximum power
Rc = data['Plasma Model Coupling Resistance [Ohm] (calculated)'].values
Pmax = data['Worse Power Limit [MW]'].values

# some data are missing : the Pmax value is either 0 or nan. 
# Filter those data
idx = pd.notnull(Pmax) * (Pmax > 0)
Rc = Rc[idx]
Pmax = Pmax[idx]

# The max power is given for 1/2 antenna.
# We multiply to get the total power for three antennas
Pmax = 3*2*Pmax

# plot the raw data, just to see
figure(1)
clf()
plot(Rc, Pmax, '.')

# these data comes from two kinds of matching strategy : either match for a real 
# impedance (the one of the feeder, almost 30 Ohms) or match for a complex impedance,
# adding an imaginary part which will increase the current (and symmetrize them as well)
# at the depends of an increase of the VSWR for the generator.
# Let's filter these two set of data.
Zmatch = data[u'Matching Impedace Target [Ohm]'].values
strategy1 = Zmatch[idx] == '29.74 - 0j'
strategy2 = Zmatch[idx] == '29.74 - 15j'

figure(2)
clf()
plot(Rc[strategy1], Pmax[strategy1], 'ko', ms=7)
plot(Rc[strategy2], Pmax[strategy2], 'ks', ms=7)

_Rc = np.linspace(0.01, 4, 101)

def func(x, a, b, c, d ):
    return a*(x+c)**b

popt, pcov = curve_fit(func, Rc[strategy1], Pmax[strategy1])
_Pmax_stgy1 = func(_Rc, *popt)
popt, pcov = curve_fit(func, Rc[strategy2], Pmax[strategy2])
_Pmax_stgy2 = func(_Rc, *popt)

#plot(_Rc, _Pmax_stgy1)
#plot(_Rc, _Pmax_stgy2)
fill_between(_Rc, _Pmax_stgy1, _Pmax_stgy2, alpha=0.2)

xlim(0.1, 3)
ylim(0, 2*3*2)
xlabel('Coupling Resistance [$\Omega$]', fontsize=14)
ylabel('Max Coupled Power [MW]', fontsize=14)
xticks(fontsize=14)
yticks(fontsize=14)
grid(True)


fill_between(_Rc, _Pmax_stgy1, alpha=0.2, color= 'g')
fill_between(_Rc, _Pmax_stgy1, _Pmax_stgy2, alpha=0.2, color='r')
