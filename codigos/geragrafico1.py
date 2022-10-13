#Scripit que acessa o arquivo bd_rate.csv e cria gráfico com os bdrate para cada módulo

import matplotlib.pyplot as plt
import numpy as np 

def codigo_grafico1(pasta_tabelas): #Gráfico BD_Rate
    
    #Váriaveis
    bd_br = []  #eixo y
    erros=['10-3','10-4','10-5','10-6','10-7'] #eixo x
    primeira_linha=1
    
    #Abrindo arquivos:
    tabela3 = open(f"{pasta_tabelas}bd_rate.csv", "r") 
    
    #Obtendo BD-BR do arquivo
    for linha in tabela3:   
        if(primeira_linha==1): #Linha 1 não precisa ser lida
            primeira_linha+=1
        else:
            dados = linha
            dados = dados.split(';')
            if (primeira_linha==2): #Na primeira linha do arquivo ainda não foram armazenados dados na váriavel novo_grafico
                novo_grafico = dados #novo gráfico armazena dados que foram lidos na execução anterior
                primeira_linha+=1
                 
            if (dados[0]!=novo_grafico[0]): #Montar um novo gráfico quando for o módulo difente do que estava sendo lido antes
                monta_grafico(erros,bd_br,novo_grafico[0],pasta_tabelas)
                bd_br=[]
                novo_grafico=dados
                
            if (dados[4]!='0'): #não pegar dados quando o erro = 0
                bd_br.append(float(dados[5]))
                novo_grafico=dados
    monta_grafico(erros,bd_br,novo_grafico[0],pasta_tabelas)
    tabela3.close()
    
def monta_grafico(erros,bd_br,dados,pasta_tabelas): #Montando Gráfico
    plt.rcParams.update({'font.size': 13}) #tamanho fonte
    plt.figure(figsize=(8,4.5)) #aumenta tamanho do gráfico
    
    plt.bar(erros,bd_br,color='#019FE3')
    plt.yticks([])
    plt.yticks(np.arange(0.1, 0.8,0.1)) 
    # plt.yticks(np.arange(0, 115,15)) [ para as Transformadas ] 
    
    #legendas
    plt.xlabel("Taxa de erro (leitura e escrita)", fontsize = 15)
    plt.ylabel("BD-Rate (%)",fontsize = 15) 
    
    #Titulo do gráfico de acordo com o módulo
    if(dados == "fme_approx"):
        plt.title("FME", fontsize = 18)
    elif(dados == "ime_approx"):
        plt.title("IME", fontsize = 18)
    elif(dados == "intra_approx"):
        plt.title("Predição Intra", fontsize = 18)
    elif(dados == "transf_approx"):
        plt.title("Transformadas", fontsize = 18)
    else:
        plt.title(dados, fontsize = 18)
    
    plt.savefig(f'{pasta_tabelas}grafico1_{dados}.png') #Salvar imagem do gráfico no computador
    
    #legenda em barras
    cont=0
    while (cont < 5): 
        plt.text(cont-0.28, bd_br[cont]+0.03, f'{round(bd_br[cont],2)}%', color = '#1a64a8', fontweight = 'normal', bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 5}) 
        cont+=1
        #plt.text(cont-0.28, bd_br[cont]+2.5, f'{round(bd_br[cont],2)}%', color = '#1a64a8', fontweight = 'normal', bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 5})  [ Para as Transformadas ]
        
    
    plt.show()
        
    
   
    