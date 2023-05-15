# Script que renomeia arquivos do formato de saída vvenc, para o formato aceito 
# Exemplo:  filt-inter-approx-BasketballDrill_832x480_50-0-0-randomaccess_medium-22-0   (antes)
#           filt_inter_approx-BasketballDrill_832x480_50-0-0-randomaccess_medium-22-0   (depois) 

import os

def renomear(baseDir):
    files = os.listdir(baseDir)

    for fileName in files:
        newFileName = fileName

        isToRename = False

        if '1E-' in newFileName:
            newFileName = newFileName.replace('1E-', '1E_')
            isToRename = True

        if '-approx' in newFileName:
            newFileName = newFileName.replace('-approx', '_approx')
            isToRename = True
        
        if '-inter' in newFileName:
            newFileName = newFileName.replace('-inter', '_inter')
            isToRename = True
        
        if isToRename:
            print(f'Renaming: {fileName} -> {newFileName}')
            os.rename(f'{baseDir}/{fileName}', f'{baseDir}/{newFileName}')
