import socket
import os
import time

HOST = 'localhost'
PORT = 64204

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)
print('Aguardando a conexão')
conn, ender = server.accept()
print('Conectado em', ender)

def listaArquivos():
    try:
        caminhoPasta = os.path.join(os.getcwd(), 'arquivoServidor')
        arquivos = os.listdir(caminhoPasta)
        return arquivos
    except OSError as erro:
        print(f"Erro ao listar arquivos em '{caminhoPasta}': {erro}")
        return []

def removerArquivo(nomeArquivo):
    caminhoArquivo = os.path.join(os.getcwd(), 'arquivoServidor', nomeArquivo)
    if os.path.exists(caminhoArquivo):
        try:
            os.remove(caminhoArquivo)
            return "Arquivo removido com sucesso."
        except OSError as e:
            return f"Erro ao remover o arquivo {nomeArquivo}: {e}"
    else:
        return f"O arquivo {nomeArquivo} não existe."

def receberArquivoCliente(nomeArquivo):
    caminhoArquivo = os.path.join(os.getcwd(), 'arquivoServidor', nomeArquivo)
    tamanhoArquivo = (conn.recv(4))
    tamanhoArquivo = int.from_bytes(tamanhoArquivo, byteorder='big')
    with open(caminhoArquivo, "wb") as arquivo:
        print("até aqui tudo certo")
        data = conn.recv(tamanhoArquivo)
        arquivo.write(data)
        print(f"Arquivo {nomeArquivo} recebido e salvo com sucesso no servidor.")

def enviarArquivoParaCliente(nomeArquivo):
    try:
        caminhoArquivo = os.path.join(os.getcwd(), 'arquivoServidor', nomeArquivo)
        if os.path.exists(caminhoArquivo):
            tamanhoArquivo = os.path.getsize(caminhoArquivo)
            tamanhoArquivo = tamanhoArquivo.to_bytes(4, byteorder='big')
            conn.send(tamanhoArquivo)
            with open(caminhoArquivo, 'rb') as arquivo:
                data = arquivo.read()
                conn.send(data)
                print(f"Arquivo {nomeArquivo} enviado.")
        else:
            print(f"Arquivo {nomeArquivo} não encontrado no servidor.")
    except Exception as e:
        print(f"Erro ao enviar arquivo para o cliente: {e}")


while True:
    try:
        msg = conn.recv(1024)
        if not msg:
            print("server fechando em 1 minuto")
            time.sleep(60)
            conn.close
            server.close()
            break
        mensagem = msg.decode()
        mensagem = mensagem.split() 
        if mensagem[0] == "1" and len(mensagem) >= 2:
            if mensagem[1] == "server":
                lista = listaArquivos() 
                nomes = "\n".join(lista)
                conn.send(nomes.encode())
            else:
                pass

        elif mensagem[0] == "2" and len(mensagem) >= 2:
            nomeArquivo = mensagem[1]
            resposta = removerArquivo(nomeArquivo)
            conn.send(resposta.encode())
        elif mensagem[0] == "3" and len(mensagem) >= 2:
            nomeArquivo = mensagem[1]
            receberArquivoCliente(nomeArquivo)
        elif mensagem[0] == "4" and len(mensagem) >= 2:
            nomeArquivo = mensagem[1]
            enviarArquivoParaCliente(nomeArquivo)
        else:                   
            resposta = "Comando não reconhecido"
            conn.send(resposta.encode())
    except ConnectionResetError:
            print("Conexão encerrada pelo cliente.")
            conn.close()
            server.close()
            break