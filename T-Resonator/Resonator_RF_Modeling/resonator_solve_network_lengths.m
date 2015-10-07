function cfg = resonator_solve_network_length(cfg)
% ICRH T-Resonator
%
% Solve the matching problem in order to find the length of the variable
% section of the CEA and DUT branches.
%
% INPUT
%  - cfg : T-resonator configuration
%
% OUTPUT
%  - cfg : T-resonator optimized configuration
%
% Author: J.Hillairet (from A.Argouarch first issue)
% July 2013


% Search for a first solution of the matching problem
disp('Searching for a first solution...');
L_optim1 = optimize_for_resonator_variable_lengths(cfg);

% Search for a second solution of the matching problem (if any)
% which is not the same that the first one...
disp('Searching for a second solution...');
L_optim2 = optimize_for_resonator_variable_lengths(cfg, L_optim1);

% sort the solutions to take the one with the shorter CEA side 
L_CEA_optim = L_optim1(1);
L_DUT_optim = L_optim1(2); 
if not(isnan(sum(L_optim2))) && (L_optim2(1) < L_optim1(1))
    L_CEA_optim = L_optim2(1);
    L_DUT_optim = L_optim2(2); 
end

% replace the length found in the configuration
cfg.TL(1).L = L_DUT_optim; % DUT
cfg.TL(end).L = L_CEA_optim; % CEA

end % function


function L_optim = optimize_for_resonator_variable_lengths(cfg, L) 
% Optimization routine on T-resonator variable length (CEA and DUT branches)
%
% INPUT
%  - cfg : T-resonator configuration
%  - L [optionnal] : = [L_CEA, L_DUT] : length of the variable sections of
%  the T-resonator. If provided, the routine will search for optimized
%  values different that L. (typically used in case of existing first 
%  solution and looking for a second one)
%
% OUTPUT
%  - L_optim = [L_CEA_optim, L_DUT_optim] : optimized length in order to
%  match the T-resonator or [NaN NaN] is the solution has not been found.

    if nargin == 1 % no previous solution to check vs
        L = [0 0];
    end

    % The routine is running NB_ITER_MAX iterations
    NB_ITER_MAX = 10;

    random_length1 = 0 + (0.5 - 0).*rand(1,NB_ITER_MAX);
    random_length2 = 0 + (0.5 - 0).*rand(1,NB_ITER_MAX);

    optim_options = optimset('Display','off');

    nb_iter = 0;
    solution_found = false;

    while not(solution_found)
        nb_iter = nb_iter+1;

        if nb_iter >= NB_ITER_MAX
            disp('Maximum number of iteration achieved ; solution NOT found !')
            L_optim = [NaN NaN];
            break
        end

        L_CEA0 = random_length1(nb_iter);
        L_DUT0 = random_length2(nb_iter);

        % solve for impedance matching at the input of the T-resonator
        % ie. real(Zin)=30Ohm and imag(Zin)=0
        [L_optim,dummy,exitflag] = fsolve(@(x) optimfun_resonator_impedance_matching(cfg.f,x(1),x(2),cfg), [L_CEA0, L_DUT0], optim_options); 

        
        if (exitflag == 1)
            % disp('A solution has been found :')
            
            % test if the solution found is realitisc
            if L_optim(2)>0 && L_optim(1)>0  && L_optim(1) < 2 && L_optim(2) < 2
                % disp('This solution seems physical')
                
                % test if the solution is idenentical to the one proposed
                % precision requested : 1/10mm, ie 1e-4 mm
                if (abs(L_optim(1) - L(1)) < 1e-4) || (abs(L_optim(2) - L(2)) < 1e-4)
                    disp('Same solution than before. Passing...')
                else
                    solution_found = true;
                end
            else
                %disp('This solution is not physical ! Retrying...')
            end
        end
    end
    
    % Display the solution only if it has been found
    if not(isnan(L_optim))
        disp('Solution found :')
        disp(['L_CEA= ',num2str(L_optim(1)), ' m,  L_DUT= ', num2str(L_optim(2)), ' m.']);
    end
end % function


function A = optimfun_resonator_impedance_matching(f,L_CEA,L_DUT,cfg)
    %  - L=[L_CEA,L_DUT] : lengths of the variable sections of the T-resonator
    %                      L_CEA: Branch 1 , CEA part
    %                      L_DUT: Branch 2 , DUT

    % replace the original parameters by the test ones
    cfg.f = f;
    cfg.TL(1).L = L_DUT;
    cfg.TL(end).L = L_CEA;

    % compute the input impedance of the T-resonator    
    Zin = resonator_inputImpedance(cfg);

    % Because this function aims to be used by an optimization function such as fsolve, 
    % the output is splitted into two for real and imaginary parts

    A(1) = real(30 - Zin); % feeder sous 30 Ohm
    A(2) = imag(Zin);
end