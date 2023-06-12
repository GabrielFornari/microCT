%fileName='C:\Users\fmasm\Desktop\SharedVBox\Simulations_outputs\TestClassic\array_3d.bin' 
%folder='C:\Users\fmasm\Desktop\SharedVBox\Simulations_outputs\TestVRT\output\';
clear all
close all

% Load background
pix_X=200;
pix_Y=150;
%fileName="C:\Users\fmasm\Dropbox\CEPEDI WORK\Simulations\QA6 output\backgound_PhantomQA_00_120_1E9_000.dat"
%fid = fopen(fileName);
%bckg=fread(fid,'single');
%fclose(fid);
%bckg=reshape(bckg,pix_X,pix_Y);


folder='D:\workspace\XRMC\IBTI\FullDetector\Spectrum_Bone\Out_2\';

%folder='C:\Users\fmasm\Desktop\SharedVBox\QA2 simulation\output\'
info=dir([folder 'img_*.dat']);

z=length(info);
projCT=zeros(pix_X,pix_Y,z);

for i=[1:z]
   fileName=cat(2, folder, info(i).name)
   fid = fopen(fileName);
   data=fread(fid,'double');
   fclose(fid);
   data=reshape(data,pix_X,pix_Y);
   indice=str2num(info(i).name(5:end-4))+1%str2num(fileName(end-6:end-4))+1;
   projCT(:,:,indice)=data;

end

% normalizing
%projCT=projCT-bckg;
projCTnorm=projCT-min(projCT(:))+1;
projCTnorm=uint16(projCTnorm/max(projCTnorm(:))*65535);

projCT=projCTnorm;
save('D:\workspace\XRMC\IBTI\FullDetector\Spectrum_Bone\Out_2_Tif_Matlab_Felix\projCT.mat','projCT');


%% exporting as Tif

formatSpec = '%04d';
folder='D:\workspace\XRMC\IBTI\FullDetector\Spectrum_Bone\Out_2_Tif_Matlab_Felix\';
for i=[1:z]    
    A=squeeze(projCTnorm(:,:,i));
    filewrite=[folder 'img_' num2str(i-1,formatSpec)  '.tif']
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







