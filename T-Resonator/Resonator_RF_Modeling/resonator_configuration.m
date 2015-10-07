function cfg = resonator_configuration(f,L_DUT, L_CEA,additional_losses)
% ICRF T-Resonator
% 
% cfg = resonator_configuration()
% 
% Generate the configuration structure cfg which contains all 
% the parameters of the T-resonator. This configuration structure can then 
% be used in many other functions (in order to calculate impedance,
% voltage/current, etc.)
% 
% INPUT
%  - f : source frequency [Hz]
%  - L_DUT : Device Under Test branch variable length [m]
%  - L_CEA : CEA branch variable length [m]
%
% OUTPUT
%  - cfg : matlab structure that contains all the T-resonator configuration
%  
% Last Updates:
%  + July 2013, creation
% 
% WARNING : if ones changes the frequency after having generated the
% configuration, the configuration MUST be regenerated ! Otherwise the
% propagation constants will not be re-calculated ! 
%
%
% Author: J.Hillairet

% Source frequency [Hz]
cfg.f=f;

% Input power [W]
cfg.Pin=70e3;

% Short Impedance [Ohm] 
cfg.short_DUT.Z=0.0052; 
cfg.short_CEA.Z=0.0087; 

% relative additional loss coefficient to multiply with the loss in the
% coaxial transmission line, in order to match measurements 
% example : +20% losses --> 1.2
if nargin == 3
    cfg.additional_losses = 0.9796;
else
    cfg.additional_losses = additional_losses; % passed as argument
end

% TL sections impedances
cfg.R = 29.8; % feeder from generator impedance

cfg.ZC2=29.8; % ZC2 for branch1 (the fix)


% Resonator TL section description
%
% Item      Length(mm)	Zc(Ohm) Inner/Outer Diam(m)	Inner   Outer
% ---------------------------------------------------------------------
% L1(DUT)	Variable	26.83   0.140,0.219         SS      SS  CEA extension
% or
% L1(DUT)	Variable	33.14   0.126,0.219         SS      SS  CCFE extenion
% L2 ~?/4	1100        18.72   0.1683,0.23         Cu      Cu
% L3        1021.5      29.8    0.14,0.23           Cu      Cu
% L4        100         49.5    0.1,0.23 ?          Ag      Ag
% L5        114         29.8    0.14,0.23           Ag      Ag
% L6        661.2       29.8    0.14,0.23           Ag      Ag
% L7        100         49.94   ?idemL4?            Ag      Ag
% L8        1497.5      29.8    0.14,0.23           SS      SS
% L9(CEA)   Variable	26.82   0.140,0.219         SS      SS
%
epsilon_r = 1;

% DUT Branch
% Characteristic Impedance of the last DUT section (L1)
% WARNING : CEA : Dout/Dint=219/140 -> 26.82 Ohm 
%           CCFE Home-made : 219/126 -> 33.14 Ohm
cfg.TL(1) = CoaxTransmissionLine(cfg.f, L_DUT,      0.140,  0.219,  epsilon_r,  Constants.conductivity_SS);

cfg.TL(2) = CoaxTransmissionLine(cfg.f, 1100e-3,    0.1683, 0.230,   epsilon_r,  Constants.conductivity_Cu); % was ZCinter=18.62 and Linter=1.1
cfg.TL(3) = CoaxTransmissionLine(cfg.f, 1021.5e-3,  0.140,  0.230,   epsilon_r,  Constants.conductivity_Cu); % 1021.5e-3 = 2.1215-Linter
cfg.TL(4) = CoaxTransmissionLine(cfg.f, 100e-3,     0.100,  0.230,   epsilon_r,  Constants.conductivity_Ag); % was ZC4=49.94 %%% ZC for small reduction copper plating
cfg.TL(5) = CoaxTransmissionLine(cfg.f, 114e-3,     0.140,  0.230,   epsilon_r,  Constants.conductivity_Ag);

% CEA Branch
cfg.TL(6) = CoaxTransmissionLine(cfg.f, 661.2e-3,	0.140,  0.230,   epsilon_r,  Constants.conductivity_Ag); % coude
cfg.TL(7) = CoaxTransmissionLine(cfg.f, 100e-3,     0.100,  0.230,   epsilon_r,  Constants.conductivity_Ag);
% Dans le code d'Arnaud, une section de ligne supplementaire de 0.016m/ZC2/gamma_copper est
% ajoutee ici entre 7 et 8. Cette section n'est pas d??crite dans la documentation D0&D1. 
% Est-ce le bellows ?
cfg.TL(8) = CoaxTransmissionLine(cfg.f, 1497.5e-3,	0.140,  0.230,   epsilon_r,  Constants.conductivity_SS);
cfg.TL(9) = CoaxTransmissionLine(cfg.f, L_CEA,      0.140,  0.219,  epsilon_r,  Constants.conductivity_SS);

% increase the conduction losses in order to match experiment (A.A.)
for idx=1:length(cfg.TL)
    cfg.TL(idx).gamma = cfg.additional_losses*real(cfg.TL(idx).gamma) + j*imag(cfg.TL(idx).gamma);
end

% affiche les impedances caract calcul??e des lignes
%disp(['Zc               gamma'])
%disp([[cfg.TL(:).Zc].',[cfg.TL(:).gamma].']);

