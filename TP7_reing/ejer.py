#!/usr/bin/env python3
# pylint: disable=invalid-name  # Nombre del módulo definido por la cátedra, no modificable


import json
import sys

# Constantes del programa 
VERSION = "1.1"
DEFAULT_KEY = "token1"


#Abstracción base (Branching by Abstraction)
class JSONReaderBase:  # pylint: disable=too-few-public-methods
    """
    Interfaz abstracta para la lectura de archivos JSON.
    Permite intercambiar implementaciones sin modificar el código cliente
    (estrategia 'Branching by Abstraction').
    La advertencia too-few-public-methods se suprime porque esta clase
    es una interfaz de un solo método por diseño.
    """

    def read_key(self, filepath, key):
        """Lee un valor de un archivo JSON dada una clave. Debe implementarse."""
        raise NotImplementedError("Subclases deben implementar read_key()")


# ─── Implementación concreta con patrón Singleton ────────────────────────────
class JSONReaderSingleton(JSONReaderBase):  # pylint: disable=too-few-public-methods
    """
    Lector de archivos JSON implementado como Singleton.

    Garantiza que sólo exista una instancia de esta clase durante
    toda la ejecución del programa, evitando múltiples aperturas
    innecesarias de recursos o estados inconsistentes.
    """

    _instance = None  # Referencia a la única instancia

    def __new__(cls):
        """
        Controla la creación de instancias.
        Si ya existe una, la retorna; si no, la crea.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def read_key(self, filepath, key):
        """
        Abre el archivo JSON indicado y retorna el valor de la clave solicitada.

        Parámetros:
            filepath (str): Ruta al archivo JSON.
            key      (str): Clave a buscar dentro del JSON.

        Retorna:
            str: Valor asociado a la clave, convertido a string.

        Lanza:
            FileNotFoundError : Si el archivo no existe.
            json.JSONDecodeError: Si el archivo no es JSON válido.
            KeyError           : Si la clave no existe en el JSON.
        """
        with open(filepath, 'r', encoding='utf-8') as json_file:
            data = json_file.read()

        obj = json.loads(data)
        return str(obj[key])


# ─── Función de compatibilidad (Branching by Abstraction) ─────────────────────
def get_json_value(filepath, key=DEFAULT_KEY):
    """
    Función pública que actúa como punto de entrada unificado.
    Delega en JSONReaderSingleton, manteniendo la misma interfaz
    que el programa original para compatibilidad hacia atrás.

    Parámetros:
        filepath (str): Ruta al archivo JSON.
        key      (str): Clave a extraer (por defecto 'token1').

    Retorna:
        str o None: El valor encontrado, o None si hubo un error.
    """
    reader = JSONReaderSingleton()
    return reader.read_key(filepath, key)


# ─── Validación de argumentos ─────────────────────────────────────────────────
def parse_arguments(args):
    """
    Valida y procesa los argumentos de línea de comandos.

    Parámetros:
        args (list): Lista de argumentos (sin el nombre del script).

    Retorna:
        tuple: (modo, filepath)
            modo     : 'version' | 'run'
            filepath : ruta al archivo JSON, o None si modo == 'version'
    """
    if len(args) == 0:
        raise ValueError(
            "Error: se requiere un argumento.\n"
            f"Uso: python {sys.argv[0]} <archivo.json>\n"
            f"     python {sys.argv[0]} -v"
        )

    if args[0] == '-v':
        return 'version', None

    if len(args) > 1:
        raise ValueError(
            "Error: demasiados argumentos.\n"
            f"Uso: python {sys.argv[0]} <archivo.json>"
        )

    return 'run', args[0]


# ─── Punto de entrada principal ───────────────────────────────────────────────
def main():
    """
    Función principal del programa.

    Orquesta la validación de argumentos, la lectura del JSON y la
    presentación del resultado. Garantiza que el programa siempre
    termine con un error controlado del programa y nunca con una
    excepción no manejada del sistema.

    Códigos de salida:
        0 : Ejecución exitosa.
        1 : Error controlado del programa (argumento inválido,
            archivo no encontrado, JSON inválido, clave ausente).
    """
    try:
        modo, filepath = parse_arguments(sys.argv[1:])
    except ValueError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    # ── Modo versión ──────────────────────────────────────────────────────
    if modo == 'version':
        print(f"getJason versión {VERSION}")
        sys.exit(0)

    # ── Modo ejecución ────────────────────────────────────────────────────
    try:
        valor = get_json_value(filepath, DEFAULT_KEY)
        print(valor)

    except FileNotFoundError:
        print(
            f"Error: el archivo '{filepath}' no existe o no es accesible.",
            file=sys.stderr
        )
        sys.exit(1)

    except PermissionError:
        print(
            f"Error: permiso denegado al intentar leer '{filepath}'.",
            file=sys.stderr
        )
        sys.exit(1)

    except json.JSONDecodeError as error:
        print(
            f"Error: el archivo '{filepath}' no contiene JSON válido. "
            f"Detalle: {error}",
            file=sys.stderr
        )
        sys.exit(1)

    except KeyError:
        print(
            f"Error: la clave '{DEFAULT_KEY}' no existe en el archivo '{filepath}'.",
            file=sys.stderr
        )
        sys.exit(1)

    except OSError as error:
        # Captura errores de E/S no contemplados arriba (disco lleno, etc.)
        print(f"Error de sistema de archivos: {error}", file=sys.stderr)
        sys.exit(1)


# ─── Ejecución desde línea de comandos ───────────────────────────────────────
if __name__ == '__main__':
    main()