
import cv2 as cv
import tifffile
import struct as st
import numpy as np
import os, glob
from pathlib import Path
import re

# Need to sort files in numerical order
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def readDatImg(fileName, nRow = 0, nCol = 0):
    if nRow == 0 or nCol == 0:
        hasHeader = True
    else:
        hasHeader = False
    
    file = open(fileName, "rb")

    if hasHeader:
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

def getDatSize(fileName):
    file = open(fileName, "rb")

    nScatter = st.unpack('i', file.read(4))[0]
    nCol = st.unpack('i', file.read(4))[0]
    nRow = st.unpack('i', file.read(4))[0]
    
    return [nRow, nCol]

def normImg(img, min, max):
    return (img - min) / (max - min)


def makeSinogram(folderName, row, nRow = 0, nCol = 0):
    if nRow == 0 or nCol == 0:
        hasHeader = True
    else:
        hasHeader = False
    
    nImgs = len(glob.glob(os.path.join(folderName, '*.dat')))
    fileName = glob.glob(os.path.join(folderName, '*.dat'))[0]
    
    if hasHeader:
        img = readDatImg(fileName)
    else:
        img = readDatImg(fileName, nRow, nCol)
    
    globalMin = img.min()
    globalMax = img.max()
    
    nCol = len(img[0])
    sinogram = np.empty((nImgs, nCol))
    
    iImage = 0
    for fileName in sorted(glob.glob(os.path.join(folderName, '*.dat')), key=numericalSort):
        
        if hasHeader:
            img = readDatImg(fileName)
        else:
            img = readDatImg(fileName, nRow, nCol)
        
        globalMin = min(globalMin, img.min())
        globalMax = max(globalMax, img.max())
        
        sinogram[iImage, :] = img[row, :]
        iImage += 1
        
    return normImg(sinogram, globalMin, globalMax)

def saveAsPNG(fileName, img):
    img = (img*255).astype("uint8")
    cv.imwrite(fileName + ".png", img)


if __name__ == "__main__":
    folder = "multi_4_cylind_rotate"
    
    sinogram = makeSinogram(folder, 75)
    
    saveAsPNG(folder + "_sinogram", sinogram)
    