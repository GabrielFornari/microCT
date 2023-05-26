
import cv2 as cv
import struct as st
import numpy as np
import os, glob
from pathlib import Path

# Header Format
# N. of scattering orders (C int format, 32 bit integer)
# N. of columns (C int format, 32 bit integer)
# N. of rows (C int format, 32 bit integer)
# Pixel size Sx (C double format, 64 bit real)
# Pixel size Sy (C double format, 64 bit real)
# Exposure time in sec. (C double format, 64 bit real)
# Pixel content type (C int format, 32 bit integer)
# N. of energy bins (C int format, 32 bit integer)
# Minimum bin energy (C double format, 64 bit real)
# Maximum bin energy (C double format, 64 bit real)
def readDatImg(fileName):
    file = open(fileName, "rb")

    nScatter = st.unpack('i', file.read(4))[0]
    nCol = st.unpack('i', file.read(4))[0]
    nRow = st.unpack('i', file.read(4))[0]
    st.unpack('3d', file.read(24))
    st.unpack('i', file.read(4))
    nBins = st.unpack('i', file.read(4))[0]
    minBinEnergy = st.unpack('d', file.read(8))[0]
    maxBinEnergy = st.unpack('d', file.read(8))[0]

    img = np.empty((nRow, nCol))
    for iBin in range(nBins):
        for i in range(nRow):
            for j in range(nCol):
                img[i,j] = st.unpack('d', file.read(8))[0]
        
        cv.imwrite(fileName + "_" + str(iBin) + ".png", img)
    
    file.close()

    #return img



if __name__ == "__main__":
    fileName = "image.dat"
    
    readDatImg(fileName)