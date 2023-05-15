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
    tabela4 = open(f"{pasta_tabelas}bd_rate_repet.csv", "r") 
    
    #Armazenando dados do arquivo em uma matriz
    matriz=[]
    for linha in tabela4:   
        if(primeira_linha == 1): #Linha 1 não precisa ser armazenada
            primeira_linha=2
        else:
            dados = linha
            dados = dados.split(';')
            matriz.append(dados)
    tabela4.close()
    
    primeira_linha=1
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
                 
            if (dados[0]!=novo_grafico[0] or dados[2]!= novo_grafico[2]): #Montar um novo gráfico quando for um módulo ou vídeo difente
                monta_grafico(erros,bd_br,novo_grafico[0],pasta_tabelas, novo_grafico[2], matriz)
                bd_br=[]
                novo_grafico=dados
                
            if (dados[4]!='0'): #não pegar dados quando o erro = 0
                bd_br.append(float(dados[5]))
                novo_grafico=dados
    monta_grafico(erros,bd_br,novo_grafico[0],pasta_tabelas, novo_grafico[2], matriz)
    tabela3.close()
    
def monta_grafico(erros,bd_br,dados,pasta_tabelas, video, matriz): #Montando Gráfico
    videoCompleto = video
    plt.rcParams.update({'font.size': 13}) #tamanho fonte
    plt.figure(figsize=(8,4.5)) #aumenta tamanho do gráfico
    
    plt.bar(erros,bd_br,color='#019FE3')
    plt.yticks([])
    
    # plt.yticks(np.arange(0, 115,15)) [ para as Transformadas ] 
    
    #legendas
    plt.xlabel("Taxa de erro (leitura e escrita)", fontsize = 15)
    plt.ylabel("BD-Rate (%)",fontsize = 15) 
    
    #Titulo do gráfico de acordo com o módulo e vídeo
    video = video.split('_')
    if(dados == "filt_inter_approx"):
        plt.title(f'{video[0]}: FSB', fontsize = 18)
    elif(dados == "reco_inter_approx"):
        plt.title(f'{video[0]}: RSB', fontsize = 18)
    elif(dados == "orig_inter_approx"):
        plt.title(f'{video[0]}: OSB', fontsize = 18)
    elif(dados == "pred_inter_approx"):
        plt.title(f'{video[0]}: PSB', fontsize = 18)
    else:
        plt.title(f'{video[0]}: {dados}', fontsize = 18)
    
    
    #legenda em barras
    """
    cont=0
    while (cont < 5):
        if (bd_br[cont] < -0.1):
            plt.text(cont-0.25, bd_br[cont]+0.13, f'{round(bd_br[cont],2)}%', color = '#1a64a8', fontweight = 'normal', bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 5}) 
        elif (bd_br[cont] < -0.05):
            plt.text(cont-0.25, bd_br[cont]+0.09, f'{round(bd_br[cont],2)}%', color = '#1a64a8', fontweight = 'normal', bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 5}) 
        elif (bd_br[cont] < 0):
            plt.text(cont-0.25, bd_br[cont]+0.04, f'{round(bd_br[cont],2)}%', color = '#1a64a8', fontweight = 'normal', bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 5}) 
        else:
            plt.text(cont-0.25, bd_br[cont]+0.02, f'{round(bd_br[cont],2)}%', color = '#1a64a8', fontweight = 'normal', bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 5}) 
        
        cont+=1
    """ 
    for linha in matriz: 
        if(linha[0] == dados and linha[2] == videoCompleto):
            if(linha[3] == "1E_03"):
                plt.scatter("10-3", float(linha[5]), c='blue')
            if(linha[3] == "1E_04"):
                plt.scatter("10-4", float(linha[5]), c='blue')
            if(linha[3] == "1E_05"):
                plt.scatter("10-5", float(linha[5]), c='blue')
            if(linha[3] == "1E_06"):
                plt.scatter("10-6", float(linha[5]), c='blue')
            if(linha[3] == "1E_07"):
                plt.scatter("10-7", float(linha[5]), c='blue')
           
    plt.yticks(np.arange(0, 0.65,0.1)) 
    plt.savefig(f'{pasta_tabelas}grafico1_{dados}-{video[0]}.png') #Salvar imagem do gráfico no computador
    plt.show()
        
    
   
    