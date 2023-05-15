#Scripit que acessa o arquivo complete_data.csv e cria outro com os calculos BD-RATE e BD-PSNR para cada repetição

from bjontegaard_metric import *
import os


def bdRate_Repet(pasta_tabelas, rep):
    #Abrindo e criando arquivos:
    if os.path.isdir(pasta_tabelas):
        tabela3 = open(f"{pasta_tabelas}bd_rate_repet.csv", "w")
    else:
        os.mkdir(pasta_tabelas)
        tabela3 = open(f"{pasta_tabelas}bd_rate_repet.csv", "w")
        
    tabela2 = open(f"{pasta_tabelas}complete_data.csv", "r") 
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
            if(dados[4]=='0' and dados[4]=='0'):  #ReadBER e WriteBER = 0 são armazenados em uma matriz de referência
                matriz_referencia.append(dados)
                num_linhas_referencia+=1
            else:
                num_linhas_matriz+=1  #Outros campos são armazenados em uma matriz separada
                matriz_tabela2.append(dados)
    tabela2.close()


    #Calculo BD-RATE das repetições
    cont = 0
    for linha2 in range(0,num_linhas_referencia, rep*4):    # para cada codificação de referência (erro = 0)
        for linha in range(cont,cont + 5, 1):               # para cada erro
            for linha in range(cont,cont + rep, 1):         # para cada repetição
                tabela3.write(f'{matriz_tabela2[linha][0]};{matriz_tabela2[linha][1]};{matriz_tabela2[linha][2]};{matriz_tabela2[linha][3]};{matriz_tabela2[linha][4]};')
            
                #dados da codificação original
                Bitrate_Original = [float(matriz_referencia[linha2][8]), float(matriz_referencia[linha2+rep][8]), float(matriz_referencia[linha2+(2*rep)][8]),float(matriz_referencia[linha2+(3*rep)][8])]
                PSNR_Original = [float(matriz_referencia[linha2][7]), float(matriz_referencia[linha2+rep][7]), float(matriz_referencia[linha2+(2*rep)][7]), float(matriz_referencia[linha2+(3*rep)][7])]

                #dados da codificação modificada
                Bitrate_Modificada = [float(matriz_tabela2[linha][8]), float(matriz_tabela2[linha+rep][8]), float(matriz_tabela2[linha+(2*rep)][8]), float(matriz_tabela2[linha+(3*rep)][8])]
                PSNR_Modificada    = [float(matriz_tabela2[linha][7]), float(matriz_tabela2[linha+rep][7]), float(matriz_tabela2[linha+(2*rep)][7]), float(matriz_tabela2[linha+(3*rep)][7])]
            
                cont += 1

                tabela3.write(f'{BD_RATE(np.array(Bitrate_Original), np.array(PSNR_Original), np.array(Bitrate_Modificada), np.array(PSNR_Modificada))};') #Calculo BD-RATE
                tabela3.write(f'{BD_PSNR(np.array(Bitrate_Original), np.array(PSNR_Original), np.array(Bitrate_Modificada), np.array(PSNR_Modificada))}\n') #Calculo BD-PSNR
            cont += rep*3 
    tabela3.close()
