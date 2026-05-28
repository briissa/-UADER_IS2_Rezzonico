"""
getJason.py  —  Recuperador de claves desde archivo JSON
=========================================================
Uso:
    python3 getJason.py <archivo_json> [clave]

Argumentos:
    archivo_json  Ruta al archivo JSON que contiene las claves (requerido).
    clave         Nombre de la clave a recuperar (opcional, default: "token1").

Salida:
    Imprime en stdout el valor asociado a la clave indicada.

Ejemplos:
    python3 getJason.py sitedata.json              -> imprime valor de "token1"
    python3 getJason.py sitedata.json token2       -> imprime valor de "token2"

Códigos de salida:
    0  Éxito.
    1  Argumentos insuficientes, archivo no encontrado, JSON inválido o clave ausente.

Historial:
    2025-05-06  Versión original compilada (getJason.pyc) — solo recuperaba "token1" fijo.
    2025-05-28  Reingeniería: se agrega soporte de clave por argumento con default "token1",
                manejo de errores y documentación.
"""

import json
import sys


DEFAULT_KEY = "token1"


def main():
    # Validar que se haya provisto al menos el nombre del archivo JSON
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <archivo_json> [clave]", file=sys.stderr)
        print(f"     clave por defecto: \"{DEFAULT_KEY}\"", file=sys.stderr)
        sys.exit(1)

    jsonfile = sys.argv[1]

    # La clave es opcional; si no se indica se usa DEFAULT_KEY
    jsonkey = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_KEY

    # Leer y parsear el archivo JSON
    try:
        with open(jsonfile, "r") as myfile:
            data = myfile.read()
    except FileNotFoundError:
        print(f"Error: archivo no encontrado: '{jsonfile}'", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error al leer '{jsonfile}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        obj = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error: JSON inválido en '{jsonfile}': {e}", file=sys.stderr)
        sys.exit(1)

    # Recuperar el valor de la clave solicitada
    if jsonkey not in obj:
        print(f"Error: clave '{jsonkey}' no encontrada en '{jsonfile}'.", file=sys.stderr)
        print(f"Claves disponibles: {list(obj.keys())}", file=sys.stderr)
        sys.exit(1)

    print(str(obj[jsonkey]))


if __name__ == "__main__":
    main()