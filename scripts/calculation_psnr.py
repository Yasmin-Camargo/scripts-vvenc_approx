# Script para calcular o PSNR pelo vídeo decodificado

from psnr import *
import os
import subprocess

# Configurações ---------------------------------------------------------
decoder_path = "/home/pc-hegel/Documentos/decoder/VVCSoftware_VTM/bin/DecoderAppStaticd"
bitstream_dir = "/media/pc-hegel/dee15016-3ed5-4dc8-bc3c-6c85f97cb6ff/VCIP_deadline_extension/error-rates/bitstreams"
video_dir = "/home/pc-hegel/Vídeos/videos-vitech/480p"
resolution = (832, 480)
frames = 17
original_bitdepth = 8
encoded_bitdepth = 10
# -----------------------------------------------------------------------

def decode_bitstream(bitstream_path, output_path): # Decodificação do vídeo
    command = [decoder_path, "-b", bitstream_path, "-o", output_path]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def calculation_psnr(pasta_tabelas):
    complete_data = open(f"{pasta_tabelas}complete_data.csv", "r") 
    new_complete_data = open(f"{pasta_tabelas}new_complete_data.csv", "w")

    for linha in complete_data:   
        linha = linha.replace('\n', '')
        linha_dados_separados = linha.split(';')
        
        if 'Approx Module' in linha:
            new_complete_data.write(f'{linha.rstrip()};PSNR Calculation\n') 
            continue

        arquivo_bin = f'{linha_dados_separados[0]}-{linha_dados_separados[2]}-{linha_dados_separados[3]}-{linha_dados_separados[4]}-{linha_dados_separados[1]}-{linha_dados_separados[5]}-{linha_dados_separados[6]}.bin'
        if 'intra_neigh_approx' in arquivo_bin:
                    arquivo_bin = arquivo_bin.replace('intra_neigh_approx', 'intra-neigh-approx')
        if 'intra_orig_approx_rw' in arquivo_bin:
                    arquivo_bin = arquivo_bin.replace('intra_orig_approx_rw', 'intra-orig-approx-rw')
        if '10E_' in arquivo_bin:
                    arquivo_bin = arquivo_bin.replace('10E_', '10E-')
        
        if not (os.path.exists(f'{bitstream_dir}/{arquivo_bin}')):
            new_complete_data.write(f'{linha.rstrip()};-\n')
            print(f'\nArquivo {arquivo_bin} não encontrado \n')
        else: 
            decode_bitstream(f'{bitstream_dir}/{arquivo_bin}',f'{pasta_tabelas}/arquivo_decodificado.yuv')

            # Cálculo PSNR
            original_video = f"{video_dir}{linha_dados_separados[2]}.yuv"
            encoded_video = f'{pasta_tabelas}/arquivo_decodificado.yuv'

            psnr_y, pnsr_u, psnr_v, psnr_yuv = calculate_psnr(
                original_video, encoded_video, resolution, 
                frames, original_bitdepth, encoded_bitdepth
            )

            new_complete_data.write(f'{linha.rstrip()};{round(psnr_yuv, 3)}\n')
            print(f'\n---> Old PSNR: {linha_dados_separados[7]} \t\t New PSNR: {round(psnr_yuv, 3)}\n')



