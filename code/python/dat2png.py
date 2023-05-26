
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

import cv2 as cv
import os
import numpy as np
import struct as st


def dat2png(fileName):
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

    imgMax = np.max(img)
    imgMin = np.min(img)
    img -= imgMin
    img /= (imgMax-imgMin)

    return (img*255).astype("uint8")


def my_datfiles_from(folder):
    fileNames = []
    for fileName in os.listdir(folder):
        if fileName.endswith(".dat"):
            fileNames.append(fileName[0:-4])
    return fileNames


if __name__ == "__main__":
    folderInput = "test_fullSpec_allLines/"
    folderOutput = "png_fullSpec_allLines/"

    imgNames = my_datfiles_from(folderInput)
    for imgName in imgNames:
        print("Converting " + imgName)
        img = dat2png(folderInput + imgName + ".dat")
        cv.imwrite(folderOutput + imgName + ".png", img)
        