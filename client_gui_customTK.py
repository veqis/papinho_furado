import threading
import socket
import tkinter as tk
import customtkinter as ctk

class janela_chat:
    def __init__(self, IPHOST, PORTA):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IPHOST, int(PORTA)))

        ################
        tela_thread = threading.Thread(target=self.interface)
        comunica_thread = threading.Thread(target=self.recebe_server)

        tela_thread.start()
        comunica_thread.start()
        ###############

    def interface(self):
        self.janela = ctk.CTk()
        self.janela.title("Chat")

        self.janela.area_chat = ctk.CTkTextbox(self.janela)
        self.janela.area_chat.grid(row=0, column=1, padx=10, pady=10)
        self.janela.area_chat.configure(state="disabled")

        self.janela.area_input = ctk.CTkTextbox(self.janela, width=400, height=50)
        self.janela.area_input.grid(row=1, column=1, padx=10, pady=10)

        self.janela.botao = ctk.CTkButton(self.janela, width=50, height=50, text=">")
        self.janela.botao.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        self.area_envia = ctk




class janela_nick():
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Insira seu nome de usuário")

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

        self.janela.ip_input = ctk.CTkEntry(self.janela, placeholder_text="IP do servidor:")
        self.janela.ip_input.grid(row=0, column=1, padx=10, pady=10)

        self.janela.porta_input = ctk.CTkEntry(self.janela, placeholder_text="Porta do servidor:")
        self.janela.porta_input.grid(row=1, column=1, padx=10, pady=10)

        self.janela.botao_conect = ctk.CTkButton(self.janela, text="Conectar", command=self.connectar)
        self.janela.botao_conect.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.janela.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def ao_fechar(self):
        self.janela.destroy()

    def connectar(self):
        IPHOST = self.janela.ip_input.get()
        PORTA = self.janela.porta_input.get()

        if not IPHOST or not PORTA:
            ctk.messagebox.showerror("Erro", "IP e porta são obrigatórios")
            return

        self.janela.destroy()

        client = janela_chat(IPHOST,PORTA)

        janela_nick().mostrar()

    def mostrar(self):
        self.janela.mainloop()

dados_server().mostrar()