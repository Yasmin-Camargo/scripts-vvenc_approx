#Scripit que busca os campos: YUV-PSNR, Bitrate, Execution Time em um arquivo .log e exporta para um arquivo .csv

import os

#FUNÇÕES:
def remove_espaco(linha):
     linha = linha.strip()
     linha = linha.replace ('       ', ';')
     linha = linha.replace ('      ', ';')
     linha = linha.replace ('     ', ';')
     linha = linha.replace ('    ', ';')
     linha = linha.replace ('   ', ';')
     linha = linha.replace (' ', ';')
     linha = linha.split (';')
     return (linha)

def codigo_tabela1(pasta_arquivos, pasta_tabelas): #Tabela 1
     if os.path.isdir(pasta_tabelas):
          tabela1 = open(f"{pasta_tabelas}complete_data.csv", "w")
     else:
          os.mkdir(pasta_tabelas)
          tabela1 = open(f"{pasta_tabelas}complete_data.csv", "w")
     
     tabela1.write("Approx Module;VVenC Profile;Video;Read BER;Write BER;QP;Rep.;YUV-PSNR;Bitrate;Execution Time\n")

     todos_arquivos = os.listdir(pasta_arquivos) #Obtendo nomes dos arquivos
     todos_arquivos.sort()
     #Extraindo informações da codificação utilizada no nome do arquivo:
     for nome_arquivo in todos_arquivos:     
          dados_nome_arquivo = nome_arquivo
          dados_nome_arquivo = dados_nome_arquivo.split('-')
          tabela1.write(f'{dados_nome_arquivo[0]};') #Approx Module
          tabela1.write(f'{dados_nome_arquivo[4]};') #VVenC Profile
          tabela1.write(f'{dados_nome_arquivo[1]};') #Video
          tabela1.write(f'{dados_nome_arquivo[2]};') #Read BER
          tabela1.write(f'{dados_nome_arquivo[3]};') #Write BER
          tabela1.write(f'{dados_nome_arquivo[5]};') #QP
          tabela1.write(f'{dados_nome_arquivo[6][0:int(len(dados_nome_arquivo[6]))-4]};') #Rep
          
          #Extraindo informações dentro do arquivo .log
          linha_dados=0
          arquivo_log = open(f'{pasta_arquivos}/{nome_arquivo}', "r")
          for ver_arquivo_log in arquivo_log:
               if (linha_dados==1):     #linha com os dados PSNR e bitrate
                    gravar = remove_espaco(ver_arquivo_log) 
                    tabela1.write(f'{float(gravar[6])};') #YUV-PSNR
                    tabela1.write(f'{float(gravar[2])};') #Bitrate   
                    linha_dados=0
               
               if (("Total Frames" in ver_arquivo_log) == True):
                    linha_dados=1
                    
               if (("Total Time:" in ver_arquivo_log) == True):  #linha com o tempo
                    gravar2 = remove_espaco(ver_arquivo_log)
                    tabela1.write(f'{float(gravar2[2])}') #Execution Time
                    
          tabela1.write('\n')
          
     tabela1.close()
     arquivo_log.close()
