classdef TransmissionLine
    %TRANSMISSIONLINE Class
    %
    % TransmissionLine object
    %
    % Author: J.Hillairet
    % July 2013
    
    properties
        f       % Frequency [Hz]
        L       % Transmission Line Length [m]
        Zc      % Transmission Line Characteristic Impedance [Ohm]
        gamma   % Transmission Line Complex Propagation Constant = alpha+j*beta [1/m]
    end
    
    methods

        function obj=TransmissionLine(f,L,Zc,gamma)
            % Transmission Line object constructor
            %
            % INPUT
            %  - f : frequency [Hz]
            %  - L : Transmission Line Length [m]
            %  - Zc: Transmission Line Characteristic Impedance [Ohm]
            %  - gamma: Transmission Line complex wavenumber = alpha+j*beta
            %
            % OUTPUT
            %  - TransmissionLine Object
            obj.f = f;
            obj.L = L;
            obj.Zc = Zc;
            obj.gamma = gamma;
        end
    end

    methods (Static = true)
        
        function Zin = ZL_2_Zin(L,Z0,gamma,ZL)
            % Calculates the input impedance seen through a lossy transmission line of
            % characteristic impedance Z0 and complex wavenumber gamma=alpha+j*beta
            %
            % Zin = ZL_2_Zin(L,Z0,gamma,ZL)
            %
            % INPUT
            %  - L : length [m] of the transmission line
            %  - Z0: characteristic impedance of the transmission line
            %  - gamma: complex wavenumber associated to the transmission line
            %  - ZL: Load impedance
            %
            % OUTPUT
            %  - Zin: input impedance
            %
            Zin = Z0*(ZL+Z0*tanh(gamma*L))./(ZL*tanh(gamma*L)+Z0);
        end

        
        function [VL, IL] = transferMatrix(L,V0,I0,Z0,gamma)
            % Calculates the voltage and current at a distance L from an
            % initial voltage V0 and current I0 on a transmission line which
            % propagation constant is gamma.
            %
            % [VL, IL] = TransmissionLine.transferMatrix(L,V0,I0,Z0,gamma)
            %
            % L is positive from the load toward the generator
            % 
            % INPUT
            %  - L  : transmission line length [m]
            %  - V0: initial voltage [V]
            %  - I0: initial current [A]
            %  - Z0 : characteristic impedance of the transmission line
            %  - gamma: =alpha+j*beta propagation constant of the transmission
            %           line
            % OUTPUT
            %  - VL: voltage at length L
            %  - IL: current at length L
            %
            TransferMatrix = [cosh(gamma*L), Z0*sinh(gamma*L) ; ...
                              sinh(gamma*L)/Z0, cosh(gamma*L)];
            A = TransferMatrix*[V0;I0];              
            VL = A(1);
            IL = A(2);
        end
        
        function VL = V0f_2_VL(L, V0f, gamma, reflectionCoefficient)
            % Propagation of the voltage at a distance L from the forward
            % voltage and reflection coefficient
            %
            % VL = V0f_2_VL(L, V0f, gamma, reflectionCoefficient)
            %
            % INPUT
            %  - L : Transmission Line Length [m]
            %  - V0f : forward voltage [V]
            %  - gamma : Transmission Line Complex Propagatioon Constant [1]
            %  - reflectionCoefficient : complex reflection coefficient [1]
            %  
            % OUPUT
            %  - VL : (total) voltage at length L 
            %
            VL = V0f*(exp(-gamma*L) + reflectionCoefficient*exp(+gamma*L));
        end
        

    end
end

