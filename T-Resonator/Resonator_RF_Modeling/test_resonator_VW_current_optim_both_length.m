% ICRF T-Resonator
% 
% Calculates the optimized variable length of both branches in order to
% match the T-resonator.
%
% Once an optimized configuration is found, calculates the current and
% voltage distribution along both branches of the resonator.
%
% Author: J.Hillairet
% July 2013
clear all;

% initial frequency
f=62e6;

% intitial variable length
L_DUT = 20e-3; % Variable - DUT Branch
L_CEA = 76e-3; % Variable - CEA Branch +/- 40mm

% Generate T-resonator configuration
cfg = resonator_configuration_VW_current(f, L_DUT, L_CEA);

% Solve the matching problem in order to minimize the reflected power to
% the source. This gives the optimized dimensions of the variable length
% sections of the T-resonator
cfg_optim = resonator_solve_network_lengths(cfg);

% calculates the current and voltage in the T-resonator for the optimized
% configuration found
[L_CEA, L_DUT, V_CEA, V_DUT, I_CEA, I_DUT] = resonator_voltage_current(cfg_optim);

disp(['Max voltage (CEA)=', num2str(max(abs(V_CEA)))])
disp(['Max current (DUT)=', num2str(max(abs(I_DUT)))])

%% Plotting results
figure(1)
    plot(L_DUT, abs(V_DUT), -L_CEA, abs(V_CEA), 'LineWidth', 2);
    grid on;
    ylabel('Voltage [V]');
    xlabel('L [m]');
    
figure(2)
    plot(L_DUT, abs(I_DUT), -L_CEA, abs(I_CEA), 'LineWidth', 2);
    grid on;
    xlabel('L [m]');
    ylabel('Current [A]');