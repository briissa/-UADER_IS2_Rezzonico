"""
    Patrón Estructural: PROXY
    Clases: Ping (servicio real) y PingProxy (proxy controlado).

    Funcionamiento:
    - Ping.execute(ip)      → realiza 10 pings SOLO si ip comienza con "192."
    - Ping.executefree(ip)  → realiza 10 pings SIN restricción de dirección
    - PingProxy.execute(ip) → si ip == "192.168.0.254" delega a ping.executefree("www.google.com")
                                en cualquier otro caso delega a ping.execute(ip)
"""

import subprocess
import platform
import re


# ──────────────────────────────────────────────
# Interfaz común (contrato del patrón Proxy)
# ──────────────────────────────────────────────
class IPingService:
    """Interfaz que tanto el sujeto real como el proxy implementan."""

    def execute(self, ip: str) -> None:
        raise NotImplementedError



# Sujeto Real
class Ping(IPingService):
    """
    Servicio real de ping.

    execute(ip)     → lanza 10 pings solo si ip comienza con '192.'
    executefree(ip) → lanza 10 pings sin ninguna restricción de dirección
    """

    _INTENTOS: int = 10

    # ---- helpers privados ----

    def _validar_ip(self, ip: str) -> bool:
        """Devuelve True si la dirección comienza con '192.'"""
        return ip.startswith("192.")

    def _ping(self, destino: str) -> None:
        """Ejecuta el comando ping del sistema operativo."""
        sistema = platform.system().lower()

        # Parámetro de cantidad de pings según SO
        if sistema == "windows":
            count_flag = ["-n", str(self._INTENTOS)]
        else:
            count_flag = ["-c", str(self._INTENTOS)]

        cmd = ["ping"] + count_flag + [destino]
        print(f"\n{'='*55}")
        print(f"  Ping → {destino}  ({self._INTENTOS} intentos)")
        print(f"{'='*55}")

        try:
            resultado = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print(resultado.stdout)
            if resultado.returncode != 0:
                print(f"[!] Salida con código {resultado.returncode}")
                if resultado.stderr:
                    print(resultado.stderr)
        except FileNotFoundError:
            print("[ERROR] El comando 'ping' no está disponible en este sistema.")

    # ---- interfaz pública ----

    def execute(self, ip: str) -> None:
        """
        Realiza 10 pings a `ip` SOLO si comienza con '192.'.
        Lanza ValueError en caso contrario.
        """
        if not self._validar_ip(ip):
            raise ValueError(
                f"[Ping] Dirección rechazada: '{ip}'. "
                "Solo se permiten IPs que comiencen con '192.'"
            )
        self._ping(ip)

    def executefree(self, ip: str) -> None:
        """
        Realiza 10 pings a `ip` sin restricción de dirección.
        Acepta tanto IPs como nombres de dominio.
        """
        self._ping(ip)


# ──────────────────────────────────────────────
# Proxy
# ──────────────────────────────────────────────
class PingProxy(IPingService):
    """
    Proxy de control de acceso sobre Ping.

    Regla de redirección en execute(ip):
      - Si ip == '192.168.0.254'  →  delega a ping.executefree('www.google.com')
      - Cualquier otra dirección  →  delega a ping.execute(ip)  (con su validación '192.')
    """

    _IP_ESPECIAL: str = "192.168.0.254"
    _DESTINO_GOOGLE: str = "www.google.com"

    def __init__(self) -> None:
        # El proxy crea y posee la instancia del sujeto real (composición)
        self._ping: Ping = Ping()

    def execute(self, ip: str) -> None:
        """
        Punto de entrada único del proxy.
        Aplica la lógica de redirección antes de delegar al sujeto real.
        """
        print(f"\n[PingProxy] execute('{ip}') invocado.")

        if ip == self._IP_ESPECIAL:
            print(
                f"[PingProxy] IP especial detectada ({self._IP_ESPECIAL}). "
                f"Redirigiendo a '{self._DESTINO_GOOGLE}' via executefree()."
            )
            self._ping.executefree(self._DESTINO_GOOGLE)
        else:
            print(
                f"[PingProxy] IP ordinaria. "
                f"Reenviando a Ping.execute('{ip}') con control de dirección."
            )
            self._ping.execute(ip)


# ──────────────────────────────────────────────
# Demo / prueba de concepto
# ──────────────────────────────────────────────
if __name__ == "__main__":

    proxy = PingProxy()

    print("\n" + "█"*55)
    print("  CASO 1: IP especial → redirige a www.google.com")
    print("█"*55)
    proxy.execute("192.168.0.254")

    print("\n" + "█"*55)
    print("  CASO 2: IP válida (192.x) → pasa al sujeto real")
    print("█"*55)
    proxy.execute("192.168.1.1")

    print("\n" + "█"*55)
    print("  CASO 3: IP inválida → Ping.execute() la rechaza")
    print("█"*55)
    try:
        proxy.execute("10.0.0.1")
    except ValueError as e:
        print(f"[Capturado] {e}")

    print("\n" + "█"*55)
    print("  CASO 4: ejecutar Ping.execute() directamente")
    print("  (sin proxy) con IP inválida → rechazada")
    print("█"*55)
    ping_directo = Ping()
    try:
        ping_directo.execute("8.8.8.8")
    except ValueError as e:
        print(f"[Capturado] {e}")

    print("\n" + "█"*55)
    print("  CASO 5: Ping.executefree() → sin restricción")
    print("█"*55)
    ping_directo.executefree("localhost")