# Script para análisar os maiores valores armazenados no buffer

import matplotlib.pyplot as plt

# Função para criar e exibir o histograma
def criar_histograma(nome_arquivo):
    histograma = {}
    menor_valor = float('inf')  # Define o menor valor como infinito inicialmente
    maior_valor = float('-inf')  # Define o maior valor como infinito negativo inicialmente

    # Processar o arquivo linha por linha
    with open(nome_arquivo, 'r') as file:
        for line in file:
            numero = float(line.strip())
            histograma[numero] = histograma.get(numero, 0) + 1
            menor_valor = min(menor_valor, numero)  # Atualiza o menor valor
            maior_valor = max(maior_valor, numero)  # Atualiza o maior valor

    # Exibir o histograma
    plt.bar(histograma.keys(), histograma.values(), color='blue', edgecolor='black')
    plt.xlabel('Valores')
    plt.ylabel('Frequência')
    plt.title('Histograma da Distribuição de Números')
    plt.legend(['Menor valor: {:.2f} \nMaior valor: {:.2f}'.format(menor_valor, maior_valor)], handlelength=0)

    plt.grid(True)
    plt.savefig('histograma.png')  # Salvar o gráfico como uma imagem
    plt.show()

# Nome do arquivo
nome_arquivo = '../outputs/saidaAnalise_maiores.txt'

# Criar e exibir o histograma
criar_histograma(nome_arquivo)