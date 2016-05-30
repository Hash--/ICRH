# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:39:58 2015

In this script we plot the capacitor currents vs coupling resistance.

The currents have been calculated for a input power of 1.5MW per 1/2 antenna.

@author: hash
"""
import pandas as pd
from matplotlib.pylab import *


# open the excel sheet with pandas
# The data comes from the final antenna model made with Designer
data = pd.read_excel(io='./data/TOPICA/ToreSupra_WEST/WEST_ICRH_Compilation_resultats_designer.xlsx',
                     sheetname=0)

#The information we want to plot correspond to the coupling resistance 
#and the capacitor currents

# making a new convient dataFrame and removed the missing data lines
Icapa_Designer = data[['Plasma Model Coupling Resistance [Ohm] (calculated)',
                     'Matching Impedace Target [Ohm]',
                     'I1H [kA]', 'I1B [kA]', 'I2H [kA]', 'I2B [kA]']].dropna()
Icapa_Designer.rename(columns = { \
    'Plasma Model Coupling Resistance [Ohm] (calculated)':'Rc', 
    'Matching Impedace Target [Ohm]':'Zmatch'}, inplace=True)
Icapa_Designer.set_index('Rc', inplace=True)


Icapa_Designer_ideal_matching = Icapa_Designer[Icapa_Designer['Zmatch'] == '29.74 - 0j'].drop('Zmatch', axis=1)
Icapa_Designer_degrd_matching = Icapa_Designer[Icapa_Designer['Zmatch'] == '29.74 - 15j'].drop('Zmatch', axis=1)

# Data from Python skrf modeling
#
data2 = pd.read_excel(io='./data/TOPICA/ToreSupra_WEST/WEST_ICRH_Compilation_resultats_designer.xlsx',
                     sheetname=1)

Icapa_Python = data2[['Plasma Model Coupling Resistance [Ohm] (calculated)',
                     'Matching Impedace Target [Ohm]',
                     'I1H [kA]', 'I1B [kA]', 'I2H [kA]', 'I2B [kA]']].dropna()
Icapa_Python.rename(columns = { \
    'Plasma Model Coupling Resistance [Ohm] (calculated)':'Rc', 
    'Matching Impedace Target [Ohm]':'Zmatch'}, inplace=True)
Icapa_Python.set_index('Rc', inplace=True)                   

Icapa_Python_ideal_matching = Icapa_Python[Icapa_Python['Zmatch'] == '29.74 - 0j'].drop('Zmatch', axis=1)
Icapa_Python_degrd_matching = Icapa_Python[Icapa_Python['Zmatch'] == '29.74 - 15j'].drop('Zmatch', axis=1)

def plot_figure(I_ideal, I_degrd, fig=None):
    # average and std
    I_ideal_min = I_ideal.groupby(I_ideal.index).min().min(axis=1)
    I_ideal_max = I_ideal.groupby(I_ideal.index).max().max(axis=1)
    I_degrd_min = I_degrd.groupby(I_degrd.index).min().min(axis=1)
    I_degrd_max = I_degrd.groupby(I_degrd.index).max().max(axis=1)

    # For an unkown reason, I need to cast the index values into a numpy array
    # forcing the dtype to be float with pandas '0.13.1'
    x_ideal = np.array(I_ideal_min.index.values, dtype=float)
    x_degrd = np.array(I_degrd_min.index.values, dtype=float)    

    y1_ideal = I_ideal_min.values 
    y2_ideal = I_ideal_max.values 
    y1_degrd = I_degrd_min.values 
    y2_degrd = I_degrd_max.values 
#    import pdb; pdb.set_trace()

    figure(fig)
    if fig: # clean the figure if exists
        clf()
    fill_between(x_ideal, y1_ideal, y2_ideal,
                 alpha=0.2, color= 'b')
    fill_between(x_degrd, y1_degrd, y2_degrd,
                 alpha=0.2, color= 'r')
    ylim(0, 2.2)
    grid(True)
    # The fill_between() command creates a PolyCollection that is not supported by the legend() command.
    # Therefore you will have to use another matplotlib artist (compatible with legend()) as a proxy, 
    # http://stackoverflow.com/questions/14534130/legend-not-showing-up-in-matplotlib-stacked-area-plot
    plt.plot([], [], color='b', linewidth=10, alpha=0.2)
    plt.plot([], [], color='r', linewidth=10, alpha=0.2)
    legend(('VSWR=1', 'VSWR<1.7'), loc='best')

    # position bottom right
    text(2.5, 1.0, 'PRELIMINARY',
             fontsize=50, color='gray',
             ha='right', va='bottom', alpha=0.2)

# compare dataset

plot_figure(Icapa_Python_ideal_matching, Icapa_Python_degrd_matching, 1)
title('Python')
axhline(0.85, color="k", ls='--', lw=2)
plot_figure(Icapa_Designer_ideal_matching, Icapa_Designer_degrd_matching, 2)
title('Designer')
Icapa_ideal_concat = pd.concat((Icapa_Designer_ideal_matching, Icapa_Python_ideal_matching))
Icapa_degrd_concat = pd.concat((Icapa_Designer_degrd_matching, Icapa_Python_degrd_matching))
plot_figure(Icapa_ideal_concat, Icapa_degrd_concat, 3)
title('All')