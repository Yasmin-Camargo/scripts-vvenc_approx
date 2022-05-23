from geratabela1 import *
from geratabela2 import *
from geratabela3 import *

pasta_arquivos = "test-transf-approx-2reps"  #Local da pasta com os arquivos .log

#Tabela completa com os dados dos arquivos.log
codigo_tabela1(f"../arquivos/{pasta_arquivos}", f"../tabelas/tabelas-{pasta_arquivos}/")   

#Tabela com as médias das repetições
codigo_tabela2(f"../tabelas/tabelas-{pasta_arquivos}/")    

#Tabela com o cálculo do BD-RATE e BD-PSNR
codigo_tabela3(f"../tabelas/tabelas-{pasta_arquivos}/")    