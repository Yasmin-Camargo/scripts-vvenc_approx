# Script para coletar estatisticas dos arquivos traces
import os

pasta_arquivos = "../outputs_teste"
num_repeticoes = 2

# Váriaveis
analysis1_inter = 0
analysis1_intra = 0
analysis1_others = 0
analysis2_ime = 0
analysis2_fme = 0
analysis2_affine = 0
analysis2_others = 0

todos_arquivos = os.listdir(pasta_arquivos) # obtendo arquivos
todos_arquivos.sort()

# cria arquivo csv para armazenar dados
tabela = open(f"tabela-trace_analysis.csv", "w") 
tabela.write("Branch-approx; Video; Read BER; Write BER; QP; inter; intra; others; ime; fme; affine; others\n")

# percorre todos arquivos
for nome_arquivo in todos_arquivos:
   
    arquivoTrace = open(f"{pasta_arquivos}/{nome_arquivo}", "r")    # Abrindo arquivo trace
    
    # percorre todo arquivo 
    for linha in arquivoTrace:
        if(linha.split(' ')[0] == '#'): # ignora primeiras linhas do arquivo
            continue
                
        linha = linha.split(';')
        
        if(linha[6] == 'PredMode'):                       # ANÁLISE 1: Modo de predição (intra ou inter)
            if (linha[7][0] == '0'):
                analysis1_inter += int(linha[4]) * int(linha[5]) # incrementa contador: ponderando pela altura x largura do bloco
            elif (linha[7][0] == '1'):
                analysis1_intra += int(linha[4]) * int(linha[5])
            elif (linha[7][0] == '2'):
                analysis1_others += int(linha[4]) * int(linha[5])
        
        
        if(linha[6] == 'MVL0' or linha[6] == 'MVL1'):    # ANÁLISE 2: Vetor inteiro (ime) ou fracionário (fme)
            binario_X = bin(int(linha[7])).replace("0b","")     # converte para binário X do vetor de movimento
            binario_Y = bin(int(linha[8])).replace("0b","")     # converte para binário Y do vetor de movimento
            binario_X = binario_X[-2:].replace("-", "")         # extrai os dois bits menos significativos
            binario_Y = binario_Y[-2:].replace("-", "") 
            
            # coloca dois dígitos para os bínarios que não possuem
            if (binario_X == '0'):
                binario_X = '00'
            elif (binario_X == '1'):
                binario_X = '01'
            if (binario_Y == '0'):
                binario_Y = '00'
            elif (binario_Y == '1'):
                binario_Y = '01'

            binario_XY = binario_X + binario_Y  # concatena X e Y
            
            # Identifica qual é o tipo da classificação
            if (binario_XY == '0000'):  # inteiro
                analysis2_ime += int(linha[4]) * int(linha[5]) # incrementa contador: ponderando pela altura x largura do bloco
            else:                       # fracionário
                analysis2_fme += int(linha[4]) * int(linha[5])
                
        if(linha[6] == 'AffineMVL0' or linha[6] == 'AffineMVL1'):   # ANÁLISE 2: Vetor affine
            analysis2_affine += int(linha[4]) * int(linha[5])
            
        if(linha[6] == 'GeoMVL0' or linha[6] == 'GeoMVL1'):         # ANÁLISE 2: Outros
            analysis2_others += int(linha[4]) * int(linha[5])
   
    if (int(nome_arquivo.split('-')[6][0]) == num_repeticoes - 1): # chegou no último arquivo da repetição
        analysis1_inter = (analysis1_inter / num_repeticoes)       # realiza média das repetições
        analysis1_intra = (analysis1_intra / num_repeticoes) 
        analysis1_others = (analysis1_others / num_repeticoes) 
        analysis2_ime = (analysis2_ime / num_repeticoes) 
        analysis2_fme = (analysis2_fme / num_repeticoes)
        analysis2_affine = (analysis2_affine / num_repeticoes)
        analysis2_others = (analysis2_others / num_repeticoes)
        
        # armazena dados do nome do arquivo no csv
        tabela.write(f"{nome_arquivo.split('-')[0]}; {nome_arquivo.split('-')[1]}; {nome_arquivo.split('-')[2]}; {nome_arquivo.split('-')[3]}; {nome_arquivo.split('-')[5]}; ")
    
        
        total = analysis1_inter + analysis1_intra + analysis1_others    # calcula porcentagem da Análise 1
        analysis1_inter = (analysis1_inter * 100) / total
        analysis1_intra = (analysis1_intra * 100) / total
        analysis1_others = (analysis1_others * 100) / total
        
        total = analysis2_ime + analysis2_fme + analysis2_affine + analysis2_others    # calcula porcentagem da Análise 2
        analysis2_ime = (analysis2_ime * 100) / total
        analysis2_fme = (analysis2_fme * 100) / total
        analysis2_affine = (analysis2_affine * 100) / total
        analysis2_others = (analysis2_others * 100) / total
        
        # armazena resultados analysis1 e analysis2 no arquivo csv
        tabela.write(f"{analysis1_inter}; {analysis1_intra}; {analysis1_others}; ")
        tabela.write(f"{analysis2_ime}; {analysis2_fme}; {analysis2_affine}; {analysis2_others} \n")
        
        analysis1_inter = 0     # reinicializa contadores
        analysis1_intra = 0
        analysis1_others = 0
        analysis2_ime = 0
        analysis2_fme = 0
        analysis2_affine = 0
        analysis2_others = 0
        
tabela.close()