# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 21:00:22 2013

@author: hash
"""
import numpy as np
import skrf as rf


class TopicaResult:

    def __init__(self, filename, z0=50):
        """
        TOPICA result constructor.
        
        Parameters
        ----------
        filename (str): 
            filename of the ascii file
        [z0 (float)]: 
            characteristic impedance of the port in Ohm (default: 50)

        """
        self.filename = filename
        self.z = self.get_z()
        self.nbPorts = len(self.z)
        self.z0 = z0
        self.s = self.get_s()

    def set_z0(self, z0):
        """ 
        Set the characteristic impedance of the ports in Ohm.

        Parameters
        ----------        
        z0 : :class:`numpy.ndarray` of length n
                characteristic impedance for network
                
        """
        self.z0 = z0
	
    def get_z(self):
        """ 
        Get the impedance matrix as an NxN array, N being the number of ports.
        
        Returns
        ----------        
        z : :class:`numpy.ndarray` 
                impedance matrix
                
        """        
        data = np.loadtxt(self.filename, skiprows=3)
        z = np.zeros((np.sqrt(np.size(data, 0)), np.sqrt(np.size(data, 0))), dtype='complex')
        for id1 in range(np.size(data, 0)):
            z[data[id1, 0]-1, data[id1, 1]-1] = complex(data[id1, 2], data[id1, 3])
        return(z)
    
    def get_s(self):
        """ 
        Get the scattering parameters as an NxN array, N being the number of ports.
        
        Returns
        ---------
        s : :class:`numpy.ndarray` of shape n x n
                scattering parameters of the TOPICA result
                
        """
        Zref = np.diag(np.repeat(self.z0, self.nbPorts))

        G = 1/np.sqrt(np.real(self.z0)) 
        Gref = np.diag(np.repeat(G, self.nbPorts))
        # Z to S formulae
        S = Gref.dot(self.z - Zref).dot(np.linalg.inv(self.z + Zref)).dot(np.linalg.inv(Gref))

        return(S)

    def to_skrf_network(self, skrf_frequency, name='plasma'):
        """ 
        Convert into a skrf Network.
        
        Assume the scattering parameters of the network are the same 
        for all the frequencies of the network. 
        
        Parameters
        ----------
        skrf_frequency : :class: 'skrf.frequency' 
            Frequency of the network (for compatibility with skrf)
        name : string
            name of the network
        
        Returns
        ----------
        network : :class: 'skrf.network' 
        
        """
        network = rf.Network(name=name)
        network.s = np.tile(self.s, (len(skrf_frequency), 1, 1))
        network.z0 = self.z0
        network.frequency = skrf_frequency
        return(network)

    def write_touchstone(self, filename, skrf_frequency, name=''):
        """
        Write the scattering parameters into a Touchstone file format
        (.sNp where N is the number of ports).

        Parameters
        ----------
        filename : string
            Touchstone filename
        skrf_frequency : :class: ' skrf.frequency' 
            skrf Frequency object
        name : string: 
            name of the network
        """
        network = self.to_skrf_network(skrf_frequency, name=name)
        network.write_touchstone(filename=filename, write_z0=True)
        
    def get_Rc(self, I=[1, -1, -1, 1], freq=None):
        """
        Calculate the coupling resistance of the TOPICA Z-matrix for 
        a given current excitation.
        
        Coupling resistance is defined as in :
        W. Helou, L. Colas, J. Hillairet et al., Fusion Eng. Des. 96–97 (2015) 5–8. doi:10.1016/j.fusengdes.2015.01.005.
        
        Parameters
        ----------
        I : list
            Current excitation at port. Default is [1, -1, -1, 1], ie. dipole phasing of 2x2 straps antenna
        freq : list. Default is None
            List of frequencies to calculate the Rc. Default is all frequencies    
        
        Returns
        -------
        Rc : float
            Coupling Resistance
        """
        N = length(I) # number of ports
        V = self.z @ I
        Pt = np.real(V.conj() @ I) / 2
        Is = np.sqrt(np.sum(np.abs(I)) / N)
        Rc = Pt / (2*Is**2)
        return Rc
        
