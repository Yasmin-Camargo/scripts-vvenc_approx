#Scripit que acessa o arquivo tabela2.csv e cria outro com a comparação dos tempos de execução

import os

def codigo_tabela4(pasta_tabelas): #Tabela 4
    #Abrindo e criando arquivos:
    if os.path.isdir(pasta_tabelas):
        tabela4 = open(f"{pasta_tabelas}runtime.csv", "w")
    else:
        os.mkdir(pasta_tabelas)
        tabela4 = open(f"{pasta_tabelas}runtime.csv", "w")
        
    tabela4.write(" ;Medium; ; ; ;Slower; ; \n")
    tabela4.write("Error Rate;22;27;32;37;22;27;32;37\n")
    
    tabela2 = open(f"{pasta_tabelas}tabela2.csv", "r") 
    
    #Váriaveis
    matriz_referencia=[]
    num_linhas_referencia=0
    matriz_tabela2=[]
    num_linhas_matriz=0
    primeira_linha=1
    
    #Armazenando dados do arquivo em uma matriz
    for linha in tabela2:   
        if(primeira_linha==1): #Linha 1 não precisa ser armazenada
            primeira_linha+=1
        else:
            dados = linha
            dados = dados.split(';')
            
            if('faster' in dados[1]):  #Faster são armazenados em uma matriz de referência
                matriz_referencia.append(dados)
                num_linhas_referencia+=1
            else:               #Outros campos são armazenados em uma matriz separada
                num_linhas_matriz+=1  
                matriz_tabela2.append(dados)
    tabela2.close()
    matriz_tabela2.append(" ; ; ; ; ; ; ; ; ")
    
    #Cálculo tempos tabela 
    cont=0
    primeira_linha=1
    for linha in range(0,num_linhas_matriz):
        if (primeira_linha==1): #Adciona o primeiro dado no arquivo csv
            tabela4.write(f'{matriz_tabela2[linha][3]};')
            primeira_linha=2
            
        for linha2 in range(0,num_linhas_referencia):  
            if (matriz_tabela2[linha][0] == matriz_referencia[linha2][0] and matriz_tabela2[linha][2] == matriz_referencia[linha2][2] and matriz_tabela2[linha][3] == matriz_referencia[linha2][3] and matriz_tabela2[linha][4] == matriz_referencia[linha2][4] and matriz_tabela2[linha][5] == matriz_referencia[linha2][5] ):
                conta = float(matriz_tabela2[linha][8])/float(matriz_referencia[linha2][8])  #Divisão dos tempo em relação ao referencia 
                tabela4.write(f'{conta};') #Armazena no arquivo csv
                    
        cont+=1
        if (cont==8): #Nova linha na tabela
            tabela4.write(f'\n{matriz_tabela2[linha+1][3]};')
            cont=0
            
    tabela4.close()
               
    