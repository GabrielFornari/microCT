
import cv2 as cv
import tifffile
import struct as st
import numpy as np
import os, glob
from pathlib import Path
import re

# Needed to sort files in numerical order
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

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

def dat2tiffs(folderName):
    [globalMin, globalMax] = findMinMax(folderName)

    outputFolder = folderName + "_tiff"
    os.mkdir(outputFolder)
    imgCounter = 0
    for fileName in sorted(glob.glob(os.path.join(folderName, '*.dat')), key=numericalSort):
        img = readDatImg(fileName)
        img = normImg(img, globalMin, globalMax)
        saveAsTiff(img, outputFolder + "/" + "img" + "_" + str(imgCounter).zfill(4))
        imgCounter += 1



if __name__ == "__main__":
    path = "bone_1deg"
    
    dat2tiffs(path)
