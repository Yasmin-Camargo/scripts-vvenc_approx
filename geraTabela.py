import glob

#caminho = "/home/research-data-ssd/yasmin/reports/"
caminho = "C:/Users/yasmi/codigos_github/Script-Gerar_Tabela/reports/"
nomeout="*.out"
teste2=""
cont=0
cont2=0
cont5=0
cont6=0
nomeArquivo = ""
config = ""
qp = ""
tempo=0

tabela = open("tabela.csv", "w")
tabela.write("Video;Config;QP;Frames;BitRate;PSNR;Tempo\n")
tabela.close

#NOME ARQUIVOS
arquivos_out = glob.glob(f'{caminho}{nomeout}') 

for nome in arquivos_out:
    for letra in nome:
        if (letra == "."):
            cont6=0
        if (cont6 == 1):
            nomeArquivo += letra
       
        elif (letra == "\\"):
            cont6=1
    nomeArquivo += ".out\n!\n"
    
for f in nomeArquivo:
    if (f == "!"):
        nome = teste2.strip('\n')
        tabela = open("tabela.csv", "a")
        tabela.write(nome)
        tabela.close
        
        #Determinar qual configuração
        cont3=0
        cont4=0
        for word in teste2:
            if (cont3 == 1):
                config += word
            if (word == "_"):
                cont3+=1
                cont4+=1
            if (cont4 == 2):
                qp = ""
                cont4+=1
                if (config == "LD_"):
                    tabela = open("tabela.csv", "a")
                    tabela.write(";Low Delay;")
                    tabela.close
                elif (config == "RA_"):
                    tabela = open("tabela.csv", "a")
                    tabela.write(";Randon Acces;")
                    tabela.close
                cont4 = 0
                cont3 = 0
                cont5 = 5
                
           
           #Determinar qual QP
            if (cont5 == 5):
                if (word == "."):
                    cont5 += 1
                else:
                    qp += word
                    if (qp == "_22"):
                        tabela = open("tabela.csv", "a")
                        tabela.write("22;")
                        tabela.close
                    elif (qp == "_27"):
                        tabela = open("tabela.csv", "a")
                        tabela.write("27;")
                        tabela.close   
                    elif (qp == "_32"):
                        tabela = open("tabela.csv", "a")
                        tabela.write("32;")
                        tabela.close   
                    elif (qp == "_37"):
                        tabela = open("tabela.csv", "a")
                        tabela.write("37;")
                        tabela.close 
                        
        
        #CODIGO PARA BUSCAR Frames, BitRate, PSNR, Tempo
        cont=0
        cont6=0
        espaco=0
        layerId=0
        erro=0
        testeErro = 0
        arquivo = open (f'{caminho}{nome}','r')
        for linha in arquivo:
            if (layerId == 2):
                for word in linha:
                    #Erro quando lê duas linhas
                    if (erro==0 and word == "P"):
                        erro=5
                    if (erro == 5):
                        if (word == "]"):
                            testeErro+=1
                            if (testeErro==4):
                                erro = 1
                        else:
                            erro = 5
                    #     
                    elif (word==" "):
                        espaco+=1
                        if(cont==0): 
                            cont6+=1
                            cont=1   
                        if (espaco<=1):
                            tabela = open("tabela.csv", "a")
                            tabela.write(";")
                            tabela.close
                    elif (word!='a' and cont6<=2): # Armazenar Frames e BitRate
                        tabela = open("tabela.csv", "a")
                        tabela.write(word.strip())
                        tabela.close
                        cont=0
                        espaco=0
                    elif (cont6==6):     # Armazenar PSNR
                        tabela = open("tabela.csv", "a")
                        tabela.write(word.strip())
                        tabela.close
                        cont=0
                        espaco=0
                    else:
                        cont=0
                        
            if ("LayerId  0") in linha:
                layerId = 0
            if (layerId>=0 and layerId<=2):
                layerId+=1           
            else:
                layerId=0
               
            tempo=0
            if ("Total Time:") in linha: # Armazenar tempo
                for word in linha:
                    if (word == "s"):
                        tempo=2
                    if (tempo == 1):
                        tabela = open("tabela.csv", "a")
                        tabela.write(word.strip())
                        tabela.close
                    if (word == ":"):
                        tempo=1 
                    if (word == "p"):
                        tabela = open("tabela.csv", "a")
                        tabela.write("\n")
                        tabela.close
    
        teste2 = ""
        nome = ""  
        config = ""      
    else:
        teste2 += f 
        
    
        

