import threading
import socket

nome = input("Insira seu nome de usuário: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('189.127.47.106',55555))

def recebe_do_serv():
    while True:
        try:
            mensagem = client.recv(1024).decode('ascii')
            if mensagem == 'Qual seu nickname?':
                client.send(nome.encode('ascii'))
            else:
                print(mensagem)
        except:
            print("Alguma coisa deu errado!!\nContate o ademir mais proximo")
            client.close()
            break

def enviar_pro_servidor():
    while True:
        mensagem = f'{nome}: {input("")}'
        client.send(mensagem.encode('ascii'))

receber_thread = threading.Thread(target=recebe_do_serv)
receber_thread.start()

enviar_thread = threading.Thread(target=enviar_pro_servidor)
enviar_thread.start()
