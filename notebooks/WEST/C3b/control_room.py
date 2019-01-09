from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import pywed as pw
import pandas as pd

signals = {
    ## Shot properties
    'Datetime': {'name': None, 'fun': 'pulse_datetime', 'unit':'', 'label':'pulse datetime'},
    ## Magnetics
    'Ip': {'name': 'SMAG_IP', 'unit': 'kA', 'label': 'Plasma current'},
    'Vloop': {'name': 'GMAG_VLOOP%1', 'unit': 'V', 'label': 'Loop voltage'},
    'Rext_upper': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext upper'},  # Rext upper
    'Rext_median': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext median'},  # Rext median
    'Rext_lower': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext lower'},  # Rext lower
    'Zgeo': {'name': 'GMAG_BARY%2', 'unit': 'm', 'label': 'Zgeo'},  # Zgeo barycentre
    'R0': {'name': 'GMAG_BARY%1', 'unit': 'm', 'label': 'Large radius'},  # grand rayon
    # Movable limiter position (LPA)
    'LPA': {'name': 'GMAG_POSLPA%1', 'unit': 'm', 'label': 'LPA'},
    ## Fueling
    'nl': {'name': 'GINTLIDRT%3', 'unit': '$m^{-2}$', 'label': 'Line integrated density'},
    'Valve7': {'name': 'GDEBIT%7', 'unit': '$Pa.m^3/s$', 'label': 'Valve#7 (LPA)'},
    'Valve9': {'name': 'GDEBIT%9', 'unit': '$Pa.m^3/s$', 'label': 'Valve#9 (Q1)'},
    'Valve10': {'name': 'GDEBIT%10', 'unit': '$Pa.m^3/s$', 'label': 'Valve#10 (Q2)'},
    'Valve11': {'name': 'GDEBIT%11', 'unit': '$Pa.m^3/s$', 'label': 'Valve#11 (up.divertor)'},
    'Valve21': {'name': 'GDEBIT%21', 'unit': '$Pa.m^3/s$', 'label': 'Valve#21'},
    ## ICRH
    # IC coupled powers
    'IC_P_tot': {'name': 'SICHPTOT', 'unit': 'kW', 'label': 'IC total coupled power'},
    'IC_P_Q1': {'name': 'SICHPQ1', 'unit': 'kW', 'label': 'IC Q1 coupled power'},
    'IC_P_Q2': {'name': 'SICHPQ2', 'unit': 'kW', 'label': 'IC Q2 coupled power'},
    'IC_P_Q4': {'name': 'SICHPQ4', 'unit': 'kW', 'label': 'IC Q4 coupled power'},
    'IC_P_PCS_Q1': {'name': 'GICHCONSPCS%1', 'unit': 'kW', 'label': 'Power waveform request Q1'},
    'IC_P_PCS_Q2': {'name': 'GICHCONSPCS%2', 'unit': 'kW', 'label': 'Power waveform request Q2'},
    'IC_P_PCS_Q4': {'name': 'GICHCONSPCS%3', 'unit': 'kW', 'label': 'Power waveform request Q4'},
    'IC_PCS_auth_Q1': {'name': 'GICHCONSPCS%7', 'unit': '', 'label': 'PCS interdiction Q1'},
    'IC_PCS_auth_Q2': {'name': 'GICHCONSPCS%8', 'unit': '', 'label': 'PCS interdiction Q2'},
    'IC_PCS_auth_Q4': {'name': 'GICHCONSPCS%9', 'unit': '', 'label': 'PCS interdiction Q4'},
    # IC antenna positions (use tsmat)
    'IC_Positions': {'name': None, 'fun': 'IC_Positions', 'unit': 'm', 'label': 'IC Antenna positions'},
    'LH_Positions': {'name': None, 'fun': 'LH_Positions', 'unit': 'm', 'label': 'LH Antenna positions'},
    # IC antenna frequencies (use tsmat)
    'IC_Frequencies': {'name': None, 'fun': 'IC_Frequencies', 'unit': 'MHz', 'label': 'IC Antenna Frequencies'},
    # IC antennas left and right forward and reflected powers
    'IC_P_Q1_left_fwd': {'name': 'GICHANTPOWQ1%1', 'unit': 'kW', 'label': 'Left Fwd Power Q1'},
    'IC_P_Q1_left_ref': {'name': 'GICHANTPOWQ1%2', 'unit': 'kW', 'label': 'Left Ref Power Q1'},
    'IC_P_Q1_right_fwd': {'name': 'GICHANTPOWQ1%3',  'unit': 'kW', 'label': 'Right Fwd Power Q1'},
    'IC_P_Q1_right_ref': {'name': 'GICHANTPOWQ1%4', 'unit': 'kW', 'label': 'Right Ref Power Q1'},
    'IC_P_Q2_left_fwd': {'name': 'GICHANTPOWQ2%1', 'unit': 'kW', 'label': 'Left Fwd Power Q2'},
    'IC_P_Q2_left_ref': {'name': 'GICHANTPOWQ2%2', 'unit': 'kW', 'label': 'Left Ref Power Q2'},
    'IC_P_Q2_right_fwd': {'name': 'GICHANTPOWQ2%3', 'unit': 'kW', 'label': 'Right Fwd Power Q2'},
    'IC_P_Q2_right_ref': {'name': 'GICHANTPOWQ2%4', 'unit': 'kW', 'label': 'Right Ref Power Q2'},
    # IC Antennas coupling resistances
    'IC_Rc_Q1_left': {'name': 'GICHCOUPRES%1', 'unit': 'Ohm', 'label': 'Rc - Q1 Left'},
    'IC_Rc_Q1_right': {'name': 'GICHCOUPRES%2', 'unit': 'Ohm', 'label': 'Rc - Q1 Right'},
    'IC_Rc_Q2_left': {'name': 'GICHCOUPRES%3', 'unit': 'Ohm', 'label': 'Rc - Q2 Left'},
    'IC_Rc_Q2_right': {'name': 'GICHCOUPRES%4', 'unit': 'Ohm', 'label': 'Rc - Q2 Right'},
    'IC_Rc_Q4_left': {'name': 'GICHCOUPRES%5', 'unit': 'Ohm', 'label': 'Rc - Q4 Left'},
    'IC_Rc_Q4_right': {'name': 'GICHCOUPRES%6', 'unit': 'Ohm', 'label': 'Rc - Q4 Right'},
    'IC_Rc_Q1_avg': {'name': None, 'fun': 'IC_Rc_Q1_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q1'},
    'IC_Rc_Q2_avg': {'name': None, 'fun': 'IC_Rc_Q2_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q2'},
    'IC_Rc_avg': {'name': None, 'fun': 'IC_Rc_avg', 'unit': 'Ohm', 'label': 'Avg. IC Rc'},
    # IC antennas phase Q1
    'IC_Phase_Q1 (Pf_Left - Pf_Right)': {'name': 'GICHPHASESQ1%1', 'unit': 'deg', 'label': 'Phase (Pf left - Pf right) antenna Q1'},
    'IC_Phase_Q1 (Pr_Left - Pf_Right)': {'name': 'GICHPHASESQ1%2', 'unit': 'deg', 'label': 'Phase (Pr left - Pf right) antenna Q1'},
    'IC_Phase_Q1 (Pr_Right - Pf_Right)': {'name': 'GICHPHASESQ1%3', 'unit': 'deg', 'label': 'Phase (Pr right - Pf right) antenna Q1'},
    'IC_Phase_Q1 (V1 - Pf_Left)': {'name': 'GICHPHASESQ1%4', 'unit': 'deg', 'label': 'Phase (V1 - Pf left) antenna Q1'},
    'IC_Phase_Q1 (V2 - Pf_Left)': {'name': 'GICHPHASESQ1%5', 'unit': 'deg', 'label': 'Phase (V2 - Pf left) antenna Q1'},
    'IC_Phase_Q1 (V3 - Pf_Right)': {'name': 'GICHPHASESQ1%6', 'unit': 'deg', 'label': 'Phase (V3 - Pf right) antenna Q1'},
    'IC_Phase_Q1 (V4 - Pf_Right)': {'name': 'GICHPHASESQ1%7', 'unit': 'deg', 'label': 'Phase (V4 - Pf right) antenna Q1'},
    # IC antennas phase Q2
    'IC_Phase_Q2 (Pf_Left - Pf_Right)': {'name': 'GICHPHASESQ2%1', 'unit': 'deg', 'label': 'Phase (Pf left - Pf right) antenna Q2'},
    'IC_Phase_Q2 (Pr_Left - Pf_Right)': {'name': 'GICHPHASESQ2%2', 'unit': 'deg', 'label': 'Phase (Pr left - Pf right) antenna Q2'},
    'IC_Phase_Q2 (Pr_Right - Pf_Right)': {'name': 'GICHPHASESQ2%3', 'unit': 'deg', 'label': 'Phase (Pr right - Pf right) antenna Q2'},
    'IC_Phase_Q2 (V1 - Pf_Left)': {'name': 'GICHPHASESQ2%4', 'unit': 'deg', 'label': 'Phase (V1 - Pf left) antenna Q2'},
    'IC_Phase_Q2 (V2 - Pf_Left)': {'name': 'GICHPHASESQ2%5', 'unit': 'deg', 'label': 'Phase (V2 - Pf left) antenna Q2'},
    'IC_Phase_Q2 (V3 - Pf_Right)': {'name': 'GICHPHASESQ2%6', 'unit': 'deg', 'label': 'Phase (V3 - Pf right) antenna Q2'},
    'IC_Phase_Q2 (V4 - Pf_Right)': {'name': 'GICHPHASESQ2%7', 'unit': 'deg', 'label': 'Phase (V4 - Pf right) antenna Q2'},
    # IC antennas phase Q4
    'IC_Phase_Q4 (Pf_Left - Pf_Right)': {'name': 'GICHPHASESQ4%1', 'unit': 'deg', 'label': 'Phase (Pf left - Pf right) antenna Q4'},
    'IC_Phase_Q4 (Pr_Left - Pf_Right)': {'name': 'GICHPHASESQ4%2', 'unit': 'deg', 'label': 'Phase (Pr left - Pf right) antenna Q4'},
    'IC_Phase_Q4 (Pr_Right - Pf_Right)': {'name': 'GICHPHASESQ4%3', 'unit': 'deg', 'label': 'Phase (Pr right - Pf right) antenna Q4'},
    'IC_Phase_Q4 (V1 - Pf_Left)': {'name': 'GICHPHASESQ4%4', 'unit': 'deg', 'label': 'Phase (V1 - Pf left) antenna Q4'},
    'IC_Phase_Q4 (V2 - Pf_Left)': {'name': 'GICHPHASESQ4%5', 'unit': 'deg', 'label': 'Phase (V2 - Pf left) antenna Q4'},
    'IC_Phase_Q4 (V3 - Pf_Right)': {'name': 'GICHPHASESQ4%6', 'unit': 'deg', 'label': 'Phase (V3 - Pf right) antenna Q4'},
    'IC_Phase_Q4 (V4 - Pf_Right)': {'name': 'GICHPHASESQ4%7', 'unit': 'deg', 'label': 'Phase (V4 - Pf right) antenna Q4'},
    # IC Antennas internal vacuum (y = 10**(1.5*y - 10))
    'IC_Vacuum_Q1_left': {'name': None, 'fun': 'IC_Q1_vacuum_left', 'unit': 'Pa', 'label': 'Vaccum Q1 left'},
    'IC_Vacuum_Q1_right': {'name': None, 'fun': 'IC_Q1_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q1 right'},
    'IC_Vacuum_Q2_left': {'name': None, 'fun': 'IC_Q2_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q2 left'},
    'IC_Vacuum_Q2_right': {'name': None, 'fun': 'IC_Q2_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q2 right'},
    'IC_Vacuum_Q4_left': {'name': None, 'fun': 'IC_Q4_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q4 left'},
    'IC_Vacuum_Q4_right': {'name': None, 'fun': 'IC_Q4_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q4 right'},
    # PCS power request
    'IC_PCS_P_Q1': {'name': 'GICHCONSPCS%1', 'unit': 'kW', 'label': 'PCS Power request Q1'},
    'IC_PCS_P_Q2': {'name': 'GICHCONSPCS%2', 'unit': 'kW', 'label': 'PCS Power request Q2'},
    'IC_PCS_P_Q3': {'name': 'GICHCONSPCS%3', 'unit': 'kW', 'label': 'PCS Power request Q4'},
    # IC antennas Capacitor values
    'IC_Capa_Q1_left_upper': {'name': 'GICHCAPA%1', 'unit': 'pF', 'label': 'Capa.Q1 L-U'},
    'IC_Capa_Q1_left_lower': {'name': 'GICHCAPA%2', 'unit': 'pF', 'label': 'Capa.Q1 L-L'},
    'IC_Capa_Q1_right_upper': {'name': 'GICHCAPA%3', 'unit': 'pF', 'label': 'Capa.Q1 R-U'},
    'IC_Capa_Q1_right_lower': {'name': 'GICHCAPA%4', 'unit': 'pF', 'label': 'Capa.Q1 R-L'},
    'IC_Capa_Q2_left_upper': {'name': 'GICHCAPA%5', 'unit': 'pF', 'label': 'Capa.Q2 L-U'},
    'IC_Capa_Q2_left_lower': {'name': 'GICHCAPA%6', 'unit': 'pF', 'label': 'Capa.Q2 L-L'},
    'IC_Capa_Q2_right_upper': {'name': 'GICHCAPA%7', 'unit': 'pF', 'label': 'Capa.Q2 R-U'},
    'IC_Capa_Q2_right_lower': {'name': 'GICHCAPA%8', 'unit': 'pF', 'label': 'Capa.Q2 R-L'},
    # IC antennas Capacitor error signals
    'IC_ErrSig_Q1_left_upper': {'name': 'GICHSIGERR%1', 'unit': '', 'label': 'Err.Sig.Q1 L-U'},
    'IC_ErrSig_Q1_left_lower': {'name': 'GICHSIGERR%2', 'unit': '', 'label': 'Err.Sig.Q1 L-L'},
    'IC_ErrSig_Q1_right_upper': {'name': 'GICHSIGERR%3', 'unit': '', 'label': 'Err.Sig.Q1 R-U'},
    'IC_ErrSig_Q1_right_lower': {'name': 'GICHSIGERR%4', 'unit': '', 'label': 'Err.Sig.Q1 R-L'},
    'IC_ErrSig_Q2_left_upper': {'name': 'GICHSIGERR%5', 'unit': '', 'label': 'Err.Sig.Q2 L-U'},
    'IC_ErrSig_Q2_left_lower': {'name': 'GICHSIGERR%6', 'unit': '', 'label': 'Err.Sig.Q2 L-L'},
    'IC_ErrSig_Q2_right_upper': {'name': 'GICHSIGERR%7', 'unit': '', 'label': 'Err.Sig.Q2 R-U'},
    'IC_ErrSig_Q2_right_lower': {'name': 'GICHSIGERR%8', 'unit': '', 'label': 'Err.Sig.Q2 R-L'},
    # IC antennas Capacitor Voltages
    'IC_Voltage_left_upper_Q1': {'name': 'GICHVPROBEQ1%1', 'unit': 'kV', 'label': 'Left upper capacitor voltage Q1'},
    'IC_Voltage_left_lower_Q1': {'name': 'GICHVPROBEQ1%2', 'unit': 'kV', 'label': 'Left lower capacitor voltage Q1'},
    'IC_Voltage_right_upper_Q1': {'name': 'GICHVPROBEQ1%3', 'unit': 'kV', 'label': 'Right upper capacitor voltage Q1'},
    'IC_Voltage_right_lower_Q1': {'name': 'GICHVPROBEQ1%4', 'unit': 'kV', 'label': 'Right lower capacitor voltage Q1'}, 
    'IC_Voltage_left_upper_Q2': {'name': 'GICHVPROBEQ2%1', 'unit': 'kV', 'label': 'Left upper capacitor voltage Q2'},
    'IC_Voltage_left_lower_Q2': {'name': 'GICHVPROBEQ2%2', 'unit': 'kV', 'label': 'Left lower capacitor voltage Q2'},
    'IC_Voltage_right_upper_Q2': {'name': 'GICHVPROBEQ2%3', 'unit': 'kV', 'label': 'Right upper capacitor voltage Q2'},
    'IC_Voltage_right_lower_Q2': {'name': 'GICHVPROBEQ2%4', 'unit': 'kV', 'label': 'Right lower capacitor voltage Q2'},
    'IC_Voltage_left_upper_Q4': {'name': 'GICHVPROBEQ4%1', 'unit': 'kV', 'label': 'Left upper capacitor voltage Q4'},
    'IC_Voltage_left_lower_Q4': {'name': 'GICHVPROBEQ4%2', 'unit': 'kV', 'label': 'Left lower capacitor voltage Q4'},
    'IC_Voltage_right_upper_Q4': {'name': 'GICHVPROBEQ4%3', 'unit': 'kV', 'label': 'Right upper capacitor voltage Q4'},
    'IC_Voltage_right_lower_Q4': {'name': 'GICHVPROBEQ4%4', 'unit': 'kV', 'label': 'Right lower capacitor voltage Q4'},     
    # IC antennas Capacitor Currents
    'IC_Current_left_upper_Q1': {'name': 'GICHICAPA%1', 'unit': 'A', 'label': 'Left upper capacitor current Q1'},
    'IC_Current_left_lower_Q1': {'name': 'GICHICAPA%2', 'unit': 'A', 'label': 'Left lower capacitor current Q1'},
    'IC_Current_right_upper_Q1': {'name': 'GICHICAPA%3', 'unit': 'A', 'label': 'Right upper capacitor current Q1'},
    'IC_Current_right_lower_Q1': {'name': 'GICHICAPA%4', 'unit': 'A', 'label': 'Right lower capacitor current Q1'},
    'IC_Current_left_upper_Q2': {'name': 'GICHICAPA%5', 'unit': 'A', 'label': 'Left upper capacitor current Q2'},
    'IC_Current_left_lower_Q2': {'name': 'GICHICAPA%6', 'unit': 'A', 'label': 'Left lower capacitor current Q2'},
    'IC_Current_right_upper_Q2': {'name': 'GICHICAPA%7', 'unit': 'A', 'label': 'Right upper capacitor current Q2'},
    'IC_Current_right_lower_Q2': {'name': 'GICHICAPA%8', 'unit': 'A', 'label': 'Right lower capacitor current Q2'},   
    'IC_Current_left_upper_Q4': {'name': 'GICHICAPA%9', 'unit': 'A', 'label': 'Left upper capacitor current Q4'},
    'IC_Current_left_lower_Q4': {'name': 'GICHICAPA%10', 'unit': 'A', 'label': 'Left lower capacitor current Q4'},
    'IC_Current_right_upper_Q4': {'name': 'GICHICAPA%11', 'unit': 'A', 'label': 'Right upper capacitor current Q4'},
    'IC_Current_right_lower_Q4': {'name': 'GICHICAPA%12', 'unit': 'A', 'label': 'Right lower capacitor current Q4'},       
    ## LHCD
    'LH_P_tot': {'name': 'SHYBPTOT', 'unit': 'MW', 'label': 'LH total coupled power'},
    'LH_P_LH1': {'name': 'SHYBPFORW1', 'unit': 'kW', 'label': 'LH1 coupled power'},
    'LH_P_LH2': {'name': 'SHYBPFORW2', 'unit': 'kW', 'label': 'LH2 coupled power'},
    'LH_Rc_LH1': {'name': 'SHYBREF1', 'unit': '%', 'label': 'Avg. Refl. Coeff LH1'},
    'LH_Rc_LH2': {'name': 'SHYBREF2', 'unit': '%', 'label': 'Avg. Refl. Coeff LH2'},
    # Impurities (SURVIE)
    'Cu': {'name': 'scu19', 'unit': None, 'label': 'Copper'},
    'Fe': {'name': 'SFE15', 'unit': None, 'label': 'Iron'},
    ## Temperature
    'Te1': {'name': None, 'fun': 'ECE_1', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    'Te2': {'name': None, 'fun': 'ECE_2', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    'Te3': {'name': None, 'fun': 'ECE_3', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    'Te4': {'name': None, 'fun': 'ECE_4', 'unit': 'eV', 'label': 'Temperature (ECE)'},

    }

def smooth(y, window_length=51, polyorder=3):
    return savgol_filter(np.squeeze(y), window_length, polyorder)

def IC_Positions(pulse):
    y = pw.tsmat(pulse, 'EXP=T=S;Position;PosICRH')
    return y, np.array([-1, -1, -1])

def LH_Positions(pulse):
    y = pw.tsmat(pulse, 'EXP=T=S;Position;PosLHCD')
    return y, np.array([-1, -1])

def IC_Frequencies(pulse):
    y = pw.tsmat(pulse, 'DFCI;PILOTAGE;ICHFREQ')
    return y, np.array([-1, -1, -1])

def IC_Rc_Q1_avg(pulse):
    Q1RcLeft,  t_Q1RcLeft  = pw.tsbase(pulse, 'GICHCOUPRES%1', nargout=2)
    Q1RcRight, t_Q1RcRight = pw.tsbase(pulse, 'GICHCOUPRES%2', nargout=2)
    # clean non physical values
    Q1RcLeft = np.where((Q1RcLeft < 3) & (Q1RcLeft > 0), Q1RcLeft, np.nan)
    Q1RcRight= np.where((Q1RcRight < 3) & (Q1RcRight > 0), Q1RcRight, np.nan)
    # averages
    IC_Rc_Q1 = np.nanmean([Q1RcLeft, Q1RcRight], axis=0)
    return IC_Rc_Q1, t_Q1RcLeft

def IC_Rc_Q2_avg(pulse):
    Q2RcLeft,  t_Q2RcLeft  = pw.tsbase(pulse, 'GICHCOUPRES%3', nargout=2)
    Q2RcRight, t_Q2RcRight = pw.tsbase(pulse, 'GICHCOUPRES%4', nargout=2)
    # clean non physical values
    Q2RcLeft = np.where((Q2RcLeft < 3) & (Q2RcLeft > 0), Q2RcLeft, np.nan)
    Q2RcRight= np.where((Q2RcRight < 3) & (Q2RcRight >0), Q2RcRight, np.nan)
    # averages
    IC_Rc_Q2 = np.nanmean([Q2RcLeft, Q2RcRight], axis=0)
    return IC_Rc_Q2, t_Q2RcLeft

def IC_Rc_avg(pulse):
    """
    Return the average Rc of Q1 and Q2
    """
    Rc_Q1, t = IC_Rc_Q1_avg(pulse)
    Rc_Q2, t = IC_Rc_Q2_avg(pulse)
    Rc_avg = np.mean([Rc_Q1, Rc_Q2], axis=0)
    return Rc_avg, t

def IC_Q1_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%1', nargout=2)
    y = 10**(1.5*y - 10)
    return y,t

def IC_Q1_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%2', nargout=2)
    y = 10**(1.5*y - 10)
    return y,t    

def IC_Q2_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%3', nargout=2)
    y = 10**(1.5*y - 10)
    return y,t

def IC_Q2_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%4', nargout=2)
    y = 10**(1.5*y - 10)
    return y,t    

def get_sig(pulse, sig, do_smooth=False):
    """
    Return the (y,t) numpy arrays of the signal sig for a WEST pulse
    """
    try:
        if sig['name']:
            # if a tsbase signal name
            y, t = pw.tsbase(pulse, sig['name'], nargout=2)
        else:
            # if a specific routine
            eval_str = f"{sig['fun']}({pulse}) "
            y, t = eval(eval_str)

        t = np.squeeze(t)

        if do_smooth:
            y_smooth = smooth(y)
            y = y_smooth
    except (pw.PyWEDException, pw.tsExQueryError) as e:
        print(f"{sig['name']} #{pulse}: {e}")
        return np.nan, np.nan
    return y, t


def in_between(y, t, t_start=0, t_end=1000):
    """
    Filter the signal between t>=t_start and t<=t_end
    """
    idx = np.where((t >= t_start) & (t <= t_end))
    if np.any(idx):
        new_y = y[idx]
        new_t = t[idx]
    else:
        new_y = np.nan
        new_t = np.nan
        
    return new_y, new_t
        

def is_sig(pulse, sig, thres=0):
    """
    Return true if data from sig are available for the pulse.

    The signal data are tested against a threshold thres.
    If larger than this threshold, means there data are available.
    """
    y, t = get_sig(pulse, sig)

    if np.any(y >= thres):
        return True
    else:
        return False


def pulse_datetime(pulse):
    """
    Return the pulse datetime as a (pandas.)Timestamp and a Python datetime
    """
    date_apilote = pw.tsmat(pulse, 'APILOTE;+VME_PIL;Date_Choc')
    pulse_dt = pd.to_datetime(date_apilote)
    return pulse_dt, pulse_dt.to_pydatetime()


def mean_min_max(y):
    """
    Return the mean, min and max of an array
    """
    return np.mean(y), np.amin(y), np.amax(y)


def mean_std(y):
    """
    Return the mean and standard deviation of an array
    """
    return np.mean(y), np.std(y)


def scope(pulses, signames, do_smooth=False, style_label='default'):
    
    with plt.style.context(style_label):
    
        t_fin_acq = []
        fig, axes = plt.subplots(len(signames), 1, sharex=True, figsize=(7, 10))
        color_cycle = axes[0]._get_lines.prop_cycler
        plt.locator_params(axis='y', nbins=6)
        if type(axes) is not list:  # case of only one signal -> put axe in a list
            axes = np.array(axes)
    
        for pulse in pulses:
            _color = next(color_cycle)['color']
            # end of acquisition time - ignitron
            try:
                t_fin_acq.append(pw.tsmat(pulse, 'FINACQ|1')[0] - 32)
            except IndexError as e:
                t_fin_acq.append(100)
    
            for (sigs, ax) in zip(signames, axes):
                _legend = ''
                
                
                if not isinstance(sigs, list):
                    sigs = [sigs]
                for sig in sigs:
                    y, t = get_sig(pulse, sig, do_smooth)
        
                    ax.plot(t, y, label=f'#{pulse}', color=_color)
                    _legend += f"{sig['label']}, "
                ax.set_ylabel(f"[{sig['unit']}]")
                ax.text(0.01, 0.85, _legend, color='gray',
                        horizontalalignment='left', transform=ax.transAxes)
        # time axis
        axes[-1].set_xlabel('t [s]')
        axes[-1].set_xlim(-0.5, np.max(t_fin_acq))
        [a.grid(True, alpha=0.2) for a in axes]
    
        fig.subplots_adjust(hspace=0)
        fig.show()
        return fig, axes


def ECE_1(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH1','+')
    return Te, t_Te-32
def ECE_2(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH2','+')
    return Te, t_Te-32
def ECE_3(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH3','+')
    return Te, t_Te-32
def ECE_4(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH4','+')
    return Te, t_Te-32

def Prad(pulse):
    try:
        from  pradwest import pradwest
    
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError('pradwest only available on linux machines')
#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#
#def big_scope(pulses, signals_list):
#    """
#    - pulses: list of int
#    - signals_config: list of list of signals 1st dim = num col
#    """
#    fig = plt.figure(constrained_layout=True)
#    gs0 = fig.add_gridspec(1, len(signals_list))
#    _, col = gs0.get_geometry()
#
#    t_fin_acq = []
#
#    gs00 = []
#    for c in range(col):
#        gs00.append(gs0[c].subgridspec(4, 1))
#
#    for c in range(col):
#        row, _ = gs00[c].get_geometry()
#
#            for pulse in pulses:
#            # end of acquisition time - ignitron
#            t_fin_acq.append(pw.tsmat(pulse, 'FINACQ|1')[0] - 32)
#
#            for (sig, ax) in zip(signames, axes):
#                y, t = get_sig(pulse, sig, do_smooth)
#
#                ax.plot(t, y, label=f'#{pulse}')
#                ax.set_ylabel(f"[{sig['unit']}]")
#                ax.text(0.01, 0.85, f"{sig['label']}", color='gray',
#                        horizontalalignment='left', transform=ax.transAxes)
#        # time axis
#        axes[-1].set_xlabel('t [s]')
#        axes[-1].set_xlim(-0.5, np.max(t_fin_acq))
#        [a.grid(True, alpha=0.2) for a in axes]
#
#        fig.subplots_adjust(hspace=0)
#
#
#        for r in range(row):
#            fig.add_subplot(gs00[c][r])
#
#    fig.show()
#    return fig