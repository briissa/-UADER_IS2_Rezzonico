class Factorial:
    _instancia = None  # variable de clase (privada)

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Factorial, cls).__new__(cls)
        return cls._instancia

    def calcular(self, n):
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos")

        resultado = 1
        for i in range(1, n + 1):
            resultado *= i
        return resultado
    


# Esta parte del codgo es para probar la clase factorial y ver si funciona el Singleton 

f1 = Factorial()
f2 = Factorial()

print(f1.calcular(5))  # nos deberia dar 120
print(f2.calcular(3))  # nos deberia dar 6

# Verificamos que es el mismo objeto (single)
print(f1 is f2)  # True