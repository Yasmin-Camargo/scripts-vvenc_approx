# Script que cria gráfico do injection calls dos arquivos de mem-access-logs da PIN

import matplotlib.pyplot as plt
import numpy as np

pasta_tabelas = '../results/vcip_randomaccess_origRW'

def injection_calls(pasta_tabelas):       
    #Váriaveis
    primeira_linha = 1
    num_linhas = 0
    todos_injection_calls = []
    
    #Abrindo arquivo:
    tabela = open(f"{pasta_tabelas}/average.csv", "r") 

    #Armazenando dados do arquivo csv em uma matriz
    matriz = []
    cont = 0
    for linha in tabela: 
        if(primeira_linha == 1): #Linha 1 não precisa ser armazenada
            primeira_linha=2
        else:
            dados = linha
            dados = dados.split(';')
            todos_injection_calls.append(float(dados[9]))
            matriz.append(dados)
            num_linhas += 1
            cont += 1
    tabela.close()
    
    matriz.append([0,0,0,0,0])
    y_min = min(todos_injection_calls)
    y_max = max(todos_injection_calls) 
    y_range = y_max - y_min
    
    # Configuração dos parâmetros
    errors = ["10E_02", "10E_03", "10E_04", "10E_05", "10E_06"]
    dados = [[[], [], [], [], []] for _ in range(4)]
    num_qp = -1

    for i in range(0, num_linhas): 
        if matriz[i][5] == '22':
            num_qp = 0
        elif matriz[i][5] == '27':
            num_qp = 1
        elif matriz[i][5] == '32':
            num_qp = 2
        elif matriz[i][5] == '37':
            num_qp = 3
        
        if(matriz[i][3] == "10E_02"):
            dados[num_qp][0] = float(matriz[i][9])
        if(matriz[i][3] == "10E_03"):
            dados[num_qp][1] = float(matriz[i][9])
        if(matriz[i][3] == "10E_04"):
            dados[num_qp][2] = float(matriz[i][9])
        if(matriz[i][3] == "10E_05"):
            dados[num_qp][3] = float(matriz[i][9])
        if(matriz[i][3] == "10E_06"):
            dados[num_qp][4] = float(matriz[i][9])
        
        
        if matriz[i][0] != matriz[i+1][0] or matriz[i][2] != matriz[i+1][2]:    # novo video ou memória = plotar gráfico
            print(dados[0])
            # Posição no eixo x para as barras
            x = np.arange(len(errors))

            # Largura das barras
            largura = 0.15

            # Criando o gráfico de barras
            fig, ax = plt.subplots()

            # Plotando cada conjunto de barras
            ax.bar(x - 2 * largura, dados[0], largura, label='QP 22')
            ax.bar(x - largura, dados[1], largura, label='QP 27')
            ax.bar(x, dados[2], largura, label='QP 32')
            ax.bar(x + largura, dados[3], largura, label='QP 37')

            # Adicionando título e rótulos dos eixos
            ax.set_xlabel('Taxas de erro')
            ax.set_ylabel('Injection calls')
            ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.2 * y_range)
            plt.title(f'{matriz[i][2].split("_")[0]}: {matriz[i][0].split("_")[1]} - {matriz[i][1].split("_")[0]}')
            ax.set_xticks(x)
            ax.set_xticklabels(errors)
            ax.legend()

            # Exibindo o gráfico
            plt.show()
            fig.savefig(f'{pasta_tabelas}/graph-error_injection/{matriz[i][0]}-{matriz[i][2].split("_")[0]}-{matriz[i][1].split("_")[0]}.png', dpi=1000)
            
            dados = [[[], [], [], [], []] for _ in range(4)]
    
injection_calls(pasta_tabelas)