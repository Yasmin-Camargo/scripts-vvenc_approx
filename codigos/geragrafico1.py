#Scripit que acessa o arquivo bd_rate.csv e cria gráfico com os bdrate para cada módulo

import matplotlib.pyplot as plt
import numpy as np 

def codigo_grafico1(pasta_tabelas): #Gráfico BD_Rate
    
    #Váriaveis
    bd_br = []  #eixo y
    erros=['1E_03','1E_04','1E_05','1E_06','1E_07'] #eixo x
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
    plt.figure(figsize=(8,4)) #aumenta tamanho do gráfico
    plt.bar(erros,bd_br,color='#1a64a8')
    
    #legendas
    plt.xlabel("Taxa de erro (leitura e escrita)") 
    plt.ylabel("BD-BR (%)") 
    plt.title(dados) 
    
    plt.savefig(f'{pasta_tabelas}grafico1_{dados}.png') #Salvar imagem do gráfico no computador 
    
    plt.show()
        
    
   
    