% Plot the coupling resistance of the antenna vs distance to cut-off

fileNames = {'Zs_TSproto2_Profile1.txt', ...
             'Zs_TSproto2_Profile2.txt', ...
             'Zs_TSproto2_Profile3.txt', ...
             'Zs_TSproto2_Profile4.txt', ...
             'Zs_TSproto2_Profile5.txt', ...
             'Zs_TSproto2_Profile6.txt', ...
             'Zs_TSproto2_Profile7.txt', ...
             'Zs_TSproto2_Profile8.txt'};

for idx = 1:length(fileNames)
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
    
    V2=[1;-1;-1;1];
    I2=inv(Z)*V;
    Prf2=0.5*V2'*I2;
    Rc2=real(Prf)/Lstrap
end

Rc