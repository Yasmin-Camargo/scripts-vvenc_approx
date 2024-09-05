# Script para a avaliação da distribuição dos vetores fracionários

import os

pasta_arquivos = "testset_BasketballDrill_traces"

def vetores_fracionarios(pasta_arquivos, nome_arquivo): 
    # Váriaveis
    mvL0 = {'I':0, 'H0': 0, 'H1':  0, 'H2': 0, 'Q0': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0, 'Q8': 0, 'Q8': 0, 'Q9': 0, 'Q10': 0, 'Q11': 0 }
    mvL1 = {'I':0, 'H0': 0, 'H1':  0, 'H2': 0, 'Q0': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0, 'Q8': 0, 'Q8': 0, 'Q9': 0, 'Q10': 0, 'Q11': 0 }
    flag = 0
    linha_certa = 0
    CTU_Line_Total = 4
    
    temp_LD_Line = []
    for i in range (0, CTU_Line_Total):
        temp_LD_Line.append('')
    
    temp_RA_Line = []
    for i in range (0, CTU_Line_Total):
        temp_RA_Line.append('')

    # Abrindo arquivo:
    tabela = open(f"tabela-Fractional_samples_analysis.csv", "a") 
    arquivo = open(f"{pasta_arquivos}/{nome_arquivo}", "r")
    nome_arquivo = nome_arquivo.split('_')

    # percorre todo arquivo
    for linha in arquivo:
        linha = linha.split(';')
        if (linha_certa == 0):     # ignora primeiras linhas
            if(linha[0] == 'BlockStat'):
                linha_certa = 1
                frame = "#"
                cont_line_CTU = 0
                
        if (linha_certa == 1): 
            if (frame != linha[1]): # se mudou de frame, armazena dados no csv
                for i in range (0, CTU_Line_Total):
                    if (temp_LD_Line[i] != ''):
                        tabela.write(f'{temp_LD_Line[i]}')
                        
                for i in range (0, CTU_Line_Total):
                    if (temp_RA_Line[i] != ''):
                        tabela.write(f'{temp_RA_Line[i]}') 
                
                # reinicializa variaveis
                temp_LD_Line = []
                for i in range (0, CTU_Line_Total):
                    temp_LD_Line.append('')
                temp_RA_Line = []
                for i in range (0, CTU_Line_Total):
                    temp_RA_Line.append('')
                cont_line_CTU = 0
                frame = linha[1]
                flag = 0
                mvL0 = {'I':0, 'H0': 0, 'H1':  0, 'H2': 0, 'Q0': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0, 'Q8': 0, 'Q8': 0, 'Q9': 0, 'Q10': 0, 'Q11': 0 }
                mvL1 = {'I':0, 'H0': 0, 'H1':  0, 'H2': 0, 'Q0': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0, 'Q8': 0, 'Q8': 0, 'Q9': 0, 'Q10': 0, 'Q11': 0 }

            if (flag == 1):
                if (int(linha[3]) > ((cont_line_CTU + 1) * 128)): # mudou de linha CTU
                    temp_LD_Line[cont_line_CTU] += (f'{nome_arquivo[0]}; {nome_arquivo[2].split(".")[0]}; {nome_arquivo[1]}; ')
                    temp_LD_Line[cont_line_CTU] += (f'{frame}; L0; {(cont_line_CTU)} --> y[{(cont_line_CTU)*128}, {((cont_line_CTU+1)*128)}]; {mvL0["I"]}; {mvL0["H0"]}; {mvL0["H1"]}; {mvL0["H2"]}; {mvL0["Q0"]}; {mvL0["Q1"]}; {mvL0["Q2"]}; {mvL0["Q3"]}; {mvL0["Q4"]}; {mvL0["Q5"]}; {mvL0["Q6"]}; {mvL0["Q7"]}; {mvL0["Q8"]}; {mvL0["Q9"]}; {mvL0["Q10"]}; {mvL0["Q11"]}\n')
                    temp_RA_Line[cont_line_CTU] += (f'{nome_arquivo[0]}; {nome_arquivo[2].split(".")[0]}; {nome_arquivo[1]}; ')
                    temp_RA_Line[cont_line_CTU] += (f'{frame}; L1; {(cont_line_CTU)} --> y[{(cont_line_CTU)*128}, {((cont_line_CTU+1)*128)}]; {mvL1["I"]}; {mvL1["H0"]}; {mvL1["H1"]}; {mvL1["H2"]}; {mvL1["Q0"]}; {mvL1["Q1"]}; {mvL1["Q2"]}; {mvL1["Q3"]}; {mvL1["Q4"]}; {mvL1["Q5"]}; {mvL1["Q6"]}; {mvL1["Q7"]}; {mvL1["Q8"]}; {mvL1["Q9"]}; {mvL1["Q10"]}; {mvL1["Q11"]}\n')
                    
                    # reinicializa variaveis
                    mvL0 = {'I':0, 'H0': 0, 'H1':  0, 'H2': 0, 'Q0': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0, 'Q8': 0, 'Q8': 0, 'Q9': 0, 'Q10': 0, 'Q11': 0 }
                    mvL1 = {'I':0, 'H0': 0, 'H1':  0, 'H2': 0, 'Q0': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Q5': 0, 'Q6': 0, 'Q7': 0, 'Q8': 0, 'Q8': 0, 'Q9': 0, 'Q10': 0, 'Q11': 0 }
                    flag = 0
                    cont_line_CTU += 1

            # linha de interesse
            if(linha[6] == 'MVL0' or linha[6] == 'MVL1'): 
                frame = linha[1]
                flag = 1                                            # converte para binário:
                binario_X = bin(int(linha[7])).replace("0b","")     # -> X do vetor de movimento
                binario_Y = bin(int(linha[8])).replace("0b","")     # -> Y do vetor de movimento
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

                binario_XY = binario_X + binario_Y             # concatena X e Y
        
                # Identifica qual é o tipo da classificação
                classificacao = ''
                if (binario_XY == '0000'):
                    classificacao = 'I'
                elif (binario_XY == '0001'):
                    classificacao = 'Q0'
                elif (binario_XY == '0010'):
                    classificacao = 'H0'
                elif (binario_XY == '0011'):
                    classificacao = 'Q1'
                elif (binario_XY == '0100'):
                    classificacao = 'Q2'
                elif (binario_XY == '0101'):
                    classificacao = 'Q3'
                elif (binario_XY == '0110'):
                    classificacao = 'Q4'
                elif (binario_XY == '0111'):
                    classificacao = 'Q5'
                elif (binario_XY == '1000'):
                    classificacao = 'H1'
                elif (binario_XY == '1001'):
                    classificacao = 'Q6'
                elif (binario_XY == '1010'):
                    classificacao = 'H2'
                elif (binario_XY == '1011'):
                    classificacao = 'Q7'
                elif (binario_XY == '1100'):
                    classificacao = 'Q8'
                elif (binario_XY == '1101'):
                    classificacao = 'Q9'
                elif (binario_XY == '1110'):
                    classificacao = 'Q10'
                elif (binario_XY == '1111'):
                    classificacao = 'Q11'
                else:
                    print(binario_XY)
                
                # incrementa contador: ponderando pela altura x largura do bloco
                if (linha[6] == 'MVL0'):
                    mvL0[classificacao] += int(linha[4]) * int(linha[5])
                elif (linha[6] == 'MVL1'): 
                    mvL1[classificacao] += int(linha[4]) * int(linha[5])
            
# -------------------------------------------------------------------------------------

todos_arquivos = os.listdir(pasta_arquivos) # obtendo arquivos
todos_arquivos.sort()

# cria arquivo csv para armazenar dados
tabela = open(f"tabela-Fractional_samples_analysis.csv", "w") 
tabela.write("Video; QP; Config; Frame POC; Ref. frame list; I; H0; H1; H2; Q0; Q1; Q2; Q3; Q4; Q5; Q6; Q7; Q8; Q9; Q10; Q11\n")
tabela.close()

# percorre todos arquivos
for nome_arquivo in todos_arquivos:
    if (nome_arquivo.split(".")[1] == "csv"):
        vetores_fracionarios(pasta_arquivos, nome_arquivo)