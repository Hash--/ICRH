# -*- coding: utf-8 -*-
"""

"""
# %%
from control_room import *
import numpy as np

pulses = [88]

sigs_general = [
    #signals['IC_P_Q1_left_fwd'],
    #signals['IC_P_Q1_left_ref'],
    #signals['IC_P_Q2_left_fwd'],
    #signals['IC_P_Q2_left_ref'],
    #signals['IC_P_Q4_left_fwd'],
    #signals['IC_P_Q4_left_ref'],   

    #signals['IC_PCS_Power_Q1'],
    #signals['IC_PCS_Power_Q2'],
    #signals['IC_PCS_Power_Q4'],
    #signals['IC_PCS_Phase_Q1'],
    #signals['IC_PCS_Phase_Q2'],
    #signals['IC_PCS_Phase_Q4'],
    
    signals['IC_Voltage_left_upper_Q1'],
    signals['IC_Voltage_left_lower_Q1'],
    signals['IC_Voltage_right_upper_Q1'],
    signals['IC_Voltage_right_lower_Q1'],
    
    # signals['IC_Rc_Q1_left'],
    # signals['IC_Rc_Q1_right'],
    # signals['IC_Rc_Q2_left'],
    # signals['IC_Rc_Q2_right'],
    # signals['IC_Rc_Q4_left'],
    # signals['IC_Rc_Q4_right'],
    
    #signals['IC_PCS_interdiction_Q1'],
    #signals['IC_PCS_interdiction_Q2'],
    #signals['IC_PCS_interdiction_Q4'],
    ]

fig, axes = scope(pulses, sigs_general, do_smooth=False)
axes[-1].set_xlim(0, 20)
axes[0].legend()


# %%
pulses = [53778]

sigs_general = [
        signals['ne'],
        signals['Te'],
    signals['nl'],
    signals['LH_P_tot'],
    signals['IC_P_tot']]

fig, axes = scope(pulses, sigs_general, do_smooth=False)
axes[-1].set_xlim(0, 8)
axes[0].legend()



# %%npulse of 06/12/2018
pulses = [54095, 54108,  # LH only 
          54102,  # Q2 
          54105,  # Q1
          ]
# %%
pulses = [53872]

sigs_general = [signals['Ip'], 
        signals['nl'],
        signals['LH_P_tot'],
        signals['IC_P_tot']]
fig, axes = scope(pulses, sigs_general, do_smooth=False)
axes[-1].set_xlim(-1, 35)
axes[0].legend()
axes[1].set_ylim(bottom=0)
axes[2].set_ylim(bottom=0, top=3.5)

# %%

pulses = [54177, 54178 ]

sigs_general = [signals['Ip'], 
        signals['nl'],
        signals['LH_P_tot'], 
        signals['IC_P_Q2']]

fig, axes = scope(pulses, sigs_general, do_smooth=False)
axes[-1].set_xlim(0, 40)
axes[0].legend()


# %%
pulses = [53257, 53259]
sigs_general = [signals['Ip'], signals['Te3']]
fig, axes = scope(pulses, sigs_general, do_smooth=False)
axes[0].legend()

# %%
sigs_general = [signals['Ip'], 
        signals['nl'],
        signals['LH_P_tot'], 
        [signals['Valve10'], signals['Valve11']],
        signals['IC_P_Q1'], 
        signals['IC_Rc_Q1_avg'],
        signals['IC_P_Q2'], 
        signals['IC_Rc_Q2_avg'],
        signals['Cu'], signals['Fe']]

fig, axes = scope(pulses, sigs_general, do_smooth=False)
axes[-1].set_xlim(0, 40)
axes[0].legend()

# %%
sigs_Q2 = [signals['Ip'], 
        signals['nl'],
        signals['LH_P_tot'], 
        [signals['Valve10'], signals['Valve11']],
        [signals['IC_P_Q2_left_fwd'], signals['IC_P_Q2_right_fwd']],
        [signals['IC_P_Q2_left_ref'], signals['IC_P_Q2_right_ref']],
        [signals['IC_Rc_Q2_left'], signals['IC_Rc_Q2_right']],
        [signals['IC_Vacuum_Q2_left'], signals['IC_Vacuum_Q2_right']],
        signals['Cu'], signals['Fe']]

fig, axes = scope(pulses, sigs_Q2, do_smooth=False)
axes[-1].set_xlim(0, 15)
axes[0].legend()
fig.set

# %%
sigs_Q1 = [signals['Ip'], 
        signals['nl'],
        signals['LH_P_tot'], 
        [signals['Valve10'], signals['Valve11']],
        [signals['IC_P_Q1_left_fwd'], signals['IC_P_Q1_right_fwd']],
        [signals['IC_P_Q1_left_ref'], signals['IC_P_Q1_right_ref']],
        [signals['IC_Rc_Q1_left'], signals['IC_Rc_Q1_right']],
        [signals['IC_Vacuum_Q1_left'], signals['IC_Vacuum_Q1_right']],
        signals['Cu'], signals['Fe']]

fig, axes = scope(pulses, sigs_Q1, do_smooth=False)
axes[-1].set_xlim(0, 15)
axes[0].legend()