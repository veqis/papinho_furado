import threading
import socket

host = '192.168.100.5' #localhost
porta = 55555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, porta))
servidor.listen()

clients= []
nomes = []

def broadcast(mensagem):
    for client in clients:
        client.send(mensagem)

def visualizar(client):
    while True:
        try:
            mensagem = client.recv(1024)
            broadcast(mensagem)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            nome = nomes[index]
            broadcast(f'{nome} saiu'.encode('ascii'))
            nomes.remove(nome)
            break

def receber():
    while True:
        client, adress = servidor.accept()
        print(f"{str(adress)} conectou-se")

        client.send('Qual seu nickname?'.encode('ascii'))
        nome = client.recv(1024).decode('ascii')
        nomes.append(nome)

        clients.append(client)

        print(f'Nome do client: {nome}')
        broadcast(f'{nome} entrou!'.encode('ascii'))

        client.send('Conectado ao servidor com sucesso'.encode('ascii'))

        threads = threading.Thread(target=visualizar, args=(client,))
        threads.start()

print("[*]servidor iniciado com sucesso\n")
receber()