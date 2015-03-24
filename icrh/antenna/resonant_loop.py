# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:57:00 2014

@author: hash
"""
import numpy as np
import skrf as rf        
import scipy as sp
        
class ResonantDoubleLoop(object):

    def __init__(self, CT1, CT2, plasma, C=np.tile(60e-12,4)):
        """
        Resonant Double Loop Initializer 
        
        Parameters
        -----------
        CT1, CT2: :class: ConjugateT
            Conjugate-T objects
        plasma: :class: 'skrf.network'
            Plasma network 
        C=[C1H, C1B, C2H, C2B]: 4 elements array
            Capacitor values in Farad
        
        """
        self.CT1 = CT1
        self.CT2 = CT2
        self.plasma = plasma
        self.C = C
    
    @property
    def C(self):
        """
        Returns the capacitor set values
        """
        return self._C
    
    @C.setter
    def C(self, C):
        """
        Set the capacitor values
        
        Parameters
        -----------
        C=[C1H, C1B, C2H, C2B]: 4 elements array
            Capacitor values in Farad
        """
        self._C = C
        self.CT1.C = [self.C[0], self.C[1]]
        self.CT2.C = [self.C[2], self.C[3]]
        # update the network
        self.network = self.get_network()
        
    def get_network(self):
        '''
        Connect the both RDLs to the 4-ports plasma and return the resulting network
        
        Parameters
        ----------
        None
            
        Returns
        ----------
        antenna : :class: 'skrf.network' 2 ports network
        '''
        # connect the network together
        temp = rf.innerconnect(rf.connect(self.plasma, 0, self.CT1.network, 1), 1, 4) # watch out ! plasma ports 0 & 2 to RDL (TOPICA indexing)
        network = rf.innerconnect(rf.connect(temp, 0, self.CT2.network, 1), 0, 3)
        network.name = 'antenna'
        return(network)
    
    def match(self, a_in, f_match, Z_match):
        """
        Match the resonant double antenna for a given matching frequency and impedance
        
        Parameters
        ----------
        a_in=[a1, a2] : 2 elements array
            Input power waves
        f_match: scalar
            Matching frequency in Hz
        Z_match: 2-elements array    
            Matching impedance of each transmission line
        
        Returns
        ----------
        sol: scipy.optimize.solution
            Solution found
            
        """
        success = False
        while success == False:
            # a random number between 12 and 120 pF
            C0 = 12e-12 + sp.random.rand(4)*(120e-12 - 12e-12)
            # a random number centered on 70 pF +/- 50pF
            C0 = 70e-12 + (-1+2*sp.random.rand(4))*50e-12
            
            sol = sp.optimize.root(self._match_function, C0, args=(a_in, f_match, Z_match))
            success = sol.success
            
            print(success, sol.x/1e-12)
                
            for idm,Cm in enumerate(sol.x):
                if (Cm < 12e-12) or (Cm > 200e-12):
                    success = False
                    print('Bad solution found (out of range capacitor) ! Re-doing...')
    
        print('Solution found : C={}'.format(sol.x/1e-12))
        # Apply the solution         
        self.C = sol.x
        return(sol)        
        
    def _match_function(self, C, a_in, f_match, Z_match):
        """
        Match a double RDL on a given plasma.
        
        Parameters
        -----------
        C = [C1H, C1B, C2H, C2B] :
            capacitor values in F
        a_in=[a1, a2] : 2 elements array
            Power waves input
        f_match : number
            Matching frequency in Hz
        Z_match = [Z1_match, Z2_match] :
            (characteristic) impedances to match with
            
        Returns
        -----------
        y = [Re[Z1_active] - Re[Z1_match], Im[Z1_active] - Im[Z1_match],
             Re[Z2_active] - Re[Z2_match], Im[Z2_active] - Im[Z2_match]] :
             Matching criteria.
        
        """
        self.C = C
        
        # create the antenna network with the given capacitor values
        network = self.get_network()
        
        # optimization target
        index_f_match = np.argmin(np.abs(network.frequency.f - f_match))

        Z_active = self.get_z_active(a_in)

        y = [np.real(Z_active[index_f_match,0]) - np.real(Z_match[0]), 
             np.imag(Z_active[index_f_match,0]) - np.imag(Z_match[0]),
             np.real(Z_active[index_f_match,1]) - np.real(Z_match[1]), 
             np.imag(Z_active[index_f_match,1]) - np.imag(Z_match[1])]
        
        return(y)
        
    def get_s_active(self, a_in):
        """
        Get the "active" scattering parameters S1act and S2act.
        
        These "active" scattering parameters are defined by [from HFSS definition]
        
        Sn_active = \sum_{k=1}^N S_{nk} a_k / a_n 

        Parameters
        ----------
        a_in=[a_1,a_2]: 2 elements array
            power waves input
        
        Returns
        ----------
        Sact=[S1_active, S2_active]: 2 elements array
            active scattering parameters
            
        """
        S = self.get_network().s
        S1_active = (S[:,0,0]*a_in[0] + S[:,0,1]*a_in[1])/a_in[0]
        S2_active = (S[:,1,0]*a_in[0] + S[:,1,1]*a_in[1])/a_in[1]
        # transpose in order to have an array f x 2
        return(np.transpose([S1_active, S2_active]))

    def get_z_active(self, a_in):
        """
        Get the "active" impedance parameters Z1act and Z2act.
        
        These "active" impedance parameters are defined by [from HFSS] definition
        
        Zn_active = Z0_n * (1+Sn_active)/(1-Sn_active)
        
        Parameters
        ----------
        a_in=[a_1,a_2]: 2 elements array
            power waves input
        
        Returns
        ----------
        Zact=[Z1_active, Z2_active]: 2 elements array
            active impedance parameters        
        
        """
        # active s parameters
        Sact = self.get_s_active(a_in)
        # port characteristic impedances
        Z0 = self.get_network().z0 
        # active impedance parameters
        Z1_active = Z0[:,0]*(1+Sact[:,0])/(1-Sact[:,0])
        Z2_active = Z0[:,1]*(1+Sact[:,1])/(1-Sact[:,1])
        # transpose in order to have an array f x 2
        return(np.transpose([Z1_active, Z2_active]))
        
        
    def get_vswr_active(self, a_in):
        """
        Get the "active" VSWR vswr_1_act and vswr_2_act.
        
        These "active" VSWR are defined by [from HFSS definition]
        
        vswr_n_active = Z0_n * (1+|Sn_active|)/(1-|Sn_active|)
        
        Parameters
        ----------
        a_in=[a_1,a_2]: 2 elements array
            power waves input
        
        Returns
        ----------
        vswr_act=[vswr1_active, vswr2_active]: 2 elements array
            active VSWR
        
        """
        # active s parameters
        Sact = self.get_s_active(a_in)
#        # port characteristic impedances
#        Z0 = self.get_network().z0 
        # active vswr parameters
        vswr1_active = (1+np.abs(Sact[:,0]))/(1-np.abs(Sact[:,0]))
        vswr2_active = (1+np.abs(Sact[:,1]))/(1-np.abs(Sact[:,1]))
        # transpose in order to have an array f x 2
        return(np.transpose([vswr1_active, vswr2_active]))

    def get_f(self):
        """
        Returns the frequency values of the network
        
        Returns
        ________
        f : (f,) array
            Frequency values of the network
            alias to self.get_network().frequency.f
            
        """
        return(self.get_network().frequency.f)     

    def get_currents(self, a):
        """
        Returns the currents at the capacitors for a prescribed excitation.
        """
        # from the device scattering parameters, deduces the reflected power waves
        S = self.get_network(a)
        b=tensordot(S, a_in, axes=1)

        self.CT1.network.z #
        
        S1 = np.squeeze(self.CT1.network.s)
        
        # For all frequencies
        # Deduces the b scattering parameters from a prescribed excitation a
        # Deduces the current from b
        for idx,f in enumerate(self.CT1.network.frequency):
            b = self.CT1.network.s.dot(a)
            
    
    def get_voltages(self, a_in):
        """
        Returns the voltage at the capacitors for a prescribed excitation.
        """
        pass        