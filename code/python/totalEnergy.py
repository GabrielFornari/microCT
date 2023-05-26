
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

    return img


if __name__ == "__main__":
    folder = "imgs/"
    imgName = ["nosample_sigma005.dat", "nosample_divzero.dat", "nosample_highdiv.dat",
               "nosample_sigmazero.dat", "pmmacylind_sigmazero.dat", "alcylind_sigmazero.dat"]
    
    for name in imgName:
        img = readDatImg(folder + name)
        print(name)
        print(str(img.sum()))
        print(str(100*img.sum()/10**10))
        print(str(img.sum()-10**10))
        print()
