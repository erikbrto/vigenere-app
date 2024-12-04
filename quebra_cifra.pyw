import __main__
import json
import os
import re
import tkinter as tk
from functools import partial
from string import ascii_uppercase
from tkinter import ttk

from src.vigenere import calcular_freq_letras
from src.vigenere import mapear_sequencias


class BotaoChave(tk.Button):
    def __init__(self, posicao: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.posicao = posicao
        self.letras = [letra for letra in ascii_uppercase]
        self.indice = 0


    def criar(self):
        self["bg"] = "white"
        self["fg"] = "black"
        self["text"] = self.letras[self.indice]
        self["font"] = "sans 16 bold"
        self.place(x=(545 + (self.posicao * 35)), y=340, width=30, height=30)

 
    def atualizar(self):
        self["bg"] = "blue"
        self["fg"] = "white"
        self["text"] = self.letras[self.indice]
        self["font"] = "sans 16 bold"
        self.place(x=(545 + (self.posicao * 35)), y=340, width=30, height=30)

    
    def selecionar_letra_seguinte(self):
        self.indice = (self.indice + 1) if (self.indice < (len(self.letras) - 1)) else 0
        self.atualizar()

    
    def selecionar_letra_anterior(self):
        self.indice = (self.indice - 1) if (self.indice > 0) else (len(self.letras) - 1)
        self.atualizar()


class AppQuebraCifra(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_freq = os.path.join(os.path.dirname(os.path.abspath(__main__.__file__)), "cfg\\frequencias.json")
        self.config_freq = json.load(open(json_freq))
        self.botoes_chave = []
        self.indice_chave = 0
        self.place(x=0, y=0, width=1280, height=720)
        self.criar_widgets()


    def criar_widgets(self):
        """Inicialização dos widgets da aplicação."""

        # Campo de entrada do texto a ser cifrado/decifrado
        self.texto_entrada = tk.Text(self, bg="white")
        self.texto_entrada.place(x=10, y=10, width=445, height=300)

        # Barras de rolagem do texto de entrada
        self.scroll_entrada_x = tk.Scrollbar(self, orient="horizontal", command=self.texto_entrada.xview)
        self.scroll_entrada_y = tk.Scrollbar(self, orient="vertical", command=self.texto_entrada.yview)
        self.scroll_entrada_x.place(x=10, y=310, width=445, height=15)
        self.scroll_entrada_y.place(x=455, y=10, width=15, height=315)
        self.texto_entrada["xscrollcommand"] = self.scroll_entrada_x.set
        self.texto_entrada["yscrollcommand"] = self.scroll_entrada_y.set

        # Botão de calcular sequências
        self.botao_tam_chave = tk.Button(self, text="Calcular Possível Tamanho da Chave", command=self.identificar_sequencias)
        self.botao_tam_chave.place(x=10, y=335, width=445, height=30)

        # Seletor de idioma para frequências
        self.idioma_selecionado = tk.StringVar()
        self.seletor_idioma = ttk.Combobox(self, values=tuple(self.config_freq.keys()), textvariable=self.idioma_selecionado, state="readonly")
        self.seletor_idioma.bind("<<ComboboxSelected>>", func=self.atualizar_graf_freq_idiomas)
        self.seletor_idioma.place(x=1160, y=5, width=100, height=25)

        # Gráfico de frequências de letras do alfabeto
        self.graf_freq_alfabeto = tk.Canvas(self, bg="white")
        self.graf_freq_alfabeto.place(x=480, y=35, width=790, height=300)

        # Seletor de número da chave
        self.tamanho_chave = tk.StringVar()
        self.seletor_tam_chave = ttk.Combobox(self, values=tuple(range(2, 21)), textvariable=self.tamanho_chave, state="readonly")
        self.seletor_tam_chave.bind("<<ComboboxSelected>>", func=self.atualizar_botoes_quebra_chave)
        self.seletor_tam_chave.place(x=500, y=340, width=40, height=30)

        # Gráfico de frequências de letras na mensagem
        self.graf_freq_mensagem = tk.Canvas(self, bg="white")
        self.graf_freq_mensagem.place(x=480, y=375, width=790, height=300) 

        # Botões de rotação do gráfico de frenquências da mensagem
        self.botao_rotacao_esq = tk.Button(self, text="<<<", command=self.rotacionar_graf_freq_mensagem_esq)
        self.botao_rotacao_esq.place(x=500, y=680, width=120, height=30)
        
        self.botao_rotacao_dir = tk.Button(self, text=">>>", command=self.rotacionar_graf_freq_mensagem_dir)
        self.botao_rotacao_dir.place(x=1140, y=680, width=120, height=30)


    def identificar_sequencias(self):
        """Preenche a tabela com o possível tamanho da chave com base na análise de sequências repetidas da mensagem."""

        sequencias = mapear_sequencias(self.texto_entrada.get("1.0", "end"))
        
        # Tabela de sequências
        self.tabela_frequencia = ttk.Treeview(self, 
            columns=("sequencias", "espacamento") + tuple(range(2,21)), 
            show="headings", 
            height=5
        )
        self.tabela_frequencia.place(x=10, y=370, width=445, height=320)
        
        # Barras de rolagem da tabela de sequências
        self.scroll_tabela_x = tk.Scrollbar(self, orient="horizontal", command=self.tabela_frequencia.xview)
        self.scroll_tabela_y = tk.Scrollbar(self, orient="vertical", command=self.tabela_frequencia.yview)
        self.scroll_tabela_x.place(x=10, y=690, width=445, height=15)
        self.scroll_tabela_y.place(x=455, y=370, width=15, height=335)
        self.tabela_frequencia["xscrollcommand"] = self.scroll_tabela_x.set
        self.tabela_frequencia["yscrollcommand"] = self.scroll_tabela_y.set

        # Criação da colunas da tabela de sequências
        self.tabela_frequencia.column("# 1", width=5, anchor="center")
        self.tabela_frequencia.heading("# 1", text="Sequências")
        self.tabela_frequencia.column("# 2", width=5, anchor="center")
        self.tabela_frequencia.heading("# 2", text="Espaçamento")

        for i in range(2, 21):
            self.tabela_frequencia.column("# %s" % (i + 1), width=1, anchor="center")
            self.tabela_frequencia.heading("# %s" % (i + 1), text=str(i))
        
        # Alimentação dos dados da tabela
        for i in range(len(sequencias)):
            self.tabela_frequencia.insert(
                "", i, 
                values=(sequencias[i]["sequencia"], sequencias[i]["espacamento"]) + tuple(["X" if i else "" for i in sequencias[i]["tam_possiveis"]])
            )


    def atualizar_graf_freq_idiomas(self, evento):
        """Preenche o gráfico de frequências das letras do alfabeto em um idioma, conforme selecionado pelo usuário."""

        dados_frequencia  = self.config_freq[self.seletor_idioma.get()]
        maior_frequencia  = max([dados_frequencia[d] for d in dados_frequencia])
        altura_barras     = 240
        largura_barras    = 20
        espaco_horizontal = 10
        espaco_vertical   = 20
        pos_y_texto_letra = 270
        i = 0

        self.graf_freq_alfabeto.delete("all")

        for letra in sorted(dados_frequencia.keys()):
            # Barras
            self.graf_freq_alfabeto.create_rectangle(
                espaco_horizontal + (i * (largura_barras + espaco_horizontal)), # x1
                espaco_vertical + (altura_barras - (altura_barras * (dados_frequencia[letra] / maior_frequencia))), # y1
                (largura_barras + espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x2
                altura_barras + espaco_vertical, # y2
                fill="blue"
            )

            # Frequências
            self.graf_freq_alfabeto.create_text(
                (2 * espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x1
                (altura_barras - (altura_barras * (dados_frequencia[letra] / maior_frequencia))) + 10, # y1
                text=round(dados_frequencia[letra], 2)
            )

            # Letras
            self.graf_freq_alfabeto.create_text(
                (2 * espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x1
                pos_y_texto_letra, # y1
                text=letra
            )

            i += 1


    def atualizar_graf_freq_mensagem(self):
        """Preenche o gráfico de frequência de ocorrência das letras na mensagem de acordo com o tamanho 
            de chave e posição selecionada.
        """

        if not re.search(r"\w+", self.texto_entrada.get("1.0", "end")):
            return

        dados_frequencia  = calcular_freq_letras(self.texto_entrada.get("1.0", "end"), self.indice_chave, self.seletor_tam_chave.get())
        letra_selecionada = self.botoes_chave[self.indice_chave].indice
        maior_frequencia  = max([d[2] for d in dados_frequencia])
        altura_barras     = 240
        largura_barras    = 20
        espaco_horizontal = 10
        espaco_vertical   = 20
        pos_y_texto_letra = 270
        pos_y_texto_total = 285

        self.graf_freq_mensagem.delete("all")

        # Reordenar a lista a partir da letra selecionada na letra em uso para análise das frequências
        dados_frequencia = dados_frequencia[letra_selecionada:] + dados_frequencia[:letra_selecionada]

        for i in range(len(dados_frequencia)):
            letra, qtd, freq = dados_frequencia[i]

            # Barras
            self.graf_freq_mensagem.create_rectangle(
                espaco_horizontal + (i * (largura_barras + espaco_horizontal)), # x1
                espaco_vertical + (altura_barras - (altura_barras * (freq / maior_frequencia))), # y1
                (largura_barras + espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x2
                altura_barras + espaco_vertical, # y2
                fill="blue"
            )

            # Frequências
            self.graf_freq_mensagem.create_text(
                (2 * espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x1
                (espaco_vertical - 10) + (altura_barras - (altura_barras * (freq / maior_frequencia))), # y1
                text=round(freq, 2)
            )

            # Letras
            self.graf_freq_mensagem.create_text(
                (2 * espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x1
                pos_y_texto_letra, # y1
                text=letra
            )

            # Quantidade total de cada letra
            self.graf_freq_mensagem.create_text(
                (2 * espaco_horizontal) + (i * (largura_barras + espaco_horizontal)), # x1
                pos_y_texto_total, # y1
                text=qtd
            )


    def atualizar_botoes_quebra_chave(self, evento):
        """Cria/atualiza os botões de seleção de posição e tamanho da chave."""

        for botao in self.botoes_chave:
            botao.destroy()

        del self.botoes_chave
        self.botoes_chave = []

        for i in range(int(self.tamanho_chave.get())):
            self.botoes_chave.append(BotaoChave(i, master=self, command=partial(self.atualizar_indice_botao_chave, i)))
            self.botoes_chave[i].criar()

        self.atualizar_graf_freq_mensagem()


    def atualizar_indice_botao_chave(self, indice):
        """Altera a posição selecionada de referência da chave."""

        self.indice_chave = indice
        
        for i in range(len(self.botoes_chave)):
            self.botoes_chave[i]["bg"] = "blue" if (i == indice) else "white"
            self.botoes_chave[i]["fg"] = "white" if (i == indice) else "black"
        
        self.atualizar_graf_freq_mensagem()


    def rotacionar_graf_freq_mensagem_esq(self):
        """Desloca o início do gráfico de frequência de ocorrência das letras na mensagem em uma posição para a esquerda."""

        if not self.botoes_chave:
            return
        self.botoes_chave[self.indice_chave].selecionar_letra_anterior()
        self.atualizar_graf_freq_mensagem()


    def rotacionar_graf_freq_mensagem_dir(self):
        """Desloca o início do gráfico de frequência de ocorrência das letras na mensagem em uma posição para a direita."""

        if not self.botoes_chave:
            return
        self.botoes_chave[self.indice_chave].selecionar_letra_seguinte()
        self.atualizar_graf_freq_mensagem()


def iniciar():
    janela_raiz = tk.Tk()
    aplicacao   = AppQuebraCifra(master=janela_raiz)
    
    janela_raiz.minsize(1280, 720)
    janela_raiz.maxsize(1280, 720)
    janela_raiz.title("Quebra Cifra Vigenère")
    aplicacao.mainloop()


if __name__ == "__main__":
    iniciar()
