#Scripit que cria um gráfico box plot

import matplotlib.pyplot as plt
import numpy as np 

pasta_tabelas = f"../tabelas/tabelas-10rp/"  #Nome da pasta com os arquivos .log

#Váriaveis
erros = ['10-3','10-4','10-5','10-6','10-7']  # eixo x
primeira_linha = 1
num_linhas = 0

#Abrindo arquivo:
tabela = open(f"{pasta_tabelas}bd_rate_repet.csv", "r") 

#Armazenando dados do arquivo csv em uma matriz
matriz = []
for linha in tabela:   
    if(primeira_linha == 1): #Linha 1 não precisa ser armazenada
        primeira_linha=2
    else:
        dados = linha
        dados = dados.split(';')
        matriz.append(dados)
        num_linhas += 1
tabela.close()
matriz.append([0,0,0,0,0,0,0])

# gerando gráfico box plot
dados = [[],[],[],[],[]]
for cont in range(0,num_linhas):
    if(matriz[cont][0] == matriz[cont + 1][0] and matriz[cont][2] == matriz[cont + 1][2]):
        if(matriz[cont][3] == "1E_03"):
            dados[0].append(float(matriz[cont][5]))
        if(matriz[cont][3] == "1E_04"):
            dados[1].append(float(matriz[cont][5]))
        if(matriz[cont][3] == "1E_05"):
            dados[2].append(float(matriz[cont][5]))
        if(matriz[cont][3] == "1E_06"):
            dados[3].append(float(matriz[cont][5]))
        if(matriz[cont][3] == "1E_07"):
            dados[4].append(float(matriz[cont][5]))
        
    elif (matriz[cont][2] != matriz[cont + 1][2] or matriz[cont][0] == matriz[cont + 1][0]):
        # Criar o gráfico de boxplot
        fig, ax = plt.subplots()

        # Personalizar os títulos e os rótulos dos eixos
        # --> titulo
        video = matriz[cont][2].split('_')
        if(matriz[cont][0] == "filt_inter_approx"):      
            ax.set_title(f'{video[0]}: FSB')
        elif(matriz[cont][0] == "reco_inter_approx"):
            ax.set_titlee(f'{video[0]}: RSB')
        elif(matriz[cont][0] == "orig_inter_approx"):
            ax.set_title(f'{video[0]}: OSB')
        elif(matriz[cont][0] == "pred_inter_approx"):
            ax.set_title(f'{video[0]}: PSB')
        else:
            ax.set_title(f'{video[0]}:{matriz[cont][0]}')
        
        # --> legenda eixo X e Y
        ax.set_xlabel('Error rate (read and write)')
        ax.set_ylabel('BD-Rate (%)')

        # Personalizar o eixo x
        ax.set_xticklabels(erros)

        # Personalizar as cores das caixas
        boxprops = dict(linewidth=1.5, color='black')       # caixa
        flierprops = dict(markerfacecolor='black')          # bolinhas
        medianprops = dict(linewidth=1.5, color='black')    # mediana
        whiskerprops = dict(linewidth=1.5, color='black')   # linhas
        ax.boxplot(dados, boxprops=boxprops, flierprops=flierprops, medianprops=medianprops, whiskerprops=whiskerprops) 
        
        # salvar gráfico 
        fig = plt.gcf()
        plt.show()
        fig.savefig(f'../tabelas/box_plot/grafico1_{matriz[cont][0]}-{video[0]}.png') #Salvar imagem do gráfico no computador
        
        # reinicializa variavel
        dados = [[],[],[],[],[]]
        

    

    
   
    