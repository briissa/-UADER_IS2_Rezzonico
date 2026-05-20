import os

class Memento:
    def __init__(self, file, content):

        self.file = file
        self.content = content


class FileWriterUtility:

    def __init__(self, file):

        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    # recibe el estado que debe restaurar
    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


class FileWriterCaretaker:

    def __init__(self):
        # lista para guardar hasta 4 estados
        self.history = []

    def save(self, writer):

        # guarda el estado actual
        self.history.append(writer.save())

        # si supera 4 estados elimina el más viejo
        if len(self.history) > 4:
            self.history.pop(0)

    
    def undo(self, writer, position=0):

        if len(self.history) == 0:
            print("No hay estados guardados")
            return

        if position >= len(self.history):
            print("No existe ese estado anterior")
            return

        # obtiene el estado solicitado
        memento = self.history[-(position + 1)]

        # restaura el estado
        writer.undo(memento)


if __name__ == '__main__':

    os.system("clear")

    print("Crea un objeto que gestionará versiones anteriores")
    caretaker = FileWriterCaretaker()

    print("Crea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")

    print("Se graba algo en el objeto y se salva")
    writer.write("Clase de IS2 en UADER\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se agrega información adicional")
    writer.write("Material adicional de la clase de patrones\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se agrega información adicional II")
    writer.write("Material adicional de la clase de patrones II\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se agrega información adicional III")
    writer.write("Material adicional de la clase de patrones III\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se agrega información adicional IV")
    writer.write("Material adicional de la clase de patrones IV\n")
    print(writer.content + "\n")

    # Recupera el último estado guardado
    print("UNDO(0) -> estado inmediato anterior")
    caretaker.undo(writer, 0)
    print(writer.content + "\n")

    # Recupera un estado más viejo
    print("UNDO(2) -> dos estados anteriores")
    caretaker.undo(writer, 2)
    print(writer.content + "\n")

""""
Ahora el Caretaker guarda varios estados en una lista llamada history.
Puede almacenar hasta 4 versiones anteriores.
El método undo(writer, position) permite recuperar:
0 =último estado guardado
1 = el anterior
2 = dos estados atrás
3 = tres estados atrás
Si se guardan más de 4 estados, el más viejo se elimina automáticamente.
"""
