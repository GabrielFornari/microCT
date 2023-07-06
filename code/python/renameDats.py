
import os, glob
import re

# Needed to sort files in numerical order
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def genarateNewName(fileName):
    fileNameNumber = fileName.split("_")[1]
    
    while len(fileNameNumber) < 8:
        fileNameNumber = '0' + fileNameNumber
    
    return "img_" + fileNameNumber


def renameDatsIn(folderName):
    for fileName in glob.glob(os.path.join(folderName, '*.dat')):
        newFileName = genarateNewName(fileName.split("/")[1])
        os.rename(fileName, folderName + "/" + newFileName)
        
        
if __name__ == "__main__":
    path = "multi_2_cylind_clockwise"
    
    renameDatsIn(path)
    