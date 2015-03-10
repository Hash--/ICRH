# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 21:00:22 2013

@author: hash
"""
import numpy as np

class TOPICA_ZResult:
    def __init__(self,filename):
        self.filename = filename
        self.Z = self.TOPICA_Z()
        self.nbPorts = len(self.Z)
    
    def TOPICA_Z(self):
        data = np.loadtxt(self.filename, skiprows=3)
        Z = np.zeros(( np.sqrt(np.size(data,0)),np.sqrt(np.size(data,0))),dtype='complex')
        for id1 in xrange(np.size(data,0)):
            Z[data[id1,0]-1, data[id1,1]-1] = complex(data[id1,2], data[id1,3])
        return(Z)
    
    def TOPICA_ZtoS(self,Zref0):
        Zref = np.diag(np.repeat(Zref0, self.nbPorts))
        
        G = 1/np.sqrt(np.real(Zref0))        
        Gref = np.diag(np.repeat(G, self.nbPorts))
   
        S = Gref.dot(self.Z - Zref).dot(np.linalg.inv(self.Z + Zref)).dot(np.linalg.inv(Gref))
        
        return S

# Get the average real part of the Z parameters 
# of a list of TOPICA Z-filenames data
def get_Zii_avg(filenames):
    Zii = []
    Zii_avg = []
    for idx,filename in enumerate(filenames):
        data = TOPICA_ZResult(filename)
        # average real part of Zii
        Zii.append(np.real(np.diag(data.Z)))
        Zii_avg.append(np.mean(Zii[idx]))
    return(Zii_avg)

if __name__ == "__main__":
    filenames = ['Zs_TSproto1_Profile1.txt',
                'Zs_TSproto1_Profile2.txt',
                'Zs_TSproto1_Profile3.txt',
                'Zs_TSproto1_Profile4.txt',
                'Zs_TSproto1_Profile5.txt',
                'Zs_TSproto1_Profile6.txt',
                'Zs_TSproto1_Profile7.txt',
                'Zs_TSproto1_Profile8.txt']
    filenames = ['Zs_TSproto2_Profile1.txt',
                'Zs_TSproto2_Profile2.txt',
                'Zs_TSproto2_Profile3.txt',
                'Zs_TSproto2_Profile4.txt',
                'Zs_TSproto2_Profile5.txt',
                'Zs_TSproto2_Profile6.txt',
                'Zs_TSproto2_Profile7.txt',
                'Zs_TSproto2_Profile8.txt']
                
#    filenames = ['Zs_TSproto9_Profile1.txt',
#                 'Zs_TSproto9_Profile2.txt',
#                 'Zs_TSproto9_Profile3.txt',
#                 'Zs_TSproto9_Profile4.txt',
#                 'Zs_TSproto9_Profile5.txt',
#                 'Zs_TSproto9_Profile6.txt',
#                 'Zs_TSproto9_Profile7.txt',
#                 'Zs_TSproto9_Profile8.txt']
#
#    filenames = ['Zs_TS9a_Profile1.txt',
#                 'Zs_TS9a_Profile2.txt',
#                 'Zs_TS9a_Profile3.txt',
#                 'Zs_TS9a_Profile4.txt',
#                 'Zs_TS9a_Profile5.txt',
#                 'Zs_TS9a_Profile6.txt',
#                 'Zs_TS9a_Profile7.txt',
#                 'Zs_TS9a_Profile8.txt']
                 
                 
#    Z0 = 23.8 # characteristic impedance 
    Zii_avg = get_Zii_avg(filenames)
        

    