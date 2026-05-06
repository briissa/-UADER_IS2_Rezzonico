"""
Patrón Estructural: BRIDGE
Dominio: Producción de láminas de acero de 0.5" × 1.5 m
enviadas a uno de dos trenes laminadores (5 m ó 10 m).

Estructura Bridge:
  Abstracción   → LaminaAcero          (puede ser subclasada libremente)
  Implementor   → ITrenLaminador        (contrato de los trenes)
  Concret. impl → TrenLaminador5m
                  TrenLaminador10m

El puente es el atributo  _tren: ITrenLaminador  dentro de LaminaAcero.
Se puede cambiar en tiempo de ejecución con  set_tren(tren).
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# implementador comun (con)

class ITrenLaminador(ABC):
    """
    Implementor del patrón Bridge.
    Define el contrato que todo tren laminador debe cumplir.
    """

    @abstractmethod
    def laminar(self, lamina: "LaminaAcero") -> None:
        """Ejecuta el proceso de laminado para la lámina recibida."""
        ...

    @abstractmethod
    def longitud_plancha(self) -> float:
        """Devuelve la longitud de plancha que produce este tren (metros)."""
        ...


class TrenLaminador5m(ITrenLaminador):
    """Implementación concreta – tren que genera planchas de 5 metros."""

    _LONGITUD: float = 5.0   # metros

    def longitud_plancha(self) -> float:
        return self._LONGITUD

    def laminar(self, lamina: "LaminaAcero") -> None:
        print(
            f"[Tren 5 m] Laminando: espesor={lamina.espesor}\" "
            f"| ancho={lamina.ancho} m "
            f"→ plancha de {self._LONGITUD} m"
        )
        self._proceso(lamina)

    def _proceso(self, lamina: "LaminaAcero") -> None:
        area = self._LONGITUD * lamina.ancho
        print(
            f"           Velocidad de laminación: alta  "
            f"| Área de plancha: {area:.2f} m²"
        )


class TrenLaminador10m(ITrenLaminador):
    """Implementación concreta – tren que genera planchas de 10 metros."""

    _LONGITUD: float = 10.0  # metros

    def longitud_plancha(self) -> float:
        return self._LONGITUD

    def laminar(self, lamina: "LaminaAcero") -> None:
        print(
            f"[Tren 10 m] Laminando: espesor={lamina.espesor}\" "
            f"| ancho={lamina.ancho} m "
            f"→ plancha de {self._LONGITUD} m"
        )
        self._proceso(lamina)

    def _proceso(self, lamina: "LaminaAcero") -> None:
        area = self._LONGITUD * lamina.ancho
        print(
            f"            Velocidad de laminación: baja  "
            f"| Área de plancha: {area:.2f} m²"
        )


# LADO ABSTRACCIÓN  (Abstraction)


class LaminaAcero:
    """
    Abstracción del patrón Bridge.

    Representa una lámina de acero de especificaciones fijas:
      espesor = 0.5 pulgadas
      ancho   = 1.5 metros

    El tren laminador al que se enviará se asigna con set_tren()
    y puede cambiarse en tiempo de ejecución sin modificar esta clase.
    """

    ESPESOR_DEFAULT: float = 0.5   # pulgadas
    ANCHO_DEFAULT:   float = 1.5   # metros

    def __init__(
        self,
        tren: ITrenLaminador | None = None,
        espesor: float = ESPESOR_DEFAULT,
        ancho: float = ANCHO_DEFAULT,
    ) -> None:
        self._espesor: float = espesor
        self._ancho:   float = ancho
        self._tren:    ITrenLaminador | None = tren

    # ── propiedades 

    @property
    def espesor(self) -> float:
        return self._espesor

    @property
    def ancho(self) -> float:
        return self._ancho

    @property
    def tren(self) -> ITrenLaminador | None:
        return self._tren

    # ── bridge 
    def set_tren(self, tren: ITrenLaminador) -> "LaminaAcero":
        """
        Asigna (o reemplaza) el tren laminador en tiempo de ejecución.
        Devuelve self para permitir encadenamiento fluido.
        """
        if not isinstance(tren, ITrenLaminador):
            raise TypeError(
                f"Se esperaba ITrenLaminador, se recibió {type(tren).__name__}"
            )
        self._tren = tren
        return self

    # ── operación de alto nivel 

    def producir(self) -> None:
        """
        Delega el laminado al tren asignado (el 'puente').
        Lanza RuntimeError si no se ha asignado ningún tren.
        """
        if self._tren is None:
            raise RuntimeError(
                "No se ha asignado ningún tren laminador. "
                "Use set_tren() antes de llamar a producir()."
            )
        print(f"\n{'─'*55}")
        print(
            f"  Lámina → {self._espesor}\" espesor | {self._ancho} m ancho"
            f"  [tren: {type(self._tren).__name__}]"
        )
        print(f"{'─'*55}")
        self._tren.laminar(self)

    def __repr__(self) -> str:
        tren_nombre = (
            type(self._tren).__name__ if self._tren else "sin asignar"
        )
        return (
            f"LaminaAcero(espesor={self._espesor}\", "
            f"ancho={self._ancho} m, tren={tren_nombre})"
        )



# ABSTRACCIÓN REFINADA (opcional, muestra extensibilidad)


class LaminaAceroInoxidable(LaminaAcero):
    """
    Abstracción refinada: especialización de LaminaAcero
    para acero inoxidable.  Añade lógica propia sin tocar
    los trenes laminadores — el Bridge lo permite sin fricción.
    """

    GRADO_DEFAULT: str = "304"

    def __init__(
        self,
        grado: str = GRADO_DEFAULT,
        tren: ITrenLaminador | None = None,
    ) -> None:
        super().__init__(tren=tren)
        self._grado = grado

    def producir(self) -> None:
        print(f"  [Inoxidable grado {self._grado}]")
        super().producir()

    def __repr__(self) -> str:
        base = super().__repr__()
        return base.replace("LaminaAcero", f"LaminaAceroInoxidable-{self._grado}")



#demo
if __name__ == "__main__":

    tren5  = TrenLaminador5m()
    tren10 = TrenLaminador10m()

    print("=" * 55)
    print("  CASO 1 – Lámina estándar → Tren 5 m")
    print("=" * 55)
    lamina_a = LaminaAcero(tren=tren5)
    lamina_a.producir()

    print("\n" + "=" * 55)
    print("  CASO 2 – Lámina estándar → Tren 10 m")
    print("=" * 55)
    lamina_b = LaminaAcero(tren=tren10)
    lamina_b.producir()

    print("\n" + "=" * 55)
    print("  CASO 3 – Cambio de tren en tiempo de ejecución")
    print("  (misma lámina, primero 5 m, luego 10 m)")
    print("=" * 55)
    lamina_c = LaminaAcero()
    lamina_c.set_tren(tren5).producir()
    lamina_c.set_tren(tren10).producir()

    print("\n" + "=" * 55)
    print("  CASO 4 – Abstracción refinada: inoxidable 316")
    print("=" * 55)
    inox = LaminaAceroInoxidable(grado="316", tren=tren10)
    inox.producir()

    print("\n" + "=" * 55)
    print("  CASO 5 – Producción sin tren asignado (error controlado)")
    print("=" * 55)
    lamina_sin_tren = LaminaAcero()
    try:
        lamina_sin_tren.producir()
    except RuntimeError as e:
        print(f"[RuntimeError capturado] {e}")

    print("\n" + "=" * 55)
    print("  Estado final de objetos")
    print("=" * 55)
    for obj in [lamina_a, lamina_b, lamina_c, inox, lamina_sin_tren]:
        print(" ", repr(obj))