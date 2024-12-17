from collections import deque

# Clase que representa una interrupción
class Interrupt:
    def __init__(self, message):
        self.message = message

# Clase que maneja las interrupciones
class InterruptHandler:
    def __init__(self):
        self.interrupt_queue = deque()  # Cola para manejar las interrupciones

    def add_interrupt(self, interrupt):
        self.interrupt_queue.append(interrupt)
        print(f"Interrupción añadida: {interrupt.message}")

    def handle_interrupts(self):
        while self.interrupt_queue:
            interrupt = self.interrupt_queue.popleft()  # Obtener la primera interrupción
            print(f"Manejando interrupción: {interrupt.message}")
            # Aquí podrías agregar lógica adicional para manejar la interrupción

# Clase que simula un dispositivo que puede generar interrupciones
class Device:
    def __init__(self, name, interrupt_handler):
        self.name = name
        self.interrupt_handler = interrupt_handler

    def generate_interrupt(self, message):
        interrupt = Interrupt(f"{self.name}: {message}")
        self.interrupt_handler.add_interrupt(interrupt)

# Clase principal para ejecutar el programa
if __name__ == "__main__":
    # Crear un manejador de interrupciones
    interrupt_handler = InterruptHandler()

    # Crear dispositivos que generarán interrupciones
    keyboard = Device("Teclado", interrupt_handler)
    mouse = Device("Ratón", interrupt_handler)
    timer = Device("Temporizador", interrupt_handler)

    # Simular la generación de interrupciones
    keyboard.generate_interrupt("Tecla presionada")
    mouse.generate_interrupt("Clic detectado")
    timer.generate_interrupt("Tiempo agotado")

    # Manejar las interrupciones
    interrupt_handler.handle_interrupts()