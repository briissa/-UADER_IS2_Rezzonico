class Publicador:
    def __init__(self):
        self.suscriptores = []

    def suscribir(self, observer):
        self.suscriptores.append(observer)

    def emitir(self, id_emitido):
        print(f"\nID emitido: {id_emitido}")
        for obs in self.suscriptores:
            obs.actualizar(id_emitido)


class Observer:
    def __init__(self, nombre, id_propio):
        self.nombre = nombre
        self.id_propio = id_propio

    def actualizar(self, id_emitido):
        if id_emitido == self.id_propio:
            print(f"  {self.nombre} (ID: {self.id_propio}): ¡ID coincide!")


# Crear publicador
pub = Publicador()

# Crear y suscribir 4 observers con ID propio
pub.suscribir(Observer("Clase A", "AB12"))
pub.suscribir(Observer("Clase B", "CD34"))
pub.suscribir(Observer("Clase C", "EF56"))
pub.suscribir(Observer("Clase D", "GH78"))

# Emitir 8 IDs (4 coinciden, 4 no)
ids = ["AB12", "XX99", "CD34", "ZZ00", "EF56", "QQ11", "GH78", "WW22"]
for id_ in ids:
    pub.emitir(id_)




"""

Publicador — mantiene la lista de suscriptores y emite IDs llamando a actualizar() en cada uno.
Observer — tiene un nombre y su propio ID. Solo reacciona cuando el ID emitido coincide con el suyo.

Se emiten 8 IDs: AB12, CD34, EF56, GH78 coinciden; XX99, ZZ00, QQ11, WW22 no coinciden con nadie
"""