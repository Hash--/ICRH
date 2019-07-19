# -*- coding: utf-8 -*-
"""

"""
# %%
from control_room import *
import numpy as np


#%%
def generate_sig_generalQi(i=1):
    sigs_general_Qi = [
        signals[f'IC_PCS_interdiction_Q{i}'],
        signals[f'IC_PCS_Power_Q{i}'],
                
        [signals[f'IC_P_Q{i}_left_fwd'], signals[f'IC_P_Q{i}_left_ref']],
    
        [signals[f'IC_P_Q{i}_right_fwd'], signals[f'IC_P_Q{i}_right_ref']],
        
        [signals[f'IC_VSWR_Q{i}_Left'], signals[f'IC_VSWR_Q{i}_Right']],
    
        [signals[f'IC_Rc_Q{i}_left'], signals[f'IC_Rc_Q{i}_right']],
    [signals[f'IC_Voltage_left_upper_Q{i}'], signals[f'IC_Voltage_left_lower_Q{i}']],
    [signals[f'IC_Voltage_right_upper_Q{i}'], signals[f'IC_Voltage_right_lower_Q{i}']],
    [signals[f'IC_delta_phi_toro_Q{i}_Bot_LmR'], signals[f'IC_delta_phi_toro_Q{i}_Top_LmR']],        
        [signals[f'IC_Vacuum_Q{i}_right'], signals[f'IC_Vacuum_Q{i}_left']],
        
        [signals[f'IC_ErrSig_Q{i}_left_upper'], signals[f'IC_ErrSig_Q{i}_left_lower']],
        [signals[f'IC_ErrSig_Q{i}_right_upper'], signals[f'IC_ErrSig_Q{i}_right_lower']],
    ]
    return sigs_general_Qi

def generate_sig_probes_Qi(i=1):
    sig_probes_Qi = [
    signals[f'IC_P_Q{i}'],
        [signals[f'IC_Rc_Q{i}_left'], signals[f'IC_Rc_Q{i}_right']],
    [signals[f'IC_Voltage_left_upper_Q{i}'], signals[f'IC_Voltage_left_lower_Q{i}']],
    [signals[f'IC_Voltage_right_upper_Q{i}'], signals[f'IC_Voltage_right_lower_Q{i}']],
    
    [signals[f'IC_delta_phi_toro_Q{i}_Bot_LmR'], signals[f'IC_delta_phi_toro_Q{i}_Top_LmR']],
    [signals[f'IC_delta_phi_polo_Q{i}_Left_BmT'], signals[f'IC_delta_phi_polo_Q{i}_Right_BmT']],        
    ]
    return sig_probes_Qi

def generate_sig_capas_Qi(i=1):
    sig_probes_Qi = [
        [signals[f'IC_P_Q{i}_left_fwd'], signals[f'IC_P_Q{i}_left_ref']],    
        [signals[f'IC_P_Q{i}_right_fwd'], signals[f'IC_P_Q{i}_right_ref']],
        [signals[f'IC_Rc_Q{i}_left'], signals[f'IC_Rc_Q{i}_right']],                    
        [signals[f'IC_ErrSig_Q{i}_left_upper'], signals[f'IC_ErrSig_Q{i}_left_lower']],
        [signals[f'IC_ErrSig_Q{i}_right_upper'], signals[f'IC_ErrSig_Q{i}_right_lower']],  
        [signals[f'IC_Capa_Q{i}_left_upper'], signals[f'IC_Capa_Q{i}_left_lower']],
        [signals[f'IC_Capa_Q{i}_right_upper'], signals[f'IC_Capa_Q{i}_right_lower']],
    ]
    return sig_probes_Qi

#%%
pulses = [54449, 54453]
pulses = [54461]

#%%
sig_generalQ1 = generate_sig_generalQi(1)
fig, axes = scope(pulses, sig_generalQ1, do_smooth=False)
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_generalQ2 = generate_sig_generalQi(2)
fig, axes = scope(pulses, sig_generalQ2, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_generalQ4 = generate_sig_generalQi(4)
fig, axes = scope(pulses, sig_generalQ4, do_smooth=False, window_loc=(1200,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%%
sig_probes_Q1 = generate_sig_probes_Qi(1)
fig, axes = scope(pulses, sig_probes_Q1, do_smooth=False)
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_probes_Q2 = generate_sig_probes_Qi(2)
fig, axes = scope(pulses, sig_probes_Q2, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_probes_Q4 = generate_sig_probes_Qi(4)
fig, axes = scope(pulses, sig_probes_Q4, do_smooth=False, window_loc=(1200,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%% capacitors
sig_capa_Q1 = generate_sig_capas_Qi(1)
fig, axes = scope(pulses, sig_capa_Q1, do_smooth=False)
axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_capa_Q2 = generate_sig_capas_Qi(2)
fig, axes = scope(pulses, sig_capa_Q2, do_smooth=False, window_loc=(600,0))
axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

#sig_capa_Q4 = generate_sig_capas_Qi(4)
#fig, axes = scope(pulses, sig_capa_Q4, do_smooth=False, window_loc=(1200,0))
#axes[-1].set_xlim(0, 10)
#axes[0].legend()


#%% General view and Gaz
sig_general = [
        signals['Ip'],
        signals['nl'],
        signals['Rext_median'],
        [signals['LH_P_LH1'], signals['LH_P_LH2']],
        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
        [signals['IC_Rc_Q1_avg'], signals['IC_Rc_Q2_avg'], signals['IC_Rc_Q4_avg']],
        [signals['Valve9'], signals['Valve10'], signals['Valve8'], ],
        [signals[f'IC_Vacuum_Q1_right'], signals[f'IC_Vacuum_Q2_right'], signals[f'IC_Vacuum_Q4_right'] ],
        ]
fig, axes = scope(pulses, sig_general, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%%
sig_currents = [
        [signals['IC_Current_left_upper_Q1'], signals['IC_Current_left_lower_Q1']],
        [signals['IC_Current_right_upper_Q1'], signals['IC_Current_right_lower_Q1']],
        [signals['IC_Current_left_upper_Q2'], signals['IC_Current_left_lower_Q2']],
        [signals['IC_Current_right_upper_Q2'], signals['IC_Current_right_lower_Q2']],
        [signals['IC_Current_left_upper_Q4'], signals['IC_Current_left_lower_Q4']],
        [signals['IC_Current_right_upper_Q4'], signals['IC_Current_right_lower_Q4']],        
        ]
fig, axes = scope(pulses, sig_currents, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(0, 10)
axes[0].legend()


#%% barometry is perturbed by ICRH
sig_baro = [
        signals['IC_P_tot'],
        signals['baro_Q2'],
        signals['baro_Q4']
        ]
fig, axes = scope(pulses, sig_baro, do_smooth=False)
axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()