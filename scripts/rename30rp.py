# Script que renomeia arquivos de 0-14 para 15-29

import os

baseDir = "/home/pc-hegel/Documentos/novos_experimentos-vvenc/outputs/bitstreams"

files = os.listdir(baseDir)
files.sort()
for fileName in files:
    repeticao = fileName.split("-")[-1]
    
    if int(repeticao.split(".")[0]) < 15:
        new_repeticao = str(int(repeticao.split(".")[0]) + 15) + "." + repeticao.split(".")[1]

        newFileName = fileName.replace(repeticao, new_repeticao)
        
        print(f'Renaming: {fileName} -> {newFileName}')
        os.rename(f'{baseDir}/{fileName}', f'{baseDir}/{newFileName}')
        
        
       