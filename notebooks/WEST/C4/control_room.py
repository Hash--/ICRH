from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import pywed as pw
import pandas as pd
from itertools import cycle

signals = {
    ## Shot properties
    'Datetime': {'name': None, 'fun': 'pulse_datetime', 'unit':'', 'label':'pulse datetime'},
    ## Magnetics
    'Ip': {'name': 'SMAG_IP', 'unit': 'kA', 'label': 'Plasma current'},
    'Vloop': {'name': 'GMAG_VLOOP%1', 'unit': 'V', 'label': 'Loop voltage'},
    'Rext_upper': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext upper'},  # Rext upper
    'Rext_median': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext median', 'options':{'ylim':(2950, 3010)}},  # Rext median
    'Rext_lower': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext lower'},  # Rext lower
    'Zgeo': {'name': 'GMAG_BARY%2', 'unit': 'm', 'label': 'Zgeo'},  # Zgeo barycentre
    'R0': {'name': 'GMAG_BARY%1', 'unit': 'm', 'label': 'Large radius'},  # grand rayon
    # Movable limiter position (LPA)
    'LPA': {'name': 'GMAG_POSLPA%1', 'unit': 'm', 'label': 'LPA'},
    ## Fueling
    'nl': {'name': 'GINTLIDRT%3', 'unit': '$m^{-2}$', 'label': 'Line integrated density'},
    'Valve7': {'name': 'GDEBIT%7', 'unit': '$Pa.m^3/s$', 'label': 'Valve#7 (LPA)'},
    'Valve8': {'name': 'GDEBIT%8', 'unit': '$Pa.m^3/s$', 'label': 'Valve#8 (Q4)'},
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
    'IC_P_Q4_left_fwd': {'name': 'GICHANTPOWQ4%1', 'unit': 'kW', 'label': 'Left Fwd Power Q4'},
    'IC_P_Q4_left_ref': {'name': 'GICHANTPOWQ4%2', 'unit': 'kW', 'label': 'Left Ref Power Q4'},
    'IC_P_Q4_right_fwd': {'name': 'GICHANTPOWQ4%3', 'unit': 'kW', 'label': 'Right Fwd Power Q4'},
    'IC_P_Q4_right_ref': {'name': 'GICHANTPOWQ4%4', 'unit': 'kW', 'label': 'Right Ref Power Q4'},
    # IC Antennas coupling resistances
    'IC_Rc_Q1_left': {'name': 'GICHCOUPRES%1', 'unit': 'Ohm', 'label': 'Rc - Q1 Left', 'options':{'ylim':(0,1.5)} },
    'IC_Rc_Q1_right': {'name': 'GICHCOUPRES%2', 'unit': 'Ohm', 'label': 'Rc - Q1 Right', 'options':{'ylim':(0,1.5)}},
    'IC_Rc_Q2_left': {'name': 'GICHCOUPRES%3', 'unit': 'Ohm', 'label': 'Rc - Q2 Left', 'options':{'ylim':(0,1.5)}},
    'IC_Rc_Q2_right': {'name': 'GICHCOUPRES%4', 'unit': 'Ohm', 'label': 'Rc - Q2 Right','options':{'ylim':(0,1.5)}},
    'IC_Rc_Q4_left': {'name': 'GICHCOUPRES%5', 'unit': 'Ohm', 'label': 'Rc - Q4 Left','options':{'ylim':(0,1.5)}},
    'IC_Rc_Q4_right': {'name': 'GICHCOUPRES%6', 'unit': 'Ohm', 'label': 'Rc - Q4 Right', 'options':{'ylim':(0,1.5)}},
    'IC_Rc_Q1_avg': {'name': None, 'fun': 'IC_Rc_Q1_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q1', 'options':{'ylim':(0,1.5)}},
    'IC_Rc_Q2_avg': {'name': None, 'fun': 'IC_Rc_Q2_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q2', 'options':{'ylim':(0,1.5)}},
    'IC_Rc_Q4_avg': {'name': None, 'fun': 'IC_Rc_Q4_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q4', 'options':{'ylim':(0,1.5)}},    
    'IC_Rc_avg': {'name': None, 'fun': 'IC_Rc_avg', 'unit': 'Ohm', 'label': 'Avg. IC Rc', 'options':{'ylim':(0,1.5)}},
    # IC VSWR
    'IC_VSWR_Q1_Left': {'name':None, 'fun':'VSWR_Q1_Left', 'unit': '', 'label':'VSWR Q1 Left', 'options':{'ymin':0}},
    'IC_VSWR_Q1_Right': {'name':None, 'fun':'VSWR_Q1_Right', 'unit': '', 'label':'VSWR Q1 Right', 'options':{'ymin':0}},
    'IC_VSWR_Q2_Left': {'name':None, 'fun':'VSWR_Q2_Left', 'unit': '', 'label':'VSWR Q2 Left', 'options':{'ymin':0}},
    'IC_VSWR_Q2_Right': {'name':None, 'fun':'VSWR_Q2_Right', 'unit': '', 'label':'VSWR Q2 Right', 'options':{'ymin':0}},
    'IC_VSWR_Q4_Left': {'name':None, 'fun':'VSWR_Q4_Left', 'unit': '', 'label':'VSWR Q4 Left', 'options':{'ymin':0}},
    'IC_VSWR_Q4_Right': {'name':None, 'fun':'VSWR_Q4_Right', 'unit': '', 'label':'VSWR Q4 Right', 'options':{'ymin':0}},    
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
    # IC antenna phase differences
    'IC_delta_phi_toro_Q1_Top_LmR': {'name': None, 'fun': 'delta_phi_toro_Q1_Top_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q1 (L - R) Top'},
    'IC_delta_phi_toro_Q2_Top_LmR': {'name': None, 'fun': 'delta_phi_toro_Q2_Top_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q2 (L - R) Top'},
    'IC_delta_phi_toro_Q4_Top_LmR': {'name': None, 'fun': 'delta_phi_toro_Q4_Top_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q4 (L - R) Top'},
    'IC_delta_phi_toro_Q1_Bot_LmR': {'name': None, 'fun': 'delta_phi_toro_Q1_Bot_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q1 (L - R) Bot'},
    'IC_delta_phi_toro_Q2_Bot_LmR': {'name': None, 'fun': 'delta_phi_toro_Q2_Bot_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q2 (L - R) Bot'},
    'IC_delta_phi_toro_Q4_Bot_LmR': {'name': None, 'fun': 'delta_phi_toro_Q4_Bot_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q4 (L - R) Bot'},  
    'IC_delta_phi_polo_Q1_Left_BmT': {'name':None, 'fun': 'delta_phi_polo_Q1_Left_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q1 (B - T) Left'},
    'IC_delta_phi_polo_Q2_Left_BmT': {'name':None, 'fun': 'delta_phi_polo_Q2_Left_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q2 (B - T) Left'},
    'IC_delta_phi_polo_Q4_Left_BmT': {'name':None, 'fun': 'delta_phi_polo_Q4_Left_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q4 (B - T) Left'},
    'IC_delta_phi_polo_Q1_Right_BmT': {'name':None, 'fun': 'delta_phi_polo_Q1_Right_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q1 (B - T) Right'},
    'IC_delta_phi_polo_Q2_Right_BmT': {'name':None, 'fun': 'delta_phi_polo_Q2_Right_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q2 (B - T) Right'},
    'IC_delta_phi_polo_Q4_Right_BmT': {'name':None, 'fun': 'delta_phi_polo_Q4_Right_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q4 (B - T) Right'},    
    # IC Antennas internal vacuum (y = 10**(1.5*y - 10))
    'IC_Vacuum_Q1_left': {'name': None, 'fun': 'IC_Q1_vacuum_left', 'unit': 'Pa', 'label': 'Vaccum Q1 left', 'options': {'yscale':'log', 'ylimit':4.5e-3}},
    'IC_Vacuum_Q1_right': {'name': None, 'fun': 'IC_Q1_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q1 right', 'options': {'yscale':'log', 'ylimit':4.5e-3}},
    'IC_Vacuum_Q2_left': {'name': None, 'fun': 'IC_Q2_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q2 left', 'options': {'yscale':'log', 'ylimit':4.5e-3}},
    'IC_Vacuum_Q2_right': {'name': None, 'fun': 'IC_Q2_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q2 right', 'options': {'yscale':'log', 'ylimit':4.5e-3}},
    'IC_Vacuum_Q4_left': {'name': None, 'fun': 'IC_Q4_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q4 left', 'options': {'yscale':'log', 'ylimit':4.5e-3}},
    'IC_Vacuum_Q4_right': {'name': None, 'fun': 'IC_Q4_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q4 right', 'options': {'yscale':'log', 'ylimit':4.5e-3}},
    # Acquisition des Consignes de puissance en sortie des FPGA 
    'IC_cons_Power_Q1': {'name': 'GICHSPP%1', 'unit': 'kW', 'label': 'Acquisition consigne generee Q1'},
    'IC_cons_Power_Q2': {'name': 'GICHSPP%2', 'unit': 'kW', 'label': 'Acquisition consigne generee Q1'},
    'IC_cons_Power_Q4': {'name': 'GICHSPP%3', 'unit': 'kW', 'label': 'Acquisition consigne generee Q1'},
    # PCS: power, phase request and authorisation
    'IC_PCS_Power_Q1': {'name': 'GICHCONSPCS%1', 'unit': 'kW', 'label': 'PCS Power request Q1'},
    'IC_PCS_Power_Q2': {'name': 'GICHCONSPCS%2', 'unit': 'kW', 'label': 'PCS Power request Q2'},
    'IC_PCS_Power_Q4': {'name': 'GICHCONSPCS%3', 'unit': 'kW', 'label': 'PCS Power request Q4'},
    'IC_PCS_Phase_Q1': {'name': 'GICHCONSPCS%4', 'unit': 'deg', 'label': 'PCS Phase request Q1'},
    'IC_PCS_Phase_Q2': {'name': 'GICHCONSPCS%5', 'unit': 'deg', 'label': 'PCS Phase request Q2'},
    'IC_PCS_Phase_Q4': {'name': 'GICHCONSPCS%6', 'unit': 'deg', 'label': 'PCS Phase request Q4'},    
    'IC_PCS_interdiction_Q1': {'name': 'GICHCONSPCS%7', 'unit': '--', 'label': 'PCS interdiction Q1'},
    'IC_PCS_interdiction_Q2': {'name': 'GICHCONSPCS%8', 'unit': '--', 'label': 'PCS interdiction Q2'},
    'IC_PCS_interdiction_Q4': {'name': 'GICHCONSPCS%9', 'unit': '--', 'label': 'PCS interdiction Q4'},    
    # NB : coupling resistance is also send to PCS for real time control.
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
    'IC_ErrSig_Q4_left_upper': {'name': 'GICHSIGERR%9', 'unit': '', 'label': 'Err.Sig.Q4 L-U'},
    'IC_ErrSig_Q4_left_lower': {'name': 'GICHSIGERR%10', 'unit': '', 'label': 'Err.Sig.Q4 L-L'},
    'IC_ErrSig_Q4_right_upper': {'name': 'GICHSIGERR%11', 'unit': '', 'label': 'Err.Sig.Q4 R-U'},
    'IC_ErrSig_Q4_right_lower': {'name': 'GICHSIGERR%12', 'unit': '', 'label': 'Err.Sig.Q4 R-L'},    
    # IC antennas Capacitor Voltages
    'IC_Voltage_left_upper_Q1': {'name': 'GICHVPROBEQ1%1', 'unit': 'kV', 'label': 'Left upper capacitor voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_left_lower_Q1': {'name': 'GICHVPROBEQ1%2', 'unit': 'kV', 'label': 'Left lower capacitor voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_right_upper_Q1': {'name': 'GICHVPROBEQ1%3', 'unit': 'kV', 'label': 'Right upper capacitor voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_right_lower_Q1': {'name': 'GICHVPROBEQ1%4', 'unit': 'kV', 'label': 'Right lower capacitor voltage Q1', 'options': {'ylimit':27}}, 
    'IC_Voltage_left_upper_Q2': {'name': 'GICHVPROBEQ2%1', 'unit': 'kV', 'label': 'Left upper capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_left_lower_Q2': {'name': 'GICHVPROBEQ2%2', 'unit': 'kV', 'label': 'Left lower capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_right_upper_Q2': {'name': 'GICHVPROBEQ2%3', 'unit': 'kV', 'label': 'Right upper capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_right_lower_Q2': {'name': 'GICHVPROBEQ2%4', 'unit': 'kV', 'label': 'Right lower capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_left_upper_Q4': {'name': 'GICHVPROBEQ4%1', 'unit': 'kV', 'label': 'Left upper capacitor voltage Q4', 'options': {'ylimit':27}},
    'IC_Voltage_left_lower_Q4': {'name': 'GICHVPROBEQ4%2', 'unit': 'kV', 'label': 'Left lower capacitor voltage Q4'},
    'IC_Voltage_right_upper_Q4': {'name': 'GICHVPROBEQ4%3', 'unit': 'kV', 'label': 'Right upper capacitor voltage Q4', 'options': {'ylimit':27}},
    'IC_Voltage_right_lower_Q4': {'name': 'GICHVPROBEQ4%4', 'unit': 'kV', 'label': 'Right lower capacitor voltage Q4', 'options': {'ylimit':27}},     
    # IC antennas Capacitor Currents
    'IC_Current_left_upper_Q1': {'name': 'GICHICAPA%1', 'unit': 'A', 'label': 'Left upper capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_left_lower_Q1': {'name': 'GICHICAPA%2', 'unit': 'A', 'label': 'Left lower capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_right_upper_Q1': {'name': 'GICHICAPA%3', 'unit': 'A', 'label': 'Right upper capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_right_lower_Q1': {'name': 'GICHICAPA%4', 'unit': 'A', 'label': 'Right lower capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_left_upper_Q2': {'name': 'GICHICAPA%5', 'unit': 'A', 'label': 'Left upper capacitor current Q2', 'options': {'ylimit':915}},
    'IC_Current_left_lower_Q2': {'name': 'GICHICAPA%6', 'unit': 'A', 'label': 'Left lower capacitor current Q2', 'options': {'ylimit':915}},
    'IC_Current_right_upper_Q2': {'name': 'GICHICAPA%7', 'unit': 'A', 'label': 'Right upper capacitor current Q2', 'options': {'ylimit':915}},
    'IC_Current_right_lower_Q2': {'name': 'GICHICAPA%8', 'unit': 'A', 'label': 'Right lower capacitor current Q2', 'options': {'ylimit':915}},   
    'IC_Current_left_upper_Q4': {'name': 'GICHICAPA%9', 'unit': 'A', 'label': 'Left upper capacitor current Q4', 'options': {'ylimit':915}},
    'IC_Current_left_lower_Q4': {'name': 'GICHICAPA%10', 'unit': 'A', 'label': 'Left lower capacitor current Q4', 'options': {'ylimit':915}},
    'IC_Current_right_upper_Q4': {'name': 'GICHICAPA%11', 'unit': 'A', 'label': 'Right upper capacitor current Q4', 'options': {'ylimit':915}},
    'IC_Current_right_lower_Q4': {'name': 'GICHICAPA%12', 'unit': 'A', 'label': 'Right lower capacitor current Q4', 'options': {'ylimit':915}}, 
    # IC Errors

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
    ## Langmuir probes
    'Langmuir_LHCD1': {'name': 'GISLH%1', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #1'},
    'Langmuir_LHCD2': {'name': 'GISLH%2', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #2'},
    'Langmuir_LHCD3': {'name': 'GISLH%3', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #3'},
    'Langmuir_LHCD4': {'name': 'GISLH%4', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #4'},
    'Langmuir_LHCD5': {'name': 'GISLH%5', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #5'},
    'Langmuir_LHCD6': {'name': 'GISLH%6', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #6'},
    'Langmuir_LHCD7': {'name': 'GISLH%7', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #7'},
    'Langmuir_LHCD8': {'name': 'GISLH%8', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #8'},
    ## Barometry
    'baro_Q2': {'name':'GBARDB8%4', 'unit': '--', 'label':'barometry Q2 raw'},
    'baro_Q4': {'name':'GBARDB8%9', 'unit': '--', 'label':'barometry Q4 raw'},
    }

def VSWR_Q1_Left(pulse):
    Pow_IncRefQ1, tPow_IncRefQ1 = pw.tsbase(pulse,'GICHANTPOWQ1', nargout=2)   
    VSWR_Q1_Left  = (1 + np.sqrt(Pow_IncRefQ1[:,1]/Pow_IncRefQ1[:,0])) / \
                    (1 - np.sqrt(Pow_IncRefQ1[:,1]/Pow_IncRefQ1[:,0]))
    return VSWR_Q1_Left, tPow_IncRefQ1

def VSWR_Q1_Right(pulse):
    Pow_IncRefQ1, tPow_IncRefQ1 = pw.tsbase(pulse,'GICHANTPOWQ1', nargout=2)   
    VSWR_Q1_Right  = (1 + np.sqrt(Pow_IncRefQ1[:,3]/Pow_IncRefQ1[:,2])) / \
                    (1 - np.sqrt(Pow_IncRefQ1[:,3]/Pow_IncRefQ1[:,2]))
    return VSWR_Q1_Right, tPow_IncRefQ1

def VSWR_Q2_Left(pulse):
    Pow_IncRefQ2, tPow_IncRefQ2 = pw.tsbase(pulse,'GICHANTPOWQ2', nargout=2)   
    VSWR_Q2_Left  = (1 + np.sqrt(Pow_IncRefQ2[:,1]/Pow_IncRefQ2[:,0])) / \
                    (1 - np.sqrt(Pow_IncRefQ2[:,1]/Pow_IncRefQ2[:,0]))
    return VSWR_Q2_Left, tPow_IncRefQ2

def VSWR_Q2_Right(pulse):
    Pow_IncRefQ2, tPow_IncRefQ2 = pw.tsbase(pulse,'GICHANTPOWQ2', nargout=2)   
    VSWR_Q2_Right  = (1 + np.sqrt(Pow_IncRefQ2[:,3]/Pow_IncRefQ2[:,2])) / \
                    (1 - np.sqrt(Pow_IncRefQ2[:,3]/Pow_IncRefQ2[:,2]))
    return VSWR_Q2_Right, tPow_IncRefQ2

def VSWR_Q4_Left(pulse):
    Pow_IncRefQ4, tPow_IncRefQ4 = pw.tsbase(pulse,'GICHANTPOWQ4', nargout=2)   
    VSWR_Q4_Left  = (1 + np.sqrt(Pow_IncRefQ4[:,1]/Pow_IncRefQ4[:,0])) / \
                    (1 - np.sqrt(Pow_IncRefQ4[:,1]/Pow_IncRefQ4[:,0]))
    return VSWR_Q4_Left, tPow_IncRefQ4

def VSWR_Q4_Right(pulse):
    Pow_IncRefQ4, tPow_IncRefQ4 = pw.tsbase(pulse,'GICHANTPOWQ4', nargout=2)   
    VSWR_Q4_Right  = (1 + np.sqrt(Pow_IncRefQ4[:,3]/Pow_IncRefQ4[:,2])) / \
                    (1 - np.sqrt(Pow_IncRefQ4[:,3]/Pow_IncRefQ4[:,2]))
    return VSWR_Q4_Right, tPow_IncRefQ4


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

def IC_Errors(pulse):
    '''
    Renvoie un
        // Ecriture des sécurités
    TabIT[0]=NbIntTOS[0]; TabIT[6]=NbIntTOS[1]; TabIT[12]=NbIntTOS[2];
    TabIT[1]=NbIntSHAD[0]; TabIT[7]=NbIntSHAD[1]; TabIT[13]=NbIntSHAD[2];
    TabIT[2]=NbIntOPT[0]; TabIT[8]=NbIntOPT[1]; TabIT[14]=NbIntOPT[2];
    TabIT[3]=NbIntDV[0]; TabIT[9]=NbIntDV[1]; TabIT[15]=NbIntDV[2];
    TabIT[4]=NbIntTTF[0]; TabIT[10]=NbIntTTF[1]; TabIT[16]=NbIntTTF[2];    
    TabIT[5]=TotalInt[0]; TabIT[11]=TotalInt[1]; TabIT[17]=TotalInt[2];

    '''
    y = pw.tsmat(pulse, 'DFCI;PILOTAGE;ICHINT')
    return y, np.array([-1, -1, -1])

def IC_Rc_Q1_avg(pulse):
    #Q1RcLeft,  t_Q1RcLeft  = pw.tsbase(pulse, 'GICHCOUPRES%1', nargout=2)
    Q1RcRight, t_Q1RcRight = pw.tsbase(pulse, 'GICHCOUPRES%2', nargout=2)
    # clean non physical values
    #Q1RcLeft = np.where((Q1RcLeft < 3) & (Q1RcLeft > 0), Q1RcLeft, np.nan)
    Q1RcRight= np.where((Q1RcRight < 3) & (Q1RcRight > 0), Q1RcRight, np.nan)
    # averages
    #IC_Rc_Q1 = np.nanmean([Q1RcLeft, Q1RcRight], axis=0)
    #return IC_Rc_Q1, t_Q1RcLeft
    return Q1RcRight, t_Q1RcRight

def IC_Rc_Q2_avg(pulse):
    Q2RcLeft,  t_Q2RcLeft  = pw.tsbase(pulse, 'GICHCOUPRES%3', nargout=2)
    Q2RcRight, t_Q2RcRight = pw.tsbase(pulse, 'GICHCOUPRES%4', nargout=2)
    # clean non physical values
    Q2RcLeft = np.where((Q2RcLeft < 3) & (Q2RcLeft > 0), Q2RcLeft, np.nan)
    Q2RcRight= np.where((Q2RcRight < 3) & (Q2RcRight >0), Q2RcRight, np.nan)
    # averages
    IC_Rc_Q2 = np.nanmean([Q2RcLeft, Q2RcRight], axis=0)
    return IC_Rc_Q2, t_Q2RcLeft

def IC_Rc_Q4_avg(pulse):
    Q4RcLeft,  t_Q4RcLeft  = pw.tsbase(pulse, 'GICHCOUPRES%5', nargout=2)
    Q4RcRight, t_Q4RcRight = pw.tsbase(pulse, 'GICHCOUPRES%6', nargout=2)
    # clean non physical values
    Q4RcLeft = np.where((Q4RcLeft < 3) & (Q4RcLeft > 0), Q4RcLeft, np.nan)
    Q4RcRight= np.where((Q4RcRight < 3) & (Q4RcRight >0), Q4RcRight, np.nan)
    # averages
    IC_Rc_Q4 = np.nanmean([Q4RcLeft, Q4RcRight], axis=0)
    return IC_Rc_Q4, t_Q4RcLeft

def IC_Rc_avg(pulse):
    """
    Return the average Rc of Q1 and Q2 and Q4
    """
    Rc_Q1, t = IC_Rc_Q1_avg(pulse)
    Rc_Q2, t = IC_Rc_Q2_avg(pulse)
    Rc_Q4, t = IC_Rc_Q4_avg(pulse)
    Rc_avg = np.mean([Rc_Q1, Rc_Q2, Rc_Q4], axis=0)
    return Rc_avg, t

"""
phases ICRH
"""
# TODO : passing argument to get_sig
def delta_phi_toro_Q1_Top_LmR(pulse):
    return delta_phi_toro_Qi_Top_LmR(pulse, i=1)
def delta_phi_toro_Q2_Top_LmR(pulse):
    return delta_phi_toro_Qi_Top_LmR(pulse, i=2)
def delta_phi_toro_Q4_Top_LmR(pulse):
    return delta_phi_toro_Qi_Top_LmR(pulse, i=4)    

def delta_phi_toro_Q1_Bot_LmR(pulse):
    return delta_phi_toro_Qi_Bot_LmR(pulse, i=1)
def delta_phi_toro_Q2_Bot_LmR(pulse):
    return delta_phi_toro_Qi_Bot_LmR(pulse, i=2)
def delta_phi_toro_Q4_Bot_LmR(pulse):
    return delta_phi_toro_Qi_Bot_LmR(pulse, i=4)

def delta_phi_polo_Q1_Left_BmT(pulse):
    return delta_phi_polo_Qi_Left_BmT(pulse, i=1)
def delta_phi_polo_Q2_Left_BmT(pulse):
    return delta_phi_polo_Qi_Left_BmT(pulse, i=2)
def delta_phi_polo_Q4_Left_BmT(pulse):
    return delta_phi_polo_Qi_Left_BmT(pulse, i=4)

def delta_phi_polo_Q1_Right_BmT(pulse):
    return delta_phi_polo_Qi_Right_BmT(pulse, i=1)
def delta_phi_polo_Q2_Right_BmT(pulse):
    return delta_phi_polo_Qi_Right_BmT(pulse, i=2)
def delta_phi_polo_Q4_Right_BmT(pulse):
    return delta_phi_polo_Qi_Right_BmT(pulse, i=4)

# Q1
def delta_phi_toro_Qi_Top_LmR(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiToroTOP_LmR = PhasesQi[:,3] + PhasesQi[:,1] - PhasesQi[:,5]
    return  dPhiToroTOP_LmR, tPhasesQi[:,0]

def delta_phi_toro_Qi_Bot_LmR(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiToroBOT_LmR = PhasesQi[:,4] + PhasesQi[:,0] - PhasesQi[:,6]
    return  dPhiToroBOT_LmR, tPhasesQi[:,0]

def delta_phi_polo_Qi_Left_BmT(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiPoloLEFT_BmT  = PhasesQi[:,4] - PhasesQi[:,3]
    return dPhiPoloLEFT_BmT, tPhasesQi[:,0]

def delta_phi_polo_Qi_Right_BmT(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiPoloRIGHT_BmT = PhasesQi[:,6] - PhasesQi[:,5]
    return dPhiPoloRIGHT_BmT, tPhasesQi[:,0]

def IC_Q1_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%1', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t

def IC_Q1_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%2', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t    

def IC_Q2_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%3', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t

def IC_Q2_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%4', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t    

def IC_Q4_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%5', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t

def IC_Q4_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%6', nargout=2)
    y = 10**(1.667*y - 9.333)
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


def scope(pulses, signames, do_smooth=False, style_label='default', window_loc=(0,0)):
    
    with plt.style.context(style_label):
    
        t_fin_acq = []
        fig, axes = plt.subplots(len(signames), 1, sharex=True, figsize=(7, 10))
        # move the figure 
        fig.canvas.manager.window.move(window_loc[0], window_loc[1])
        # cycle the color for each shot number
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
                _lines = cycle(['-',':', '--', '-x'])
                # if a list: superpose the trace on the same axe
                if not isinstance(sigs, list):
                    sigs = [sigs]
                for sig in sigs:
                    
                    y, t = get_sig(pulse, sig, do_smooth)
        
                    ax.plot(t, y, label=f'#{pulse}', color=_color, ls=next(_lines))
                    _legend += f"{sig['label']}, "
                ax.set_ylabel(f"[{sig['unit']}]")
                ax.text(0.01, 0.85, _legend, color='gray',
                        horizontalalignment='left', transform=ax.transAxes)

                if 'options' in sig:           
                    if 'yscale' in sig['options']:
                        ax.set_yscale(sig['options']['yscale'])
                    if 'ylim' in sig['options']:
                        ax.set_ylim(sig['options']['ylim'])
                    if 'ymin' in sig['options']:
                        ax.set_ylim(bottom=sig['options']['ymin'])
                    if 'ylimit' in sig['options']:
                        ax.axhline(sig['options']['ylimit'], color='r')

        # time axis
        axes[-1].set_xlabel('t [s]')
        axes[-1].set_xlim(-0.5, np.max(t_fin_acq))
        [a.grid(True, alpha=0.2) for a in axes]
    
        fig.tight_layout()
        fig.subplots_adjust(hspace=0)
        fig.show()
        return fig, axes


def baro_Q2(pulse):
    baroQ2BP, tbaroQ2BP = pw.tsbase(pulse, 'GBARDB8%4', nargout=2)
    return baroQ2BP, tbaroQ2BP 

def baro_Q4(pulse):
    baroQ4BP, tbaroQ4BP = pw.tsbase(pulse, 'GBARDB8%9', nargout=2)
    return baroQ4BP, tbaroQ4BP 

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
