%fileName='C:\Users\fmasm\Desktop\SharedVBox\Simulations_outputs\TestClassic\array_3d.bin' 
%folder='C:\Users\fmasm\Desktop\SharedVBox\Simulations_outputs\TestVRT\output\';
clear all
close all

% Load background
pix_X=128*6;
pix_Y=128;
fileName="C:\Users\fmasm\Dropbox\CEPEDI WORK\Simulations\QA6 output\backgound_PhantomQA_00_120_1E9_000.dat"
fid = fopen(fileName);
bckg=fread(fid,'single');
fclose(fid);
bckg=reshape(bckg,pix_X,pix_Y);


folder='C:\Users\fmasm\Dropbox\CEPEDI WORK\Simulations\QA6 output\';

%folder='C:\Users\fmasm\Desktop\SharedVBox\QA2 simulation\output\'
info=dir([folder 'PhantomQA_00_120_1E9_*.dat']);

z=length(info);
projCT=zeros(pix_X,pix_Y,z);

for i=[1:z]
   fileName=cat(2, folder, info(i).name)
   fid = fopen(fileName);
   data=fread(fid,'single');
   fclose(fid);
   data=reshape(data,pix_X,pix_Y);
   indice=str2num(fileName(end-6:end-4))+1;
   projCT(:,:,indice)=data;

end

% normalizing
%projCT=projCT-bckg;
projCTnorm=projCT-min(projCT(:))+1;
projCTnorm=uint16(projCTnorm/max(projCTnorm(:))*65535);

projCT=projCTnorm;
save('C:\Users\fmasm\Dropbox\CEPEDI WORK\Programas\Felix Matlab Reconstruction Program\projCT_QA6.mat','projCT');


%% exporting as Tif

formatSpec = '%04d';
folder='C:\Users\fmasm\Dropbox\CEPEDI WORK\Programas\FelixSimulationQA6bckg\';
for i=[1:z]    
    A=squeeze(projCTnorm(:,:,i));
    filewrite=[folder 'QA6_bckg_' num2str(i-1,formatSpec)  '.tif']
    t = Tiff(filewrite,'w');
    tagstruct.ImageLength = size(A,2);
    tagstruct.ImageWidth = size(A,1);
    tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
    tagstruct.BitsPerSample = 16;
    tagstruct.SamplesPerPixel = 1;
    tagstruct.RowsPerStrip = 128;
    tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
    tagstruct.Compression = 1;
    setTag(t,tagstruct);
    write(t,A');
    close(t);

    
end







