from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import pywed as pw

signals = {
    ## Magnetics
    'Ip': {'name': 'SMAG_IP', 'unit': 'kA', 'label': 'Plasma current'},
    'Vloop': {'name': 'GMAG_VLOOP%1', 'unit': 'V', 'label': 'Loop voltage'},
    'Rext_upper': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext upper'},  # Rext upper
    'Rext_median': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext median'},  # Rext median
    'Rext_lower': {'name': 'GMAG_TEST%2', 'unit': 'm', 'label': 'Rext lower'},  # Rext lower
    'Zgeo': {'name': 'GMAG_BARY%2', 'unit': 'm', 'label': 'Zgeo'},  # Zgeo barycentre
    'R0': {'name': 'GMAG_BARY%1', 'unit': 'm', 'label': 'Large radius'},  # grand rayon
    ## Fueling
    'nl': {'name': 'GINTLIDRT%3', 'unit': '$m^{-2}$', 'label': 'Line integrated density'},
    'Valve7': {'name': 'GDEBIT%7', 'unit': '', 'label': 'Valve#7 (LPA)'},
    'Valve9': {'name': 'GDEBIT%9', 'unit': '', 'label': 'Valve#9 (Q1)'},
    'Valve10': {'name': 'GDEBIT%10', 'unit': '', 'label': 'Valve#10 (Q2)'},
    'Valve11': {'name': 'GDEBIT%11', 'unit': '', 'label': 'Valve#11 (up.divertor)'},
    'Valve21': {'name': 'GDEBIT%21', 'unit': '', 'label': 'Valve#21'},
    ## ICRH
    # IC coupled powers
    'P_IC_tot': {'name': 'SICHPTOT', 'unit': 'kW', 'label': 'IC total coupled power'}, 
    'P_IC_Q1': {'name': 'SICHPQ1', 'unit': 'kW', 'label': 'IC Q1 coupled power'},
    'P_IC_Q2': {'name': 'SICHPQ2', 'unit': 'kW', 'label': 'IC Q2 coupled power'},
    'P_IC_Q4': {'name': 'SICHPQ4', 'unit': 'kW', 'label': 'IC Q4 coupled power'},
    # IC antenna positions (use tsmat)
    'Positions': {'name': 'EXP=T=S;Position;PosICRH', 'unit': 'm', 'label': 'IC Antenna positions'},
    # IC antennas left and right forward and reflected powers
    'P_Q1_left_fwd': {'name': 'GICHANTPOWQ1%1', 'unit': 'kW', 'label': ''}, 
    'P_Q1_left_ref': {'name': 'GICHANTPOWQ1%2', 'unit': 'kW', 'label': ''},
    'P_Q1_right_fwd': {'name': 'GICHANTPOWQ1%3',  'unit': 'kW', 'label': ''},
    'P_Q1_right_ref': {'name': 'GICHANTPOWQ1%4', 'unit': 'kW', 'label': ''},
    'P_Q2_left_fwd': {'name': 'GICHANTPOWQ2%1', 'unit': 'kW', 'label': ''},
    'P_Q2_left_ref': {'name': 'GICHANTPOWQ2%2', 'unit': 'kW', 'label': ''},
    'P_Q2_right_fwd': {'name': 'GICHANTPOWQ2%3', 'unit': 'kW', 'label': ''},
    'P_Q2_right_ref': {'name': 'GICHANTPOWQ2%4', 'unit': 'kW', 'label': ''},
    # IC Antennas coupling resistances
    'Rc_Q1_left': {'name': 'GICHCOUPRES%1', 'unit': 'Ohm', 'label': ''}, 
    'Rc_Q1_right': {'name': 'GICHCOUPRES%2', 'unit': 'Ohm', 'label': ''},
    'Rc_Q2_left': {'name': 'GICHCOUPRES%3', 'unit': 'Ohm', 'label': ''},
    'Rc_Q2_right': {'name': 'GICHCOUPRES%4', 'unit': 'Ohm', 'label': ''},           
    'Rc_Q4_left': {'name': 'GICHCOUPRES%5', 'unit': 'Ohm', 'label': ''},
    'Rc_Q4_right': {'name': 'GICHCOUPRES%6', 'unit': 'Ohm', 'label': ''},
    'Rc_Q1_avg': {'name': None, 'fun': 'IC_Rc_Q1_avg', 'unit': 'Ohm', 'label': 'Avg. Rc Q1'},
    'Rc_Q2_avg': {'name': None, 'fun': 'IC_Rc_Q2_avg', 'unit': 'Ohm', 'label': 'Avg. Rc Q2'},
    'Rc_avg': {'name': None, 'fun': 'IC_Rc_avg', 'unit': 'Ohm', 'label': 'Avg. IC Rc'},
    # IC Antennas internal vacuum (y = 10**(1.5*y - 10))
    'Vacuum_Q1_left': {'name': 'GICHVTRANSFO%1', 'unit': 'Pa', 'label': 'Vaccum Q1 left'},
    'Vacuum_Q1_right': {'name': 'GICHVTRANSFO%2', 'unit': 'Pa', 'label': 'Vaccum Q1 right'},
    'Vacuum_Q2_left': {'name': 'GICHVTRANSFO%3', 'unit': 'Pa', 'label': 'Vaccum Q2 left'},
    'Vacuum_Q2_right': {'name': 'GICHVTRANSFO%4', 'unit': 'Pa', 'label': 'Vaccum Q2 right'},
    'Vacuum_Q4_left': {'name': 'GICHVTRANSFO%5', 'unit': 'Pa', 'label': 'Vaccum Q4 left'},
    'Vacuum_Q4_right': {'name': 'GICHVTRANSFO%6', 'unit': 'Pa', 'label': 'Vaccum Q4 right'},
    # PCS power request
    'PCS_Q1_Pow': {'name': 'GICHCONSPCS%1', 'unit': 'kW', 'label': 'PCS Power request Q1'},
    'PCS_Q2_Pow': {'name': 'GICHCONSPCS%2', 'unit': 'kW', 'label': 'PCS Power request Q2'},
    'PCS_Q3_Pow': {'name': 'GICHCONSPCS%3', 'unit': 'kW', 'label': 'PCS Power request Q4'},
    # Phase
    # TODO
   #'': {'name': ' GICHPHASESQ2%3', 'unit': '', 'label': ''}, 
    # IC antennas Capacitor values
    'Capa_Q1_left_upper': {'name': 'GICHCAPA%1', 'unit': 'pF', 'label': 'Capa.Q1 L-U'}, 
    'Capa_Q1_left_lower': {'name': 'GICHCAPA%2', 'unit': 'pF', 'label': 'Capa.Q1 L-L'}, 
    'Capa_Q1_right_upper': {'name': 'GICHCAPA%3', 'unit': 'pF', 'label': 'Capa.Q1 R-U'}, 
    'Capa_Q1_right_lower': {'name': 'GICHCAPA%4', 'unit': 'pF', 'label': 'Capa.Q1 R-L'}, 
    'Capa_Q2_left_upper': {'name': 'GICHCAPA%5', 'unit': 'pF', 'label': 'Capa.Q2 L-U'}, 
    'Capa_Q2_left_lower': {'name': 'GICHCAPA%6', 'unit': 'pF', 'label': 'Capa.Q2 L-L'}, 
    'Capa_Q2_right_upper': {'name': 'GICHCAPA%7', 'unit': 'pF', 'label': 'Capa.Q2 R-U'}, 
    'Capa_Q2_right_lower': {'name': 'GICHCAPA%8', 'unit': 'pF', 'label': 'Capa.Q2 R-L'},
    # IC antennas Capacitor error signals
    'ErrSig_Q1_left_upper': {'name': 'GICHSIGERR%1', 'unit': '', 'label': 'Err.Sig.Q1 L-U'}, 
    'ErrSig_Q1_left_lower': {'name': 'GICHSIGERR%2', 'unit': '', 'label': 'Err.Sig.Q1 L-L'}, 
    'ErrSig_Q1_right_upper': {'name': 'GICHSIGERR%3', 'unit': '', 'label': 'Err.Sig.Q1 R-U'}, 
    'ErrSig_Q1_right_lower': {'name': 'GICHSIGERR%4', 'unit': '', 'label': 'Err.Sig.Q1 R-L'},     
    'ErrSig_Q2_left_upper': {'name': 'GICHSIGERR%5', 'unit': '', 'label': 'Err.Sig.Q2 L-U'}, 
    'ErrSig_Q2_left_lower': {'name': 'GICHSIGERR%6', 'unit': '', 'label': 'Err.Sig.Q2 L-L'}, 
    'ErrSig_Q2_right_upper': {'name': 'GICHSIGERR%7', 'unit': '', 'label': 'Err.Sig.Q2 R-U'}, 
    'ErrSig_Q2_right_lower': {'name': 'GICHSIGERR%8', 'unit': '', 'label': 'Err.Sig.Q2 R-L'},     
    ## LHCD
    'P_LH_tot': {'name': 'SHYBPTOT', 'unit': 'MW', 'label': 'LH total coupled power'}, 
    'P_LH1': {'name': 'SHYBPFORW1', 'unit': 'kW', 'label': 'LH1 coupled power'}, 
    'P_LH2': {'name': 'SHYBPFORW2', 'unit': 'kW', 'label': 'LH2 coupled power'}, 
    'Rc_LH1': {'name': 'SHYBREF1', 'unit': '%', 'label': 'Avg. Refl. Coeff LH1'}, 
    'Rc_LH2': {'name': 'SHYBREF2', 'unit': '%', 'label': 'Avg. Refl. Coeff LH2'},     
    # Impurities (SURVIE)
    'Cu': {'name': 'scu19', 'unit': None, 'label': 'Copper'}, 
    'Fe': {'name': 'SFE15', 'unit': None, 'label': 'Iron'}, 
    }

