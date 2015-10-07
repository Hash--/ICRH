function [Zin, Z_CEA, Z_DUT] = resonator_inputImpedance(cfg)
%RESONATOR_INPUTIMPEDANCE 
% Calculate the input impedance of the T-resonator
% 
% INPUT
%  - cfg : T-resonator configuration structure
%
% OUTPUT
%  - Zin : input impedance of the T-resonator
%  - Z_CEA [optionnal] : input impedances at each sections of the CEA
%                       branch, from short to T
%  - Z_DUT [optionnal] : input impedances at each sections of the DUT
%                       branch, from short to T
%
% Author: J.Hillairet, inspired from original A.Argouarch code
% July 2013



% DUT BRANCH

Z_DUT(1)  = TransmissionLine.ZL_2_Zin(cfg.TL(1).L,       cfg.TL(1).Zc, cfg.TL(1).gamma, cfg.short_DUT.Z);
% WARNING
% Dans le code d'Arnaud, l'imp??dance d'entree de la section L1 est calculee
% en utilisant le gamma_cea, soit le gamma de la section L2 (cuivre!). Ce
% qui serait donc equivalent ?? :
%Z_DUT(1)  = TransmissionLine.ZL_2_Zin(cfg.TL(1).L,       cfg.TL(1).Zc, cfg.TL(2).gamma, cfg.short_DUT.Z);

Z_DUT(2)  = TransmissionLine.ZL_2_Zin(cfg.TL(2).L, cfg.TL(2).Zc, cfg.TL(2).gamma, Z_DUT(1)); % previously Zinter
Z_DUT(3)  = TransmissionLine.ZL_2_Zin(cfg.TL(3).L, cfg.TL(3).Zc, cfg.TL(3).gamma, Z_DUT(2));
Z_DUT(4)  = TransmissionLine.ZL_2_Zin(cfg.TL(4).L, cfg.TL(4).Zc, cfg.TL(4).gamma, Z_DUT(3));
Z_DUT(5)  = TransmissionLine.ZL_2_Zin(cfg.TL(5).L, cfg.TL(5).Zc, cfg.TL(5).gamma, Z_DUT(4));

% Z_DUT(6)  = TransmissionLine.ZL_2_Zin(cfg.TL(6).L, cfg.TL(6).Zc, cfg.TL(6).gamma, Z_DUT(5));
% Z_DUT(7)  = TransmissionLine.ZL_2_Zin(cfg.TL(7).L, cfg.TL(7).Zc, cfg.TL(7).gamma, Z_DUT(6));


%Z1_1=ZC_core*(Zcontact+ZC_core*tanh(gamma_cea*L_DUT))/(Zcontact*tanh(gamma_cea*L_DUT)+ZC_core);%%%% trolley AREA ZC=26.82
%Zinter=ZCinterx*(Z1_1+ZCinterx*tanh(gamma_mockup*Linterx))/(Z1_1*tanh(gamma_mockup*Linterx)+ZCinterx); %%% 1.1m in_diam=168.3, ZC=18.62
%Z1_2=ZC2*(Zinter+ZC2*tanh(gamma_copper*(2.1215-Linterx)))/(Zinter*tanh(gamma_copper*(2.1215-Linterx))+ZC2);%%%% L_fix_match = 1021.5 SS
%Z1_3=ZC4*(Z1_2+ZC4*tanh(gamma_copper_2*0.1))/(Z1_2*tanh(gamma_copper_2*0.1)+ZC4);%%%% L = 100mm CU ZC=49.94
%Z1_4=ZC2*(Z1_3+ZC2*tanh(gamma_copper*0.114))/(Z1_3*tanh(gamma_copper*0.114)+ZC2);%%%% L=140mm, CU

% CEA BRANCH

Z_CEA(1) = TransmissionLine.ZL_2_Zin(cfg.TL(9).L,       cfg.TL(9).Zc, cfg.TL(9).gamma, cfg.short_CEA.Z); % 9
% WARNING
% Meme remarque que precedemment : dans son code, Arnaud utilise gamma_cea
% pour decrire la partie o?? est le contact. Or, gamma_cea est en cuivre
% alors que le contact est sur une partie SS (?? verifier pour la branche
% CEA). Du coup si on veut retrouver les resultats d'arnaud, cela donnerait cela :
%Z_CEA(1) = TransmissionLine.ZL_2_Zin(cfg.TL(9).L,       cfg.TL(9).Zc, cfg.TL(2).gamma, cfg.short_CEA.Z);

Z_CEA(2)  = TransmissionLine.ZL_2_Zin(cfg.TL(8).L, cfg.TL(8).Zc, cfg.TL(8).gamma, Z_CEA(1)); % 8

% WARNING
% La section de ligne suivante n'est pas d??crite dans le documentation mais
% existe dans les codes d'Arnaud... Est-ce le bellows ?
%Z_CEA(3)  = TransmissionLine.ZL_2_Zin(0.016      , cfg.TL(3).Zc, cfg.TL(3).gamma, Z_CEA(2));  

Z_CEA(3)  = TransmissionLine.ZL_2_Zin(cfg.TL(7).L, cfg.TL(7).Zc, cfg.TL(7).gamma, Z_CEA(2));% 7
Z_CEA(4)  = TransmissionLine.ZL_2_Zin(cfg.TL(6).L, cfg.TL(6).Zc, cfg.TL(6).gamma, Z_CEA(3));% 6


% Z2_1=ZC_core*(Zcontact+ZC_core*tanh(gamma_cea*L_CEA))/(Zcontact*tanh(gamma_cea*L_CEA)+ZC_core); %%% Trolley AREA
% Z2_2=ZC2*(Z2_1+ZC2*tanh(gamma*1.4975))/(Z2_1*tanh(gamma*1.4975)+ZC2); %%% L2_2 = 1497.5 (SS)
% Z2_3=ZC2*(Z2_2+ZC2*tanh(gamma_copper*0.016))/(Z2_2*tanh(gamma_copper*0.016)+ZC2); %%% L2_3 = 16mm (CU)
% Z2_4=ZC4*(Z2_3+ZC4*tanh(gamma_copper_2*0.1))/(Z2_3*tanh(gamma_copper_2*0.1)+ZC4); %%% L2_4 = 100mm (CU) ZC=49.94
% Z2_5=ZC2*(Z2_4+ZC2*tanh(gamma_copper*0.6612))/(Z2_4*tanh(gamma_copper*0.6612)+ZC2); %%% L2_5 = 661.2mm (CU)

% At T-junction. Impedance are associated in parallel.
Zin = (Z_DUT(end).*Z_CEA(end))./(Z_DUT(end)+Z_CEA(end));



end

