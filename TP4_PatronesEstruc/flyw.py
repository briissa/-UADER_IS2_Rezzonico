"""
Patrón Estructural: FLYWEIGHT
Mapa urbano con miles de árboles.

Problema: si cada árbol almacena su especie, color y textura,
con 10 000 árboles la memoria explota.

Solución Flyweight: el estado INTRÍNSECO (especie, color, textura)
se comparte en un único objeto por tipo de árbol.
El estado EXTRÍNSECO (x, y) lo guarda el contexto, no el flyweight.
"""

class TipoArbol:
    """Flyweight: estado intrínseco compartido."""
    def __init__(self, especie, color, textura):
        self.especie  = especie
        self.color    = color
        self.textura  = textura

    def dibujar(self, x, y):
        print(f"  [{self.especie}] color={self.color} "
              f"textura={self.textura}  en ({x}, {y})")


class FabricaTipoArbol:
    """Fábrica / caché de flyweights."""
    _tipos = {}

    @classmethod
    def obtener(cls, especie, color, textura):
        clave = (especie, color, textura)
        if clave not in cls._tipos:
            cls._tipos[clave] = TipoArbol(especie, color, textura)
            print(f"  [Fábrica] nuevo tipo creado: {especie}")
        return cls._tipos[clave]

    @classmethod
    def total_tipos(cls):
        return len(cls._tipos)


class Arbol:
    """Contexto: guarda posición + referencia al flyweight."""
    def __init__(self, x, y, especie, color, textura):
        self.x = x
        self.y = y
        self.tipo = FabricaTipoArbol.obtener(especie, color, textura)

    def dibujar(self):
        self.tipo.dibujar(self.x, self.y)


# ── demo ────────────────────────────────────────────

import random

TIPOS = [
    ("Roble",   "verde oscuro", "rugosa"),
    ("Pino",    "verde claro",  "lisa"),
    ("Gomero",  "verde oliva",  "gruesa"),
]

print("=== Plantando 12 árboles (3 tipos) ===\n")
random.seed(0)
bosque = [
    Arbol(random.randint(0,100), random.randint(0,100), *random.choice(TIPOS))
    for _ in range(12)
]

print("\n=== Mapa ===")
for a in bosque:
    a.dibujar()

print(f"\nÁrboles en el mapa : {len(bosque)}")
print(f"Objetos TipoArbol  : {FabricaTipoArbol.total_tipos()}  "
      f"← solo estos viven en memoria")