#Scripit que cria um gráfico box plot

import matplotlib.pyplot as plt
import numpy as np 

pasta_tabelas = f"SIM2023-inter"  #Nome da pasta com os arquivos .log

#Váriaveis
erros = ['10-3','10-4','10-5','10-6','10-7']  # eixo x
primeira_linha = 1
num_linhas = 0
todos_bdRate = []
median_values = []

#Abrindo arquivo:
tabela = open(f"../tabelas/tabelas-{pasta_tabelas}/bd_rate_repet.csv", "r") 

#Armazenando dados do arquivo csv em uma matriz
matriz = []
cont = 0
for linha in tabela:   
    if(primeira_linha == 1): #Linha 1 não precisa ser armazenada
        primeira_linha=2
    else:
        dados = linha
        dados = dados.split(';')
        matriz.append(dados)
        num_linhas += 1
        todos_bdRate.append(float(matriz[cont][5]))   # armazena todos os valores de BD-Rate encontrados para saber o menor e o maior valor
        cont += 1
tabela.close()
matriz.append([0,0,0,0,0,0,0])

# Calcular limites do eixo Y
y_min = min(todos_bdRate)
y_max = max(todos_bdRate)
y_range = y_max - y_min

# gerando gráfico box plot
dados = [[],[],[],[],[]]
for cont in range(0,num_linhas):
    # Definir tamanho de fonte global
    plt.rcParams.update({'font.size': 18}) 
    
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
        fig, ax = plt.subplots(figsize=(8, 4.5))


        # Personalizar os títulos e os rótulos dos eixos
        # --> titulo
        video = matriz[cont][2].split('_')
        if(matriz[cont][0] == "filt_inter_approx"):      
            ax.set_title(f'{video[0]}: FiltSB')
        elif(matriz[cont][0] == "reco_inter_approx"):
            ax.set_title(f'{video[0]}: RecoSB')
        elif(matriz[cont][0] == "orig_inter_approx"):
            ax.set_title(f'{video[0]}: OrigSB')
        elif(matriz[cont][0] == "pred_inter_approx"):
            ax.set_title(f'{video[0]}: PredSB')
    
        # --> legenda eixo X e Y
        ax.set_xlabel('Error rate (read and write)')
        ax.set_ylabel('BD-Rate (%)')

        # Personalizar o eixo x
        ax.set_xticklabels(erros)
        
        # Configurar intervalo dos valores nos eixos Y
        ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.2 * y_range)

        # Personalizar as cores das caixas
        boxprops = dict(linewidth=1.5, color='black')       # caixa
        flierprops = dict(markerfacecolor='black')          # bolinhas
        medianprops = dict(linewidth=1.5, color='black')    # mediana
        whiskerprops = dict(linewidth=1.5, color='black')   # linhas
        ax.boxplot(dados, boxprops=boxprops, flierprops=flierprops, medianprops=medianprops, whiskerprops=whiskerprops) 
        plt.tight_layout()
        
        # print da mediana do gráfico
        median_1E_03 = np.average(dados[0])
        median_1E_04 = np.average(dados[1])
        median_1E_05 = np.average(dados[2])
        median_1E_06 = np.average(dados[3])
        median_1E_07 = np.average(dados[4])

        median_values.append([median_1E_03, median_1E_04, median_1E_05, median_1E_06, median_1E_07])
        
        # Adicionar medianas ao gráfico
        for i, median in enumerate([median_1E_03, median_1E_04, median_1E_05, median_1E_06, median_1E_07]):
            ax.text(i + 1, y_max , f'{median:.2f}', ha='center', va='bottom', color='black', fontweight='bold')
        
        # salvar gráfico 
        fig = plt.gcf()
        plt.show()
        fig.savefig(f'../tabelas/tabelas-{pasta_tabelas}/box_plot/grafico1_{matriz[cont][0]}-{video[0]}.png') #Salvar imagem do gráfico no computador
        
        # reinicializa variavel
        dados = [[],[],[],[],[]]
   
