from tokenizador import (Token, ErrorDeSintaxis, LITERAL, GRUPO_INI,
                         GRUPO_FIN, OPERADOR, UNARIO, CONCATENACION, EPSILON)


def _extraer_operando(salida):
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