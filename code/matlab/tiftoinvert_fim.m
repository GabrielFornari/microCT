%{
 A rotina "tiftoinvert" percorre um conjunto de arquivos .tif em escala 
de cinza e inverte as tonalidades. Cria um novo arquivo agregando inv ao 
inicio do nome
 
Os nomes dos arquvios devem ter a forma nomeddd.tif onde nome corresponde 
a um sufijo comum a todos os arquivos e ddd um numero consecutivo que
individualiza o arquivo

As variáveis a serem atualizadas são:
    filename: sufijo do nome comum a todos os arquivos
    dig: o numero de digitos do consecutivo dos arquivos
    inicio: numero inicial do consecutivo
    fim: numero final do consecutivo

Autor: Joel Sánchez Domínguez
Data: 12/09/2021
%} 

clear all;
clc;
close all;
inicio=0;
fim=359;
dig=4;

exttif='.tif';
%extbmp='.bmp';
filename='..\ImagesFromGabriel\NRecon tif files\bone_1deg-raw\img_';

for n = inicio:fim
    number='0';
    sn=num2str(n);
    number=strcat(number,sn);
    while length(number) < dig 
        number=strcat('0',number);
    end
    filework=strcat(filename,number);
    fileread=strcat(filework,exttif)
    A = imread(fileread);
    
    A_Net=imadjust(A,[0,1],[1,0]);;
    
    filewrite=strcat('inv',fileread)
    t = Tiff(filewrite,'w');
tagstruct.ImageLength = size(A,1);
tagstruct.ImageWidth = size(A,2);
tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
tagstruct.BitsPerSample = 16;
tagstruct.SamplesPerPixel = 1;
tagstruct.RowsPerStrip = 1746;
tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
tagstruct.Compression = 1;
setTag(t,tagstruct);
write(t,A_Net);
    
end;
clear all;