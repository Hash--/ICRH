function [L_CEA, L_DUT, V_CEA, V_DUT, I_CEA, I_DUT]=resonator_voltage_current(cfg)
% ICRH T-resonator
%
% Calculates the voltage and current distribution in the T-resonator
%
% INPUT
%  - cfg : T-resonator configuration
%
% OUTPUT
%  - 


% calculate the input impedance and input branch impedance
[Zin, Z_CEA, Z_DUT] = resonator_inputImpedance(cfg);

% calculate the voltage and current along the T-resonator branches
[L_CEA, V_CEA, I_CEA] = voltage_current_CEAbranch(cfg, Zin, Z_CEA);
[L_DUT, V_DUT, I_DUT] = voltage_current_DUTbranch(cfg, Zin, Z_DUT);


% 
% % -- snip
% rau_25=(Z2_5-ZC2)/(Z2_5+ZC2);
% Vf_25=Vin/(1+rau_25);
% Vr_25=Vf_25*rau_25;
% V_25=Vf_25*exp(-gamma_copper*0.6612)+Vr_25*exp(gamma_copper*0.6612);
% for t=1:pv_25(2) %
% Z25(t)=ZC2*(Z2_5+ZC2*tanh(gamma_copper*-L_25(t)))/(Z2_5*tanh(gamma_copper*-L_25(t))+ZC2);
% V25(t)=(Vf_25*exp(-gamma_copper*L_25(t))+Vr_25*exp(gamma_copper*L_25(t)));
% I25(t)=V25(t)/Z25(t);
% end
% % --
% 
% rau_24=(Z2_4-ZC4)/(Z2_4+ZC4);
% Vf_24=V_25/(1+rau_24);
% Vr_24=Vf_24*rau_24;
% V_24=Vf_24*exp(-gamma_copper_2*0.1)+Vr_24*exp(gamma_copper_2*0.1);
% for t=1:pv_24(2) %
% Z24(t)=ZC4*(Z2_4+ZC4*tanh(gamma_copper_2*-L_24(t)))/(Z2_4*tanh(gamma_copper_2*-L_24(t))+ZC4);
% V24(t)=(Vf_24*exp(-gamma_copper_2*L_24(t))+Vr_24*exp(gamma_copper_2*L_24(t)));
% I24(t)=V24(t)/Z24(t);
% end
% rau_23=(Z2_3-ZC2)/(Z2_3+ZC2);
% Vf_23=V_24/(1+rau_23);
% Vr_23=Vf_23*rau_23;
% V_23=Vf_23*exp(-gamma_copper*0.016)+Vr_23*exp(gamma_copper*0.016);
% for t=1:pv_23(2) %
% Z23(t)=ZC2*(Z2_3+ZC2*tanh(gamma_copper*-L_23(t)))/(Z2_3*tanh(gamma_copper*-L_23(t))+ZC2);
% V23(t)=(Vf_23*exp(-gamma_copper*L_23(t))+Vr_23*exp(gamma_copper*L_23(t)));
% I23(t)=V23(t)/Z23(t);
% end
% rau_22=(Z2_2-ZC2)/(Z2_2+ZC2);
% Vf_22=V_23/(1+rau_22);
% Vr_22=Vf_22*rau_22;
% V_22=Vf_22*exp(-gamma*1.4975)+Vr_22*exp(gamma*1.4975);
% for t=1:pv_22(2) %
% Z22(t)=ZC2*(Z2_2+ZC2*tanh(gamma*-L_22(t)))/(Z2_2*tanh(gamma*-L_22(t))+ZC2);
% V22(t)=(Vf_22*exp(-gamma*L_22(t))+Vr_22*exp(gamma*L_22(t)));
% I22(t)=V22(t)/Z22(t);
% end
% rau_21=(Z2_1-ZC_core)/(Z2_1+ZC_core);
% Vf_21=V_22/(1+rau_21);
% Vr_21=Vf_21*rau_21;
% V_21=Vf_21*exp(-gamma_cea*x(1))+Vr_21*exp(gamma_cea*x(1));
% for t=1:pv_match(2) % 
% Z21(t)=ZC_core*(Z2_1+ZC_core*tanh(gamma_cea*-L_match(t)))/(Z2_1*tanh(gamma_cea*-L_match(t))+ZC_core);
% V21(t)=(Vf_21*exp(-gamma_cea*L_match(t))+Vr_21*exp(gamma_cea*L_match(t)));
% I21(t)=V21(t)/Z21(t);
% end
% 
% 
% 
% % DUT SIDE
% L_DUT=[0:dz:x(2)]; % DUT
% pv_DUT=size(L_DUT);
% Lginter=[0:dz:Linterx]; % 1.1m of 18.62 Ohms line
% pv_inter=size(Lginter);
% L_12=[0:dz:(2.1215-Linterx)];
% pv_12=size(L_12);
% L_13=[0:dz:0.1];
% pv_13=size(L_13);
% L_14=[0:dz:0.114];
% pv_14=size(L_14);
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% V/Z/I
% rau_14=(Z1_4-ZC2)/(Z1_4+ZC2);
% Vf_14=Vin/(1+rau_14);
% Vr_14=Vf_14*rau_14;
% V_14=Vf_14*exp(-gamma_copper*0.114)+Vr_14*exp(gamma_copper*0.114);
% for t=1:pv_14(2) %
% Z14(t)=ZC2*(Z1_4+ZC2*tanh(gamma_copper*-L_14(t)))/(Z1_4*tanh(gamma_copper*-L_14(t))+ZC2);
% V14(t)=(Vf_14*exp(-gamma_copper*L_14(t))+Vr_14*exp(gamma_copper*L_14(t)));
% I14(t)=V14(t)/Z14(t);
% end
% rau_13=(Z1_3-ZC4)/(Z1_3+ZC4);
% Vf_13=V_14/(1+rau_13);
% Vr_13=Vf_13*rau_13;
% V_13=Vf_13*exp(-gamma_copper_2*0.1)+Vr_13*exp(gamma_copper_2*0.1);
% for t=1:pv_13(2) %
% Z13(t)=ZC4*(Z1_3+ZC4*tanh(gamma_copper_2*-L_13(t)))/(Z1_3*tanh(gamma_copper_2*-L_13(t))+ZC4);
% V13(t)=(Vf_13*exp(-gamma_copper_2*L_13(t))+Vr_13*exp(gamma_copper_2*L_13(t)));
% I13(t)=V13(t)/Z13(t);
% end
% rau_12=(Z1_2-ZC2)/(Z1_2+ZC2);
% Vf_12=V_13/(1+rau_12);
% Vr_12=Vf_12*rau_12;
% V_12=Vf_12*exp(-gamma_copper*(2.1215-Linterx))+Vr_12*exp(gamma_copper*(2.1215-Linterx));
% for t=1:pv_12(2) %
% Z12(t)=ZC2*(Z1_2+ZC2*tanh(gamma_copper*-L_12(t)))/(Z1_2*tanh(gamma_copper*-L_12(t))+ZC2);
% V12(t)=(Vf_12*exp(-gamma_copper*L_12(t))+Vr_12*exp(gamma_copper*L_12(t)));
% I12(t)=V12(t)/Z12(t);
% end
% rau_inter=(Zinter-ZCinterx)/(Zinter+ZCinterx);
% Vf_inter=V_12/(1+rau_inter);
% Vr_inter=Vf_inter*rau_inter;
% V_inter=Vf_inter*exp(-gamma_mockup*Linterx)+Vr_inter*exp(gamma_mockup*Linterx);
% for t=1:pv_inter(2)
% Zint(t)=ZCinterx*(Zinter+ZCinterx*tanh(gamma_mockup*-Lginter(t)))/(Zinter*tanh(gamma_mockup*-Lginter(t))+ZCinterx); %%% WARNIG 
% Vinter(t)=(Vf_inter*exp(-gamma_mockup*Lginter(t))+Vr_inter*exp(gamma_mockup*Lginter(t)));
% Iinter(t)=Vinter(t)/Zint(t); %%% WARNING VARIABLE NAME CHANGE ZINT
% end
% rau_11=(Z1_1-ZC_core)/(Z1_1+ZC_core);
% Vf_11=V_inter/(1+rau_11);
% Vr_11=Vf_11*rau_11;
% V_11=Vf_11*exp(-gamma_cea*x(2))+Vr_11*exp(gamma_cea*x(2));
% for t=1:pv_DUT(2) % with MC contact
% Z11(t)=ZC_core*(Z1_1+ZC_core*tanh(gamma_cea*-L_DUT(t)))/(Z1_1*tanh(gamma_cea*-L_DUT(t))+ZC_core);
% V11(t)=(Vf_11*exp(-gamma_cea*L_DUT(t))+Vr_11*exp(gamma_cea*L_DUT(t)));
% I11(t)=V11(t)/Z11(t);
% end
% 
% z_CEA =0;
% z_DUT= 0;
% V_CEA = 0;
% V_DUT = 0;
% I_CEA = 0;
% I_DUT = 0;

