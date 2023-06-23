'''
    Script que recebe um diretorio com projecoes tif (0.5 graus de step, 720 imgs)
    faz uma redução do numero de imagens para um menor numero de projeções definido
    pela variável reduce 
'''
import numpy as np
import os, glob
from pathlib import Path

def reduceAngleProjections(inFolderName, redFactor, outFolderName):

    countOri = 0
    countDest = 0
    current = 0
    for fileName in glob.glob(os.path.join(inFolderName, '*.tif')):                
        fileAuxName = Path(fileName).stem
        auxNum = int(fileAuxName[5:])
        if (auxNum != countOri):
            print(f'Process error!!!. File: {auxNum}')
            exit()
        #print(fileName, fileAuxName, auxNum)
        if current == countOri:
            os.system(f'copy {inFolderName}\{fileAuxName}.tif {outFolderName}\img_{countDest:04d}.tif')
            print(f'copy {inFolderName}\{fileAuxName}.tif {outFolderName}\img_{countDest:04d}.tif')
            current = current + redFactor
            countDest += 1
        
        countOri += 1


if __name__ == "__main__":
    path = "..\IBTI_Out_05_tif_prjs"
    reduce = 40
    out = "..\IBTI_Out_20_tif"
    
reduceAngleProjections(path, reduce, out)