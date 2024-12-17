# Clase que representa un dispositivo
class Device:
    def __init__(self, name):
        self.name = name
        self.status = "Desconectado"

    def connect(self):
        self.status = "Conectado"
        print(f"{self.name} está conectado.")

    def disconnect(self):
        self.status = "Desconectado"
        print(f"{self.name} está desconectado.")

    def operate(self):
        if self.status == "Conectado":
            print(f"{self.name} está operando.")
        else:
            print(f"{self.name} no puede operar porque está desconectado.")

# Clase que maneja los dispositivos
class DeviceManager:
    def __init__(self):
        self.device_table = []  # Tabla de estructuras para los dispositivos

    def add_device(self, device):
        self.device_table.append(device)
        print(f"Dispositivo {device.name} añadido a la tabla.")

    def connect_device(self, device_name):
        for device in self.device_table:
            if device.name == device_name:
                device.connect()
                return
        print(f"Dispositivo {device_name} no encontrado.")

    def disconnect_device(self, device_name):
        for device in self.device_table:
            if device.name == device_name:
                device.disconnect()
                return
        print(f"Dispositivo {device_name} no encontrado.")

    def operate_device(self, device_name):
        for device in self.device_table:
            if device.name == device_name:
                device.operate()
                return
        print(f"Dispositivo {device_name} no encontrado.")

# Clase principal para ejecutar el programa
if __name__ == "__main__":
    # Crear un manejador de dispositivos
    device_manager = DeviceManager()

    # Crear dispositivos
    keyboard = Device("Teclado")
    mouse = Device("Ratón")
    printer = Device("Impresora")

    # Añadir dispositivos a la tabla
    device_manager.add_device(keyboard)
    device_manager.add_device(mouse)
    device_manager.add_device(printer)

    # Conectar y operar dispositivos
    device_manager.connect_device("Teclado")
    device_manager.operate_device("Teclado")

    device_manager.connect_device("Ratón")
    device_manager.operate_device("Ratón")

    device_manager.disconnect_device("Teclado")
    device_manager.operate_device("Teclado")

    device_manager.operate_device("Impresora")  # Intentar operar sin conexión