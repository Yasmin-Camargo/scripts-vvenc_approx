#Scripit que acessa o arquivo tabela2.csv e cria outro com os calculos BD-RATE e BD-PSNR

from bjontegaard_metric import *
import os

def codigo_tabela3(pasta_tabelas): #Tabela 3
    #Abrindo e criando arquivos:
    if os.path.isdir(pasta_tabelas):
        tabela3 = open(f"{pasta_tabelas}bd_rate.csv", "w")
    else:
        os.mkdir(pasta_tabelas)
        tabela3 = open(f"{pasta_tabelas}bd_rate.csv", "w")
        
    tabela2 = open(f"{pasta_tabelas}tabela2.csv", "r") 
    tabela3.write("Approx Module;VVenC Profile;Video;Read BER;Write BER;BD-Rate;BD-PSNR\n")
    
    #Váriaveis
    matriz_tabela2=[]
    matriz_referencia=[]
    num_linhas_matriz=0
    num_linhas_referencia=0
    primeira_linha=1
    
    #Armazenando dados do arquivo em uma matriz
    for linha in tabela2:   
        if(primeira_linha==1): #Linha 1 não precisa ser armazenada
            primeira_linha=2
        else:
            dados = linha
            dados = dados.split(';')
            if(dados[3]=='0' and dados[4]=='0'):  #ReadBER e WriteBER = 0 são armazenados em uma matriz de referência
                matriz_referencia.append(dados)
                num_linhas_referencia+=1
            else:
                num_linhas_matriz+=1  #Outros campos são armazenados em uma matriz separada
                matriz_tabela2.append(dados)
    tabela2.close()
    
    #Calculo BD-RATE e BD-PSNR
    for linha2 in range(0,num_linhas_referencia):
        if (matriz_referencia[linha2][5] == '22'): #CALCULA para BERs (0,0) - Linha referencia da tabela
            tabela3.write(f'{matriz_referencia[linha2][0]};{matriz_referencia[linha2][1]};{matriz_referencia[linha2][2]};{matriz_referencia[linha2][3]};{matriz_referencia[linha2][4]};')
            
            Bitrate_Original = [float(matriz_referencia[linha2][7]), float(matriz_referencia[linha2+1][7]), float(matriz_referencia[linha2+2][7]),float(matriz_referencia[linha2+3][7])]
            PSNR_Original = [float(matriz_referencia[linha2][6]), float(matriz_referencia[linha2+1][6]), float(matriz_referencia[linha2+2][6]), float(matriz_referencia[linha2+3][6])]
            
            Bitrate_Modificada = [float(matriz_referencia[linha2][7]), float(matriz_referencia[linha2+1][7]), float(matriz_referencia[linha2+2][7]),float(matriz_referencia[linha2+3][7])]
            PSNR_Modificada = [float(matriz_referencia[linha2][6]), float(matriz_referencia[linha2+1][6]), float(matriz_referencia[linha2+2][6]), float(matriz_referencia[linha2+3][6])]
            
            #Gravando dados na matriz
            tabela3.write(f'{BD_RATE(np.array(Bitrate_Original), np.array(PSNR_Original), np.array(Bitrate_Modificada), np.array(PSNR_Modificada))};') #Calculo BD-RATE
            tabela3.write(f'{BD_PSNR(np.array(Bitrate_Original), np.array(PSNR_Original), np.array(Bitrate_Modificada), np.array(PSNR_Modificada))}\n') #Calculo BD-PSNR
        
        #CALCULA para BERs diferentes de (0,0)
        for linha in range(0,num_linhas_matriz):
            if (matriz_tabela2[linha][0] == matriz_referencia[linha2][0] and matriz_tabela2[linha][1] == matriz_referencia[linha2][1] and matriz_tabela2[linha][2] == matriz_referencia[linha2][2] and matriz_tabela2[linha][5] == '22' and matriz_referencia[linha2][5] == '22'):
                
                tabela3.write(f'{matriz_tabela2[linha][0]};{matriz_tabela2[linha][1]};{matriz_tabela2[linha][2]};{matriz_tabela2[linha][3]};{matriz_tabela2[linha][4]};')
                
                #dados da codificação original
                Bitrate_Original = [float(matriz_referencia[linha2][7]), float(matriz_referencia[linha2+1][7]), float(matriz_referencia[linha2+2][7]),float(matriz_referencia[linha2+3][7])]
                PSNR_Original = [float(matriz_referencia[linha2][6]), float(matriz_referencia[linha2+1][6]), float(matriz_referencia[linha2+2][6]), float(matriz_referencia[linha2+3][6])]

                #dados da codificação modificada
                Bitrate_Modificada = [float(matriz_tabela2[linha][7]), float(matriz_tabela2[linha+1][7]), float(matriz_tabela2[linha+2][7]), float(matriz_tabela2[linha+3][7])]
                PSNR_Modificada    = [float(matriz_tabela2[linha][6]), float(matriz_tabela2[linha+1][6]), float(matriz_tabela2[linha+2][6]), float(matriz_tabela2[linha+3][6])]
                
                tabela3.write(f'{BD_RATE(np.array(Bitrate_Original), np.array(PSNR_Original), np.array(Bitrate_Modificada), np.array(PSNR_Modificada))};') #Calculo BD-RATE
                tabela3.write(f'{BD_PSNR(np.array(Bitrate_Original), np.array(PSNR_Original), np.array(Bitrate_Modificada), np.array(PSNR_Modificada))}\n') #Calculo BD-PSNR
                
    
    tabela3.close()
                     

        
        
    
    
    
      
    
       

    