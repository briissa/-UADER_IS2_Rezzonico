# pylint: disable=invalid-name
"""getJason.py - versión 1.2 - Sistema de pagos automatizado con selección balanceada."""

import json
import sys


class TokenStore:
    """Singleton: carga sitedata.json y devuelve la clave de un token."""

    _instance = None

    def __init__(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            self._data = json.loads(f.read())

    @classmethod
    def get_instance(cls, filepath="sitedata.json"):
        """Retorna la única instancia, creándola si no existe."""
        if cls._instance is None:
            cls._instance = cls(filepath)
        return cls._instance

    def get_key(self, token):
        """Retorna la clave asociada al token dado."""
        return str(self._data[token])


class BankAccount:
    """Nodo de la cadena de comando: procesa el pago o lo delega al siguiente."""

    def __init__(self, token, balance):
        self.token = token
        self.balance = balance
        self._next = None
        self._payments = []

    def get_payments(self):
        """Retorna la lista de pagos de esta cuenta."""
        return self._payments

    def set_next(self, account):
        """Encadena la siguiente cuenta."""
        self._next = account
        return account

    def handle(self, order_id, amount):
        """Intenta pagar; si no hay saldo, propaga al siguiente nodo."""
        if self.balance >= amount:
            self.balance -= amount
            self._payments.append((order_id, self.token, amount))
            key = TokenStore.get_instance().get_key(self.token)
            print(f"  Pedido #{order_id:03d} | token: {self.token} | clave: {key} "
                  f"| monto: ${amount:.2f} | saldo restante: ${self.balance:.2f}")
            return True
        if self._next:
            return self._next.handle(order_id, amount)
        print(f"  Pedido #{order_id:03d} | RECHAZADO - saldo insuficiente.")
        return False


class PaymentChain:
    """Administra la cadena de cuentas y enruta pagos en forma balanceada."""

    def __init__(self, accounts):
        """Recibe lista de (token, saldo_inicial) y construye la cadena."""
        self._accounts = [BankAccount(t, b) for t, b in accounts]
        for i in range(len(self._accounts) - 1):
            self._accounts[i].set_next(self._accounts[i + 1])
        self._turn = 0

    def pay(self, order_id, amount):
        """Enruta el pago a la cuenta de turno; si no tiene saldo, propaga."""
        self._accounts[self._turn % len(self._accounts)].handle(order_id, amount)
        self._turn += 1

    def listing(self):
        """Muestra todos los pagos en orden cronológico (patrón iterator)."""
        all_payments = sorted(
            [p for acc in self._accounts for p in acc.get_payments()],
            key=lambda r: r[0]
        )
        print("\n=== Listado cronológico de pagos ===")
        for order_id, token, amount in all_payments:
            print(f"  #{order_id:03d} | {token} | ${amount:.2f}")


def main():
    """Inicializa el sistema y ejecuta pedidos de prueba."""
    if len(sys.argv) < 2:
        print("Uso: python getJason.py <archivo_json>")
        sys.exit(1)

    TokenStore.get_instance(sys.argv[1])

    chain = PaymentChain([("token1", 1000.00), ("token2", 2000.00)])

    print("=== Procesando pedidos de pago ($500 c/u) ===")
    for order_num in range(1, 9):
        chain.pay(order_num, 500.00)

    chain.listing()


if __name__ == "__main__":
    main()