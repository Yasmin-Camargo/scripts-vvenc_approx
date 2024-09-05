#script que cria um gráfico box plot

import matplotlib.pyplot as plt
import numpy as np 
import os

def box_plot(pasta_tabelas, erros_SRAM):
    if erros_SRAM is True:
        erros = ['0.55V', '0.6V', '0.7V']   # eixo x
    else:
        erros = ['10-2','10-3','10-4','10-5','10-6']  # eixo x
          
    #Váriaveis
    primeira_linha = 1
    num_linhas = 0
    todos_bdRate = []
    median_values = []
    
    #Abrindo arquivo:
    tabela = open(f"{pasta_tabelas}/bd_rate_repet.csv", "r") 

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
            todos_bdRate.append(float(matriz[cont][6]))   # armazena todos os valores de BD-Rate encontrados para saber o menor e o maior valor
            cont += 1
    tabela.close()
    
    if erros_SRAM is True:
        matriz.append([0,0,0])
    else:
        matriz.append([0,0,0,0,0])

    # gerando gráfico box plot
    if erros_SRAM is True:
        dados = [[],[],[]]
    else:
        dados = [[],[],[],[],[]]
        
    for cont in range(0,num_linhas):
        # Definir tamanho de fonte global
        plt.rcParams.update({'font.size': 18}) 
        
        if(matriz[cont][0] == matriz[cont + 1][0] and matriz[cont][2] == matriz[cont + 1][2]):
            if erros_SRAM is True:
                if(matriz[cont][3] == "0.55V"):
                    dados[0].append(float(matriz[cont][6]))
                if(matriz[cont][3] == "0.6V"):
                    dados[1].append(float(matriz[cont][6]))
                if(matriz[cont][3] == "0.7V"):
                    dados[2].append(float(matriz[cont][6]))
            else: 
                if(matriz[cont][3] == "10E_02"):
                    dados[0].append(float(matriz[cont][6]))
                if(matriz[cont][3] == "10E_03"):
                    dados[1].append(float(matriz[cont][6]))
                if(matriz[cont][3] == "10E_04"):
                    dados[2].append(float(matriz[cont][6]))
                if(matriz[cont][3] == "10E_05"):
                    dados[3].append(float(matriz[cont][6]))
                if(matriz[cont][3] == "10E_06"):
                    dados[4].append(float(matriz[cont][6]))
            
        elif (matriz[cont][2] != matriz[cont + 1][2] or matriz[cont][0] == matriz[cont + 1][0]):
            # Criar o gráfico de boxplot
            fig, ax = plt.subplots(figsize=(8, 3.5))

            # Limite de 40% de bd para plotar
            if erros_SRAM is True: 
                if np.median(dados[0]) > 40 or np.median(dados[0]) < -40:
                    dados[0] = []
                if np.median(dados[1]) > 40 or np.median(dados[1]) < -40:
                    dados[1] = []
                if np.median(dados[2]) > 40 or np.median(dados[2]) < -40:
                    dados[2] = []
            else: 
                if np.median(dados[0]) > 40 or np.median(dados[0]) < -40:
                    dados[0] = []
                if np.median(dados[1]) > 40 or np.median(dados[1]) < -40:
                    dados[1] = []
                if np.median(dados[2]) > 40 or np.median(dados[2]) < -40:
                    dados[2] = []
                if np.median(dados[3]) > 40 or np.median(dados[3]) < -40:
                    dados[3] = []
                if np.median(dados[4]) > 40 or np.median(dados[4]) < -40:
                    dados[4] = []

            # Personalizar os títulos e os rótulos dos eixos
            # --> titulo
            video = matriz[cont][2].split('_')
            if(matriz[cont][0] == "filt_inter_approx" or matriz[cont][0] == "inter_filt"):      
                ax.set_title(f'{video[0]}: FiltSB')
            elif(matriz[cont][0] == "reco_inter_approx"):
                ax.set_title(f'{video[0]}: RecoSB')
            elif(matriz[cont][0] == "orig_inter_approx" or matriz[cont][0] == "inter_orig"):
                ax.set_title(f'{video[0]}: OrigSB')
            elif(matriz[cont][0] == "pred_inter_approx"):
                ax.set_title(f'{video[0]}: PredSB')
            elif(matriz[cont][0] == "intra_approx"):
                ax.set_title(f'{video[0]}: intra')
            elif(matriz[cont][0] == "neighborintra_approx"):
                plt.title(f'{video[0]}: neighbor', fontsize = 18)
            else:
                plt.title(f'{video[0]}: {matriz[cont][0].split("_")[1]} - {matriz[cont][1].split("_")[0]}', fontsize = 18)
        
            # --> legenda eixo X e Y
            ax.set_xlabel('Error rate (read and write)')
            ax.set_ylabel('BD-Rate (%)')
            plt.rc('font', family='serif')
            plt.rc('text', antialiased=True)

            # Personalizar o eixo x
            ax.set_xticklabels(erros)
            
            # Configurar intervalo dos valores nos eixos Y e limites
            if matriz[cont][0] == 'intra_orig_approx' or matriz[cont][0] == 'intra_orig_approx_rw':
                y_min = 0
                y_max = 13
                y_range = 13
            elif matriz[cont][0] == 'intra_neigh_approx' and matriz[cont][1].split("_")[0] == 'allintra':
                y_min = 0
                y_max = 20
                y_range = 20
            elif matriz[cont][0] == 'intra_neigh_approx' and matriz[cont][1].split("_")[0] == 'randomaccess':
                y_min = 0
                y_max = 60
                y_range = 60
            else:
                y_min = min(todos_bdRate)
                y_max = max(todos_bdRate) 
                y_range = y_max - y_min
            
            ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.2 * y_range)

            # Personalizar as cores das caixas
            boxprops = dict(linewidth=1.5, color='black')       # caixa
            flierprops = dict(markerfacecolor='black')          # bolinhas
            medianprops = dict(linewidth=1.5, color='black')    # mediana
            whiskerprops = dict(linewidth=1.5, color='black')   # linhas
            ax.boxplot(dados, boxprops=boxprops, flierprops=flierprops, medianprops=medianprops, whiskerprops=whiskerprops) 
            plt.tight_layout()
            
            # print da mediana do gráfico
            if erros_SRAM is True:
                median_55 = np.median(dados[0])
                median_06 = np.median(dados[1])
                median_07 = np.median(dados[2])
                median_values.append([median_55, median_06, median_07])
                
                # Adicionar medianas ao gráfico
                for i, median in enumerate([median_55, median_06, median_07]):
                    ax.text(i + 1, y_max , f'{median:.2f}', ha='center', va='bottom', color='black', fontweight='bold')
                    
            else:
                median_1E_02 = np.median(dados[0])
                median_1E_03 = np.median(dados[1])
                median_1E_04 = np.median(dados[2])
                median_1E_05 = np.median(dados[3])
                median_1E_06 = np.median(dados[4])
                median_values.append([median_1E_02, median_1E_03, median_1E_04, median_1E_05, median_1E_06])
            
                # Adicionar medianas ao gráfico
                for i, median in enumerate([median_1E_02, median_1E_03, median_1E_04, median_1E_05, median_1E_06]):
                    ax.text(i + 1, y_max , f'{median:.2f}', ha='center', va='bottom', color='black', fontweight='bold')
            
            # salvar gráfico 
            
            plt.show()
            
            # Verifique se o diretório já existe
            if not os.path.exists(f'{pasta_tabelas}/graph-box_plot'):
                # Se não existir, crie o diretório
                os.makedirs(f'{pasta_tabelas}/graph-box_plot')
            fig.savefig(f'{pasta_tabelas}/graph-box_plot/{matriz[cont][0]}-{video[0]}-{matriz[cont][1].split("_")[0]}.png', dpi=1000) #Salvar imagem do gráfico no computador
            
            # reinicializa variavel
            if erros_SRAM is True:
                dados = [[],[],[]]
            else:
                dados = [[],[],[],[],[]]
            

        

        
    
        