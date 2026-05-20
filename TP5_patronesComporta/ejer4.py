import os

class State:
    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))


class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate


class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate


# Memorias: cada una tiene una frecuencia y su banda (AM o FM)
class MemoryState(State):
    def __init__(self, radio):
        self.radio = radio
        self.name = "MEMORIA"
        # Formato: (etiqueta, frecuencia, banda)
        self.stations = [
            ("M1", "1250", "AM"),
            ("M2", "103.9", "FM"),
            ("M3", "1510", "AM"),
            ("M4", "89.1", "FM"),
        ]
        self.pos = -1

    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        etiqueta, freq, banda = self.stations[self.pos]
        print("Sintonizando... Memoria {} → {} {}".format(etiqueta, freq, banda))

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate


class Radio:
    def __init__(self):
        self.fmstate     = FmState(self)
        self.amstate     = AmState(self)
        self.memorystate = MemoryState(self)
        self.state       = self.fmstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()

    def toggle_memory(self):
        print("Cambiando a MEMORIAS")
        self.state = self.memorystate


if __name__ == "__main__":
    os.system("clear")
    radio = Radio()

    # Un ciclo: 3 FM → cambio AM → 3 AM → cambio memorias → 4 memorias → cambio FM
    actions = (
        [radio.scan] * 3 +
        [radio.toggle_amfm] +
        [radio.scan] * 3 +
        [radio.toggle_memory] +
        [radio.scan] * 4 +
        [radio.toggle_amfm]   # vuelve a FM
    )
    actions *= 2

    print("Recorre las acciones ejecutando la acción")
    for action in actions:
        action()


"""
Lo unico que se agregó al original fue:

MemoryState — nuevo estado con las 4 memorias (M1 a M4), cada una con etiqueta, frecuencia y banda (AM o FM). Su scan() las recorre en secuencia.
radio.toggle_memory() — método para cambiar al estado de memorias.
El ciclo de acciones ahora incluye el barrido de las 4 memorias en cada vuelta.
"""