# Script que renomeia arquivos do formato de saída vvenc, para o formato aceito 
# Exemplo:  filt-inter-approx-BasketballDrill_832x480_50-0-0-randomaccess_medium-22-0   (antes)
#           filt_inter_approx-BasketballDrill_832x480_50-0-0-randomaccess_medium-22-0   (depois) 

import os

def renomear(baseDir):
    files = os.listdir(baseDir)

    for fileName in files:
        newFileName = fileName

        isToRename = False
        
        if 'intra_orig_approx-rw' in newFileName:
            newFileName = newFileName.replace('intra_orig_approx-rw', 'intra_orig_approx_rw')
            isToRename = True
            
        if 'intra-orig-approx-rw' in newFileName:
            newFileName = newFileName.replace('intra-orig-approx-rw', 'intra_orig_approx_rw')
            isToRename = True
            
        if '10E-' in newFileName:
            newFileName = newFileName.replace('10E-', '10E_')
            isToRename = True
            
        if '-approx' in newFileName:
            newFileName = newFileName.replace('-approx', '_approx')
            isToRename = True
        
        if 'intra-' in newFileName:
            newFileName = newFileName.replace('intra-', 'intra_')
            isToRename = True
        
        if isToRename:
            print(f'Renaming: {fileName} -> {newFileName}')
            os.rename(f'{baseDir}/{fileName}', f'{baseDir}/{newFileName}')

