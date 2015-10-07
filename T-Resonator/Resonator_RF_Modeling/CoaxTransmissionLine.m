classdef CoaxTransmissionLine < TransmissionLine
    % CoaxTransmissionLine class
    %
    % Inherit from TransmissionLine class
    %
    % Author: J.Hillairet
    % July 2013
    
    properties (GetAccess='public')
        Dint    % Inner Diameter [m]
        Dout    % Outer Diameter [m]
        eps_r   % Relative Permittivity of the coaxial dielectric [1]
        sigma   % Coaxial inner AND outer conductors conductivity [S/m]
    end
    
    methods
        
        function obj=CoaxTransmissionLine(frequency, length, Dint, Dout, eps_r, conductorConductivity)
            % Coaxial Transmission Line object constructor
            %
            % INPUT
            %  - frequency : frequency [Hz]
            %  - length : Coaxial Transmission Line Length [m]
            %  - Dint : inner diameter [m]
            %  - Dout : outer diameter [m]
            %  - eps_r: coaxial dielectric relative permittivity [1]
            %  - conductorConductivity: conductivity for *both* conductors [S/m]
            % 
            % OUTPUT
            %  - CoaxialTransmissionLine Object
                        
            Zc = CoaxTransmissionLine.compute_characteristic_impedance(Dint,Dout,eps_r);
            gamma = CoaxTransmissionLine.compute_coaxial_losses(frequency,Dint,Dout,eps_r,conductorConductivity) ...
                        + j*(2*pi*frequency)/Constants.c;
            % Super constructor        
            obj = obj@TransmissionLine(frequency, length, Zc, gamma);
            
            % set Coaxial Properties
            obj.Dint = Dint;
            obj.Dout = Dout;
            obj.eps_r = eps_r;
            obj.sigma = conductorConductivity;
        end
       
    end
    
    % Static methods
    methods (Static = true) 
        function Zc = compute_characteristic_impedance(Dint, Dout, eps_r)
            % Calculates the characteristic impedance of the coaxial line
            % From the dimensions of the inner and outer conductor
            %
            % Zc = compute_characteristic_impedance(Dint, Dout, eps_r)
            % 
            % INPUT
            %  - Dint : inner conductor diameter [m]
            %  - Dout : outer conductor diameter [m]
            %  - eps_r: coaxial dielectric relative permittivity [1]
            %
            % OUTPUT
            %  - Zc : Characteristic Impedance [Ohm]
            %
            assert(Dint>0);
            assert(Dout>0);
            assert(eps_r>0);
          
            Zc = 1/(2*pi)*sqrt(Constants.mu0/Constants.eps0./eps_r).*log(Dout./Dint);
        end  
        
        function alpha = compute_coaxial_losses(f,Dint, Dout, eps_r, sigma)
            % Calculates the loss/meter associated to the transmission line
            % 
            % NB: Inner and outer conductor are suposed to be of the same kind of
            % conductor
            % 
            % Source: http://www.microwaves101.com/encyclopedia/Coaxloss.cfm 
            % or Pozar p.95
            %
            % INPUT
            %  - f    : frequency [Hz]
            %  - Dint : inner conductor diameter [m]
            %  - Dout : outer conductor diameter [m]
            %  - eps_r: coaxial dielectric relative permittivity [1]
            %  - sigma: conductors conductivity [S/m]
            % 
            % OUTPUT
            %  - alpha : attenuation constant [Neper/m]
            %
            
            % RF sheet resistance of conductors. 
            omega = 2*pi*f;
            Rs = sqrt(omega.*Constants.mu0/(2*sigma));
            % Characteristic impedance
            Zc = CoaxTransmissionLine.compute_characteristic_impedance(Dint, Dout, eps_r);
            
            alpha = Rs/pi.*(1/Dint + 1./Dout) ./ (2*Zc);
        end
        
        function [phi_inner, phi_outer] = compute_conductionLosses_heatFluxes(f,Dint,Dout,sigma,Pin,gamma)
            phi_inner = 0;
            phi_outer = 0;
        end
        
    end % methods
    



end
