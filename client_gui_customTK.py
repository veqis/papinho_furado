import threading
import socket
import customtkinter as ctk
import tkinter as tk

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

        self.janela.mainloop()

    def connectar(self):
        IPHOST = self.janela.ip_input.get()
        PORTA = self.janela.porta_input.get()

        if not IPHOST or not PORTA:
            ctk.messagebox.showerror("Erro", "IP e porta são obrigatórios")
            return

        self.janela.destroy()
        janela_nick(IPHOST, PORTA)

class janela_nick():
    def __init__(self, IPHOST, PORTA):
        self.janela = ctk.CTk()
        self.janela.title("Insira seu nome de usuário")

        self.janela.login_input = ctk.CTkEntry(self.janela, placeholder_text="Nome de usuario:")
        self.janela.login_input.grid(row=0, column=1, padx=10, pady=10)

        self.janela.confirm_button = ctk.CTkButton(self.janela, text="Confirmar", command=lambda: self.confirma_nick(IPHOST, PORTA))
        self.janela.confirm_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.janela.mainloop()

    def confirma_nick(self, IPHOST, PORTA):
        NOME = self.janela.login_input.get()

        if not NOME:
            ctk.mensagembox.showerror("Erro", "Um nick é obrigatorio")
            return

        self.janela.destroy()
        tela_chat(IPHOST, PORTA, NOME)


class tela_chat():
    def __init__(self, IPHOST, PORTA, NOME):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IPHOST, int(PORTA)))
        
        self.NOME = NOME    

        # msg = tk.Tk()
        # msg.withdraw()

        # dialog = janela_nick(msg)
        # msg.wait_window(dialog)  

        self.gui_completa = False
        self.executando = True

        tela_thread = threading.Thread(target=self.interface)
        comunica_thread = threading.Thread(target=self.recebe_server)
        
        tela_thread.start()
        comunica_thread.start()
        

    def interface(self):
        self.janela = ctk.CTk()
        self.janela.title("Chat")

        self.area_chat = ctk.CTkTextbox(self.janela, width=400)
        self.area_chat.grid(row=0, column=1, padx=10, pady=10)
        self.area_chat.configure(state="disabled")

        self.area_enviar = ctk.CTkTextbox(self.janela, width=400, height=50)
        self.area_enviar.grid(row=1, column=1, padx=10, pady=10)

        self.botao = ctk.CTkButton(self.janela, width=50, height=50, text=">", command=self.envia_msg_server)
        self.botao.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        self.gui_completa = True
        
        self.janela.mainloop()

    def envia_msg_server(self):
        mensagem = f"{self.NOME}: {self.area_enviar.get('1.0', 'end')}"
        self.sock.send(mensagem.encode('utf-8'))
        self.area_enviar.delete('1.0', ctk.END)
        self.area_enviar.mark_set("insert", "1.0")


    def recebe_server(self):
        while self.executando:
            try:
                mensagem = self.sock.recv(1024).decode('utf-8')
                if mensagem == '99,,45468,,':
                    self.sock.send(self.NOME.encode('utf-8'))
                else:
                    if self.gui_completa:
                        self.area_chat.configure(state='normal')
                        self.area_chat.insert('end', mensagem)
                        self.area_chat.yview('end')
                        self.area_chat.configure(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("ERRO!!")
                self.sock.close()
                break

dados_server()
