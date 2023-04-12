import threading
import socket
import tkinter as tk
import customtkinter as ctk

class Client:
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((IPHOST, int(PORTA)))

    msg = ctk.Tk()
    msg.withdraw()

    dialog = login(msg)
    msg.wait_window(dialog)

    self.nome = dialog.login

    self.gui_completa = False
    self.executando = True

    tela_thread = threading.Thread(target=self.interface)
    recebe_server_thread = threading.Thread(target=self.recebe_server)
    tela_thread.start()
    recebe_server_thread.start()



class janela_nick():
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Insira seu nome de usuário")
        self.janela.geometry("160x100")

        self.janela.login_input = ctk.CTkEntry(self.janela, placeholder_text="Nome de usuário:")
        self.janela.login_input.grid(row=0, column=1, padx=10, pady=10)

        self.janela.confirm_button = ctk.CTkButton(self.janela, text="Confirmar", command=self.confirma_nick)
        self.janela.confirm_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.janela.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def ao_fechar(self):
        self.janela.destroy()

    def confirma_nick(self):
        self.janela.login = self.janela.login_input.get()
        self.janela.destroy()

    def mostrar(self):
        self.janela.mainloop()

class dados_server():
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Dados do servidor")
        self.janela.geometry("160x150")

        self.janela.ip_input = ctk.CTkEntry(self.janela, placeholder_text="IP do servidor:")
        self.janela.ip_input.grid(row=0, column=1, padx=10, pady=10)

        self.janela.porta_input = ctk.CTkEntry(self.janela, placeholder_text="Porta do servidor:")
        self.janela.porta_input.grid(row=1, column=1, padx=10, pady=10)

        self.janela.botao_conect = ctk.CTkButton(self.janela, text="Conectar", command=self.connect)
        self.janela.botao_conect.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.janela.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def ao_fechar(self):
        self.janela.destroy()

    def connect(self):
        IPHOST = self.janela.ip_input.get()
        PORTA = self.janela.porta_input.get()

        if not IPHOST or not PORTA:
            ctk.messagebox.showerror("Erro", "IP e porta são obrigatórios")
            return

        self.janela.destroy()
        janela_nick().mostrar()

    def mostrar(self):
        self.janela.mainloop()

dados_server().mostrar()
