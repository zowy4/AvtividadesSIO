package singleton;

// Interfaz que define las operaciones básicas de un dispositivo
interface Device {
    void readInput(String input);
    void processInput();
}

// Clase que implementa un dispositivo de entrada
class InputDevice implements Device {
    private String inputData;

    @Override
    public void readInput(String input) {
        this.inputData = input;
        System.out.println("Datos leídos: " + inputData);
    }

    @Override
    public void processInput() {
        if (inputData != null) {
            System.out.println("Procesando datos: " + inputData);
            // Aquí podrías agregar lógica adicional para procesar los datos
            inputData = null; // Limpiar los datos después de procesarlos
        } else {
            System.out.println("No hay datos para procesar.");
        }
    }
}

// Clase que gestiona el dispositivo de entrada
class DeviceManager {
    private Device device;

    public DeviceManager(Device device) {
        this.device = device;
    }

    public void handleInput(String input) {
        device.readInput(input);
        device.processInput();
    }
}

// Clase principal para ejecutar el programa
public class Main {
    public static void main(String[] args) {
        // Crear un dispositivo de entrada
        InputDevice inputDevice = new InputDevice();

        // Crear un manejador de dispositivos
        DeviceManager deviceManager = new DeviceManager(inputDevice);

        // Simular la entrada de datos
        deviceManager.handleInput("Hola, mundo!");
        deviceManager.handleInput("Java es genial.");
        deviceManager.handleInput(""); // Intentar procesar sin datos
    }
}