"""
Problema 2 - Balanceo de expresiones infix usando una pila.

Uso:
    python main.py [archivo]

Si no se indica archivo, se usa 'expresiones.txt' por defecto.
"""

import sys

from balanceador import balancear

ARCHIVO_POR_DEFECTO = "expresiones.txt"


def leer_expresiones(ruta):
    """Devuelve una lista con las lineas no vacias del archivo."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def imprimir_traza(resultado):
    """Imprime la tabla de pasos que siguio la pila."""
    print("  %-5s %-8s %-6s %-32s %s" % ("PASO", "CARACTER", "POS", "ACCION", "PILA"))
    print("  " + "-" * 78)
    for paso in resultado.pasos:
        print("  %-5d %-8s %-6d %-32s %s" % (paso.numero, paso.caracter,
                                             paso.posicion, paso.accion, paso.pila))


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else ARCHIVO_POR_DEFECTO

    try:
        expresiones = leer_expresiones(ruta)
    except FileNotFoundError:
        print("No se encontro el archivo '%s'." % ruta)
        return

    print("=" * 82)
    print("PROBLEMA 2 - BALANCEO DE EXPRESIONES  (archivo: %s)" % ruta)
    print("=" * 82)

    for numero, expresion in enumerate(expresiones, start=1):
        print("\nLinea %d: %s" % (numero, expresion))
        print("-" * 82)

        resultado = balancear(expresion)
        imprimir_traza(resultado)

        estado = "BALANCEADA" if resultado.balanceada else "NO BALANCEADA"
        print("  Resultado: %s -> %s" % (estado, resultado.mensaje))

    print("\n" + "=" * 82)


if __name__ == "__main__":
    main()