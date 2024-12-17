class DiskScheduler:
    def __init__(self, requests, head_start, direction, disk_size):
        self.requests = sorted(requests)  # Solicitudes ordenadas
        self.head_start = head_start  # Posición inicial del cabezal
        self.direction = direction  # Dirección inicial ('up' o 'down')
        self.disk_size = disk_size  # Tamaño del disco

    def scan(self):
        # Inicializar la secuencia de servicio
        sequence = []
        current_position = self.head_start

        # Si la dirección es hacia arriba
        if self.direction == 'up':
            # Atender solicitudes en dirección ascendente
            for request in self.requests:
                if request >= current_position:
                    sequence.append(request)
            # Atender el final del disco
            if self.disk_size - 1 not in sequence:
                sequence.append(self.disk_size - 1)
            # Atender solicitudes en dirección descendente
            for request in reversed(self.requests):
                if request < current_position:
                    sequence.append(request)

        # Si la dirección es hacia abajo
        elif self.direction == 'down':
            # Atender solicitudes en dirección descendente
            for request in reversed(self.requests):
                if request <= current_position:
                    sequence.append(request)
            # Atender el inicio del disco
            if 0 not in sequence:
                sequence.append(0)
            # Atender solicitudes en dirección ascendente
            for request in self.requests:
                if request > current_position:
                    sequence.append(request)

        return sequence

# Función principal para ejecutar el programa
if __name__ == "__main__":
    # Solicitudes de acceso al disco
    requests = [98, 180, 34, 60, 92, 11, 41, 114]
    head_start = 50  # Posición inicial del cabezal
    direction = 'up'  # Dirección inicial ('up' o 'down')
    disk_size = 200  # Tamaño del disco

    # Crear un programador de disco
    scheduler = DiskScheduler(requests, head_start, direction, disk_size)

    # Obtener la secuencia de servicio
    service_sequence = scheduler.scan()

    # Mostrar la secuencia de servicio
    print("Secuencia de servicio del algoritmo SCAN:")
    print(service_sequence)