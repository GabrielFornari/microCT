
import cv2 as cv
import tifffile
import struct as st
import numpy as np

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

    imgMax = np.max(img)
    imgMin = np.min(img)
    img -= imgMin
    img /= (imgMax-imgMin)

    return img

def readTiffHeader(fileName):
    with tifffile.TiffFile(fileName) as tif:
        #tif_tags = {}
        for tag in tif.pages[0].tags.values():
            name, value = tag.name, tag.value
            print(name + " :: " + str(value))
            #tif_tags[name] = value
            #image = tif.pages[0].asarray()

    img = tifffile.imread(fileName)
    print(img[490:500, 490:500])
    cv.imshow("", (img*255).astype("uint8"))
    cv.waitKey(0);

def tiff2png(inputFile, outputFile):
    img = tifffile.imread(inputFile)
    cv.imwrite(outputFile, img)


# Tiff Header:
# ImageWidth = 1266
# ImageLength = 1746
# BitsPerSample = 16
# Compression = 1
# PhotometricInterpretation = 1
# StripOffsets = (8,)           -> not included
# SamplesPerPixel = 1
# RowsPerStrip = 1746
# StripByteCounts = (4420872,)  -> not included
# PlanarConfiguration = 1
def saveAsTiff(img, fileName):
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) # Normalize img [0, 1]
    tifffile.imsave(fileName, (img*(2**16)).astype("uint16"), compress = 0,
                    photometric = 1, planarconfig = "CONTIG", contiguous = False,
                    rowsperstrip = 1746, 
                    software = '')

if __name__ == "__main__":
    inputFile = "dente_0000.tif"
    img = cv.imread("dente.png", cv.IMREAD_GRAYSCALE)
    saveAsTiff(img, "dente.tif")

    #readTiffHeader(inputFile)
    #print("\n\n")
    inputFile = "dente.tif"
    readTiffHeader(inputFile)

    #fileInput = "image.dat"
    #img = readDatImg(fileInput)
    #saveAsTiff(img, "image.tif")


