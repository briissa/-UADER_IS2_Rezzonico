"""
Patrón Estructural: DECORATOR
Número al que se le agregan operaciones en forma anidada.
"""

class Numero:
    def __init__(self, valor):
        self.valor = valor
    def resultado(self):
        return self.valor
    def mostrar(self):
        print(self.resultado())

class Sumar2:
    def __init__(self, componente):
        self._c = componente
    def resultado(self):
        return self._c.resultado() + 2
    def mostrar(self):
        print(self.resultado())

class MultiplicarPor2:
    def __init__(self, componente):
        self._c = componente
    def resultado(self):
        return self._c.resultado() * 2
    def mostrar(self):
        print(self.resultado())

class DividirPor3:
    def __init__(self, componente):
        self._c = componente
    def resultado(self):
        return self._c.resultado() / 3
    def mostrar(self):
        print(self.resultado())


# ── demo 
n = Numero(6)

print("Sin decoradores:")
n.mostrar()                                          # 6

print("\nSolo +2:")
Sumar2(n).mostrar()                                  # 8

print("\n+2, luego ×2:")
MultiplicarPor2(Sumar2(n)).mostrar()                 # 16

print("\n+2, luego ×2, luego ÷3:")
DividirPor3(MultiplicarPor2(Sumar2(n))).mostrar()    # 5.333...