clear all
close all

inputFolderName = '..\..\XRMC\IBTI\FullDetector\Spectrum_Bone\Out_1\';
outputFolderName = 'imgOut_2\';
prefixFileName = 'img_';

numImgs = length(dir([inputFolderName 'img_*.dat']));

pixX = 200;
pixY = 150;

projCT=zeros(pixX,pixY,numImgs);
for i=1:numImgs
    inputFileName = [inputFolderName prefixFileName num2str(i-1) '.dat'];
    fid = fopen(inputFileName);
    %header = fread(fid, [1 60]);
    imgRead = fread(fid, [1 pixX*pixY], 'double');
    fclose(fid);

    imgOut = reshape(imgRead, pixX, pixY);
    projCT(:,:,i)=imgOut;
end

minVal = min(projCT(:));
projCT = projCT - minVal+1;
maxVal = max(projCT(:));
projCT = uint16((projCT/maxVal)*65535);
    
for i=1:numImgs
    imgOut = projCT(:,:,i);
    outFileName = [outputFolderName prefixFileName num2str(i-1, '%04d') '.tif'];
    t = Tiff(outFileName,'w');
    tagstruct.ImageLength = pixY;
    tagstruct.ImageWidth = pixX;
    tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
    tagstruct.BitsPerSample = 16;
    tagstruct.SamplesPerPixel = 1;
    tagstruct.RowsPerStrip = pixY;
    tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
    tagstruct.Compression = 1;
    setTag(t,tagstruct);
    write(t,imgOut');
    close(t);
end
