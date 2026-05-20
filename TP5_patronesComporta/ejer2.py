class CadenaIterator:
    def __init__(self, cadena, reverso=False):
        self.cadena = cadena
        self.reverso = reverso
        self.indice = len(cadena) - 1 if reverso else 0
 
    def __iter__(self):
        return self
 
    def __next__(self):
        if self.reverso:
            if self.indice < 0:
                raise StopIteration
            char = self.cadena[self.indice]
            self.indice -= 1
        else:
            if self.indice >= len(self.cadena):
                raise StopIteration
            char = self.cadena[self.indice]
            self.indice += 1
        return char
 
 
class Cadena:
    def __init__(self, texto):
        self.texto = texto
 
    def __iter__(self):
        return CadenaIterator(self.texto)
 
    def reverso(self):
        return CadenaIterator(self.texto, reverso=True)
 
 
# Prueba
cadena = Cadena("Hola Mundo")
 
print("Directo:")
for char in cadena:
    print(char, end=" ")
 
print("\n\nReverso:")
for char in cadena.reverso():
    print(char, end=" ")


""""
estructura es:

CadenaIterator — implementa __iter__ y __next__. Según el flag reverso, arranca desde el principio o el final y avanza/retrocede.
Cadena — almacena el texto. __iter__ devuelve el iterador directo y reverso() devuelve el inverso.
## 
"""