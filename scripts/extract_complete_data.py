#Script que busca os campos: YUV-PSNR, Bitrate, Execution Time em um arquivo .log e exporta para um arquivo .csv

import os

def remove_espaco(linha):
     linha = linha.strip()
     linha = linha.replace ('	        ', ';')
     linha = linha.replace ('	       ', ';')
     linha = linha.replace ('	      ', ';')
     linha = linha.replace ('      ', ';')
     linha = linha.replace ('     ', ';')
     linha = linha.replace ('    ', ';')
     linha = linha.replace ('   ', ';')
     linha = linha.replace (' ', ';')
     linha = linha.split (';')
     return (linha)

def complete_data(pasta_arquivos, pasta_tabelas, erros_SRAM, injection_calls): #Tabela 1
     if os.path.isdir(pasta_tabelas):
          tabela1 = open(f"{pasta_tabelas}complete_data.csv", "w")
     else:
          os.mkdir(pasta_tabelas)
          tabela1 = open(f"{pasta_tabelas}complete_data.csv", "w")
     
     tabela1.write("Approx Module;VVenC Profile;Video;Read BER;Write BER;QP;Rep.;YUV-PSNR;Bitrate;Execution Time")
     
     #Adiciona cabeçalho para porcentagem da redução de consumo de energia se for SRAM
     if injection_calls is True:  
          tabela1.write(";Injection Calls")
     if erros_SRAM is True:
          tabela1.write(";Read Energy;Write Energy;Dynamic Energy Reduction")
     else:
          tabela1.write("")
        
          
     todos_arquivos = os.listdir(f'{pasta_arquivos}logs-pin') #Obtendo nomes dos arquivos
     todos_arquivos.sort()
     
     #Extraindo informações da codificação utilizada no nome do arquivo:
     for nome_arquivo in todos_arquivos:     
          dados_nome_arquivo = nome_arquivo
          dados_nome_arquivo = dados_nome_arquivo.split('-')
          print(nome_arquivo)
          tabela1.write(f'\n{dados_nome_arquivo[0]};') #Approx Module
          tabela1.write(f'{dados_nome_arquivo[4]};') #VVenC Profile
          tabela1.write(f'{dados_nome_arquivo[1]};') #Video
          tabela1.write(f'{dados_nome_arquivo[2]};') #Read BER
          tabela1.write(f'{dados_nome_arquivo[3]};') #Write BER
          tabela1.write(f'{dados_nome_arquivo[5]};') #QP
          tabela1.write(f'{dados_nome_arquivo[6][0:int(len(dados_nome_arquivo[6]))-4]};') #Rep
          
          #Extraindo informações dentro do arquivo .log
          linha_dados = 0
          arquivo_log = open(f'{pasta_arquivos}/logs-pin/{nome_arquivo}', "r")
          for ver_arquivo_log in arquivo_log:
               if (linha_dados == 1):     #linha com os dados PSNR e bitrate
                    gravar = remove_espaco(ver_arquivo_log) 
                    tabela1.write(f'{float(gravar[8])};') #YUV-PSNR
                    tabela1.write(f'{float(gravar[4])};') #Bitrate   
                    linha_dados = 0 
               
               if (("Total Frames" in ver_arquivo_log) == True):
                    linha_dados = 1
                    
               if (("Total Time:" in ver_arquivo_log) == True):  #linha com o tempo
                    gravar2 = remove_espaco(ver_arquivo_log)
                    tabela1.write(f'{float(gravar2[4])}') #Execution Time
          
          #Extrai informaçoes de total de acesso na memória
          if injection_calls is True:
               #arquivo_log = open(f'{pasta_arquivos}/mem-access-logs/{nome_arquivo}', "r")
               arquivo_log = open(f'/home/pc-hegel/Documentos/scripts-vvenc_approx/arquivos/VCIP/mem-access-logs/{nome_arquivo}', "r")
               for linha in arquivo_log:
                    if ("Total Injection Calls" in linha) == True:
                         temp = linha.replace("\n", "").split(": ")[1]
                         tabela1.write(f';{temp}')
                              
          #Se for memória SRAM extrai informações de energia
          if erros_SRAM is True:
               linha_dados_SAVINGS = 0
               linha_dados_REFERENCE = 0
               linha_dados_APPROXIMATE = 0
               final_arquivo = 0
                    
               if "-0-0-" in nome_arquivo:
                    tabela1.write(';0;0;0')
               else:
                    arquivo_log = open(f'{pasta_arquivos}/energy-logs/{nome_arquivo}', "r")
                    Eref = 0
                    Eapprox = 0
                    for ver_arquivo_log in arquivo_log:
                         if linha_dados_SAVINGS == 1 and final_arquivo == 1:
                              tabela1.write(';')
                              tabela1.write(ver_arquivo_log.split(':')[1].replace(" ", "").replace("%", "").replace("\n", ""))
                              linha_dados_SAVINGS += 1
                         elif linha_dados_SAVINGS == 2 and final_arquivo == 1:
                              tabela1.write(';')
                              total = (Eref - Eapprox) / (Eref * 100)
                              tabela1.write(ver_arquivo_log.split(':')[1].replace(" ", "").replace("%", "").replace("\n", ""))
                              tabela1.write(f";{total * 10000}")
                              #tabela1.write(f";{round(total * 10000, 2)}")
                         
                         if linha_dados_REFERENCE == 1 and final_arquivo == 1:
                              Eref_read = float(ver_arquivo_log.split(':')[1].strip().replace('pJ', '').replace(' ', '').replace("\n", ""))
                              linha_dados_REFERENCE += 1
                         elif linha_dados_REFERENCE == 2 and final_arquivo == 1:
                              Eref_write = float(ver_arquivo_log.split(':')[1].strip().replace('pJ', '').replace(' ', '').replace("\n", ""))
                              linha_dados_REFERENCE = 0
                              Eref = Eref_read + Eref_write
                              
                         if linha_dados_APPROXIMATE == 1 and final_arquivo == 1:
                              Eapprox_read = float(ver_arquivo_log.split(':')[1].strip().replace('pJ', '').replace(' ', '').replace("\n", ""))
                              linha_dados_APPROXIMATE += 1
                         elif linha_dados_APPROXIMATE == 2 and final_arquivo == 1:
                              Eapprox_write = float(ver_arquivo_log.split(':')[1].strip().replace('pJ', '').replace(' ', '').replace("\n", ""))
                              linha_dados_APPROXIMATE = 0
                              Eapprox = Eapprox_read + Eapprox_write
                              
                         if (("ENERGY CONSUMPTION SAVINGS" in ver_arquivo_log) == True and final_arquivo == 1):
                              linha_dados_SAVINGS = 1
                         if (("REFERENCE ENERGY CONSUMPTION" in ver_arquivo_log) == True and final_arquivo == 1):
                              linha_dados_REFERENCE = 1
                         if (("APPROXIMATE ENERGY CONSUMPTION" in ver_arquivo_log) == True and final_arquivo == 1):
                              linha_dados_APPROXIMATE = 1  
                         if (("TARGET APPLICATION TOTAL ENERGY CONSUMPTION" in ver_arquivo_log) == True):
                              final_arquivo = 1
     tabela1.close()
     arquivo_log.close()
