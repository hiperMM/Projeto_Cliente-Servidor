import socket
import os

HOST = '127.0.0.1'
PORT = 64204

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

def listaArquivosCliente():
    try: 
        caminhoPasta = os.path.join(os.getcwd(), 'arquivoCliente')
        arquivos = os.listdir(caminhoPasta)
        return "\n".join(arquivos)  # Retorna a lista como uma string formatada
    except OSError as erro:
        print(f"Erro ao listar arquivos em '{caminhoPasta}': {erro}")
        return "Erro ao listar arquivos."

def enviarArquivoServer(nomeArquivo):
    try:
        caminhoArquivo = os.path.join(os.getcwd(), 'arquivoCliente', nomeArquivo)
        if os.path.exists(caminhoArquivo):
            tamanhoArquivo = os.path.getsize(caminhoArquivo)
            tamanhoArquivo = tamanhoArquivo.to_bytes(4, byteorder='big')
            cliente.send(tamanhoArquivo)
            with open(caminhoArquivo, 'rb') as arquivo:
                data = arquivo.read()
                cliente.send(data)
                print(f"Arquivo {nomeArquivo} enviado.")
        else:
            print(f"Arquivo {nomeArquivo} não encontrado.")
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")



def receberArquivoDoServidor(nomeArquivo):
    try:
        caminhoArquivo = os.path.join(os.getcwd(), 'arquivoCliente', nomeArquivo)
        tamanhoArquivo = (cliente.recv(4))
        tamanhoArquivo = int.from_bytes(tamanhoArquivo, byteorder='big')
        with open(caminhoArquivo, 'wb') as arquivo:
             print("até aqui tudo certo")
             data = cliente.recv(tamanhoArquivo)   
             arquivo.write(data)
             print(f"Arquivo {nomeArquivo} recebido do servidor e salvo com sucesso no cliente.")
    except Exception as e:
        print(f"Erro ao receber arquivo do servidor: {e}")



print("Digite 1 + cliente para mostrar os arquivos do cliente, ou server para mostrar os arquivos do servidor")
print("Digite 2 + o nome do arquivo para removê-lo")
print("digite 3 + nome do arquivo para fazer o upload para o server")
print("Digite 4 + nome do arquivo para fazer download para o cliente")
        
while True:
    mensagem = input(" ")
    cliente.send(mensagem.encode())
    mensagem = mensagem.split()

    if mensagem[0] == '1' and mensagem[1] == "cliente":
        arquivos_cliente = listaArquivosCliente()
        print(f"Lista de arquivos do cliente:\n{arquivos_cliente}")
    elif mensagem[0] == '3':
        cliente.send(mensagem.encode())
    elif mensagem[0] == '4':
        nomeArquivo = mensagem[1]
        receberArquivoDoServidor(nomeArquivo)
    else:
        resposta = cliente.recv(1024).decode()
        if resposta.startswith("Arquivo recebido com sucesso."):
            print(resposta)
        else:
            print(resposta)

