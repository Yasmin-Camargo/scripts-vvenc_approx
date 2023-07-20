# Script para gerar arquivos tracefiles da decodificação com o VVC
import os

pasta_arquivos_bin = "../bitstreams"
pasta_arquivos_out = "../outputs"

todos_arquivos = os.listdir(pasta_arquivos_bin) # Obtendo nomes dos arquivos
todos_arquivos.sort()

for nome_arquivo in todos_arquivos: # percorrendo todos arquivos
    comando = f"../VVCSoftware_VTM/bin/DecoderAppStaticd -b {pasta_arquivos_bin}/{nome_arquivo} \--TraceFile=\"{pasta_arquivos_out}/{nome_arquivo.split('.')[0]}.vtmbmsstats\" \--TraceRule=\"D_BLOCK_STATISTICS_CODED:poc>=0\""
    os.system(comando)
    
    