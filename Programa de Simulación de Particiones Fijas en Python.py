class Partition:
    def __init__(self, size):
        self.size = size
        self.process = None

    def allocate(self, process_size):
        if self.process is None and process_size <= self.size:
            self.process = process_size
            return True
        return False

    def deallocate(self):
        self.process = None

    def __str__(self):
        return f"Partition(size={self.size}, process_size={self.process})"


class MemoryManager:
    def __init__(self, partition_sizes):
        self.partitions = [Partition(size) for size in partition_sizes]

    def allocate_process(self, process_size):
        for partition in self.partitions:
            if partition.allocate(process_size):
                print(f"Allocated process of size {process_size} to {partition}")
                return
        print(f"Failed to allocate process of size {process_size}. Not enough memory.")

    def deallocate_process(self, partition_index):
        if 0 <= partition_index < len(self.partitions):
            self.partitions[partition_index].deallocate()
            print(f"Deallocated process from partition {partition_index}.")
        else:
            print("Invalid partition index.")

    def display_memory(self):
        for i, partition in enumerate(self.partitions):
            print(f"Partition {i}: {partition}")


# Ejemplo de uso
if __name__ == "__main__":
    # Definimos las particiones de memoria
    partition_sizes = [100, 200, 300, 400]
    memory_manager = MemoryManager(partition_sizes)

    # Mostramos el estado inicial de la memoria
    print("Estado inicial de la memoria:")
    memory_manager.display_memory()

    # Intentamos asignar procesos
    memory_manager.allocate_process(120)  # Debería asignarse a la partición de 200
    memory_manager.allocate_process(250)  # Debería asignarse a la partición de 300
    memory_manager.allocate_process(400)  # Debería fallar, ya que no hay suficiente espacio

    # Mostramos el estado de la memoria después de las asignaciones
    print("\nEstado de la memoria después de las asignaciones:")
    memory_manager.display_memory()

    # Liberamos un proceso
    memory_manager.deallocate_process(1)  # Liberamos la partición 1 (200)
    
    # Mostramos el estado final de la memoria
    print("\nEstado final de la memoria:")
    memory_manager.display_memory()