
function [Rc,Z]=calcul_couple(directory,filename);

%directory='TS40574\proto_2007\';
%filename='Zs_TS9a_Profile1.txt';
% Zs_TSproto2_Profile1.txt

%addpath ..\..\MATLAB\IO
[ZZ,xx,yy,x,y,nx,ny]=...
    mread_2D([directory,filename],2,3);
nbport=size(ZZ);
nbport=nbport(1);
Z=zeros(nbport,nbport);
Z=transpose(ZZ(:,:,1)+1i*ZZ(:,:,2));

%toroidal and poloidal phasing
phaset=pi; et=exp(1i*phaset);
phasep=pi; ep=exp(1i*phasep);
%strap feeding
I=[0;0;1;et;ep;ep*et];
%I=[1;-1;-1;1];
V=Z*I;
Prf=0.5*V'*I;
Lstrap=1.08;

Rc=real(Prf)/Lstrap
