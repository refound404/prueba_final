import json
from colorama import Fore

class Tarea:
    def __init__(self, descripcion, completada=False):
        """
        Inicializa una nueva tarea.
        
        :param descripcion: Descripción de la tarea.
        :param completada: Estado de la tarea, True si está completada, False si está pendiente.
        """
        self.descripcion = descripcion
        self.completada = completada

    def marcar_completada(self):
        """
        Marca la tarea como completada.
        """
        self.completada = True

    def to_dict(self):
        """
        Convierte la tarea a un diccionario.
        """
        return {'descripcion': self.descripcion, 'completada': self.completada}

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Tarea desde un diccionario.
        
        :param data: Diccionario con los datos de la tarea.
        """
        return cls(data['descripcion'], data['completada'])

    def __str__(self):
        """
        Retorna una representación en cadena de la tarea.
        """
        estado = "Completada" if self.completada else "Pendiente"
        return f"{self.descripcion} - {estado}"


class ListaDeTareas:
    def __init__(self, archivo='tareas.json'):
        """
        Inicializa una nueva lista de tareas.
        
        :param archivo: Nombre del archivo JSON donde se guardan las tareas.
        """
        self.tareas = []
        self.archivo = archivo
        self.cargar_tareas()

    def agregar_tarea(self, descripcion):
        """
        Agrega una nueva tarea a la lista.
        
        :param descripcion: Descripción de la nueva tarea.
        """
        nueva_tarea = Tarea(descripcion)
        self.tareas.append(nueva_tarea)
        self.guardar_tareas()

    def marcar_completada(self, posicion):
        """
        Marca una tarea como completada dado su índice en la lista.
        
        :param posicion: Índice de la tarea a marcar como completada.
        """
        try:
            self.tareas[posicion].marcar_completada()
            self.guardar_tareas()
        except IndexError:
            print("Error: No existe una tarea en la posición especificada.")

    def mostrar_tareas(self):
        """
        Muestra todas las tareas con su estado.
        """
        if not self.tareas:
            print("No hay tareas pendientes.")
        else:
            for indice, tarea in enumerate(self.tareas):
                print(f"{indice}. {tarea}")

    def eliminar_tarea(self, posicion):
        """
        Elimina una tarea de la lista dado su índice.
        
        :param posicion: Índice de la tarea a eliminar.
        """
        try:
            del self.tareas[posicion]
            self.guardar_tareas()
        except IndexError:
            print("Error: No existe una tarea en la posición especificada.")

    def guardar_tareas(self):
        """
        Guarda las tareas en un archivo JSON.
        """
        with open(self.archivo, 'w') as f:
            json.dump([tarea.to_dict() for tarea in self.tareas], f, indent=4)

    def cargar_tareas(self):
        """
        Carga las tareas desde un archivo JSON.
        """
        try:
            with open(self.archivo, 'r') as f:
                tareas = json.load(f)
                self.tareas = [Tarea.from_dict(tarea) for tarea in tareas]
        except FileNotFoundError:
            self.tareas = []


def menu():
    """
    Función que maneja el menú de opciones del usuario.
    """
    lista_de_tareas = ListaDeTareas()

    while True:
        print("\nGestor de Tareas Pendientes")
        print(Fore.BLUE+'1' + Fore.WHITE+" Agregar tarea")
        print(Fore.BLUE+"2" + Fore.WHITE+ " Marcar tarea como completada")
        print(Fore.BLUE+"3" + Fore.WHITE+ " Mostrar todas las tareas")
        print(Fore.BLUE+"4" + Fore.RED+" Eliminar tarea")
        print(Fore.BLUE+"5" + Fore.WHITE+" Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        if opcion == 1:
            descripcion = input("Ingrese la descripción de la tarea: ")
            lista_de_tareas.agregar_tarea(descripcion)
        elif opcion == 2:
            try:
                posicion = int(input("Ingrese el número de la tarea a marcar como completada: "))
                lista_de_tareas.marcar_completada(posicion)
            except ValueError:
                print("Por favor, ingrese un número válido.")
        elif opcion == 3:
            lista_de_tareas.mostrar_tareas()
        elif opcion == 4:
            try:
                posicion = int(input("Ingrese el número de la tarea a eliminar: "))
                lista_de_tareas.eliminar_tarea(posicion)
            except ValueError:
                print("Por favor, ingrese un número válido.")
        elif opcion == 5:
            print("Saliendo del gestor de tareas.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    menu()
