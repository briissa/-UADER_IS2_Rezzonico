class Factura:
    def __init__(self, importe):
        self.importe = importe

    def mostrar(self):
        pass


class FacturaResponsable(Factura):
    def mostrar(self):
        print(f"Factura IVA Responsable - Total: ${self.importe}")


class FacturaNoInscripto(Factura):
    def mostrar(self):
        print(f"Factura IVA No Inscripto - Total: ${self.importe}")


class FacturaExento(Factura):
    def mostrar(self):
        print(f"Factura IVA Exento - Total: ${self.importe}")


# factory para crear facturas
class FacturaFactory:

    @staticmethod
    def crear_factura(tipo, importe):
        if tipo == "responsable":
            return FacturaResponsable(importe)
        elif tipo == "no_inscripto":
            return FacturaNoInscripto(importe)
        elif tipo == "exento":
            return FacturaExento(importe)
        else:
            raise ValueError("Tipo de factura no válido")


# hacemos la prueba 
if __name__ == "__main__":
    f1 = FacturaFactory.crear_factura("responsable", 1000)
    f2 = FacturaFactory.crear_factura("exento", 2000)

    f1.mostrar()
    f2.mostrar()