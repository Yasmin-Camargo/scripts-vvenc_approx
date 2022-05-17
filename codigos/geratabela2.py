#Scripit acessa o arquivo .csv e cria outro apenas com média dos arquivos que apresentam repetição


def codigo_tabela2(): #Tabela 2
    #Abrindo e criando arquivos:
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

    #Armazenando dados do arquivo em uma matriz
    for linha in tabela1:    
        num_linhas_matriz+=1
        if(primeira_linha==1):  #Linha 1 não precisa ser armazenada
            primeira_linha=2
        else:
            dados = linha
            dados = dados.split(';')
            matriz.append(dados)
    matriz.append(['0']*9)
    tabela1.close()

    #Análise dos dados
    for linha in range(0,num_linhas_matriz-1):
        matriz[linha][9] = matriz[linha][9].replace ('\n', '')
        if (matriz[linha][6] == '0' and matriz[linha+1][6]=='1'): #Quando a repetição é 0 e a próxima é 1, calcular a média
            repeticoes=1
        elif (matriz[linha][6] == '0'): #Inicializando as váriaveis para a nova repetição
            media_psnr = 0
            media_bitrate = 0
            media_time = 0
            repeticoes=0
            
        if (repeticoes > 0): #Calculando a média para Bitrate, PSNR e tempo quando existe repetição
            media_psnr += float(matriz[linha][7])
            media_bitrate += float(matriz[linha][8])
            media_time += float(matriz[linha][9])
            repeticoes+=1
            
            if (matriz[linha+1][6] == '0'): #Fim da repetição, armazena resultados na repetiçao 0
                repeticoes-=1
                matriz[(linha+1)-repeticoes][7]=media_psnr/repeticoes   
                matriz[(linha+1)-repeticoes][8]=media_bitrate/repeticoes
                matriz[(linha+1)-repeticoes][9]=media_time/repeticoes
            
    for i in range(0,num_linhas_matriz-1): #Gravando dados na matriz
        if(matriz[i][6]=='0'): #Apenas os elementos com repetição 0 são gravados
            for j in range(0,10):
                if (j!=6):
                    tabela2.write(str(matriz[i][j]))
                    tabela2.write(';')
            tabela2.write('\n')
    tabela2.close()