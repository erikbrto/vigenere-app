import re
from itertools import cycle
from string import ascii_uppercase

def cifrar(mensagem: str, chave:str):
    """ Cifração com a cifra de Vigenere a uma mensagem utilizando à chave determinada.

        Params:
            mensagem: string
            chave: string

        Returns:
            string: mensagem após cifração.
    """

    return _aplicar_cifra(mensagem, chave)


def decifrar(mensagem: str, chave: str):
    """ Decifração com a cifra de Vigenere a uma mensagem utilizando à chave determinada.

        Params:
            mensagem: string
            chave: string

        Returns:
            string: mensagem após decifração.
    """

    return _aplicar_cifra(mensagem, chave, decifracao=True)


def mapear_sequencias(mensagem: str):
    """ Identificação das sequências de 3 caracteres repetidas em uma mensagem cifrada, o espaçamento e possíveis tamanhos de chave.

        Params:
            mensagem: string

        Returns:
            dict: {
                "sequencia": string
                "espacamento": int 
                "tam_possiveis": lista de booleanos indicando os possiveis tamanhos da chave de 2 a 20, conforme o índice.
            }
    """

    mensagem = re.sub(r"[^A-Z]", "", mensagem.upper())
    sequencias = re.findall(r"[A-Z]{3}", mensagem)
    resultado = []

    for sequencia in sequencias:
        if len(re.findall(sequencia, mensagem)) < 2:
            continue

        posicoes = [m.start() for m in re.finditer(sequencia, mensagem)]
        espacamentos = [posicoes[i] - posicoes[i - 1] for i in range(1, len(posicoes))]
            
        for espacamento in espacamentos:
            resultado.append({
                "sequencia": sequencia, 
                "espacamento": espacamento, 
                "tam_possiveis": [bool(espacamento % i == 0) for i in range(2, 21)]
            })

    return resultado


def calcular_freq_letras(mensagem: str, posicao_letra: int, tamanho_chave: int):
    """ Identificação das sequências de 3 caracteres repetidas em uma mensagem cifrada, o espaçamento e possíveis tamanhos de chave.

        Params:
            mensagem: string
            posicao_letra: int -- de 0 até (tamanho_chave - 1)
            tamanho_chave: int

        Returns:
            list: tupla(Letra, Quantidade de Ocorrências da Letra, Frequência Relativa para Aquela Posição)
    """

    mensagem = re.sub(r"[^A-Z]", "", mensagem.upper())
    sub_strings = re.findall(r"[A-Z]{%s,%s}" % (posicao_letra + 1, tamanho_chave), mensagem)
    total_letras = len(sub_strings)
    resultado = []

    for letra in ascii_uppercase:
        qtd_letra = len([s for s in sub_strings if s[posicao_letra] == letra])
        frequencia = (float(qtd_letra) / float(total_letras)) * 100.0

        resultado.append((letra, qtd_letra, frequencia))     

    return resultado


def _reordenar_alfabeto(letra_inicial: str):
    """ Reordena o alfabeto de forma circular conforme a letra inicial selecionada.

        Params:
            letra_inicial: string
        
        Returns:
            string: todas a letras ASCII iniciando pela letra selecionada, com as subsequentes ao 'A' logo após o 'Z'.
    """
    
    return "%s%s%s" % tuple([letra_inicial] + ascii_uppercase.split(letra_inicial)[::-1])


def _gerar_matriz_vigenere(decifracao: bool = False):
    """ Criação de uma matriz de aplicação da cifra de Vigenere'.

        Params:
            decifração: (opcional) boleano de definição se a matriz é utilizada para decifração. (padrão = False)

        Returns:
            dict: correspondente a matriz. Acesso ao caractere de resultado por 'matriz[coluna][linha] = caractere'.
                  Em caso de decifração coluna e caractere de resultado são invertidos: 'matriz[caractere][linha] = coluna'.
    """
    
    matriz = {letra: {} for letra in ascii_uppercase}
    
    for i in range(len(ascii_uppercase)):
        for j in range(len(ascii_uppercase)): 
            coluna = ascii_uppercase[i]
            linha  = ascii_uppercase[j]
            valor  = _reordenar_alfabeto(linha)[i]
            
            if decifracao:
                matriz[valor][linha] = coluna
            else:
                matriz[coluna][linha] = valor

    return matriz


def _aplicar_cifra(mensagem: str, chave: str, decifracao: bool = False):
    """ Aplicação da cifra de Vigenere a uma mensagem utilizando à chave determinada.

        Params:
            mensagem: string
            chave: string
            decifração: (opcional) boleano de definição se é utilizada para decifração. (padrão = False)

        Returns:
            string: mensagem após cifração/decifração, conforme o caso.
    """
    
    matriz    = _gerar_matriz_vigenere(decifracao)
    chave     = cycle(chave.upper())
    resultado = ""
    
    for caractere in mensagem:
        i = caractere.upper()

        if i in ascii_uppercase:
            j = chave.__next__()
            
            # Operador ternário para verificar se o caractere original está em caixa alta e alterar para minuscula se for o caso
            resultado += matriz[i][j] if (i == caractere) else matriz[i][j].lower()
        else:
            resultado += i

    return resultado
