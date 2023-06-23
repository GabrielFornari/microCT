'''
Este arquivo foi uma melhoria ao código de Gabriel, incluindo:

- A função de ler uma imagem sem cabecalho que venha do do XRMC

- A leitura da imagem com uma única operação, não precisa ser valor a valor por ser um
arquivo binário

!!! Falta

- As imagens são lidas duas vezes, uma vez para ler os límites de normalização, e de novo
para criar o tif, é mais eficiente ler uma vez e armazenar as projecoes em uma matriz 
tridimensional, normalizar e gravar as projeçoes tif (ver como esta feito no matlab)

- Aparentemente os resultados são levemente diferentes do Matlab, criar uma imagem no Matlab e 
outra no Python e verificar as diferenças

'''
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

def readDatImgNoHeader(fileName, nCol, nRow):
    file = open(fileName, "rb")    

    img = np.fromfile(fileName, 'float64', count=nCol*nRow)
    img = img.reshape((nCol, nRow))

    file.close()

    return img

def findMinMax(folderName):
    listMin = [];
    listMax = [];
    for fileName in glob.glob(os.path.join(folderName, '*.dat')):
        #img = readDatImg(fileName)
        img = readDatImgNoHeader(fileName, 150, 50)
        
        listMin.append(img.min())
        listMax.append(img.max())

    return [min(listMin), max(listMax)]

def normImg(img, min, max):
    return (img - min) / (max - min)

def saveAsTiff(img, fileName):
    tifffile.imsave(fileName + ".tif", (img*(2**16)).astype("uint16"), 
                    photometric = 1, planarconfig = "CONTIG", contiguous = False,
                    rowsperstrip = 150, 
                    software = '')

def dat2tiff(folderName):
    [globalMin, globalMax] = findMinMax(folderName)

    outputFolder = "tiff"
    os.mkdir(outputFolder)
    for fileName in glob.glob(os.path.join(folderName, '*.dat')):
        #img = readDatImg(fileName)
        img = readDatImgNoHeader(fileName, 150, 200)
        img = normImg(img, globalMin, globalMax)
        fileAuxName = Path(fileName).stem
        numAuxFile = int(fileAuxName[4:])
        fileOutName = 'img_' +  f'{numAuxFile:04d}'
        #print(fileName, fileAuxName, numAuxFile, f'{numAuxFile:04d}', fileOutName)
        saveAsTiff(img, outputFolder + "/" + fileOutName)



if __name__ == "__main__":
    path = "D:\workspace\XRMC\IBTI\FullDetector\Spectrum_Al\Out_Spec_1"
    
dat2tiff(path)