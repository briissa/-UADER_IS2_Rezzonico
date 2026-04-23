import copy

# PROTOTIPO
class Prototipo:
    def clonar(self):
        return copy.deepcopy(self)


# CLASE CONCRETA
class Documento(Prototipo):
    def __init__(self, titulo, contenido):
        self.titulo = titulo
        self.contenido = contenido

    def mostrar(self):
        print(f"Título: {self.titulo}")
        print(f"Contenido: {self.contenido}")


# PRUEBA
if __name__ == "__main__":
    # objeto original
    doc1 = Documento("Original", "Este es el documento original")

    # primera copia
    doc2 = doc1.clonar()

    # copia de la copia
    doc3 = doc2.clonar()

    # Modificamos para comprobar independencia
    doc2.titulo = "Copia 1"
    doc3.titulo = "Copia 2"

    print("---- ORIGINAL ----")
    doc1.mostrar()

    print("\n---- COPIA 1 ----")
    doc2.mostrar()

    print("\n---- COPIA 2 ----")
    doc3.mostrar()