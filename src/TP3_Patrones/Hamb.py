class Hamburguesa:

    def entregar_mostrador(self):
        print("La hamburguesa se entrega en el mostrador")

    def retirar_cliente(self):
        print("El cliente retira la hamburguesa en el local")

    def enviar_delivery(self):
        print("La hamburguesa es enviada por delivery")


#  hacemos la prueba (en la misma clase/archivo)
if __name__ == "__main__":
    pedido = Hamburguesa()

    pedido.entregar_mostrador()
    pedido.retirar_cliente()
    pedido.enviar_delivery()