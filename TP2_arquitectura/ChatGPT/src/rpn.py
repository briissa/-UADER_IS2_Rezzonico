"""Calculadora RPN con funciones matemáticas, constantes y memorias."""

import math
import sys
from collections.abc import Callable


class RPNError(Exception):
    """Excepción personalizada para errores de la calculadora RPN."""

    pass


class RPNCalculator:
    """Calculadora RPN que mantiene una pila y 10 memorias."""

    def __init__(self) -> None:
        """Inicializa la calculadora con pila vacía y memorias en cero."""
        self.pila: list[float] = []
        self.memorias: dict[str, float] = {f"{i:02d}": 0.0 for i in range(10)}

    def _validar_pila(self, necesarios: int = 1) -> None:
        """Verifica que haya suficientes elementos en la pila."""
        if len(self.pila) < necesarios:
            raise RPNError(
                f"Pila insuficiente: necesita {necesarios} elemento(s), "
                f"tiene {len(self.pila)}"
            )

    def _aplicar_operacion_binaria(
        self, operacion: Callable[[float, float], float], simbolo: str
    ) -> None:
        """Aplica una operación binaria a los dos elementos superiores."""
        self._validar_pila(2)
        b = self.pila.pop()
        a = self.pila.pop()
        try:
            resultado = operacion(a, b)
            self.pila.append(resultado)
        except ZeroDivisionError as exc:
            raise RPNError(f"División por cero en operación {simbolo}") from exc

    def _aplicar_operacion_unaria(
        self, operacion: Callable[[float], float], nombre: str
    ) -> None:
        """Aplica una operación unaria al elemento superior."""
        self._validar_pila(1)
        a = self.pila.pop()
        try:
            resultado = operacion(a)
            self.pila.append(resultado)
        except ValueError as e:
            raise RPNError(f"Error en {nombre}: {e}") from e

    def ejecutar(self, expresion: str) -> float:
        """Ejecuta una expresión RPN completa."""
        tokens = expresion.strip().split()
        i = 0

        while i < len(tokens):
            token = tokens[i]

            # Intentar parsear como número
            try:
                self.pila.append(float(token))
                i += 1
                continue
            except ValueError:
                # No es número, continuar con otros procesamientos
                pass

            # Operaciones básicas
            if token == "+":
                self._aplicar_operacion_binaria(lambda x, y: x + y, "+")
            elif token == "-":
                self._aplicar_operacion_binaria(lambda x, y: x - y, "-")
            elif token == "*":
                self._aplicar_operacion_binaria(lambda x, y: x * y, "*")
            elif token == "/":
                self._aplicar_operacion_binaria(lambda x, y: x / y, "/")

            # Comandos de pila
            elif token == "dup":
                self._validar_pila(1)
                self.pila.append(self.pila[-1])
            elif token == "swap":
                self._validar_pila(2)
                self.pila[-1], self.pila[-2] = self.pila[-2], self.pila[-1]
            elif token == "drop":
                self._validar_pila(1)
                self.pila.pop()
            elif token == "clear":
                self.pila.clear()

            # Constantes
            elif token == "pi":
                self.pila.append(math.pi)
            elif token == "e":
                self.pila.append(math.e)
            elif token == "phi":
                self.pila.append((1 + math.sqrt(5)) / 2)

            # Funciones matemáticas
            elif token == "sqrt":
                self._aplicar_operacion_unaria(lambda x: math.sqrt(x), "sqrt")
            elif token == "log":
                self._aplicar_operacion_unaria(lambda x: math.log10(x), "log")
            elif token == "ln":
                self._aplicar_operacion_unaria(lambda x: math.log(x), "ln")
            elif token == "e^x":
                self._aplicar_operacion_unaria(lambda x: math.exp(x), "e^x")
            elif token == "10^x":
                self._aplicar_operacion_unaria(lambda x: 10**x, "10^x")
            elif token == "y^x":
                self._validar_pila(2)
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(a**b)
            elif token == "1/x":
                self._aplicar_operacion_unaria(lambda x: 1 / x, "1/x")
            elif token == "CHS":
                self._aplicar_operacion_unaria(lambda x: -x, "CHS")

            # Funciones trigonométricas (en grados)
            elif token == "sin":
                self._aplicar_operacion_unaria(
                    lambda x: math.sin(math.radians(x)), "sin"
                )
            elif token == "cos":
                self._aplicar_operacion_unaria(
                    lambda x: math.cos(math.radians(x)), "cos"
                )
            elif token == "tg":
                self._aplicar_operacion_unaria(
                    lambda x: math.tan(math.radians(x)), "tg"
                )
            elif token == "asin":
                self._aplicar_operacion_unaria(
                    lambda x: math.degrees(math.asin(x)), "asin"
                )
            elif token == "acos":
                self._aplicar_operacion_unaria(
                    lambda x: math.degrees(math.acos(x)), "acos"
                )
            elif token == "atg":
                self._aplicar_operacion_unaria(
                    lambda x: math.degrees(math.atan(x)), "atg"
                )

            # Memorias
            elif token == "STO":
                if i + 1 >= len(tokens):
                    raise RPNError("STO requiere un número de memoria (00-09)")
                mem = tokens[i + 1]
                if mem not in self.memorias:
                    raise RPNError(f"Memoria inválida: {mem}. Use 00-09")
                self._validar_pila(1)
                self.memorias[mem] = self.pila[-1]
                self.pila.pop()
                i += 1
            elif token == "RCL":
                if i + 1 >= len(tokens):
                    raise RPNError("RCL requiere un número de memoria (00-09)")
                mem = tokens[i + 1]
                if mem not in self.memorias:
                    raise RPNError(f"Memoria inválida: {mem}. Use 00-09")
                self.pila.append(self.memorias[mem])
                i += 1

            else:
                raise RPNError(f"Token inválido: {token}")

            i += 1

        # Verificar que quede exactamente un elemento
        if len(self.pila) != 1:
            raise RPNError(
                f"La pila debe quedar con 1 elemento, pero tiene {len(self.pila)}"
            )

        return self.pila[0]


def main() -> None:
    """Función principal del programa."""
    if len(sys.argv) > 1:
        expresion = " ".join(sys.argv[1:])
    else:
        expresion = input("Ingrese expresión RPN: ")

    calc = RPNCalculator()
    try:
        resultado = calc.ejecutar(expresion)
        print(f"Resultado: {resultado}")
    except RPNError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
