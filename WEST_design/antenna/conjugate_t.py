# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:26:00 2015

@author: J.Hillairet
"""

import skrf as rf
import numpy as np
import scipy.optimize

class ConjugateT(object):
    """
    ConjugateT class.
    
    This class describes a conjugate-T with 2 matching capacitors. 
    Its consist of:
     - two capacitors (defined by their capacitance values)
     and eventually:     
     - one bridge (an ideal T-junction if not provided)
     - one impedance transformer (an ideal piece of transmission line if not provided)
     - one window (an ideal piece of transmission line if not provided)
    
    
    """

    def __init__(self, bridge, imp_tr=None, window=None, C=[60e-12, 60e-12], 
                 capacitor_model='equivalent', name='CT'):
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
        capacitor_model: string {'ideal', 'equivalent'} (defaut:'equivalent')   
            Capacitor electrical model. Ideal means just a capacitance, 
            equivalent means a capacitor equivalent circuit.
        name: string (default:'CT')
            Name of the network created 
                        
        """
        assert len(C) == 2, 'C=[CH, CB] should be of length 2.'
                
        if isinstance(window, rf.Network) and isinstance(imp_tr, rf.Network):
            # creates the circuit=window + impedance transformer + bridge
            # impedance_transformer : port0 40 Ohm ; port1 5 Ohm 
            # window                : port0 30 ohm ; port1 40 Ohm 
            #    1-imp_tr-0 -- 1-window-0 ==> 1:5 Ohm -- 0:30 Ohm
            window_imptrans = rf.connect(window, 1, imp_tr, 0)

            # bridge port0: input
            window_imptrans_bridge = rf.connect(window_imptrans, 1, bridge, 0)         
        else:
            # no impedance_transformer nor window
            window_imptrans_bridge = bridge
               
        self.circuit = window_imptrans_bridge
        
        # set various properties
        self.capacitor_model = capacitor_model
        self.frequency = window_imptrans_bridge.frequency
        self.z0 = window_imptrans_bridge.z0[0][:]        
        self.C = C 
        
        # create the network (=circuit+capacitors)
        #self = self.get_network() 
        self.name = name
        

    def __repr__(self):
        return 'Conjugate-T network with CH={} pF and CB={} pF. Network: {}'\
                .format(self._C[0]*1e12, self._C[1]*1e12, self.circuit)

    @property
    def C(self):
        return self._C
    
    @C.setter
    def C(self, C):
        """
        Set the two capacitors values.
        
        Arguments
        ---------
        C=[CH,CB] in F
        
        """
        assert len(C) == 2, 'C=[CH, CB] should be of length 2.'
        
        self._C = C        
        
        # update the network
        self.network = self.get_network() 
        
        
    def get_network(self):
        """
        Creates a two-ports (skrf) Network of conugate-T with its capacitors.
        
        The returned Network is thus a 3-ports Network, where port#0 is 
        the input port and port#1 and #2 are the load ports.
        
        Returns
        --------
         - skrf.Network
         
        """
        capa_H = self._capacitor_network(self.C[0], z0=self.z0[1])
        capa_B = self._capacitor_network(self.C[1], z0=self.z0[2])
        # return the skrf Network object
        # 1-CH-0 ** 1 - 0
        # 1-CB-0 ** 2 |
        return(rf.connect(rf.connect(self.circuit,1, capa_H,0),2, capa_B,0))
    
    def load(self, Z_plasma):
        """
        Load a the conjugate-T with a plasma impedance(s) and return 
        the loaded conjugate-T as a 1-port network.
        
        The plasma a complex impedance can be either one or two scalars 
        (ie no poloidal coupling) or a 2x2 array.
        
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
            Z_plasma = np.full(2, Z_plasma)
        
        if np.shape(Z_plasma) == (2,):  
            # convert Z into S with the bridge characteristic impedance
            #S_plasma_H = rf.z2s(Z_plasma[0]*np.ones((len(freq),1,1)), z0=z0_RDL_H)
            #S_plasma_B = rf.z2s(Z_plasma[1]*np.ones((len(freq),1,1)), z0=z0_RDL_B)
                
            #load_H = rf.Network(frequency=freq, s=S_plasma_H, z0=z0_RDL_H)
            #load_B = rf.Network(frequency=freq, s=S_plasma_B, z0=z0_RDL_B)

            load_H = rf.Network.from_z(np.full((len(freq),1,1), Z_plasma[0]), 
                                       z0=z0_RDL_H, frequency=freq)
            load_B = rf.Network.from_z(np.full((len(freq),1,1), Z_plasma[1]), 
                                       z0=z0_RDL_B, frequency=freq)
            
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
        
        Parameters
        ----------
        C : float
            capacitance [F]
        
        z0 : float 
            line characteric impedance [Ohm]
            
        Returns
        -------
        capacitor : :class: 'skrf.network'
            Resulting network (2 ports)
        
        """
        # # Previous version. Network was built from Z -> S 
        # if self.capacitor_model is 'ideal':
        #     Z_capacitor = 1./(1j*C*2*np.pi*self.frequency.f)
        # elif self.capacitor_model is 'equivalent':
        #     Z_C_serie = 1./(1j*C*2*np.pi*self.frequency.f)
        #     Z_R_serie = 0.01 # Ohm
        #     Z_L_serie = 1j*(24e-9)*2*np.pi*self.frequency.f # 24 nH serie inductance
        #     Z_R_parallel = 20e6 # Ohm
        #     Z_serie = Z_C_serie + Z_R_serie + Z_L_serie  
        #     Z_capacitor = (Z_serie * Z_R_parallel)/(Z_serie + Z_R_parallel)
        
        # # 2-port series capacity
        # S_capacitor = np.array([[Z_capacitor, np.tile(2*z0, Z_capacitor.shape)],
        #                         [np.tile(2*z0, Z_capacitor.shape), Z_capacitor]]).T \
        #               / ((Z_capacitor + 2*z0)*np.ones((2,2,len(Z_capacitor)))).T 
        
        # capacitor = rf.Network(frequency=self.frequency, s=S_capacitor, z0=z0)
        # return(capacitor)
        
        line = rf.media.DefinedGammaZ0(frequency=self.frequency, z0=z0)
        if self.capacitor_model is 'ideal':
            capacitor = line.capacitor(C)
            
        elif self.capacitor_model is 'equivalent':
            R_serie = 0.01 # Ohm
            L_serie = 24e-9 # H
            capacitor = line.resistor(R_serie) ** line.inductor(L_serie) ** line.capacitor(C)
            
        elif self.capacitor_model is 'advanced':
            R=1e-2  # Ohm
            L=29.9  # nH
            R1=1e-2  # Ohm
            C1=25.7  # pF
            L1=2.4  # nH
                    
            pre = line.resistor(R1) ** line.inductor(L1*1e-9) ** line.shunt_capacitor(C1*1e-12)
            post= line.shunt_capacitor(C1*1e-12) ** line.resistor(R1) ** line.inductor(L1*1e-9)
            cap = line.resistor(R) ** line.inductor(L*1e-9) ** line.capacitor(C)
        
            capacitor = pre ** cap ** post 

        return(capacitor)
        
    def match(self, f_match=50e6, z_load=1.0+30*1j, z_match=30+0*1j):
        """
        Match the resonant loop for a prescribed load impedance at a specified frequency
        
        Parameters
        ----------
        f_match: (default: 50 MHz)
            matching frequency in Hz
        z_load: scalar, 2-element array or 2x2 array (default: 1+30j)
            complex impedance for both bridge outputs
        z_match: scalar, matching impedance (default: 30 ohm)
        
        Returns
        ----------
        sol: :class: 'scipy.optimize.solution'
        """
        success = False
        while success == False:
            # generate a random capacitor sets, centered on 70pF +/-40pF
            # values expressed in pF
            C0_pF = 70 + (-1 + 2*scipy.random.rand(2))*40
            # use root if _optim_fun returns a vector, but then not bounds
            sol = scipy.optimize.root(self._optim_fun_single_RL, C0_pF, 
                                      args=(f_match, z_load, z_match)) 
            # sol = scipy.optimize.minimize(self._optim_fun_single_RL, C0_pF, 
            #                           args=(f_match, z_load, z_match),
            #                           bounds=((12,200),(12,200))) 
            success = sol.success
            print(success, sol.x)
                
            for idm,Cm in enumerate(sol.x):
                if (Cm < 12) or (Cm > 200):
                    success = False
                    print('Bad solution found (out of range capacitor) ! Re-doing...')

        self.C = sol.x*1e-12            
        return(sol)

    def _optim_fun_single_RL(self, C_pF, f_match, z_load, z_match):
        """
        Return the match conditions at the
        C=[C1,C2] in pF
        RL : ResonantLoop class
        f_match
        z_load 
        
        """
        self.C = C_pF * 1e-12
        
        loaded_RL = self.load(z_load)
        
        index_f_match = np.argmin(np.abs(loaded_RL.frequency.f - f_match))
        
        Z11_re = loaded_RL.z_re[index_f_match].squeeze() # 100 = ~ 50 MHz (mid-band bins point)
        Z11_im = loaded_RL.z_im[index_f_match].squeeze()
        # residuals
        y = [Z11_re - np.real(z_match),  # vector return, for root
              Z11_im - np.imag(z_match)]
        # y = (Z11_re - np.real(z_match))**2 + (Z11_im - np.imag(z_match))**2
        return(y)    
        

    def _plasma_power_waves(self, Z_plasma, a_in):
        '''
        Returns the power wave a, b at the capacitors (plasma side).
        
        Arguments
        ---------
         - a_in: power wave input of CT
         - Z_plasma: complex impedance of the plasma [2x1]
        
        Return
        --------
         - a_plasma: power wave from CT to plasma
         - b_plasma: power wave from plasma to CT
         
        '''
        # get unloaded network with the current set of capacitors        
        CT = self.get_network()
        
        S_plasma_H = rf.z2s(Z_plasma[0]*np.ones((len(CT.f),1,1)), z0=self.z0[1])
        S_plasma_B = rf.z2s(Z_plasma[1]*np.ones((len(CT.f),1,1)), z0=self.z0[2])
                 
        a_plasma = []
        b_plasma = []                 
        for idf,f in enumerate(self.frequency.f):
            S_CT = CT.s[idf]

            S_plasma = np.eye(2)*[np.squeeze(S_plasma_H[idf]), np.squeeze(S_plasma_B[idf])]

            _a = np.linalg.inv(np.eye(2) - S_CT[1:,1:].dot(S_plasma)).dot(S_CT[1:,0])*a_in
            _b = S_plasma.dot(_a)
        
            a_plasma.append(_a)
            b_plasma.append(_b)

        a_plasma = np.column_stack(a_plasma)
        b_plasma = np.column_stack(b_plasma)
        
        return a_plasma, b_plasma            
            
            
 
    def get_capacitor_currents_voltages(self, Z_plasma, Pin):
        '''
        Return the currents and voltages at the capacitors (plasma side).

        Arguments
        ---------
         - Pin: input power in the CT [W]
         - Z_plasma: complex impedance of the plasma [2x1]

        Return
        --------
         - I_capa : current in A
         - V_capa : voltage in V
         
        '''
        # Wath out the factor 2 in the power wave definition 
        # This is expected from the power wave definition
        #  as the power is defined by P = 1/2 V.I --> P = 1/2 a^2 
        a_in = np.sqrt(2*Pin)

        a, b = self._plasma_power_waves(Z_plasma, a_in)
        z0 = self.get_network().z0[:,1:]
        I_capa = (a-b).T/np.sqrt(np.real(z0))
        V_capa = (np.conjugate(z0)*a.T + z0*b.T)/np.sqrt(np.real(z0))               

        return I_capa, V_capa