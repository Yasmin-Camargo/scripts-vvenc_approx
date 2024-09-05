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
    tabela = open(f"{pasta_tabelas}/bd_rate.csv", "r") 

    #Armazenando dados do arquivo csv em uma matriz
    mat_neigh = []
    mat_orig = []
    for linha in tabela: 
        if(primeira_linha == 1): #Linha 1 não precisa ser armazenada
            primeira_linha=2
        else:
            dados = linha
            dados = dados.split(';')
            todos_injection_calls.append(float(dados[7]))
            if dados[0] == 'intra_neigh_approx':
                mat_neigh.append(dados)
                num_linhas += 1
            elif dados[0] == 'intra_orig_approx' or dados[0] == 'intra_orig_approx_rw':
                mat_orig.append(dados)
    tabela.close()
    
    mat_neigh.append([0,0,0,0,0])
    y_min = min(todos_injection_calls)
    y_max = max(todos_injection_calls) 
    y_range = y_max - y_min
    
    # Configuração dos parâmetros
    errors = ["10E_02", "10E_03", "10E_04", "10E_05", "10E_06"]
    videos = ["BQMall", "BasketballDrill", "PartyScene", "RaceHorsesC"]
    dados = [[[], [], [], [], []] for _ in range(2)]
    dados_por_video = [[0 for _ in range(4)] for _ in range(2)]

    for i in range(0, num_linhas): 
        if(mat_neigh[i][3] == "10E_02"):
            dados[0][0] = float(mat_neigh[i][7])
            dados[1][0] = float(mat_orig[i][7])
        if(mat_neigh[i][3] == "10E_03"):
            dados[0][1] = float(mat_neigh[i][7])
            dados[1][1] = float(mat_orig[i][7])
        if(mat_neigh[i][3] == "10E_04"):
            dados[0][2] = float(mat_neigh[i][7])
            dados[1][2] = float(mat_orig[i][7])
        if(mat_neigh[i][3] == "10E_05"):
            dados[0][3] = float(mat_neigh[i][7])
            dados[1][3] = float(mat_orig[i][7])
        if(mat_neigh[i][3] == "10E_06"):
            dados[0][4] = float(mat_neigh[i][7])
            dados[1][4] = float(mat_orig[i][7])
        
        if(mat_neigh[i][2] == "BQMall_832x480_60"):   
            dados_por_video[0][0] += float(mat_neigh[i][7])
            dados_por_video[1][0] += float(mat_orig[i][7])
        elif(mat_neigh[i][2] == "BasketballDrill_832x480_50"):
            dados_por_video[0][1] += float(mat_neigh[i][7])
            dados_por_video[1][1] += float(mat_orig[i][7])
        elif(mat_neigh[i][2] == "PartyScene_832x480_50"):
            dados_por_video[0][2] += float(mat_neigh[i][7])
            dados_por_video[1][2] += float(mat_orig[i][7])
        elif(mat_neigh[i][2] == "RaceHorsesC_832x480_30"):
            dados_por_video[0][3] += float(mat_neigh[i][7])
            dados_por_video[1][3] += float(mat_orig[i][7])
        
        if mat_neigh[i][2] != mat_neigh[i+1][2]:    # novo video = plotar gráfico
            # Posição no eixo x para as barras
            x = np.arange(len(errors))

            # Largura das barras
            largura = 0.25

            # Criando o gráfico de barras
            fig, ax = plt.subplots()

            # Plotando cada conjunto de barras
            print(dados[0])
            ax.bar(x - 2 * largura, dados[0], largura, label='NeighBuf')
            ax.bar(x - largura, dados[1], largura, label='OrigBuf')

            # Adicionando título e rótulos dos eixos
            ax.set_xlabel('Taxas de erro')
            ax.set_ylabel('Injection calls')
            ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.2 * y_range)
            plt.title(f'{mat_neigh[i][2].split("_")[0]}: {mat_neigh[i][1].split("_")[0]}')
            ax.set_xticks(x)
            ax.set_xticklabels(errors)
            ax.legend()

            # Exibindo o gráfico
            plt.show()
            fig.savefig(f'{pasta_tabelas}/graph-error_injection/{mat_neigh[i][2].split("_")[0]}-{mat_neigh[i][1].split("_")[0]}.png', dpi=1000)
            
            dados = [[[], [], [], [], []] for _ in range(2)]
    
    dados_por_video[0][0] /= 5
    dados_por_video[0][1] /= 5
    dados_por_video[0][2] /= 5
    dados_por_video[0][3] /= 5
    dados_por_video[1][0] /= 5
    dados_por_video[1][1] /= 5
    dados_por_video[1][2] /= 5
    dados_por_video[1][3] /= 5
    
    print(f'todos: {dados_por_video}')

    # Posição no eixo x para as barras
    x = np.arange(len(videos))

    # Largura das barras
    largura = 0.25

    # Criando o gráfico de barras
    fig, ax = plt.subplots()

    # Plotando cada conjunto de barras
    rects1 = ax.bar(x - 2 * largura, dados_por_video[0], largura, label='NeighBuf')
    rects2 = ax.bar(x - largura, dados_por_video[1], largura, label='OrigBuf')

    # Adicionando título e rótulos dos eixos
    ax.set_xlabel('Videos')
    ax.set_ylabel('Injection calls (1e9)')
    plt.title('All videos - OrigSB and NeighSB')
    ax.set_xticks(x)
    ax.set_xticklabels(videos)
    ax.legend()

    # Função para adicionar valores individuais sobre as barras
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height / 1e9:.1f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 pontos de deslocamento vertical
                        textcoords="offset points",
                        ha='center', va='bottom')

    # Chamando a função para adicionar os valores individuais
    autolabel(rects1)
    autolabel(rects2)

    # Configurando a mesma escala no eixo y para ambos os conjuntos de barras
    ax.set_ylim(0, 3.0e9)
    
    # Posicionando a legenda das barras na esquerda
    ax.legend(loc='upper left')

    # Exibindo o gráfico
    plt.tight_layout()
    plt.show()
    fig.savefig(f'{pasta_tabelas}/graph-error_injection/All videos.png', dpi=1000)
injection_calls(pasta_tabelas)