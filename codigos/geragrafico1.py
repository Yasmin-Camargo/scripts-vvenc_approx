#Scripit que acessa o arquivo bd_rate.csv e cria gráfico com os bdrate

import matplotlib.pyplot as plt
import numpy as np 

def codigo_grafico1(pasta_tabelas): #Gráfico BD_Rate
    y = []
    erros=['1E_07','1E_05', '1E_03']
    #Abrindo arquivos:
    tabela3 = open(f"{pasta_tabelas}bd_rate.csv", "r") 
    
    #Váriaveis
    matriz_tabela3=[]
    num_linhas_matriz=0
    primeira_linha=1
    
    #Armazenando dados do arquivo em uma matriz
    for linha in tabela3:   
        if(primeira_linha==1): #Linha 1 não precisa ser armazenada
            primeira_linha+=1
        else:
            dados = linha
            dados = dados.split(';')
            num_linhas_matriz+=1  
            matriz_tabela3.append(dados)
    tabela3.close()
    
    #Armazenando dados BD-Rate para o gráfico
    lista=[]
    quant_linhas=0
    quant_colunas=0
    for erros in erros:
        quant_linhas+=1
        quant_colunas=0
        dados=''
        for linha in matriz_tabela3: 
            if(erros == linha[3] and linha[3] != '0'): #Quando encontra linha do BD-Rate, não ler para os erros = 0 (referência)
                dados += linha[5]
                dados += ';'      
                quant_colunas+=1
        dados = dados.split(';')
        dados.pop(-1) #Remove útilmo elemento da lista (espaço em branco)
        lista.append(dados)
        
    #Convertendo dados para float
    for cont in range (0,quant_linhas,1):
        temp = [float(item) for item in lista[cont]]
        y.append(temp)
    
    
    #Montando Gráfico
    x = np.arange(quant_colunas) 
    width = 0.3     #largura das barras
    
    plt.figure(figsize=(10,5)) #aumenta tamanho do gráfico
    
    #criando as barras
    plt.bar(x-width, y[0], width, color='#6A5ACD') 
    plt.bar(x, y[1], width, color='#6495ED') 
    plt.bar(x+width, y[2], width, color='#00BFFF')
     
    #legendas
    plt.xlabel("Erros") 
    plt.ylabel("BD-Rate") 
    plt.xticks(x, ['1E_07','1E_05', '1E_03']) 
    plt.legend(["Faster", "Medium", "Slower"])
    plt.title(f'Tabela {matriz_tabela3[0][0]}') 
    
    plt.savefig(f'{pasta_tabelas}tabela1-bdrate.png')  #Salva figura do gráfico
    
    plt.show() #Mostra Gráfico
    
        
    
   
    