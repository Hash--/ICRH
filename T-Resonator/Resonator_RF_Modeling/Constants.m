classdef Constants
    %CONSTANTS 
    properties (Constant)
        % Speed of light [m/s]
        c = 299792458;
        % Vacuum properties
        mu0 = 4*pi*1e-7;
        eps0= 8.854187817e-12; 
        Z0 = sqrt(Constants.mu0/Constants.eps0);
        
        % Conductors conductivity [Siemens/m]
        conductivity_SS = 1.32e6; % 1.45e6 in Wikipedia
        conductivity_Cu = 5.8e7; % Annealed copper.  5.96e7 for pure Cu in Wikipedia
        conductivity_Ag = 6.3e7; % Wikipedia

    end
end

