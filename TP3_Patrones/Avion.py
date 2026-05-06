#  PRODUCTO
class Avion:
    def __init__(self):
        self.body = None
        self.turbinas = 0
        self.alas = 0
        self.tren_aterrizaje = False

    def mostrar(self):
        print("Avión construido con:")
        print(f"Body: {self.body}")
        print(f"Turbinas: {self.turbinas}")
        print(f"Alas: {self.alas}")
        print(f"Tren de aterrizaje: {self.tren_aterrizaje}")


#define los pasos por que los que se construye el avión, cada paso es un método que se implementa en el builder concreto
class AvionBuilder:
    def __init__(self):
        self.avion = Avion()

    def construir_body(self):
        pass

    def construir_turbinas(self):
        pass

    def construir_alas(self):
        pass

    def construir_tren_aterrizaje(self):
        pass

    def obtener_avion(self):
        return self.avion


# construye el avión
class AvionComercialBuilder(AvionBuilder):

    def construir_body(self):
        self.avion.body = "Body de avión comercial"

    def construir_turbinas(self):
        self.avion.turbinas = 2

    def construir_alas(self):
        self.avion.alas = 2

    def construir_tren_aterrizaje(self):
        self.avion.tren_aterrizaje = True


# indica el orden de construcción
class Director:

    def construir_avion(self, builder):
        builder.construir_body()
        builder.construir_turbinas()
        builder.construir_alas()
        builder.construir_tren_aterrizaje()


#  es la prueba para ver si el patrón funciona, se construye un avión comercial y se muestra su configuración
if __name__ == "__main__":
    builder = AvionComercialBuilder()
    director = Director()

    director.construir_avion(builder)
    avion = builder.obtener_avion()

    avion.mostrar()