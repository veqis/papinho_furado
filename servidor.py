import threading
import socket

ip = 'localhost'
porta = 9090

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ip, porta))
servidor.listen()

clients = []
nomes = []

def enviar_msg(mensagem):
    for client in clients:
        client.send(mensagem)

def visualizar(client):
    while True:
        try:
            mensagem = client.recv(1024)
            enviar_msg(mensagem)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            nome = nomes[index]
            nomes.remove(nome)
            break

def receber():
    while True:
        client, adress = servidor.accept()

        client.send('99,,45468,,'.encode('utf-8'))
        nome = client.recv(1024).decode('utf-8')
        
        nomes.append(nome)
        clients.append(client)

        print(f'[*]Client {nome}:{str(adress)} conectou-se.')
        enviar_msg(f'{nome} entrou\n'.encode('utf-8'))

        client.send('[*]Conectado ao servidor com sucesso\n'.encode('utf-8'))

        threads = threading.Thread(target=visualizar, args=(client,))
        threads.start()

print("[*]servidor iniciado com sucesso")
receber()