# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:57:00 2014

@author: hash
"""
import skrf as rf
import numpy as np
import scipy.optimize

class ResonantLoop(object):
    """
    Resonant Loop Class.
    
    This class describes a resonant loop network. 
    Its consist of:
     - two capacitors
     - one bridge
     - one impedance transformer
     - one window
    """

    def __init__(self, bridge, imp_tr, window, C=[60e-12, 60e-12], model='equivalent', name='RL'):
        """
        Resonant Loop Constructor.
                
        Arguments
        ----------
        bridge: :class: 'skrf.network'
            Bridge network
        imp_tr: :class: 'skrf.network'
            Impedance Transformer network
        window: :class: 'skrf.network'
            Window (feed-through) network
        C=[CH,CB]: float array (default: 60pF)   
            Capacitor (Upper and Lower) values in Farad
        model: string {'ideal', 'equivalent'} (defaut:'equivalent')   
            Capacitor electrical model
        name: string (default:'RL')
            Name of the network created 
            
            
        """
        # creates the circuit=window + impedance transformer + bridge
        window_imptrans = rf.connect(window, 1, imp_tr, 0)
        window_imptrans_bridge = rf.connect(window_imptrans, 1, bridge, 0)        
        self.circuit = window_imptrans_bridge
        
        # set various properties
        self.model = model
        self.frequency = window_imptrans_bridge.frequency
        self.z0 = window_imptrans_bridge.z0[0][:]        
        self.set_capacitors(C)
        
        
        # create the network (=citcuit+capacitors)
        self.network = self.get_network() 
        self.network.name = name
        
    def set_capacitors(self, C):
        """
        Set the two capacitors values.
        
        Arguments
        ---------
        C=[CH,CB] in F
        
        """
        self.CH = C[0]
        self.CB = C[1]
        
        # update the network
        self.network = self.get_network() 
        
        
    def get_network(self):
        # creates two-ports networks of the equivalent circuit of the capacitors
        capa_H = self._capacitor_network(self.CH, z0=self.z0[1])
        capa_B = self._capacitor_network(self.CB, z0=self.z0[2])
        # return the skrf Network object
        return(rf.connect(rf.connect(self.circuit,1, capa_H,0),1, capa_B,0))
    
        
    def load(self, Z_plasma):
        """
        Load a the resonant loop by complex impedances without poloidal coupling
        
        Parameters
        ----------
        Z_plasma = scalar, 2-element array [Z_plasma_upper, Z_plasma_lower] or 2x2 array:
            Complex impedances to be connected at bridges output ports
        
        Returns
        ----------
        network: :class: 'skrf.network'
            Resulting network (1 port)
        
        """
        freq = self.frequency # Frequency object
    
        z0_RDL_H = self.z0[1]
        z0_RDL_B = self.z0[2]    
   
        ## method 1 : add the complex impedance of the capacitor to the load impedance
        #Z_CH = 1.0/(1j*self.CH*2*pi*freq.f)
        #Z_CB = 1.0/(1j*self.CB*2*pi*freq.f)
        #              
        #Z_L_H =  np.reshape(Z_plasma + Z_CH, (len(freq),1,1))
        #Z_L_B =  np.reshape(Z_plasma + Z_CB, (len(freq),1,1))
        #
        #S_plasma_H = rf.z2s(Z_L_H, z0=z0_RDL_H)
        #S_plasma_B = rf.z2s(Z_L_B, z0=z0_RDL_B)
        #
        ## creates Network object from S-matrix
        #load_H = rf.Network(frequency=freq, s=S_plasma_H, z0=z0_RDL_H)
        #load_B = rf.Network(frequency=freq, s=S_plasma_B, z0=z0_RDL_B)
        #
        ## connect network
        #loaded_RDL = rf.connect(rf.connect(self.circuit,1,load_H,0),1, load_B, 0)
        
        
        # method 2 : creates a 2ports network for each capacitor and connect to 
    
        # Convert the load impedances into networks
        if np.isscalar(Z_plasma):
            Z_plasma = np.tile(Z_plasma, 2)
        
        if np.shape(Z_plasma) == (2,):     
            S_plasma_H = rf.z2s(Z_plasma[0]*np.ones((len(freq),1,1)), z0=z0_RDL_H)
            S_plasma_B = rf.z2s(Z_plasma[1]*np.ones((len(freq),1,1)), z0=z0_RDL_B)
                
            load_H = rf.Network(frequency=freq, s=S_plasma_H, z0=z0_RDL_H)
            load_B = rf.Network(frequency=freq, s=S_plasma_B, z0=z0_RDL_B)
            
            return(rf.connect(rf.connect(self.get_network(),1,load_H,0),1, load_B, 0))
        
        elif np.shape(Z_plasma) == (2,2):
            # Convert the load impedances into a S-parameter matrices (f x n x n), under the correct char. impedance
            S_L = rf.z2s(np.tile(Z_plasma, (len(freq),1,1)), z0=[z0_RDL_H, z0_RDL_B])
            
            # creates Network object from S-matrix
            load = rf.Network(s=S_L, z0=[z0_RDL_H, z0_RDL_B] )
            load.frequency = freq
            
            # Connect the loads to the bridge ports 1 & 2   
            _loaded_bridge = rf.connect(self.get_network(), 1, load, 0)
            loaded_bridge = rf.innerconnect(_loaded_bridge, 1, 2)

            return(loaded_bridge)
    
    def _capacitor_network(self, C, z0):
        """
        Return a 2 ports skrf.Network of a capacitor.
        
        """
        # 2 ports
        S_capacitor = np.zeros((len(self.frequency),2,2), dtype='complex')
                
        for idf,f in enumerate(self.frequency.f):
            if self.model == 'ideal':
                Z_capacitor = 1./(1j*C*2*np.pi*f)
            elif self.model == 'equivalent':
                Z_C_serie = 1./(1j*C*2*np.pi*f)
                Z_R_serie = 0.01 # Ohm
                Z_L_serie = 1j*(24e-9)*2*np.pi*f # 24 nH serie inductance
                Z_R_parallel = 20e6 # Ohm
                
                Z_serie = Z_C_serie + Z_R_serie + Z_L_serie  
                Z_capacitor = (Z_serie * Z_R_parallel)/(Z_serie + Z_R_parallel)
                
            # serie-thru impedance S-matrix
            S_capacitor[idf,] = 1/(Z_capacitor+2*z0)*np.array([[Z_capacitor,2*z0],[2*z0, Z_capacitor]])
        
        capacitor = rf.Network(frequency=self.frequency, s=S_capacitor, z0=z0)
        return(capacitor)    
        
        
    def match(self, C0=[60e-12, 120e-12], f_match=50e6, z_load=1.0+30*1j):
        """
        Match the resonant loop for a prescribed load impedance at a specified frequency
        
        Parameters
        ----------
        C0 = [C0H,C0B]: 
            capacitor values starting point
        f_match: (default: 50 MHz)
            matching frequency in Hz
        z_load: scalar, 2-element array or 2x2 array (default: 1+30j)
            complex impedance for both bridge outputs
        
        Returns
        ----------
        sol: :class: 'scipy.optimize.solution'
        """
        sol = scipy.optimize.root(self._optim_fun_single_RL, C0, args=(f_match, z_load) ) # 60pF as a starting point
        self.set_capacitors(sol.x)            
        return(sol)
    
    def _optim_fun_single_RL(self, C, f_match, z_load):
        """
        Return the match conditions at the
        C=[C1,C2]
        RL : ResonantLoop class
        f_match
        z_load 
        
        """
        self.set_capacitors(C)
        
        loaded_RL = self.load(z_load)
        
        index_f_match = np.argmin(np.abs(loaded_RL.frequency.f - f_match))
        
        Z11_re = loaded_RL.z_re[index_f_match].squeeze() # 100 = ~ 50 MHz (mid-band bins point)
        Z11_im = loaded_RL.z_im[index_f_match].squeeze()
        y = [Z11_re - 30, Z11_im - 0]
    
        return(y)    
        
        
class ResonantDoubleLoop(object):

    def __init__(self, RL1, RL2, plasma, C=np.tile(60e-12,4)):
        """
        Resonant Double Loop Initializer 
        
        Parameters
        -----------
        RL1, RL2: :class: ResonantLoop 
            Resonant Loop objects
        plasma: :class: 'skrf.network'
            Plasma network 
        C=[C1H, C1B, C2H, C2B]: 4 elements array
            Capacitor values in Farad
        
        """
        self.RL1 = RL1
        self.RL2 = RL2
        self.plasma = plasma
        self.set_capacitors(C)
        
    def set_capacitors(self, C):
        """
        Set the capacitor values
        
        Parameters
        -----------
        C=[C1H, C1B, C2H, C2B]: 4 elements array
            Capacitor values in Farad
        """
        self.C = C
        self.RL1.set_capacitors([self.C[0], self.C[1]])
        self.RL2.set_capacitors([self.C[2], self.C[3]])
        
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
        temp = rf.innerconnect(rf.connect(self.plasma, 0, self.RL1.network, 1), 1, 4) # watch out ! plasma ports 0 & 2 to RDL (TOPICA indexing)
        network = rf.innerconnect(rf.connect(temp, 0, self.RL2.network, 1), 0, 3)
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
            C0 = 12e-12 + scipy.random.rand(4)*(120e-12 - 12e-12)
            sol = scipy.optimize.root(self._match_function, C0, args=(a_in, f_match, Z_match))
            success = sol.success
            
            print(success, sol.x/1e-12)
                
            for idm,Cm in enumerate(sol.x):
                if (Cm < 12e-12) or (Cm > 200e-12):
                    success = False
                    print('Bad solution found (out of range capacitor) ! Re-doing...')
    
        print(sol.x/1e-12)
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
        self.set_capacitors(C)
        
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

        self.RL1.network.z #
    
    def get_voltages(self, a_in):
        """
        Returns the voltage at the capacitors for a prescribed excitation.
        """
        pass        