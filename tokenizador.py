"""
Tokenizador de expresiones regulares.

Convierte la cadena de entrada en una lista de tokens. Esto es necesario
porque el algoritmo de Shunting Yard trabaja con simbolos completos y no
con caracteres sueltos: '\\(' es un parentesis literal (un solo token) y
'[ae03]' es una clase de caracteres (tambien un solo token).
"""

# Tipos de token que maneja el programa.
LITERAL = "literal"        # a, [ae03], \(, \n, ., @
GRUPO_INI = "grupo_ini"    # (
GRUPO_FIN = "grupo_fin"    # )
OPERADOR = "operador"      # | y el punto de concatenacion
UNARIO = "unario"          # * + ?

OPERADORES_UNARIOS = "*+?"
CONCATENACION = "·"        # operador de concatenacion explicito. Se usa '·'
                           # y no '.' porque el punto aparece como literal
                           # dentro de varias de las expresiones del enunciado.
EPSILON = "ε"              # cadena vacia, necesaria para expandir el '?'


class ErrorDeSintaxis(Exception):
    """Se lanza cuando la expresion esta mal formada."""
    pass


class Token:

    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return self.valor

    def __repr__(self):
        return self.valor


def tokenizar(expresion):
    """Recibe la expresion como texto y devuelve la lista de tokens."""
    tokens = []
    i = 0
    n = len(expresion)

    while i < n:
        caracter = expresion[i]

        # Los espacios en blanco no forman parte de la expresion.
        if caracter.isspace():
            i += 1

        # Verificador de caracteres escapados: '\' mas el siguiente caracter
        # forman un unico literal, sin importar si es un metacaracter.
        elif caracter == '\\':
            if i + 1 >= n:
                raise ErrorDeSintaxis("La expresion termina con un '\\' suelto")
            tokens.append(Token(LITERAL, expresion[i:i + 2]))
            i += 2

        # Clase de caracteres: se toma completa como un solo literal.
        elif caracter == '[':
            j = i + 1
            contenido = ""
            while j < n and expresion[j] != ']':
                if expresion[j] == '\\' and j + 1 < n:
                    contenido += expresion[j:j + 2]
                    j += 2
                else:
                    contenido += expresion[j]
                    j += 1
            if j >= n:
                raise ErrorDeSintaxis("Falta cerrar la clase de caracteres '['")
            tokens.append(Token(LITERAL, '[' + contenido + ']'))
            i = j + 1

        elif caracter == '(':
            tokens.append(Token(GRUPO_INI, '('))
            i += 1

        elif caracter == ')':
            tokens.append(Token(GRUPO_FIN, ')'))
            i += 1

        elif caracter == '|':
            tokens.append(Token(OPERADOR, '|'))
            i += 1

        elif caracter in OPERADORES_UNARIOS:
            tokens.append(Token(UNARIO, caracter))
            i += 1

        # Cualquier otro caracter (letras, digitos, '.', '@', '{', '}', etc.)
        # se trata como un simbolo literal del alfabeto.
        else:
            tokens.append(Token(LITERAL, caracter))
            i += 1

    return tokens