#Scripit acessa o arquivo .csv e cria outro com apenas com média dos arquivos que apresentam repetição


def codigo_tabela2(): #Tabela 2
    #Abrindo arquivos:
    tabela2 = open("../tabelas/tabela2.csv", "w")
    tabela2.write("Approx Module;VVenC Profile;Video;Read BER;Write BER;QP;YUV-PSNR;Bitrate;Execution Time\n")
    tabela1 = open("../tabelas/complete_data.csv", "r") 

    #variaveis
    media_bitrate=0
    media_psnr=0
    media_time=0
    repeticoes=1

    matriz=[]
    num_linhas_matriz=0
    primeira_linha=1

    #CÓDIGO

    #Armazenando dados do arquivo na matriz
    for linha in tabela1:    
        num_linhas_matriz+=1
        if(primeira_linha==1):
            primeira_linha=2
        else:
            dados = linha.replace ('.', '')
            dados = dados.split(';')
            matriz.append(dados)
    matriz.append(['0']*9)

    tabela1.close()

    #Análise dos dados
    for linha in range(0,num_linhas_matriz-1):
        matriz[linha][9] = matriz[linha][9].replace ('\n', '')
        if (matriz[linha][6] == '0' and matriz[linha+1][6]=='1'):
            repeticoes=1
        elif (matriz[linha][6] == '0'):
            media_psnr = int(matriz[linha][7])
            media_bitrate = int(matriz[linha][8])
            media_time = int(matriz[linha][9])
            repeticoes=0
            
        if (repeticoes > 0):
            media_psnr += int(matriz[linha][7])
            media_bitrate += int(matriz[linha][8])
            media_time += int(matriz[linha][9])
            repeticoes+=1
            
            if (matriz[linha+1][6] == '0'):
                repeticoes-=1
                matriz[(linha+1)-repeticoes][7]=media_psnr/repeticoes   #Coloca a média na repetiçao 0
                matriz[(linha+1)-repeticoes][8]=media_bitrate/repeticoes
                matriz[(linha+1)-repeticoes][9]=media_time/repeticoes
            
    for i in range(0,num_linhas_matriz-1): #Gravando dados na matriz
        if(matriz[i][6]=='0'): #Apenas os elementos com repetição 0 são gravados
            for j in range(0,10):
                if (j!=6):
                    tabela2.write(str(matriz[i][j]))
                    tabela2.write(';')
            tabela2.write('\n')
            
            
        

