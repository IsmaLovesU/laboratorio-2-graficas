from pila import Pila

from tokenizador import (ErrorDeSintaxis, LITERAL, GRUPO_INI, GRUPO_FIN,
                         OPERADOR, UNARIO, CONCATENACION)

PRECEDENCIA = {'|': 1, CONCATENACION: 2}


class PasoSY:
    """Guarda el estado del algoritmo despues de leer un token."""

    def __init__(self, numero, token, accion, pila, salida):
        self.numero = numero
        self.token = token
        self.accion = accion
        self.pila = pila
        self.salida = salida


def _texto(lista):
    if len(lista) == 0:
        return "(vacia)"
    return " ".join(str(t) for t in lista)


def a_postfix(tokens):
    """
    Convierte la lista de tokens en infix a notacion postfix.

    Devuelve una tupla (lista_postfix, lista_de_pasos).
    """
    salida = []
    pila = Pila()
    pasos = []
    numero = 0

    for token in tokens:
        numero += 1

        if token.tipo == LITERAL:
            salida.append(token)
            accion = "operando, va directo a la salida"

        elif token.tipo == UNARIO:
            # Solo llega '*' porque '+' y '?' ya fueron expandidos.
            salida.append(token)
            accion = "operador postfijo, va directo a la salida"

        elif token.tipo == OPERADOR:
            desapilados = 0
            while (not pila.esta_vacia()
                   and pila.tope().tipo == OPERADOR
                   and PRECEDENCIA[pila.tope().valor] >= PRECEDENCIA[token.valor]):
                salida.append(pila.desapilar())
                desapilados += 1
            pila.apilar(token)
            if desapilados == 0:
                accion = "operador, se apila"
            else:
                accion = "se sacan %d operador(es) de precedencia mayor o igual" % desapilados

        elif token.tipo == GRUPO_INI:
            pila.apilar(token)
            accion = "abre grupo, se apila"

        elif token.tipo == GRUPO_FIN:
            while not pila.esta_vacia() and pila.tope().tipo != GRUPO_INI:
                salida.append(pila.desapilar())
            if pila.esta_vacia():
                raise ErrorDeSintaxis("Se encontro un ')' sin su '(' correspondiente")
            pila.desapilar()  # se descarta el '('
            accion = "cierra grupo, se vacia hasta el '(' y se descarta"

        else:
            raise ErrorDeSintaxis("Token desconocido: %s" % token)

        pasos.append(PasoSY(numero, str(token), accion, str(pila), _texto(salida)))

    # Al terminar se vacia lo que quedo en la pila.
    while not pila.esta_vacia():
        numero += 1
        tope = pila.desapilar()
        if tope.tipo == GRUPO_INI:
            raise ErrorDeSintaxis("Quedo un '(' sin cerrar")
        salida.append(tope)
        pasos.append(PasoSY(numero, "(fin)", "se vacia la pila", str(pila), _texto(salida)))

    return salida, pasos