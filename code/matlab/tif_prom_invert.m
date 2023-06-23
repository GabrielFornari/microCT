%{
A rotina "tif_prom_invert" percorre um conjunto de arquivos .tif em escala 
de cinza, agrupa segundo o parâmetro Nimgpg para encontrar a media dessas 
imagens  e inverte as tonalidadesde cinza da imagen media. Cria um novo 
de saida arquivo agregando inv a base do nome
 
Os nomes dos arquvios devem ter a forma nomeXXX_Y.tif onde nome corresponde 
a um sufijo comum a todos os arquivos, ddd um numero consecutivo que
indica o grau a que corresponde essa Rx e Y é um consecutivo que indica o
numero da radiografia no grau XXX.

As variáveis a serem atualizadas são:
    filename: sufijo do nome comum a todos os arquivos
    dig: o numero de digitos do consecutivo do grau dos arquivos
    inicio: numero inicial do consecutivo do grau
    fim: numero final do consecutivo do grau
    Nimgpg: numero de images per grau

Autor: Joel Sánchez Domínguez
Data: 12/09/2021
%}

clc;
clear all;
close all;
filename='fdente_';
inicio=0;
fim=359;
dig=3;
Nimgpg=5;
X=1746;%Altura da Imagem
Y=1266;%LArgura da Imagem
exttif='.tif';

for n = inicio:fim
    %number='0';
    number=num2str(n);
    %number=strcat(number,sn);
    while length(number) < dig 
        number=strcat('0',number);
    end
    filework=strcat(filename,number);
    filework1=strcat(filework,'_');
    A_prom=uint16(zeros(1746,1266));
    for k =1 :Nimgpg
        filework2=strcat(filework1,num2str(k));
        fileread=strcat(filework2,exttif);
        A = imread(fileread);
        A_prom=A_prom+(A/Nimgpg);
    end
    
    A_Net=imadjust(A_prom,[0,1],[1,0]);
    
    filewrite=strcat('invprom',filework1);
    filewrite=strcat(filewrite,exttif)
    t = Tiff(filewrite,'w');
    tagstruct.ImageLength = size(A_Net,1);
    tagstruct.ImageWidth = size(A_Net,2);
    tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
    tagstruct.BitsPerSample = 16;
    tagstruct.SamplesPerPixel = 1;
    tagstruct.RowsPerStrip = 1746;
    tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
    tagstruct.Compression = 1;
    setTag(t,tagstruct);
    write(t,A_Net);
    
end
clear all;

