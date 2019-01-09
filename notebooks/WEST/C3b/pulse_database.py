import h5py
import numpy as np
import pywed as pw
from control_room import get_sig, signals, is_sig
from IRFMtb import tsdernier_choc

class PulseDB():
    def __init__(self, hdf5_filename):
        self.hdf5_filename = hdf5_filename   
        
    @property
    def pulse_list(self):
        """
        Return the list of pulses as a list
        """
        with h5py.File(self.hdf5_filename, 'a') as f:
            return list(f.attrs['pulse_list'])

    @pulse_list.setter
    def pulse_list(self, pl):
        with h5py.File(self.hdf5_filename, 'a') as f:
            f.attrs.create('pulse_list', pl)
            
    def update_pulse_list(self, ref_sig=signals['IC_P_tot'], thres=100):
        """
        Update the database by adding new pulses if any
        """
        # if pulse_list already exist
        try:
            pulse_list = self.pulse_list
        except KeyError as e:
            pulse_list = []
        
        if pulse_list:  # if not empty
            pulse_start = pulse_list[-1]
        else:
            pulse_start = 53550  # first plasma with IC for W3b (tbc)

        pulse_end = tsdernier_choc()
        pulses = range(pulse_start, pulse_end+1)
        print(f'Going from {pulse_start} to {pulse_end}')

        # then append from the latest pulse
        for pulse in pulses:
            # keep only pulses where threshold is fit
            res = is_sig(pulse, ref_sig, thres)
            if res:
                pulse_list.append(pulse)

        # update the db
        self.pulse_list = pulse_list
            

    def delete_signals(self, signal_names, pulses=None):
        """
        Delete signals (ie a hdf5 group containing both (y,t) dataset)
        for the given pulses. If no pulse list given, all pulses considered

        Arguments
        ---------
        - signal_names : list of string
        - pulses: list of int (default: None)
        """
        if type(signal_names) is not list:
            raise ValueError(f'signal_names must be a list')
        
        with h5py.File(self.hdf5_filename, 'a') as f:
            if not pulses:
                pulses = self.pulse_list

            for pulse in pulses:
                for signal_name in signal_names:
                    sig_path = f'{pulse}/{signal_name}'
                    if sig_path in f:
                        del f[sig_path]
                    else:
                        print(f'nothing to supress on {sig_path}')

    def add_signals(self, pulse, signal_names, force_rewrite=False):
        """
        Add signal data into the database
        f : hdf5 file
        pulse : int
        signal_names : list of string
        """
        with h5py.File(self.hdf5_filename, 'a') as f:
            for sig_name in signal_names:
                # do not rewrite if allready exist
                sig_path = f'{pulse}/{sig_name}'
                if (sig_path not in f) or force_rewrite:
                    y, t = get_sig(pulse, signals[sig_name])
                    print(f'Getting {sig_name} for #{pulse}')

                    if sig_path+"/y" in f:
                        f[sig_path+"/y"][...] = y
                    else:
                        f[sig_path+"/y"] = y

                    if sig_path+"/t" in f:
                        f[sig_path+"/t"][...] = t
                    else:
                        f[sig_path+"/t"] = t

                else:
                    print(f'{sig_name} already exist in database for #{pulse}: passing...')

    def add_attr(self, pulse, signal_name, attr_name, attr_value, force_rewrite=False):
        """
        Write an HDF5 attribute to a signal group
        """
        with h5py.File(self.hdf5_filename, 'a') as f:
            sig_path = f'{pulse}/{signal_name}'
            if sig_path in f:
                f[sig_path].attrs.create(attr_name, attr_value)
            else:
                raise KeyError(f'{sig_path} does not exist')

    def get_attr(self, pulse, signal_name, attr_name):
        with h5py.File(self.hdf5_filename, 'a') as f:
            sig_path = f'{pulse}/{signal_name}'
            if sig_path in f:
                return f[sig_path].attrs[attr_name]
            else:
                raise KeyError(f'{sig_path} does not exist')

    def get_signal(self, pulse, signal_name):
        """
        Return the (y,t) of signal for a given pulse
        """
        with h5py.File(self.hdf5_filename, 'a') as f:
            sig_path = f'{pulse}/{signal_name}'
            if sig_path in f:
                return f[sig_path+'/y'][:], f[sig_path+'/t'][:]
            else:
                raise KeyError(f'signal {sig_path} does not exist')
                
    def list_signal(self, pulse):
        """
        List all the signals available for a pulse
        """
        with h5py.File(self.hdf5_filename, 'a') as f:
            if str(pulse) in f:
                return list(f[f'{pulse}'].keys())
            else:
                raise KeyError(f'Pulse {pulse} does not exist')