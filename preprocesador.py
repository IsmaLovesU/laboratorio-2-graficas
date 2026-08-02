"""
Preprocesamiento de la lista de tokens antes de aplicar Shunting Yard.

Se hacen dos cosas:

1. Expandir las extensiones '+' y '?' a operadores basicos:
       X+  ->  (X X*)
       X?  ->  (X | e)
   De esta manera al final solo queda '*' como operador unario, que es lo
   que necesita la construccion de Thompson.

2. Insertar el operador de concatenacion de forma explicita, porque en la
   notacion infix de las expresiones regulares la concatenacion es
   implicita y Shunting Yard necesita verla como un operador mas.
"""

from tokenizador import (Token, ErrorDeSintaxis, LITERAL, GRUPO_INI,
                         GRUPO_FIN, OPERADOR, UNARIO, CONCATENACION, EPSILON)


def _extraer_operando(salida):
    """
    Saca de la lista 'salida' el ultimo operando completo y lo devuelve.

    El operando puede ser:
      - un literal suelto:            a
      - un literal con un '*':        a*
      - un grupo entre parentesis:    (a|b)   o   (a|b)*
    """
    if len(salida) == 0:
        raise ErrorDeSintaxis("Un operador unario aparecio sin operando")

    fin = len(salida)
    indice = fin - 1

    # Si el ultimo token es un '*', el operando esta justo antes.
    if salida[indice].tipo == UNARIO:
        indice -= 1

    if indice < 0:
        raise ErrorDeSintaxis("Un operador unario aparecio sin operando")

    # Si termina en ')', hay que retroceder hasta su '(' correspondiente.
    if salida[indice].tipo == GRUPO_FIN:
        profundidad = 0
        while indice >= 0:
            if salida[indice].tipo == GRUPO_FIN:
                profundidad += 1
            elif salida[indice].tipo == GRUPO_INI:
                profundidad -= 1
                if profundidad == 0:
                    break
            indice -= 1
        if profundidad != 0:
            raise ErrorDeSintaxis("Parentesis sin cerrar en la expresion")

    operando = salida[indice:fin]
    del salida[indice:fin]
    return operando


def expandir_extensiones(tokens):
    """Reemplaza los operadores '+' y '?' por su equivalente con '*' y '|'."""
    salida = []

    for token in tokens:
        if token.tipo == UNARIO and token.valor in "+?":
            operando = _extraer_operando(salida)

            salida.append(Token(GRUPO_INI, '('))
            if token.valor == '+':
                # X+ equivale a X seguido de X*
                salida.extend(operando)
                salida.extend(operando)
                salida.append(Token(UNARIO, '*'))
            else:
                # X? equivale a X o la cadena vacia
                salida.extend(operando)
                salida.append(Token(OPERADOR, '|'))
                salida.append(Token(LITERAL, EPSILON))
            salida.append(Token(GRUPO_FIN, ')'))
        else:
            salida.append(token)

    return salida


def insertar_concatenacion(tokens):
    """
    Agrega el operador de concatenacion entre dos tokens cuando corresponde.

    Se concatena si el token de la izquierda puede terminar una expresion
    (un literal, un ')' o un '*') y el de la derecha puede empezar una
    (un literal o un '(').
    """
    puede_terminar = (LITERAL, GRUPO_FIN, UNARIO)
    puede_empezar = (LITERAL, GRUPO_INI)

    resultado = []
    for posicion, token in enumerate(tokens):
        if posicion > 0:
            anterior = tokens[posicion - 1]
            if anterior.tipo in puede_terminar and token.tipo in puede_empezar:
                resultado.append(Token(OPERADOR, CONCATENACION))
        resultado.append(token)

    return resultado