'''
Script de Python para rodar uma TC usando o XRMC (Autor DSD)

Foi necessario rodar o script pois, o shell não suporte operações de ponto flutuante, pelo que não 
permite rotação da amostra de menos de um grau.

Para rodar o script: python runCT.py param1 param2 param3
- param1 (targetFolder), diretorio com os arquivos de simulação do XRMC, input.dat e outros
- param2 (folderOutput), diretorio onde serão armazenados os arquivos raw
- param3 (angleStep), passo de rotação numérico

'''

import os
import sys
import math
from datetime import datetime

if len(sys.argv)!=4:
    print("Code need 3 arguments!!!")
    sys.exit()

currentAngle=0
targetFolder=sys.argv[1]
folderOutput=sys.argv[2]
angleStep=float(sys.argv[3])

print(f"Init Angle: {currentAngle}\n Dir: {targetFolder}\n Output: {folderOutput}\n Angle Step:{angleStep}")
os.chdir(targetFolder)
os.system(f"mkdir {folderOutput}")

print("Starting simulation...")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Init =", dt_string)

numProj = math.ceil(360/angleStep)
for i in range(numProj):
    currAngle = i*angleStep
    nextAngle = currAngle + angleStep
    print(f'Processing {i+1}/{numProj}. Angle = {currAngle}')
    os.system("xrmc input.dat >/dev/null")   
    imgName=f"img_{i}.dat"
    os.system(f"mv image.dat {folderOutput}/{imgName}")
    os.system(f"sed -i s'/RotateAll 0 0 0 0 0 -1 {currAngle}/RotateAll 0 0 0 0 0 -1 {nextAngle}/g' quadric.dat")
    #print(f"sed -i s'/RotateAll 0 0 0 0 0 1 {currAngle}/RotateAll 0 0 0 0 0 1 {nextAngle}/g' quadric.dat")

os.system(f"sed -i s'/RotateAll 0 0 0 0 0 -1 {nextAngle}/RotateAll 0 0 0 0 0 -1 0.0/g' quadric.dat")

print("End simulation...")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("End =", dt_string)
