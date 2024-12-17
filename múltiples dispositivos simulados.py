import random
import time
import threading

class CommunicationBus:
    def __init__(self):
        self.devices = []

    def register_device(self, device):
        self.devices.append(device)
        device.set_bus(self)

    def send_message(self, sender, message):
        print(f"{sender.name} envía: {message}")
        for device in self.devices:
            if device != sender:
                device.receive_message(message)

class Device:
    def __init__(self, name):
        self.name = name
        self.bus = None

    def set_bus(self, bus):
        self.bus = bus

    def send(self, message):
        if self.bus:
            self.bus.send_message(self, message)

    def receive_message(self, message):
        print(f"{self.name} recibe: {message}")

class HardDrive(Device):
    def __init__(self):
        super().__init__("Disco Duro")

    def read(self):
        data = f"Datos leídos: {random.randint(1, 100)}"
        self.send(data)

class Printer(Device):
    def __init__(self):
        super().__init__("Impresora")

    def print_document(self, document):
        self.send(f"Imprimiendo: {document}")

class Keyboard(Device):
    def __init__(self):
        super().__init__("Teclado")

    def type(self):
        keys = ["A", "B", "C", "D", "E"]
        key = random.choice(keys)
        self.send(f"Tecla presionada: {key}")

def simulate_devices(bus):
    hard_drive = HardDrive()
    printer = Printer()
    keyboard = Keyboard()

    bus.register_device(hard_drive)
    bus.register_device(printer)
    bus.register_device(keyboard)

    while True:
        time.sleep(random.uniform(1, 3))  # Espera aleatoria
        hard_drive.read()
        time.sleep(random.uniform(1, 3))
        keyboard.type()
        time.sleep(random.uniform(1, 3))
        printer.print_document("Documento de prueba")

if __name__ == "__main__":
    bus = CommunicationBus()
    device_thread = threading.Thread(target=simulate_devices, args=(bus,))
    device_thread.start()