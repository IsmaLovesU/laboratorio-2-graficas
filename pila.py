"""
Implementacion manual de una pila (LIFO).

Se hace a mano y no con los metodos de lista de Python directamente
porque el enunciado pide explicitamente el uso de una estructura de pila.
"""


class PilaVaciaError(Exception):
    """Se lanza al intentar sacar o mirar el tope de una pila vacia."""
    pass


class Pila:

    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        """Coloca un elemento en el tope de la pila."""
        self.elementos.append(elemento)

    def desapilar(self):
        """Saca y devuelve el elemento del tope."""
        if self.esta_vacia():
            raise PilaVaciaError("Se intento desapilar de una pila vacia")
        return self.elementos.pop()

    def tope(self):
        """Devuelve el elemento del tope sin sacarlo."""
        if self.esta_vacia():
            raise PilaVaciaError("Se intento ver el tope de una pila vacia")
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def __len__(self):
        return len(self.elementos)

    def __str__(self):
        """Muestra la pila de base a tope, por ejemplo: [ ( [   <- tope."""
        if self.esta_vacia():
            return "(vacia)"
        return " ".join(str(e) for e in self.elementos)