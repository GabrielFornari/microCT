clear all
close all

inputFileName = 'cylind-raw/image.dat';
outFileName = 'cylind-raw/out.dat';

pixX = 400;
pixY = 400;

fid = fopen(inputFileName);
header = fread(fid, [1 60]);

imgRead = fread(fid, [1 pixX*pixY], 'double');

fclose(fid);

%imgOut = uint16(reshape(imgRead, pixX, pixY));
imgOut = reshape(imgRead, pixX, pixY);
fid = fopen(outFileName, 'w');
fwrite(fid,imgOut,'double');
fclose(fid);

minVal = min(imgOut(:));
imgOut = imgOut - minVal+1;
maxVal = max(imgOut(:));
imgOut = (imgOut/maxVal)*65535;

imgOutInt = uint16(imgOut);
fid = fopen('cylind-raw/outInt.dat', 'w');
fwrite(fid,imgOutInt,'uint16');
fclose(fid);

t = Tiff('cylind-raw/out.tif','w');
tagstruct.ImageLength = pixX;
tagstruct.ImageWidth = pixY;
tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
tagstruct.BitsPerSample = 16;
tagstruct.SamplesPerPixel = 1;
tagstruct.RowsPerStrip = 128;
tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
tagstruct.Compression = 1;
setTag(t,tagstruct);
write(t,imgOutInt');
close(t);

