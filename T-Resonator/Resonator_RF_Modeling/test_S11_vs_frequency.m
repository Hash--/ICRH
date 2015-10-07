% ICRH T-resonator
%
% Plot the S11 vs frequency for a resonator configuration
%
% Author: J.Hillairet
% July 2013
clear all;

% Length L_CEA, L_DUT
L_CEA = 0.10974;
L_DUT = 0.040212;
L_CEA= 0.11245;
L_DUT= 0.041707;


% For each frequency point, generates the T-resonator configuration and
% calculates the input impedance at the feeder
f = linspace(60e6, 65e6, 1001);
for idx=1:length(f)
    cfg = resonator_configuration(f(idx), L_DUT, L_CEA);
    
    Zin(idx) = resonator_inputImpedance(cfg);
end

% Z to S
S11 = (Zin - cfg.R)./(Zin + cfg.R);

% Plotting results
figure(1)   
    plot(f/1e6, 10*log(abs(S11)), 'LineWidth', 2);
    xlabel('f [MHz]')
    ylabel('S11 [dB]')
    grid on;
    
% calculates the Q-factor of the resonator
% find the -3dB frequency band points 
[dummy,idx_res] = min(abs(S11));
f_res = f(idx_res)
[dummy, idx_f1] = min( abs(10*log(abs(S11(1:idx_res))) + 3) );
[dummy, idx_f2] = min( abs(10*log(abs(S11(idx_res:end))) + 3) );
delta_f = f(idx_f2 + idx_res) - f(idx_f1);

Qfactor = f_res/delta_f;
disp(['T-resonator Q-factor = ', num2str(Qfactor)]);
