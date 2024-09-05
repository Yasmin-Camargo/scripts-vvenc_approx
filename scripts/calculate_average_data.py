#Script acessa o arquivo complete_data.csv e cria outro apenas com média dos arquivos que apresentam repetição

import os

def average_data(pasta_tabelas, erros_SRAM, injection_calls): #Tabela 2
    #Abrindo e criando arquivos:
    if os.path.isdir(pasta_tabelas):
        tabela2 = open(f"{pasta_tabelas}average.csv", "w")
    else:
        os.mkdir(pasta_tabelas)
        tabela2 = open(f"{pasta_tabelas}average.csv", "w")
    tabela2.write("Approx Module;VVenC Profile;Video;Read BER;Write BER;QP;YUV-PSNR;Bitrate;Execution Time")
    tabela1 = open(f"{pasta_tabelas}complete_data.csv", "r") 

    #Adiciona cabeçalho para porcentagem da redução de consumo de energia se for SRAM
    if injection_calls is True:  
        tabela2.write(";Injection Calls")
    if erros_SRAM is True:
        tabela2.write(";Read Energy;Write Energy;Dynamic Energy Reduction\n")
    else:
        tabela2.write("\n")
        
    #variaveis
    media_bitrate = 0
    media_psnr = 0
    media_time = 0
    total_colunas = 9
    
    if injection_calls is True and erros_SRAM is True:
        media_injectioncalls = 0
        total_colunas = 13
        media_energyWrite = 0
        media_energyRead = 0
        media_energyDynamic = 0
    elif injection_calls is True:
        media_injectioncalls = 0
        total_colunas = 10
    elif erros_SRAM is True:
        media_energyWrite = 0
        media_energyRead = 0
        media_energyDynamic = 0
        total_colunas = 12
    
        
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
    tabela1.close()
    
    matriz.sort()
    
    if erros_SRAM is True and injection_calls is True:
        matriz.append(['0']*13)
    elif injection_calls is True:
        matriz.append(['0']*12)
    else: 
        matriz.append(['0']*9)
    
    #Análise dos dados
    for linha in range(0,num_linhas_matriz-1):
        matriz[linha][total_colunas] = matriz[linha][total_colunas].replace ('\n', '')
            
        if (matriz[linha][6] == '0' and matriz[linha+1][6] == '1'): #Quando a repetição é 0 e a próxima é 1, calcular a média
            repeticoes=1
        
        if (repeticoes > 0): #Calculando a média para Bitrate, PSNR e tempo quando existe repetição
            media_psnr += float(matriz[linha][7])
            media_bitrate += float(matriz[linha][8])
            media_time += float(matriz[linha][9])
            
            if injection_calls is True and erros_SRAM is True:
                media_injectioncalls += float(matriz[linha][10])
                media_energyRead += float(matriz[linha][11])
                media_energyWrite += float(matriz[linha][12])
                media_energyDynamic += float(matriz[linha][13])
            elif injection_calls is True:
                media_injectioncalls += float(matriz[linha][10])
            elif erros_SRAM is True:
                media_energyRead += float(matriz[linha][10])
                media_energyWrite += float(matriz[linha][11])
                media_energyDynamic += float(matriz[linha][12])
                
            repeticoes+=1
            
            if (matriz[linha+1][6] == '0'): #Fim da repetição, armazena resultados na repetiçao 0
                repeticoes-=1
                matriz[(linha+1)-repeticoes][7] = float(media_psnr/repeticoes)   
                matriz[(linha+1)-repeticoes][8] = float(media_bitrate/repeticoes)
                matriz[(linha+1)-repeticoes][9] = float(media_time/repeticoes)
                if injection_calls is True and erros_SRAM is True:
                    matriz[(linha+1)-repeticoes][10] = float(media_injectioncalls/repeticoes)
                    matriz[(linha+1)-repeticoes][11] = float(media_energyRead/repeticoes)
                    matriz[(linha+1)-repeticoes][12] = float(media_energyWrite/repeticoes)
                    matriz[(linha+1)-repeticoes][13] = float(media_energyDynamic/repeticoes)
                elif injection_calls is True:
                    matriz[(linha+1)-repeticoes][10] = float(media_injectioncalls/repeticoes)
                elif erros_SRAM is True:
                    matriz[(linha+1)-repeticoes][10] = float(media_energyRead/repeticoes)
                    matriz[(linha+1)-repeticoes][11] = float(media_energyWrite/repeticoes)
                    matriz[(linha+1)-repeticoes][12] = float(media_energyDynamic/repeticoes)
                    
                #Inicializando as váriaveis para a nova repetição
                media_psnr = 0
                media_bitrate = 0
                media_time = 0
                repeticoes=0
                if erros_SRAM is True:
                    media_energyWrite = 0
                    media_energyRead = 0
                    media_energyDynamic = 0
                if injection_calls is True:
                    media_injectioncalls = 0
            
    print(total_colunas)
    for i in range(0,num_linhas_matriz-1): #Gravando dados na matriz
        if(matriz[i][6]=='0'): #Apenas os elementos com repetição 0 são gravados
            for j in range(0,total_colunas+1):
                if (j!=6):
                    tabela2.write(f'{matriz[i][j]}')
                    tabela2.write(';')
            tabela2.write('\n')
    tabela2.close()