import threading
import socket
import tkinter
import tkinter.scrolledtext
import tkinter.messagebox
from tkinter import simpledialog


IPHOST = 'localhost'
PORTA = 9090

class Client:
    def __init__(self, IPHOST, PORTA):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IPHOST, int(PORTA)))

        msg = tkinter.Tk()
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

    def interface(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#444654")

        self.area_chat = tkinter.scrolledtext.ScrolledText(self.win)
        self.area_chat.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        self.area_chat.configure(bg='#646474', fg='white')
        self.area_chat.config(state='disabled')

        self.area_enviar = tkinter.Text(self.win, height=3)
        self.area_enviar.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        self.area_enviar.configure(bg='#646474', fg='white')

        #enviar mensagem com enter sem necessidade do botão, resolver erro de n resetar linha depois
        #self.area_enviar.bind("<Return>", lambda event: self.envia_msg_server())

        self.botao = tkinter.Button(self.win, text="Enviar", command=self.envia_msg_server)
        self.botao.config(font=("Arial", 12))
        self.botao.grid(row=3, column=0, padx=20, pady=5, sticky="e")

        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(1, weight=1)
        self.win.rowconfigure(2, weight=1)

        self.gui_completa = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def envia_msg_server(self):
        message = f"{self.nome}: {self.area_enviar.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.area_enviar.delete('1.0', tkinter.END)
        self.area_enviar.mark_set("insert", "1.0")


    def stop(self):
        self.executando = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def recebe_server(self):
        while self.executando:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == '99,,45468,,':
                    self.sock.send(self.nome.encode('utf-8'))
                else:
                    if self.gui_completa:
                        self.area_chat.config(state='normal')
                        self.area_chat.insert('end', message)
                        self.area_chat.yview('end')
                        self.area_chat.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("ERRO!!")
                self.sock.close()
                break

class login(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Insira seu nome de usuário")
        self.geometry("300x150")

        tkinter.Label(self, text="Nome de usuário:").grid(row=0, column=0, padx=10, pady=10)
        self.login_input = tkinter.Entry(self)
        self.login_input.grid(row=0, column=1, padx=10, pady=10)

        self.confirm_button = tkinter.Button(self, text="Confirmar", command=self.confirm)
        self.confirm_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        #self.protocol("WM_DELETE_WINDOW", self.stop)

        self.login = None

    def confirm(self):
        self.login = self.login_input.get()
        self.destroy()

class ConnectDialog(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dados do servidor")
        self.geometry("300x150")

        tkinter.Label(self, text="IP do servidor:").grid(row=0, column=0, padx=10, pady=10)
        self.ip_input = tkinter.Entry(self)
        self.ip_input.grid(row=0, column=1, padx=10, pady=10)

        tkinter.Label(self, text="Porta do servidor:").grid(row=1, column=0, padx=10, pady=10)
        self.port_input = tkinter.Entry(self)
        self.port_input.grid(row=1, column=1, padx=10, pady=10)

        self.connect_button = tkinter.Button(self, text="Conectar", command=self.connect)
        self.connect_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.ip = None
        self.port = None

    def connect(self):
        self.ip = self.ip_input.get()
        self.port = self.port_input.get()

        if not self.ip or not self.port:
            tkinter.messagebox.showerror("Erro", "IP e porta são obrigatórios")
            return

        self.destroy()


connect_dialog = ConnectDialog(None)
connect_dialog.wait_window()
IPHOST = connect_dialog.ip
PORTA = connect_dialog.port

if not IPHOST or not PORTA:
    exit(0)

client = Client(IPHOST, PORTA)
