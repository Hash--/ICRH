function [signals,xx,yy,x,y,nx,ny]=...
    mread_2D(map_filename,nbsignals,nskip)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% [signals,xx,yy,x,y,nx,ny]=mread_2D(map_filename,nbsignals,nskip)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Loads 2D maps on uniform grid from text file map_filename
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Data is either stored as follows...
% nskip lines of header, skippped when reading
% x(1) y(1) signals(1,1,1) signals(1,1,2) ... signals(1,1,nbsignals)
% x(1) y(2) signals(2,1,1) signals(1,1,2) ... signals(2,1,nbsignals)
% x(1) y(3) signals(3,1,1) signals(1,1,2) ... signals(3,1,nbsignals)
% ...
% x(1) y(ny) signals(ny,1,1) signals(ny,1,2) ... signals(ny,1,nbsignals)
% x(2) y(1) signals(1,2,1) signals(1,2,2) ... signals(1,2,nbsignals)
% x(2) y(2) signals(2,2,1) signals(2,2,2) ... signals(2,2,nbsignals)
% ...
% x(2) y(ny) signals(ny,2,1) signals(ny,2,2) ... signals(ny,2,nbsignals)
% x(3) y(1) signals(1,3,1) signals(1,3,2) ... signals(1,3,nbsignals)
% x(3) y(2) signals(2,3,1) signals(2,3,2) ... signals(2,3,nbsignals)
% ...
% x(nx) y(ny) signal(ny,nx,1) signal(ny,nx,2) ... signal(ny,nx,nbsignals)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ... or as follows
% nskip lines of header, skippped when reading
% x(1) y(1) signals(1,1,1) signals(1,1,2) ... signals(1,1,nbsignals)
% x(2) y(1) signals(1,2,1) signals(1,2,2) ... signals(1,3,nbsignals)
% x(3) y(1) signals(1,3,1) signals(1,3,2) ... signals(1,3,nbsignals)
% ...
% x(nx) y(1) signals(1,nx,1) signals(1,nx,2) ... signals(1,nx,nbsignals)
% x(1) y(2) signals(2,1,1) signals(2,1,2) ... signals(2,1,nbsignals)
% x(2) y(2) signals(2,2,1) signals(2,2,2) ... signals(2,2,nbsignals)
% ...
% x(nx) y(2) signals(2,nx,1) signals(2,nx,2) ... signals(2,nx,nbsignals)
% x(1) y(3) signals(3,1,1) signals(3,1,2) ... signals(3,1,nbsignals)
% x(2) y(3) signals(3,2,1) signals(3,2,2) ... signals(3,2,nbsignals)
% ...
% x(nx) y(ny) signal(ny,nx,1) signal(ny,nx,2) ... signal(ny,nx,nbsignals)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% output data
% signals             3D matrix(ny,nx,nbsignals)
% xx                  vector(1,nx)
% yy                  vector(1,ny)
% x                   matrix(ny,nx)
% y                   matrix(ny,nx)
% nx                  scalar
% ny                  scalar
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Latest update by L. COLAS 05-03-2012
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% addpath D:\Documents and settings\LC139825\Mes documents\MATLAB\IO

if nargin()<3
    nskip=0;
end;

[buffer]=read_text_file(map_filename,nbsignals+2,nskip);

x=buffer(:,1);
y=buffer(:,2);

if (y(2)==y(1))
    nx=find(diff(x)<0.0); nx=nx(1);
    ny=length(y)/nx;
    x=transpose(reshape(x,nx,ny));
    y=transpose(reshape(y,nx,ny));
    signals=zeros(ny,nx,nbsignals);
    for nsignal=1:nbsignals
        signals(:,:,nsignal)=transpose(reshape(buffer(:,nsignal+2),nx,ny));
    end;  
else
    ny=find(diff(y)<0.0); ny=ny(1);
    nx=length(x)/ny;
    x=reshape(x,ny,nx);
    y=reshape(y,ny,nx);
    signals=zeros(ny,nx,nbsignals);
    for nsignal=1:nbsignals
        signals(:,:,nsignal)=reshape(buffer(:,nsignal+2),ny,nx);
    end;  
end;
xx=mean(x,1);
yy=mean(y,2);

return;