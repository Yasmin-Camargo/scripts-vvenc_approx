# Script com o fluxo de execução: extração dos valores, criação de tabelas e geração dos gráficos

from extract_complete_data import *         # Extrai informações do arquivo de log do vvenc
from calculate_average_data import *        # Calcula média das repetições
from calculate_bdrate import *              # Calcula BD-RATE e BD-PSNR
from calculate_bdrate_repetions import *    # Calcula BD-RATE para cada repetição individual
from generates_bar_graph import *           # Gráfico de barras
from generates_boxplot_graph import *       # Gráfico box plot
from rename import *                        # Renomeia arquivos fora do padrao
from calculation_psnr import *              # Calcula PSNR

# CONFIGURAÇÕES ===================================================================================================================

pasta_arquivos = "../arquivos/VCIP/video_hd/"                   # Diretorio com os arquivos de entrada .log
nome_pasta_resultados = "vcip_randomaccess_errorates-30rp"      # Nome da pasta com os resultados de saida
repeticoes = 15                             # Número de repetições do experimento       
erros_SRAM = False                          # False == erros 10-7, 10-3, ...
allintra = False                            # False == tem codificações com all-intra e random acces
injection_calls = False                     # Armazena na planilha o número Total de chamadas de injeção
psnr = False                                # True == calcula PSNR

# =================================================================================================================================

pasta_saida = f"../results/{nome_pasta_resultados}/"   # Diretorio com os resultados de saida

renomear(f'{pasta_arquivos}logs-pin') #Renomeia arquivos

if erros_SRAM is True:
    renomear(f'{pasta_arquivos}energy-logs')
    total_erros = 3
else: 
    total_erros = 5
    
if injection_calls is True:
    renomear(f'/home/pc-hegel/Documentos/scripts-vvenc_approx/arquivos/VCIP/mem-access-logs')

#Tabela completa com os dados dos arquivos .log
complete_data(pasta_arquivos, pasta_saida, erros_SRAM, injection_calls)   

# Decodificação do vídeo e cálculo do PSNR
if psnr is True:
    calculation_psnr(f'../results/{nome_pasta_resultados}/') # !!! -> verificar configurações no arquivo (caminho decoder, bitstream, video, etc)

#Tabela com as médias das repetições
average_data(pasta_saida, erros_SRAM, injection_calls)    

#Tabela com o cálculo do BD-RATE e BD-PSNR
bd_rate(pasta_saida, erros_SRAM, injection_calls)    

#Tabela BD_Rate das Repetições
bdRate_Repet(pasta_saida, repeticoes, total_erros, allintra)

#Gráfico box plot
box_plot(pasta_saida, erros_SRAM)

#Gráfico Comparação BD_Rate 
#codigo_grafico1(pasta_saida, erros_SRAM)   