end % function



    function [Lfull,V,I] = voltage_current_branch(Vin, L, Zin, Zc, gamma, rho)
        Vinput_section = Vin;
        Linput_section = 0;
        
        % for all section in the branch, from T to short
        for idBranch=[length(L):-1:1]
            % Calculates impedance, voltage and current along the section's
            % length
            for idL = 1:length(L{idBranch})
                Z{idBranch}(idL) = Zc{idBranch}*(Zin{idBranch}+Zc{idBranch}*tanh(-gamma{idBranch}*L{idBranch}(idL) ))/(Zin{idBranch}*tanh(-gamma{idBranch}*L{idBranch}(idL))+Zc{idBranch});
                V{idBranch}(idL) = Vinput_section*(exp(-gamma{idBranch}*L{idBranch}(idL))+rho{idBranch}*exp(+gamma{idBranch}*L{idBranch}(idL)));
                I{idBranch}(idL) = V{idBranch}(idL)/Z{idBranch}(idL);
                Lfull{idBranch}(idL) = Linput_section + L{idBranch}(idL);
            end
            % the input voltage of the next section is the voltage at the
            % end of the current section
            Vinput_section = V{idBranch}(end);
            Linput_section = Lfull{idBranch}(end);
        end       
    end
    
    % Calculates the voltage and current along the CEA branch of the
    % T-resonator
    function [Lfull, V, I] = voltage_current_CEAbranch(cfg, Zin, Z_CEA)
        % calculates the reflection coefficient at the input of each sections
        
        % Input voltage from input power and feeder impedance
        Vin = sqrt(cfg.Pin*2*cfg.R); % forward voltage
        rho_in = (Zin - cfg.R)/(Zin + cfg.R);
        V0{1} = Vin*(1+rho_in); % total voltage
                
        % spatial sampling 
        dL = 1e-3;    

        % Going from T to short ==> minus in front of L 
        % WARNING : Z_CEA is going from short to T.  
        L{1} = [0:dL:cfg.TL(8).L];         
        I0{1} = V0{1}/Z_CEA(5);
        for idL = 1:length(L{1})
            [V{1}(idL), I{1}(idL)] = TransmissionLine.transferMatrix(-L{1}(idL), V0{1}, I0{1}, cfg.TL(8).Zc, cfg.TL(8).gamma);
            Z{1}(idL) = V{1}(idL)/I{1}(idL);
        end
        Lfull = L{1};

        L{2} = [0:dL:cfg.TL(9).L];
        V0{2} = V{1}(end);
        I0{2} = I{1}(end);
        for idL = 1:length(L{2})
            [V{2}(idL), I{2}(idL)] = TransmissionLine.transferMatrix(-L{2}(idL), V0{2}, I0{2}, cfg.TL(9).Zc, cfg.TL(9).gamma);
            Z{2}(idL) = V{2}(idL)/I{2}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{2}];

        L{3} = [0:dL:16e-3];
        V0{3} = V{2}(end);
        I0{3} = I{2}(end);
        for idL = 1:length(L{3})
            [V{3}(idL), I{3}(idL)] = TransmissionLine.transferMatrix(-L{3}(idL), V0{3}, I0{3}, cfg.ZC2, cfg.TL(3).gamma);
            Z{3}(idL) = V{3}(idL)/I{3}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{3}];


        L{4} = [0:dL:cfg.TL(10).L];
        V0{4} = V{3}(end);
        I0{4} = I{3}(end);
        for idL = 1:length(L{4})
            [V{4}(idL), I{4}(idL)] = TransmissionLine.transferMatrix(-L{4}(idL), V0{4}, I0{4}, cfg.TL(10).Zc, cfg.TL(10).gamma);
            Z{4}(idL) = V{4}(idL)/I{4}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{4}];   


        L{5} = [0:dL:cfg.TL(11).L];
        V0{5} = V{4}(end);
        I0{5} = I{4}(end);
        for idL = 1:length(L{5})
            [V{5}(idL), I{5}(idL)] = TransmissionLine.transferMatrix(-L{5}(idL), V0{5}, I0{5}, cfg.TL(11).Zc, cfg.TL(11).gamma);
            Z{5}(idL) = V{5}(idL)/I{5}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{5}];   

        % convert output into arrays
        V = cell2mat(V);
        I = cell2mat(I);
    end
    
    
    % Calculates the voltage and current along the DUT branch of the
    % T-resonator
    function [Lfull, V, I] = voltage_current_DUTbranch(cfg, Zin, Z_DUT)
        % calculates the reflection coefficient at the input of each sections
        
        % Input voltage from input power and feeder impedance
        Vin = sqrt(cfg.Pin*2*cfg.R); % forward voltage
        rho_in = (Zin - cfg.R)/(Zin + cfg.R);
        V0{1} = Vin*(1+rho_in); % total voltage
                
        % spatial sampling 
        dL = 1e-3;    

        % Going from T to short ==> minus in front of L 
        % WARNING : Z_CEA is going from short to T.        
        L{1} = [0:dL:cfg.TL(7).L];
        I0{1} = V0{1}/Z_DUT(7);
        for idL = 1:length(L{1})
            [V{1}(idL), I{1}(idL)] = TransmissionLine.transferMatrix(-L{1}(idL), V0{1}, I0{1}, cfg.TL(7).Zc, cfg.TL(7).gamma);
            Z{1}(idL) = V{1}(idL)/I{1}(idL);
        end
        Lfull = L{1};

        L{2} = [0:dL:cfg.TL(6).L];
        V0{2} = V{1}(end);
        I0{2} = I{1}(end);
        for idL = 1:length(L{2})
            [V{2}(idL), I{2}(idL)] = TransmissionLine.transferMatrix(-L{2}(idL), V0{2}, I0{2}, cfg.TL(6).Zc, cfg.TL(6).gamma);
            Z{2}(idL) = V{2}(idL)/I{2}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{2}];

        L{3} = [0:dL:cfg.TL(5).L];
        V0{3} = V{2}(end);
        I0{3} = I{2}(end);
        for idL = 1:length(L{3})
            [V{3}(idL), I{3}(idL)] = TransmissionLine.transferMatrix(-L{3}(idL), V0{3}, I0{3}, cfg.TL(5).Zc, cfg.TL(5).gamma);
            Z{3}(idL) = V{3}(idL)/I{3}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{3}];


        L{4} = [0:dL:cfg.TL(4).L];
        V0{4} = V{3}(end);
        I0{4} = I{3}(end);
        for idL = 1:length(L{4})
            [V{4}(idL), I{4}(idL)] = TransmissionLine.transferMatrix(-L{4}(idL), V0{4}, I0{4}, cfg.TL(4).Zc, cfg.TL(4).gamma);
            Z{4}(idL) = V{4}(idL)/I{4}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{4}];   


        L{5} = [0:dL:cfg.TL(3).L];
        V0{5} = V{4}(end);
        I0{5} = I{4}(end);
        for idL = 1:length(L{5})
            [V{5}(idL), I{5}(idL)] = TransmissionLine.transferMatrix(-L{5}(idL), V0{5}, I0{5}, cfg.TL(3).Zc, cfg.TL(3).gamma);
            Z{5}(idL) = V{5}(idL)/I{5}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{5}];   

        
        L{6} = [0:dL:cfg.TL(2).L];
        V0{6} = V{5}(end);
        I0{6} = I{5}(end);
        for idL = 1:length(L{6})
            [V{6}(idL), I{6}(idL)] = TransmissionLine.transferMatrix(-L{6}(idL), V0{6}, I0{6}, cfg.TL(2).Zc, cfg.TL(2).gamma);
            Z{6}(idL) = V{6}(idL)/I{6}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{6}];   
        
        L{7} = [0:dL:cfg.TL(1).L];
        V0{7} = V{6}(end);
        I0{7} = I{6}(end);
        for idL = 1:length(L{7})
            [V{7}(idL), I{7}(idL)] = TransmissionLine.transferMatrix(-L{7}(idL), V0{7}, I0{7}, cfg.TL(1).Zc, cfg.TL(1).gamma);
            Z{7}(idL) = V{7}(idL)/I{7}(idL);
        end
        Lfull = [Lfull,Lfull(end)+L{7}];   
        
        % convert output into arrays
        V = cell2mat(V);
        I = cell2mat(I);
    end