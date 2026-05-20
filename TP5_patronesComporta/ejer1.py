class Manejador:
    def __init__(self):
        self.siguiente = None
 
    def set_siguiente(self, siguiente):
        self.siguiente = siguiente
 
    def manejar(self, numero):
        if self.siguiente:
            self.siguiente.manejar(numero)
        else:
            print(f"{numero}: no consumido")
 
 
class ManejadorPrimos(Manejador):
    def es_primo(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
 
    def manejar(self, numero):
        if self.es_primo(numero):
            print(f"{numero}: consumido por ManejadorPrimos")
        else:
            super().manejar(numero)
 
 
class ManejadorPares(Manejador):
    def manejar(self, numero):
        if numero % 2 == 0:
            print(f"{numero}: consumido por ManejadorPares")
        else:
            super().manejar(numero)
 
 
# Armar la cadena
primos = ManejadorPrimos()
pares = ManejadorPares()
primos.set_siguiente(pares)
 
# Pasar los números del 1 al 100
for n in range(1, 101):
    primos.manejar(n)