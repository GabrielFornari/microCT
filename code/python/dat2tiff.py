
import cv2 as cv
import tifffile
import struct as st
import numpy as np
import os, glob
from pathlib import Path


def readDatImg(fileName):
    file = open(fileName, "rb")

    nScatter = st.unpack('i', file.read(4))[0]
    nCol = st.unpack('i', file.read(4))[0]
    nRow = st.unpack('i', file.read(4))[0]
    st.unpack('3d', file.read(24))
    st.unpack('2i2d', file.read(24))

    img = np.empty((nRow, nCol))
    for i in range(nRow):
        for j in range(nCol):
            img[i,j] = st.unpack('d', file.read(8))[0]
    file.close()

    return img

def findMinMax(folderName):
    listMin = [];
    listMax = [];
    for fileName in glob.glob(os.path.join(folderName, '*.dat')):
        img = readDatImg(fileName)
        
        listMin.append(img.min())
        listMax.append(img.max())

    return [min(listMin), max(listMax)]

def normImg(img, min, max):
    return (img - min) / (max - min)

def saveAsTiff(img, fileName):
    tifffile.imsave(fileName + ".tif", (img*(2**16)).astype("uint16"), compress = 0,
                    photometric = 1, planarconfig = "CONTIG", contiguous = False,
                    rowsperstrip = 400, 
                    software = '')

def dat2tiff(folderName):
    [globalMin, globalMax] = findMinMax(folderName)

    outputFolder = "tiff"
    os.mkdir(outputFolder)
    for fileName in glob.glob(os.path.join(folderName, '*.dat')):
        img = readDatImg(fileName)
        img = normImg(img, globalMin, globalMax)
        saveAsTiff(img, outputFolder + "/" + Path(fileName).stem)



if __name__ == "__main__":
    path = "cylind/"
    
    dat2tiff(path)
