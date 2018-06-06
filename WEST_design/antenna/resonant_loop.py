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
        # renormalize the characteritic impedance of the conjugate-T ports 2 & 3 
        # to the plasma port characteristic impedances
        self.CT1.z0[1:] = np.array([self.plasma.z0[0,0], self.plasma.z0[0,2]])
        self.CT2.z0[1:] = np.array([self.plasma.z0[0,1], self.plasma.z0[0,3]])
        
        # Should we renormalize as well the bridge output port z0 to the plasma port z0 ?
        #self.CT1.network = self.CT1.get_network().renormalize(
        #    np.tile([self.CT1.z0[0], self.plasma.z0[0,0], self.plasma.z0[0,2]], (len(self.CT1.network),1) ))
        #self.CT2.network = self.CT2.get_network().renormalize(
        #    np.tile([self.CT2.z0[0], self.plasma.z0[0,1], self.plasma.z0[0,3]], (len(self.CT2.network),1) ))
               
        # connect the network together       
        temp1 = rf.connect(self.plasma, 0, self.CT1.get_network(), 1)
        temp2 = rf.innerconnect(temp1, 1, 4) # watch out ! plasma ports 0 & 2 to RDL (TOPICA indexing)
        network = rf.innerconnect(rf.connect(temp2, 0, self.CT2.get_network(), 1), 0, 3)
        network.name = 'antenna'
        return(network)
    
    def match(self, power_in, phase_in, f_match, Z_match):
        """
        Match the resonant double antenna for a given matching frequency and impedance
        
        Parameters
        ----------
        power_in : 2 element array 
            Input wave powers [Watts]
        phase_in : 2 element array
            Input wave phases [rad]
        f_match: scalar
            Matching frequency in [Hz]
        Z_match: 2-elements array    
            Matching impedance of each transmission line in [Ohm]
        
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
            
            sol = sp.optimize.root(self._match_function, C0, args=(power_in, phase_in, f_match, Z_match))
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
        
    def _match_function(self, C, power_in, phase_in, f_match, Z_match):
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

        Z_active = self.get_z_active(power_in, phase_in)

        y = [np.real(Z_active[index_f_match,0]) - np.real(Z_match[0]), 
             np.imag(Z_active[index_f_match,0]) - np.imag(Z_match[0]),
             np.real(Z_active[index_f_match,1]) - np.real(Z_match[1]), 
             np.imag(Z_active[index_f_match,1]) - np.imag(Z_match[1])]
        
        return(y)
        
    def get_power_waves(self, power_in, phase_in):
        '''
        Returns the input power waves from power and phase excitations.        
        
        Arguments
        ---------
         - power_in [2x1] : input RF power in each ConjugateT [W]
         - phase_in [2x1] : input phase in each ConjugateT [rad]
         
        Returns
        ---------
         - a_in [2x1] : input power waves
         
        '''
        # Wath out the factor 2 in the power wave definition 
        # This is expected from the power wave definition
        #  as the power is defined by P = 1/2 V.I --> P = 1/2 a^2 
        a_in = np.sqrt(2*np.array(power_in)) * np.exp(1j*np.array(phase_in)) 
        
        return a_in
        
    def get_s_active(self, power_in, phase_in):
        """
        Get the "active" scattering parameters S1act and S2act.
        
        These "active" scattering parameters are defined by [from HFSS definition]
        
        Sn_active = \sum_{k=1}^N S_{nk} a_k / a_n 

        Arguments
        ---------
         - power_in [2x1] : input RF power in each ConjugateT [W]
         - phase_in [2x1] : input phase in each ConjugateT [rad]
        
        Returns
        ----------
        Sact=[S1_active, S2_active]: 2 elements array
            active scattering parameters
            
        """
        a_in = self.get_power_waves(power_in, phase_in)
        
        S = self.get_network().s
        S1_active = (S[:,0,0]*a_in[0] + S[:,0,1]*a_in[1])/a_in[0]
        S2_active = (S[:,1,0]*a_in[0] + S[:,1,1]*a_in[1])/a_in[1]
        # transpose in order to have an array f x 2
        return(np.transpose([S1_active, S2_active]))

    def get_z_active(self, power_in, phase_in):
        """
        Get the "active" impedance parameters Z1act and Z2act.
        
        These "active" impedance parameters are defined by [from HFSS] definition
        
        Zn_active = Z0_n * (1+Sn_active)/(1-Sn_active)
        
        Arguments
        ---------
         - power_in [2x1] : input RF power in each ConjugateT [W]
         - phase_in [2x1] : input phase in each ConjugateT [rad]
        
        Returns
        ----------
        Zact=[Z1_active, Z2_active]: 2 elements array
            active impedance parameters        
        
        """
        # active s parameters
        Sact = self.get_s_active(power_in, phase_in)
        # port characteristic impedances
        Z0 = self.get_network().z0 
        # active impedance parameters
        Z1_active = Z0[:,0]*(1+Sact[:,0])/(1-Sact[:,0])
        Z2_active = Z0[:,1]*(1+Sact[:,1])/(1-Sact[:,1])
        # transpose in order to have an array f x 2
        return(np.transpose([Z1_active, Z2_active]))
        
        
    def get_vswr_active(self, power_in, phase_in):
        """
        Get the "active" VSWR vswr_1_act and vswr_2_act.
        
        These "active" VSWR are defined by [from HFSS definition]
        
        vswr_n_active = Z0_n * (1+|Sn_active|)/(1-|Sn_active|)
        
        Arguments
        ---------
         - power_in [2x1] : input RF power in each ConjugateT [W]
         - phase_in [2x1] : input phase in each ConjugateT [rad]
        
        Returns
        ----------
        vswr_act=[vswr1_active, vswr2_active]: 2 elements array
            active VSWR
        
        """
        # active s parameters        
        Sact = self.get_s_active(power_in, phase_in)
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

    def get_currents_and_voltages(self, power_in, phase_in, frequencies=None):
        """
        Returns the currents and voltages at the capacitors (plasma side)
        for a prescribed power excitation.
        
        Arguments
        ---------
         - power_in [2x1] : input RF power in each ConjugateT [W]
         - phase_in [2x1] : input phase in each ConjugateT [rad]
         - frequencies (None) : selected frequencies as a list. 
                             If None, return results for all network frequencies
        
        Returns
        ---------
         - I_capa [fx2]: capacitor currents in [A]
         - V_capa [fx2]: capacitor voltages in [A]
         
         
        """

        a_in = self.get_power_waves(power_in, phase_in)       
        
        # For each frequencies of the network
        _a = []
        _b = []

        if frequencies is None:
            frequencies = self.CT1.frequency.f
       
        for idx, f in enumerate(self.CT1.frequency.f):
            
            if f in frequencies:
            
                S_CT1 = self.CT1.get_network().s[idx]
                S_CT2 = self.CT2.get_network().s[idx]
                S_plasma = self.plasma.s[idx]

                # convenience matrices
                A = np.array([[S_CT1[1,0], 0 ], 
                              [0         , S_CT2[1,0] ],
                              [S_CT1[2,0], 0 ],
                              [0         , S_CT2[2,0]]])
                C = np.array([[S_CT1[1,1], 0, S_CT1[1,2], 0], 
                              [0, S_CT2[1,1], 0, S_CT2[1,2]],
                              [S_CT1[2,1], 0, S_CT1[2,2], 0], 
                              [0, S_CT2[2,1], 0, S_CT2[2,2]]])
                _a_plasma = np.linalg.inv(np.eye(4) - C.dot(S_plasma)).dot(A).dot(a_in)
                _b_plasma = S_plasma.dot(_a_plasma)

                _a.append(_a_plasma)
                _b.append(_b_plasma)
            
        a_plasma = np.column_stack(_a)
        b_plasma = np.column_stack(_b)
        
        # Deduces Currents and Voltages from power waves
        z0 = np.concatenate((self.CT1.z0[1:], self.CT2.z0[1:]))
        I_plasma = (a_plasma - b_plasma).T / np.sqrt(np.real(z0))
        V_plasma = (a_plasma + b_plasma).T * np.sqrt(np.real(z0))

        return I_plasma, V_plasma            
            
    
     