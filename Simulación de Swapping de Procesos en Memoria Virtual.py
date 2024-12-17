import random
import time

class Process:
    def __init__(self, pid, size):
        self.pid = pid  # Identificador del proceso
        self.size = size  # Tamaño del proceso en memoria

class Memory:
    def __init__(self, capacity):
        self.capacity = capacity  # Capacidad total de la memoria
        self.processes = []  # Lista de procesos en memoria

    def load_process(self, process):
        if self.get_used_memory() + process.size <= self.capacity:
            self.processes.append(process)
            print(f"Proceso {process.pid} cargado en memoria.")
        else:
            print(f"Memoria llena. Realizando swapping para cargar el proceso {process.pid}.")
            self.swap_process(process)

    def swap_process(self, new_process):
        # Simulamos el swapping de un proceso
        # Elegimos un proceso aleatorio para ser removido
        process_to_swap = random.choice(self.processes)
        print(f"Swapping: Proceso {process_to_swap.pid} removido de memoria.")
        self.processes.remove(process_to_swap)
        self.processes.append(new_process)
        print(f"Proceso {new_process.pid} cargado en memoria tras el swapping.")

    def get_used_memory(self):
        return sum(process.size for process in self.processes)

    def display_memory(self):
        print("Estado actual de la memoria:")
        for process in self.processes:
            print(f"Proceso {process.pid} (Tamaño: {process.size})")
        print(f"Tamaño total usado: {self.get_used_memory()} / {self.capacity}\n")

# Simulación
if __name__ == "__main__":
    memory_capacity = 10  # Capacidad total de la memoria
    memory = Memory(memory_capacity)

    # Creamos algunos procesos con tamaños aleatorios
    processes = [Process(pid=i, size=random.randint(1, 5)) for i in range(1, 11)]

    # Intentamos cargar los procesos en memoria
    for process in processes:
        memory.load_process(process)
        memory.display_memory()
        time.sleep(1)  # Pausa para simular el tiempo de carga