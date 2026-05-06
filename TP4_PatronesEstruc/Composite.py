"""
Patrón Estructural: COMPOSITE
Ensamblado jerárquico de piezas y subconjuntos.
"""

class Componente:
    """Nodo base: pieza hoja o contenedor."""
    def __init__(self, nombre):
        self.nombre = nombre
        self._hijos = []

    def agregar(self, componente):
        self._hijos.append(componente)
        return self          # permite encadenamiento

    def mostrar(self, nivel=0):
        prefijo = "  " * nivel + ("+ " if self._hijos else "- ")
        print(f"{prefijo}{self.nombre}")
        for hijo in self._hijos:
            hijo.mostrar(nivel + 1)


# ── construcción del árbol 

producto = Componente("Producto principal")

for i in range(1, 4):
    sub = Componente(f"Subconjunto {i}")
    for j in range(1, 5):
        sub.agregar(Componente(f"Pieza {i}.{j}"))
    producto.agregar(sub)

# ── mostrar estructura base 

print("=== Ensamblado base ===")
producto.mostrar()

# ── agregar subconjunto opcional 

sub_opt = Componente("Subconjunto opcional")
for j in range(1, 5):
    sub_opt.agregar(Componente(f"Pieza opt.{j}"))
producto.agregar(sub_opt)

print("\n=== Con subconjunto opcional ===")
producto.mostrar()