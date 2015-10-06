function [signals]=read_text_file(filename,nsignals,nskip);

thefile=fopen(filename);
for iline=1:nskip
        pipo=fgetl(thefile);
end;
signals=fscanf(thefile,'%e',inf);
fclose(thefile);
npoints=length(signals);
nt=npoints/nsignals;
signals=reshape(signals,nsignals,nt)';

return

