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
Icapa_Designer.columns.values[0] = 'Rc'
Icapa_Designer.columns.values[1] = 'Zmatch'
Icapa_Designer.set_index(Icapa_Designer['Rc'], inplace=True)
Icapa_Designer.drop('Rc', axis=1, inplace=True)

Icapa_Designer_ideal_matching = Icapa_Designer[Icapa_Designer['Zmatch'] == '29.74 - 0j'].drop('Zmatch', axis=1)
Icapa_Designer_degrd_matching = Icapa_Designer[Icapa_Designer['Zmatch'] == '29.74 - 15j'].drop('Zmatch', axis=1)

# Data from Python skrf modeling
#
data2 = pd.read_excel(io='./data/TOPICA/ToreSupra_WEST/WEST_ICRH_Compilation_resultats_designer.xlsx',
                     sheetname=1)

Icapa_Python = data2[['Plasma Model Coupling Resistance [Ohm] (calculated)',
                     'Matching Impedace Target [Ohm]',
                     'I1H [kA]', 'I1B [kA]', 'I2H [kA]', 'I2B [kA]']].dropna()
Icapa_Python.columns.values[0] = 'Rc'
Icapa_Python.columns.values[1] = 'Zmatch'

Icapa_Python.set_index(Icapa_Python['Rc'], inplace=True)
Icapa_Python.drop('Rc', axis=1, inplace=True)                     

Icapa_Python_ideal_matching = Icapa_Python[Icapa_Python['Zmatch'] == '29.74 - 0j'].drop('Zmatch', axis=1)
Icapa_Python_degrd_matching = Icapa_Python[Icapa_Python['Zmatch'] == '29.74 - 15j'].drop('Zmatch', axis=1)

def plot_figure(I_ideal, I_degrd):
    # average and std
    I_ideal_min = I_ideal.groupby(I_ideal.index).mean().min(axis=1)
    I_ideal_max = I_ideal.groupby(I_ideal.index).mean().max(axis=1)
    I_degrd_min = I_degrd.groupby(I_degrd.index).mean().min(axis=1)
    I_degrd_max = I_degrd.groupby(I_degrd.index).mean().max(axis=1)

    x_ideal = I_ideal_min.index.values
    x_degrd = I_degrd_min.index.values    
#    import pdb; pdb.set_trace()
    y1_ideal = I_ideal_min.values 
    y2_ideal = I_ideal_max.values 
    y1_degrd = I_degrd_min.values 
    y2_degrd = I_degrd_max.values 
    
    figure()
    fill_between(x_ideal, y1_ideal, y2_ideal,
                 alpha=0.2, color= 'b')
    fill_between(x_degrd, y1_degrd, y2_degrd,
                 alpha=0.2, color= 'r')
    ylim(0, 2.2)
    grid(True)


# compare dataset

plot_figure(Icapa_Python_ideal_matching, Icapa_Python_degrd_matching)
plot_figure(Icapa_Designer_ideal_matching, Icapa_Designer_degrd_matching)
Icapa_ideal_concat = pd.concat((Icapa_Designer_ideal_matching, Icapa_Python_ideal_matching))
Icapa_degrd_concat = pd.concat((Icapa_Designer_degrd_matching, Icapa_Python_degrd_matching))
plot_figure(Icapa_ideal_concat, Icapa_degrd_concat)