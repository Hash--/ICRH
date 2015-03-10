clear all;
% Plot the coupling resistance of the antenna vs distance to cut-off
       
fileNames = {'Zs_TSproto12_55MHz_LAD6.txt', ...
             'Zs_TSproto12_55MHz_LAD6-2.5cm.txt', ...
             'Zs_TSproto12_55MHz_LAD6-5cm.txt', ...
             'Zs_TSproto12_55MHz_LAD9.txt', ...
             'Zs_TSproto12_55MHz_LAD9-2.5cm.txt', ...
             'Zs_TSproto12_55MHz_LAD9-5cm.txt', ...
             'Zs_TSproto12_55MHz_LAD12.txt', ...
             'Zs_TSproto12_55MHz_LAD12-2.5cm.txt', ...
             'Zs_TSproto12_55MHz_LAD12-5cm.txt'};

for idx = 1:size(fileNames,2)
    data = importdata(fileNames{idx});

    NbPorts = length(data);
    ReZ = data(:,3);
    ImZ = data(:,4);
    Z = transpose(reshape(ReZ+i*ImZ, sqrt(NbPorts), sqrt(NbPorts)));


    %toroidal and poloidal phasing
    phaset=pi; et=exp(1i*phaset);
    phasep=pi; ep=exp(1i*phasep);
    %strap feeding
    I=[1;-1;-1;1];
    V=Z*I;
    Prf=0.5*V'*I;
    Lstrap=4*0.27;

    Rc(idx)=real(Prf)/Lstrap;
end

set(gca, 'FontSize', 14)
R=[3,2.975,2.95];
Rc = (reshape(Rc, 3,3));
plot(R, Rc, '.', 'MarkerSize', 25)

legend('LAD=6e19 m^{-2}', 'LAD=9e19 m^{-2}', 'LAD=12e19 m^{-2}')
grid on
xlabel('Rant [m]')
ylabel('Coupling Resistance [Ohm/m]')

set(gca, 'xLim', [2.89, 3.05])
line([2.93, 2.93], [0,6], 'Color', 'k', 'LineStyle', '--', 'LineWidth', 2)
