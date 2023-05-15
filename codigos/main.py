from geratabela1 import *
from geratabela2 import *
from geratabela3 import *
from bdrate_repeticoes import *
from geragrafico1 import *
from renomear import *

pasta_arquivos = "SIM2023-inter"  #Nome da pasta com os arquivos .log
repeticoes = 5

#Renomeia arquivos
renomear(f"../arquivos/{pasta_arquivos}/")

#Tabela completa com os dados dos arquivos.log
codigo_tabela1(f"../arquivos/{pasta_arquivos}/", f"../tabelas/tabelas-{pasta_arquivos}/")   

#Tabela com as médias das repetições
codigo_tabela2(f"../tabelas/tabelas-{pasta_arquivos}/")    

#Tabela com o cálculo do BD-RATE e BD-PSNR
codigo_tabela3(f"../tabelas/tabelas-{pasta_arquivos}/")    

#Gráfico BD_Rate das Repetições
bdRate_Repet(f"../tabelas/tabelas-{pasta_arquivos}/", repeticoes)

#Gráfico Comparação BD_Rate 
codigo_grafico1(f"../tabelas/tabelas-{pasta_arquivos}/")   