def smooth(y, window_length=51, polyorder=3):
    return savgol_filter(np.squeeze(y), window_length, polyorder)

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

def scope(pulses, signames, do_smooth=False):
    t_fin_acq = []
    fig, axes = plt.subplots(len(signames), 1, sharex=True)
    if type(axes) is not list:  # case of only one signal -> put axe in a list
        axes = np.array(axes)
    
    for pulse in pulses:
        # end of acquisition time - ignitron
        t_fin_acq.append(pw.tsmat(pulse, 'FINACQ|1')[0] - 32) 
        
        for (sig, ax) in zip(signames, axes):
            if sig['name']:
                y, t = pw.tsbase(pulse, sig['name'], nargout=2)
            else:
                eval_str = f"{sig['fun']}({pulse}) "
                y, t = eval(eval_str)

            if do_smooth:
                y_smooth = smooth(y)
                ax.fill_between(t, 
                    y - (y - y_smooth),
                    y + (y - y_smooth))
                y = y_smooth
            
            ax.plot(t, y, label=f'#{pulse}')
            ax.set_ylabel(f"[{sig['unit']}]")
            ax.text(0.01, 0.85, f"{sig['label']}", color='gray',
                    horizontalalignment='left', transform=ax.transAxes)
    # time axis
    axes[-1].set_xlabel('t [s]')
    axes[-1].set_xlim(-0.5, np.max(t_fin_acq))
    [a.grid(True, alpha=0.2) for a in axes]

    fig.subplots_adjust(hspace=0)
                
    return fig, axes