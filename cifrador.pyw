import re
import tkinter as tk

from src.vigenere import cifrar
from src.vigenere import decifrar

class AppCifrador(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.place(x=0, y=0, width=480, height=640)
        self.criar_widgets()

    def criar_widgets(self):
        """Inicialização dos widgets da aplicação."""

        # Campo de entrada do texto a ser cifrado/decifrado
        self.texto_entrada = tk.Text(self, bg="white")
        self.texto_entrada.place(x=10, y=10, width=445, height=270)

        # Barras de rolagem do texto de entrada
        self.scroll_entrada_x = tk.Scrollbar(self, orient="horizontal", command=self.texto_entrada.xview)
        self.scroll_entrada_y = tk.Scrollbar(self, orient="vertical", command=self.texto_entrada.yview)
        self.scroll_entrada_x.place(x=10, y=280, width=445, height=15)
        self.scroll_entrada_y.place(x=455, y=10, width=15, height=285)
        self.texto_entrada["xscrollcommand"] = self.scroll_entrada_x.set
        self.texto_entrada["yscrollcommand"] = self.scroll_entrada_y.set
        
        # Botão de cifrar texto
        self.botao_cifrar = tk.Button(self, text="Cifrar Mensagem")
        self.botao_cifrar["text"] = "Cifrar Mensagem"
        self.botao_cifrar["command"] = self.cifrar_mensagem
        self.botao_cifrar.place(x=10, y=305, width=120, height=25)

        # Campo de entrada da chave de cifração/decifração
        self.chave = tk.StringVar()
        self.texto_chave = tk.Entry(self, textvariable=self.chave)
        self.texto_chave["bg"] = "white"
        self.texto_chave.place(x=140, y=305, width=200, height=25)

        # Botão de decifrar texto
        self.botao_decifrar = tk.Button(self)
        self.botao_decifrar["text"] = "Decifrar Mensagem"
        self.botao_decifrar["command"] = self.decifrar_mensagem
        self.botao_decifrar.place(x=350, y=305, width=120, height=25)

        # Campo de saída do texto a ser cifrado/decifrado
        self.texto_saida = tk.Text(self, bg="gray", fg="white")
        self.texto_saida["state"] = "disabled"
        self.texto_saida.place(x=10, y=340, width=445, height=270)

        # Barras de rolagem do texto de saída
        self.scroll_saida_x = tk.Scrollbar(self, orient="horizontal", command=self.texto_saida.xview)
        self.scroll_saida_y = tk.Scrollbar(self, orient="vertical", command=self.texto_saida.yview)
        self.scroll_saida_x.place(x=10, y=610, width=445, height=15)
        self.scroll_saida_y.place(x=455, y=340, width=15, height=285)
        self.texto_saida["xscrollcommand"] = self.scroll_saida_x.set
        self.texto_saida["yscrollcommand"] = self.scroll_saida_y.set
       

    def cifrar_mensagem(self):
        """Cifração da mensagem digitada no campo de entrada."""

        mensagem = self.texto_entrada.get("1.0", "end")
        chave = self.chave.get()

        if self.validar_chave():
            msg_cifrada = cifrar(mensagem, chave)
            
            # Atualização do conteúda da caixa de texto de saída
            self.texto_saida["state"] = "normal"
            self.texto_saida.delete("1.0", "end")
            self.texto_saida.insert("1.0", msg_cifrada)
            self.texto_saida["state"] = "disabled"


    def decifrar_mensagem(self):
        """Decifração da mensagem digitada no campo de entrada."""

        mensagem = self.texto_entrada.get("1.0", "end")
        chave = self.chave.get()

        if self.validar_chave():
            msg_decifrada = decifrar(mensagem, chave)
            
            # Atualização do conteúda da caixa de texto de saída
            self.texto_saida["state"] = "normal"
            self.texto_saida.delete("1.0", "end")
            self.texto_saida.insert("1.0", msg_decifrada)
            self.texto_saida["state"] = "disabled"

    
    def validar_chave(self):
        """Verificação se a chave de cifração/decifração é válida."""

        chave = self.chave.get()

        if re.match(r"^[A-z]+$", chave, re.ASCII):
            # Verificação se a chave é composta apenas por letras ASCII
            return True
        else:
            # Informa ao usuário que a chave escolhida é inválida
            self.texto_saida["state"] = "normal"
            self.texto_saida.delete("1.0", "end")
            self.texto_saida.insert("1.0", "Chave em formato inválido!\n\nA chave deve conter apenas caracteres do alfabeto \ne sem acentos gráficos.")
            self.texto_saida["state"] = "disabled"


def iniciar():
    janela_raiz = tk.Tk()
    aplicacao   = AppCifrador(master=janela_raiz)
    
    janela_raiz.minsize(480, 640)
    janela_raiz.maxsize(480, 640)
    janela_raiz.title("Cifrador Vigenère")
    aplicacao.mainloop()

if __name__ == "__main__":
    iniciar()
