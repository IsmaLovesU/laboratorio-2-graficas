from pila import Pila

# Pares de simbolos que nos interesa rastrear.
PARES = {')': '(', ']': '[', '}': '{'}
APERTURAS = set(PARES.values())
CIERRES = set(PARES.keys())


class Paso:
    """Guarda la informacion de un paso individual para poder imprimir la traza."""

    def __init__(self, numero, caracter, posicion, accion, pila):
        self.numero = numero
        self.caracter = caracter
        self.posicion = posicion
        self.accion = accion
        self.pila = pila


class Resultado:
    """Resultado del analisis de una linea."""

    def __init__(self, expresion):
        self.expresion = expresion
        self.balanceada = False
        self.mensaje = ""
        self.pasos = []


def balancear(expresion):
    """
    Analiza una expresion y devuelve un objeto Resultado con el veredicto
    y la secuencia de pasos que siguio la pila.
    """
    resultado = Resultado(expresion)
    pila = Pila()
    numero_paso = 0
    i = 0

    while i < len(expresion):
        caracter = expresion[i]
        numero_paso += 1

        # Un caracter escapado con '\' se toma como literal, junto con
        # el caracter que le sigue. Asi '\(' no cuenta como parentesis.
        if caracter == '\\' and i + 1 < len(expresion):
            accion = "escapado, se ignora '%s'" % expresion[i:i + 2]
            resultado.pasos.append(Paso(numero_paso, expresion[i:i + 2], i, accion, str(pila)))
            i += 2
            continue

        if caracter in APERTURAS:
            pila.apilar(caracter)
            accion = "APILAR '%s'" % caracter

        elif caracter in CIERRES:
            esperado = PARES[caracter]
            if pila.esta_vacia():
                accion = "ERROR: cierre '%s' sin apertura" % caracter
                resultado.pasos.append(Paso(numero_paso, caracter, i, accion, str(pila)))
                resultado.balanceada = False
                resultado.mensaje = ("No balanceada: se encontro '%s' en la posicion %d "
                                     "sin una apertura previa." % (caracter, i))
                return resultado

            if pila.tope() != esperado:
                encontrado = pila.tope()
                accion = "ERROR: se esperaba cerrar '%s'" % encontrado
                resultado.pasos.append(Paso(numero_paso, caracter, i, accion, str(pila)))
                resultado.balanceada = False
                resultado.mensaje = ("No balanceada: '%s' en la posicion %d no corresponde "
                                     "con '%s' que estaba en el tope." % (caracter, i, encontrado))
                return resultado

            pila.desapilar()
            accion = "DESAPILAR '%s'" % esperado

        else:
            accion = "no es simbolo de interes"

        resultado.pasos.append(Paso(numero_paso, caracter, i, accion, str(pila)))
        i += 1

    # Si sobraron aperturas, la expresion no esta balanceada.
    if not pila.esta_vacia():
        pendiente = pila.tope()
        resultado.balanceada = False
        resultado.mensaje = ("No balanceada: quedaron %d aperturas sin cerrar "
                             "(la ultima fue '%s')." % (len(pila), pendiente))
        return resultado

    resultado.balanceada = True
    resultado.mensaje = "Balanceada correctamente."
    return resultado