# Administración de Memoria

## 3.1 Política y filosofía

### 1. ¿Cuál es la diferencia entre fragmentación interna y externa? Explica cómo cada una afecta el rendimiento de la memoria.

#### Fragmentación interna:
Ocurre cuando un bloque de memoria asignado a un proceso es mayor que el espacio requerido por el proceso, dejando un fragmento interno no utilizado dentro del bloque asignado.
- **Ejemplo**: Si un proceso necesita 2.5 KB y el sistema asigna bloques de 4 KB, quedan 1.5 KB inutilizados en cada bloque asignado.
- **Impacto en el rendimiento**: Reduce la eficiencia de uso de la memoria, ya que el espacio asignado no es completamente aprovechado.

#### Fragmentación externa:
Sucede cuando hay suficiente memoria libre en total, pero está dividida en bloques pequeños no contiguos que no pueden satisfacer las solicitudes de los procesos.
- **Ejemplo**: Si un proceso necesita 8 KB y hay 16 KB de memoria libre dividida en bloques de 2 KB, no puede asignarse porque no hay un espacio contiguo disponible.
- **Impacto en el rendimiento**: Dificulta la asignación de memoria para nuevos procesos, aumentando la posibilidad de fallos de asignación, aunque haya suficiente memoria disponible.

### 2. Investiga y explica las políticas de reemplazo de páginas en sistemas operativos. ¿Cuál consideras más eficiente y por qué?

Cuando un sistema operativo necesita cargar una página y no hay espacio disponible en la memoria, utiliza una política de reemplazo de páginas para decidir cuál página sacar. Las principales políticas son:

#### 1. FIFO (First In, First Out):
La página más antigua (la primera que se cargó en la memoria) es la que se reemplaza.
- **Ventajas**: Fácil de implementar.
- **Desventajas**: Puede provocar el *Belady's anomaly* (un aumento en los fallos de página al incrementar los marcos).

#### 2. LRU (Least Recently Used):
Reemplaza la página que no ha sido utilizada por el mayor tiempo.
- **Ventajas**: Más eficiente en muchos casos que FIFO, ya que prioriza páginas recientemente usadas.
- **Desventajas**: Requiere hardware o algoritmos para rastrear el historial de uso, aumentando la complejidad.

#### 3. OPT (Optimal):
Reemplaza la página que no será usada por el mayor tiempo en el futuro.
- **Ventajas**: Es la política más eficiente en teoría, minimizando fallos de página.
- **Desventajas**: No es práctico porque requiere conocimiento del futuro.

#### 4. Clock (Second-Chance):
Usa un bit para indicar si una página ha sido referenciada. Si una página no ha sido usada, se reemplaza; de lo contrario, su bit se resetea y se revisa la siguiente.
- **Ventajas**: Menor sobrecarga que LRU, pero más eficiente que FIFO.
- **Desventajas**: Puede requerir más tiempo para encontrar una página candidata.

---

### ¿Cuál es más eficiente y por qué?
- **Elección sugerida**: **LRU (Least Recently Used)**  
  Aunque tiene mayor complejidad que FIFO, es más eficiente en sistemas reales porque da prioridad a páginas que probablemente seguirán siendo usadas.
  
- **Alternativa en recursos limitados**: El algoritmo **Clock** puede ser una opción práctica, ya que balancea eficiencia y simplicidad.

- **Teoría**: **OPT** es ideal en simulaciones para análisis, pero no es aplicable en tiempo real.
# 3.2 Memoria real

## 1. Escribe un programa en C o Python que simule la administración de memoria mediante particiones fijas.

```python
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
```
## 2. Diseña un algoritmo para calcular qué procesos pueden ser asignados a un sistema con memoria real limitada utilizando el algoritmo de "primera cabida".

```python
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

    def is_free(self):
        return self.process is None

    def __str__(self):
        return f"Partition(size={self.size}, process_size={self.process})"


class FirstFitMemoryManager:
    def __init__(self, partition_sizes):
        self.partitions = [Partition(size) for size in partition_sizes]

    def allocate_process(self, process_size):
        for partition in self.partitions:
            if partition.allocate(process_size):
                print(f"Allocated process of size {process_size} to {partition}")
                return
        print(f"Failed to allocate process of size {process_size}. Not enough memory.")

    def display_memory(self):
        for i, partition in enumerate(self.partitions):
            print(f"Partition {i}: {partition}")


# Ejemplo de uso
if __name__ == "__main__":
    # Definimos las particiones de memoria
    partition_sizes = [100, 200, 300, 400]
    memory_manager = FirstFitMemoryManager(partition_sizes)

    # Mostramos el estado inicial de la memoria
    print("Estado inicial de la memoria:")
    memory_manager.display_memory()

    # Intentamos asignar procesos
    processes = [120, 200, 150, 300, 100, 50]
    for process in processes:
        memory_manager.allocate_process(process)

    # Mostramos el estado de la memoria después de las asignaciones
    print("\nEstado de la memoria después de las asignaciones:")
    memory_manager.display_memory()
```
# 3.3 Organización de memoria virtual

## 1. Investiga y explica el concepto de "paginación" y "segmentación". ¿Cuáles son las ventajas y desventajas de cada técnica?

# Paginación

La **paginación** es una técnica de administración de memoria en la que la memoria física y la memoria virtual se dividen en bloques de tamaño fijo llamados **marcos** (en la memoria física) y **páginas** (en la memoria virtual). Estas páginas se asignan a marcos en cualquier lugar de la memoria física, permitiendo un uso eficiente del espacio disponible.

### Ventajas:
- Evita la **fragmentación externa**, ya que todas las páginas y marcos tienen el mismo tamaño.
- Permite la **multitarea eficiente**, ya que los procesos pueden cargarse parcialmente en la memoria.
- Facilita la **protección de memoria**, porque cada página tiene permisos definidos.

### Desventajas:
- Introduce **fragmentación interna** si una página no utiliza completamente un marco.
- Requiere una **tabla de páginas** para cada proceso, lo que puede consumir memoria y afectar el rendimiento.

---

# Segmentación

La **segmentación** divide la memoria en bloques de tamaño variable llamados **segmentos**, que representan estructuras lógicas del programa como código, datos y pila. Cada segmento tiene una dirección base y un límite que determinan su posición y tamaño en la memoria física.

### Ventajas:
- Se adapta a las **necesidades lógicas** del programa, lo que facilita la programación modular.
- Puede reducir la **fragmentación interna**, ya que los segmentos se ajustan al tamaño lógico de cada estructura.

### Desventajas:
- Sufre de **fragmentación externa**, ya que los segmentos tienen tamaños variables.
- La **administración de memoria** es más compleja, porque requiere un manejo adicional de las tablas de segmentos y su traducción.
---
## 2. Escribe un programa que simule una tabla de páginas para procesos con acceso aleatorio a memoria virtual.
```python
import random

class Page:
    def __init__(self, page_number):
        self.page_number = page_number
        self.frame_number = None  # Número de marco en la memoria física
        self.valid = False  # Indica si la página es válida

    def __str__(self):
        return f"Page {self.page_number}: Frame {self.frame_number}, Valid: {self.valid}"


class PageTable:
    def __init__(self, num_pages):
        self.pages = [Page(i) for i in range(num_pages)]

    def map_page(self, page_number, frame_number):
        if 0 <= page_number < len(self.pages):
            self.pages[page_number].frame_number = frame_number
            self.pages[page_number].valid = True
            print(f"Mapped Page {page_number} to Frame {frame_number}.")
        else:
            print(f"Page {page_number} is out of range.")

    def access_page(self, page_number):
        if 0 <= page_number < len(self.pages):
            page = self.pages[page_number]
            if page.valid:
                print(f"Accessing {page}")
            else:
                print(f"Page {page_number} is not valid (not loaded in memory).")
        else:
            print(f"Page {page_number} is out of range.")

    def display_table(self):
        print("Page Table:")
        for page in self.pages:
            print(page)


class MemorySimulator:
    def __init__(self, num_pages, num_frames):
        self.page_table = PageTable(num_pages)
        self.num_frames = num_frames
        self.free_frames = list(range(num_frames))  # Lista de marcos de memoria libres

    def load_page(self, page_number):
        if self.free_frames:
            frame_number = self.free_frames.pop(0)  # Asignar el primer marco libre
            self.page_table.map_page(page_number, frame_number)
        else:
            print("No free frames available to load the page.")

    def random_access(self, num_accesses):
        for _ in range(num_accesses):
            page_number = random.randint(0, len(self.page_table.pages) - 1)
            self.page_table.access_page(page_number)

    def display_memory(self):
        self.page_table.display_table()


# Ejemplo de uso
if __name__ == "__main__":
    num_pages = 10  # Número de páginas virtuales
    num_frames = 5  # Número de marcos de memoria física

    simulator = MemorySimulator(num_pages, num_frames)

    # Cargamos algunas páginas en la memoria
    for page_number in range(5):  # Cargamos las primeras 5 páginas
        simulator.load_page(page_number)

    # Mostramos la tabla de páginas
    simulator.display_memory()

    # Acceso aleatorio a páginas
    print("\nAcceso aleatorio a páginas:")
    simulator.random_access(10)  # Realizamos 10 accesos aleatorios a páginas
```
# 3.4 Administración de memoria virtual

## 1. Escribe un código que implemente el algoritmo de reemplazo de página "Least Recently Used" (LRU).
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()  # Usamos OrderedDict para mantener el orden de acceso
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1  # Página no encontrada
        else:
            # Mover la página a la posición más reciente
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Actualizar el valor y mover a la posición más reciente
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Eliminar la página menos recientemente utilizada
            self.cache.popitem(last=False)

    def display_cache(self):
        print("Current Cache State:")
        for key, value in self.cache.items():
            print(f"Page: {key}, Value: {value}")


# Ejemplo de uso
if __name__ == "__main__":
    lru_cache = LRUCache(capacity=3)

    # Simulamos el acceso a páginas
    lru_cache.put(1, "Page 1")
    lru_cache.put(2, "Page 2")
    lru_cache.put(3, "Page 3")
    lru_cache.display_cache()

    # Accedemos a algunas páginas
    print("\nAccessing Page 1:")
    print(lru_cache.get(1))  # Debería devolver "Page 1"
    lru_cache.display_cache()

    # Agregamos una nueva página, lo que debería causar que se reemplace la menos recientemente utilizada
    print("\nAdding Page 4:")
    lru_cache.put(4, "Page 4")  # Esto debería eliminar Page 2
    lru_cache.display_cache()

    # Accedemos a una página que no está en la caché
    print("\nAccessing Page 2:")
    print(lru_cache.get(2))  # Debería devolver -1, ya que Page 2 fue eliminada
```
## 2.Diseña un diagrama que represente el proceso de traducción de direcciones virtuales a físicas en un sistema con memoria virtual.

![Diagrama en blanco](https://drive.google.com/file/d/1xuyB-BUMGtnGugICWaJzNllasqxldboi/view)

[Enlace al archivo](https://drive.google.com/file/d/1xuyB-BUMGtnGugICWaJzNllasqxldboi/view)

# Integración
## 1. Analiza un sistema operativo moderno (por ejemplo, Linux o Windows) e identifica cómo administra la memoria virtual.

## Análisis de la Gestión de Memoria Virtual en un Sistema Operativo Moderno: Linux

### 1. Conceptos Básicos de Memoria Virtual en Linux
Linux, como otros sistemas operativos modernos, implementa un sistema de memoria virtual que permite abstraer la memoria física, ofreciendo a cada proceso la ilusión de que tiene acceso a una memoria continua y privada, sin importar la cantidad de memoria física disponible. La gestión de la memoria virtual en Linux se realiza de manera eficiente a través de diversas técnicas, principalmente el uso de **paginación** y **segmentación**, aunque la paginación es el método más prevalente.

### 2. Estructura de la Memoria Virtual
En Linux, la memoria virtual se divide en dos partes principales:

- **Espacio de Usuario (User Space)**: Es la memoria que los procesos de usuario pueden usar. Cada proceso tiene su propio espacio de direcciones virtuales, lo que significa que no puede acceder directamente a la memoria de otros procesos sin permisos especiales.
- **Espacio del Núcleo (Kernel Space)**: Es el área reservada para el sistema operativo y sus procesos. Es accesible solo por el núcleo del sistema operativo.

### 3. Paginación (Paging)
En Linux, la memoria virtual está gestionada principalmente a través de páginas, que son bloques de memoria de tamaño fijo (típicamente 4 KB en sistemas modernos, aunque puede variar según la arquitectura). Cada proceso tiene un conjunto de direcciones virtuales que se mapean a marcos de memoria física a través de una tabla de páginas.

- **Dirección Virtual**: Se divide en dos partes: un número de página y un desplazamiento dentro de la página.
- **Tabla de Páginas**: Es una estructura que almacena los mapeos entre las direcciones virtuales y las direcciones físicas.
- **MMU (Memory Management Unit)**: Se encarga de la traducción entre direcciones virtuales y físicas mediante la tabla de páginas.

### 4. Manejo de Fallos de Página (Page Fault)
Cuando un proceso intenta acceder a una página de memoria que no está en la RAM (es decir, que no tiene un marco de página asignado en ese momento), se produce un fallo de página. El núcleo de Linux maneja estos fallos de página realizando las siguientes acciones:

- **Interrupción de Fallo de Página**: La MMU genera una interrupción que alerta al núcleo de Linux.
- **Carga desde Disco**: Si la página no está en memoria, el núcleo buscará la página en el disco (generalmente en el espacio de intercambio o swap).
- **Reemplazo de Páginas**: Si la memoria está llena, el núcleo puede utilizar algoritmos de reemplazo de páginas (como LRU o FIFO) para cargar la nueva página, desplazando alguna página que no está en uso o que ha estado en memoria por más tiempo.

### 5. Memoria Virtual y Segmentación
Aunque Linux utiliza principalmente paginación para la gestión de la memoria, también puede usar **segmentación** en algunos casos. La segmentación divide la memoria en segmentos de tamaño variable que pueden ser utilizados para almacenar diferentes tipos de datos (por ejemplo, código, datos, pila). Sin embargo, la segmentación en Linux no es tan común como la paginación, ya que la paginación simplifica la gestión de la memoria y proporciona una mayor flexibilidad y eficiencia.

### 6. Swap (Espacio de Intercambio)
El **swap** es un área en el disco duro que Linux utiliza cuando la memoria física está llena. Si el sistema se queda sin memoria RAM, las páginas que no están en uso se trasladan al espacio de intercambio. Cuando una página es necesaria de nuevo, se transfiere desde el disco a la memoria RAM.

- **Swap File**: Un archivo de intercambio en el disco.
- **Swap Partition**: Una partición del disco dedicada exclusivamente para el intercambio.

### 7. Seguridad y Aislamiento de Procesos
Una de las características más importantes de la memoria virtual es que permite el aislamiento entre los procesos. Cada proceso tiene su propio espacio de direcciones virtuales, lo que significa que un proceso no puede leer ni escribir en la memoria de otro proceso a menos que tenga los permisos adecuados.

- **Protección de Memoria**: El sistema operativo garantiza que las direcciones virtuales sean válidas y que los procesos no puedan acceder a áreas de memoria no permitidas.
- **Modo de Usuario y Núcleo**: Los procesos en modo usuario no tienen acceso directo a la memoria del núcleo, lo que mejora la seguridad.

### 8. Optimización de la Memoria Virtual
Linux tiene mecanismos avanzados para la gestión dinámica de la memoria, como:

- **Asignación de memoria por demanda (Demand Paging)**.
- **Compresión de páginas en la memoria** para ahorrar espacio.
- **Caché de páginas**, utilizada para almacenar páginas recientemente accedidas, mejorando la eficiencia al evitar búsquedas en el disco.

### 9. Conclusión
Linux utiliza un sistema eficiente de paginación para gestionar la memoria virtual, lo que permite a los procesos acceder a una memoria virtual continua e independiente, independientemente de la cantidad de memoria física disponible. Además, las técnicas como el manejo de fallos de página, la segmentación, el uso de swap y la protección de memoria proporcionan un entorno seguro y eficiente para la ejecución de aplicaciones.

## 2. Realiza una simulación en cualquier lenguaje de programación que emule el swapping de procesos en memoria virtual.
```python
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
```
# Administración de Entrada/Salida

## 4.1 Dispositivos y Manejadores de Dispositivos

### 1. Explica la diferencia entre dispositivos de bloque y dispositivos de carácter. Da un ejemplo de cada uno.

### Diferencia entre Dispositivos de Bloque y Dispositivos de Carácter

#### 1. Dispositivos de Bloque (Block Devices)
Un **dispositivo de bloque** es un dispositivo de almacenamiento que maneja datos en bloques de tamaño fijo. Estos dispositivos permiten el acceso aleatorio a los datos, lo que significa que el sistema operativo puede leer o escribir en cualquier parte del dispositivo sin necesidad de procesar los datos de manera secuencial.

- **Características**:
  - **Acceso aleatorio**: Se puede leer o escribir en cualquier bloque del dispositivo sin depender del orden.
  - Los datos están organizados en **bloques de tamaño fijo** (por ejemplo, 512 bytes o 4 KB).
  - Son adecuados para almacenar grandes volúmenes de datos que pueden ser accedidos de manera independiente.

- **Ejemplo**:
  - **Discos Duros (HDD)** y **Discos de Estado Sólido (SSD)**: Ambos son dispositivos de almacenamiento que gestionan grandes cantidades de datos en bloques.

---

#### 2. Dispositivos de Carácter (Character Devices)
Un **dispositivo de carácter** es un dispositivo que maneja los datos de forma secuencial, es decir, los datos se leen o escriben un carácter a la vez. No permiten acceso aleatorio, y los datos se transfieren de forma continua y sin estructuras fijas de bloques.

- **Características**:
  - **Acceso secuencial**: Los datos son procesados en el mismo orden en que se leen o escriben.
  - Los dispositivos de carácter son típicamente más simples en su operación.
  - Suelen ser dispositivos que interactúan con usuarios o periféricos que requieren flujo de datos continuo.

- **Ejemplo**:
  - **Teclados**, **Ratones**, **Puertos Serie (como RS-232)** y **Dispositivos de Audio**: Estos dispositivos manejan datos de forma secuencial y no tienen la capacidad de acceder a bloques de datos de manera aleatoria.

  ### 2. Diseña un programa que implemente un manejador de dispositivos sencillo para un dispositivo virtual de entrada. 
```java

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
```
# 4.2 Mecanismos y Funciones de los Manejadores de Dispositivos

## 1. ¿Qué es la Interrupción por E/S?

### Concepto
La **interrupción por E/S (Entrada/Salida)** es un mecanismo utilizado por el sistema operativo para manejar las operaciones de entrada y salida de forma eficiente. Las interrupciones permiten que el sistema operativo interrumpa la ejecución normal de un proceso en curso para atender una solicitud de E/S, como leer desde un dispositivo de almacenamiento o escribir en una pantalla.

---

### Cómo la Administra el Sistema Operativo

1. **Generación de la Interrupción**:
   - Un dispositivo de E/S, como un disco o un teclado, genera una interrupción para notificar al sistema operativo que un evento relevante ha ocurrido (por ejemplo, la finalización de una operación de lectura o escritura).

2. **Interrupción del Proceso Actual**:
   - El procesador detiene momentáneamente la ejecución del proceso en curso, guardando su estado (contexto de interrupción), incluyendo el contador de programa (PC) y los registros de la CPU.

3. **Manejo de la Interrupción**:
   - El sistema operativo utiliza un controlador de interrupciones (Interrupt Handler o ISR) para gestionar la interrupción.
   - Este controlador identifica el tipo de interrupción y transfiere el control a la rutina correspondiente.

4. **Restauración del Contexto**:
   - Tras procesar la interrupción, el sistema operativo restaura el estado del proceso interrumpido (contexto de recuperación) y reanuda su ejecución.

---

### Ejemplo de Interrupción por E/S en Pseudocódigo

```plaintext
// Pseudocódigo para manejar interrupciones por E/S

// Simula el controlador de interrupciones
función controlador_de_interrupciones(interrupción):
    si interrupción.tipo == "E/S" entonces
        // Procesar la interrupción de E/S
        imprimir("Procesando solicitud de E/S")
        dispositivo = obtener_dispositivo(interrupción)

        si dispositivo.está_listo_para_operación entonces
            realizar_operación_E/S(dispositivo)
            actualizar_estado_del_dispositivo(dispositivo)
        sino
            imprimir("El dispositivo no está listo para E/S")
        fin si
    fin si
fin función

// Función que simula un proceso que requiere E/S
función proceso_con_requisito_de_E/S():
    imprimir("Iniciando proceso que requiere E/S")
    generar_interrupción("E/S")  // Genera una interrupción por E/S
fin función

// Función que simula una solicitud de E/S
función generar_interrupción(tipo):
    interrupción = crear_interrupción(tipo)
    controlador_de_interrupciones(interrupción)
fin función

// Simulación de la operación de E/S
función realizar_operación_E/S(dispositivo):
    imprimir("Realizando operación de E/S en el dispositivo...")
    // Simula la lectura o escritura en el dispositivo
fin función

// Ejemplo de ejecución
proceso_con_requisito_de_E/S()
```
### Descripción del Pseudocódigo

1. **Controlador de Interrupciones**:
   - El controlador de interrupciones detecta cuando se produce una interrupción de E/S.
   - Si es una interrupción de E/S, el sistema operativo verifica si el dispositivo está listo para operar y ejecuta la operación de E/S (por ejemplo, leer o escribir datos en un dispositivo).

2. **Generación de Interrupción**:
   - Un proceso que necesita realizar una operación de E/S genera una interrupción, lo que simula la solicitud de datos al dispositivo de E/S.

3. **Realización de la Operación de E/S**:
   - Una vez que la interrupción es manejada, el controlador de interrupciones ejecuta la operación de E/S correspondiente.

4. **Flujo**:
   - Un proceso genera una interrupción por E/S, y el sistema operativo gestiona la interrupción, realizando la operación solicitada por el dispositivo.

Este ejemplo ilustra el flujo básico de una **interrupción por E/S** en un sistema operativo, mostrando cómo se interrumpe la ejecución del proceso actual, se maneja la solicitud de E/S, y luego se reanuda el proceso.

### 2. Escribe un programa que utilice el manejo de interrupciones en un sistema básico de simulación. 
```python
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
```
# 4.3 Estructuras de datos para manejo de dispositivos

## 1. Investiga y explica qué es una cola de E/S. Diseña una simulación de una cola con prioridad.

### ¿Qué es una Cola de E/S?
Una **cola de E/S** es una estructura de datos que organiza y gestiona las solicitudes de entrada/salida de dispositivos en un sistema operativo. Estas solicitudes pueden provenir de procesos que necesitan interactuar con dispositivos como discos, impresoras o teclados. 

#### Características de una Cola de E/S con Prioridad
- **Prioridades asignadas**: Cada solicitud tiene una prioridad asociada que determina su orden de procesamiento.
- **Procesamiento según prioridad**: Las solicitudes con mayor prioridad se procesan antes, independientemente del orden de llegada.
- **Adaptable a necesidades críticas**: Es ideal para manejar solicitudes donde ciertas operaciones tienen mayor urgencia.

---

### Pseudocódigo para Simular una Cola de E/S con Prioridad

```pseudocode
// Estructura de la solicitud de E/S
estructura SolicitudDeES:
    entero id_solicitud
    entero prioridad
    cadena dispositivo
    cadena operacion

// Cola de E/S (con prioridad)
cola = []

// Función para agregar una solicitud a la cola con prioridad
función agregar_solicitud(prioridad, dispositivo, operacion):
    solicitud = crear_solicitud(prioridad, dispositivo, operacion)
    insertar_en_orden(solicitud, cola)
fin función
// Función para crear una nueva solicitud
función crear_solicitud(prioridad, dispositivo, operacion):
    solicitud = nueva SolicitudDeES()
    solicitud.id_solicitud = generar_id_solicitud()
    solicitud.prioridad = prioridad
    solicitud.dispositivo = dispositivo
    solicitud.operacion = operacion
    devolver solicitud
fin función

// Función para insertar una solicitud en la cola según su prioridad
función insertar_en_orden(solicitud, cola):
    si cola está vacía entonces
        agregar solicitud al final de la cola
    sino
        para i desde 0 hasta tamaño(cola) hacer
            si solicitud.prioridad < cola[i].prioridad entonces
                insertar solicitud en posición i
                salir del bucle
            fin si
        fin para
    fin si
fin función

// Función para procesar una solicitud
función procesar_solicitud():
    si cola no está vacía entonces
        solicitud = quitar_primera_solicitud(cola)
        imprimir("Procesando solicitud:", solicitud.id_solicitud, "Operación:", solicitud.operacion, "Dispositivo:", solicitud.dispositivo)
    sino
    imprimir("No hay solicitudes pendientes")
    fin si
fin función

// Función para quitar la primera solicitud de la cola
función quitar_primera_solicitud(cola):
    devolver cola[0]  // Devuelve la primera solicitud
    eliminar cola[0]  // Elimina la solicitud de la cola
fin función

// Ejemplo de ejecución
agregar_solicitud(1, "Disco", "Lectura")    // Prioridad 1 (alta)
agregar_solicitud(3, "Red", "Escritura")    // Prioridad 3 (baja)
agregar_solicitud(2, "Teclado", "Lectura")  // Prioridad 2
procesar_solicitud()  // Procesará la solicitud del disco (prioridad 1)
procesar_solicitud()  // Procesará la solicitud del teclado (prioridad 2)
procesar_solicitud()  // Procesará la solicitud de la red (prioridad 3)
```
## Explicación del Pseudocódigo

1. **Estructura `SolicitudDeES`**:  
   Define una solicitud de E/S, que incluye:  
   - Un identificador único.  
   - La prioridad de la solicitud.  
   - El dispositivo de E/S.  
   - La operación que se desea realizar.

2. **Cola**:  
   Es una lista que almacena las solicitudes de E/S. Las solicitudes no se agregan directamente al final de la cola; en su lugar, se insertan en la posición correspondiente según su prioridad.

3. **Función `agregar_solicitud`**:  
   Agrega una nueva solicitud a la cola, asegurando que se inserte en la posición adecuada basada en la prioridad de la solicitud.

4. **Función `insertar_en_orden`**:  
   Organiza las solicitudes en la cola para que estén ordenadas por prioridad, colocando las de mayor prioridad al frente.

5. **Función `procesar_solicitud`**:  
   Procesa la primera solicitud en la cola, que es la de mayor prioridad. Si no hay solicitudes pendientes, informa que la cola está vacía.

6. **Ejemplo de ejecución**:  
   - Se agregan tres solicitudes con prioridades 1, 2 y 3.  
   - Las solicitudes se procesan en el orden de sus prioridades: primero la de prioridad 1, luego la de prioridad 2, y finalmente la de prioridad 3.

---

## Conclusión
Este pseudocódigo simula una **cola de E/S con prioridad**, en la que las solicitudes no se procesan según el orden de llegada, sino en función de su prioridad asignada.  
- Las solicitudes con mayor prioridad son atendidas primero, lo que permite manejar operaciones críticas o urgentes de manera más eficiente.  
- Esta técnica es común en sistemas operativos para optimizar la gestión de dispositivos de entrada/salida, mejorando la eficiencia y control en sistemas complejos.
## 2. Escribe un programa que simule las operaciones de un manejador de dispositivos utilizando una tabla de estructuras.
```python
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
```
# 4.4 Operaciones de Entrada/Salida

## 1. Diseña un flujo que describa el proceso de lectura de un archivo desde un disco magnético. Acompáñalo con un programa básico que simule el proceso.

## Flujo del Proceso de Lectura de un Archivo
1. **Inicio**: Comienza el proceso de lectura.
2. **Seleccionar Archivo**: El usuario selecciona el archivo que desea leer.
3. **Verificar Existencia del Archivo**:  
   - Comprobar si el archivo existe en el disco.  
   - Si el archivo no existe, mostrar un mensaje de error y finalizar.
4. **Abrir Archivo**: Abrir el archivo en modo lectura.
5. **Leer Contenido**: Leer el contenido del archivo.
6. **Mostrar Contenido**: Mostrar el contenido leído al usuario.
7. **Cerrar Archivo**: Cerrar el archivo.
8. **Fin**: Terminar el proceso.

---

## Programa en Python que Simula el Proceso

```python
import os

def read_file(file_path):
    # Paso 3: Verificar existencia del archivo
    if not os.path.exists(file_path):
        print("Error: El archivo no existe.")
        return

    # Paso 4: Abrir archivo
    try:
        with open(file_path, 'r') as file:
            # Paso 5: Leer contenido
            content = file.read()
            # Paso 6: Mostrar contenido
            print("Contenido del archivo:")
            print(content)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

# Clase principal para ejecutar el programa
if __name__ == "__main__":
    # Paso 2: Seleccionar archivo
    file_name = input("Introduce el nombre del archivo a leer (incluye la ruta si es necesario): ")
    
    # Paso 1: Inicio
    print("Iniciando el proceso de lectura del archivo...")
    
    # Llamar a la función para leer el archivo
    read_file(file_name)
    
    # Paso 8: Fin
    print("Proceso de lectura finalizado.")
```
## 2. Implementa un programa en Python, C o java que realice operaciones de entrada/salidas asíncronas usando archivos. 
```python
import asyncio
import aiofiles

async def write_to_file(file_path, content):
    """Función asíncrona para escribir contenido en un archivo."""
    async with aiofiles.open(file_path, 'w') as file:
        await file.write(content)
        print(f"Escrito en {file_path}: {content}")

async def read_from_file(file_path):
    """Función asíncrona para leer contenido de un archivo."""
    async with aiofiles.open(file_path, 'r') as file:
        content = await file.read()
        print(f"Leído de {file_path}: {content}")

async def main():
    file_path = 'example.txt'
    
    # Contenido a escribir en el archivo
    content_to_write = "Hola, este es un contenido de ejemplo.\n"
    
    # Llamar a las funciones de escritura y lectura de manera asíncrona
    await write_to_file(file_path, content_to_write)
    await read_from_file(file_path)

# Ejecutar el programa
if __name__ == "__main__":
    asyncio.run(main())
```
# Integración

## 1. Escribe un programa que implemente el algoritmo de planificación de discos "Elevator (SCAN)".

```python
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
```
## 2. Diseña un sistema que maneje múltiples dispositivos simulados (disco duro, impresora, teclado) y muestra cómo se realiza la comunicación entre ellos.

```python
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

```

# Avanzados
# Optimización de las Operaciones de Entrada/Salida mediante Memoria Caché en Sistemas Operativos Modernos

Los sistemas operativos modernos optimizan las operaciones de entrada/salida (E/S) utilizando memoria caché para mejorar la eficiencia de las transferencias de datos entre el sistema y los dispositivos de E/S (como discos duros, SSDs, redes, etc.). El uso de memoria caché en las operaciones de E/S permite reducir los tiempos de acceso y mejorar el rendimiento general del sistema.

---

## ¿Qué es la Memoria Caché?

La memoria caché es una forma de memoria de acceso rápido que almacena datos temporales o recientemente accedidos. En el contexto de las operaciones de E/S, la caché almacena bloques de datos leídos de dispositivos de almacenamiento o escritos en ellos, para evitar que el sistema tenga que acceder repetidamente a los dispositivos de E/S, los cuales suelen ser mucho más lentos que la memoria principal.

---

## Cómo los Sistemas Operativos Utilizan la Memoria Caché para Optimizar las Operaciones de E/S

### 1. Caché de Disco (Disk Caching)
- **Lectura de Caché**: Cuando un programa solicita datos que están en el disco, el sistema operativo primero verifica si esos datos ya están en la caché. Si los datos están en caché, se pueden entregar inmediatamente, sin necesidad de realizar una operación de E/S en el disco.
- **Escritura de Caché**: Los datos se escriben primero en la caché y luego en el disco en un proceso denominado *escritura diferida* (*write-back*).

### 2. Caché de Páginas (Page Cache)
- **Optimización de Archivos**: Almacena páginas de memoria leídas/escritas del disco. Si un proceso solicita una página almacenada, la operación es más rápida.
- **Gestión de Memoria Virtual**: Facilita el manejo de la memoria paginada y el espacio de intercambio (*swap space*).

### 3. Caché de Entrada/Salida en el Controlador de Disco
- **Interfaz Directa con la Caché**: Los controladores de disco incluyen una caché integrada que reduce la latencia al almacenar datos recientemente utilizados.

### 4. Caché de Red (Network Caching)
- **Reducción de Latencia**: Almacena datos solicitados recientemente de la red para minimizar accesos remotos y mejorar el rendimiento en aplicaciones distribuidas.

---

## Beneficios de Usar Memoria Caché en las Operaciones de E/S

1. **Reducción de la Latencia**: Minimiza accesos a discos y dispositivos de E/S lentos.
2. **Mejor Uso de Recursos**: Disminuye la carga en dispositivos y optimiza el uso de la CPU.
3. **Escritura Diferida**: Permite almacenar temporalmente datos en caché mientras las escrituras se realizan en segundo plano.
4. **Rendimiento General Mejorado**: Asegura que los datos más utilizados estén disponibles para acceso rápido.

---

## Ejemplo: Flujo de Operación con Caché en un Sistema de E/S

1. Un proceso solicita datos de un archivo almacenado en un disco.
2. El sistema operativo consulta la caché de disco para verificar si los datos están en la memoria RAM.
3. Si los datos están en la caché, se devuelven al proceso sin necesidad de acceder al disco.
4. Si no están en la caché, se realiza una lectura desde el disco, se almacena en la caché y se entrega al proceso.
5. Para escrituras, los datos se almacenan en la caché y se escriben al disco posteriormente mediante *escritura diferida*.

---

## Conclusión

La utilización de memoria caché en los sistemas operativos modernos es clave para optimizar las operaciones de entrada/salida. Al almacenar datos en memoria de acceso rápido, los sistemas operativos pueden minimizar el acceso a dispositivos de E/S más lentos, como discos y redes. Esto resulta en una mejora significativa en el rendimiento del sistema y en la eficiencia general de las operaciones de E/S.

# Actividades: Dispositivos de entrada y salida en Linux

## Introducción
En este ejercicio, aprenderá a **listar**, **verificar** y **analizar** los dispositivos de entrada y salida en Linux. Usarán comandos básicos y herramientas comunes disponibles en cualquier distribución.

---

## Actividad 1: Listar dispositivos conectados

### Objetivo
Conocer los dispositivos de entrada y salida conectados al sistema.

### Instrucciones
1. Abra una **terminal** en su entorno Linux.
2. Ejecute los siguientes comandos y anote sus observaciones:

   - `lsblk`: Enumera los dispositivos de bloque.
   - `lsusb`: Lista los dispositivos conectados a los puertos USB.
   - `lspci`: Muestra los dispositivos conectados al bus PCI.
   - `dmesg | grep usb`: Muestra los mensajes del kernel relacionados con dispositivos USB.

---

### Conteste:
1. **¿Qué tipos de dispositivos se muestran en la salida de `lsblk`?**

2. **¿Cuál es la diferencia entre `lsusb` y `lspci`?**

3. **¿Qué información adicional proporciona `dmesg | grep usb`?**
---
## 1. `lsblk`
Este comando se utiliza para **listar todos los dispositivos de bloque** en el sistema, como discos duros, particiones y dispositivos de almacenamiento extraíbles. La salida típicamente incluye columnas que muestran el **nombre del dispositivo**, su **tamaño**, **tipo**, y **punto de montaje**.

**Observaciones:**

- **Tipos de dispositivos**: Podrías ver dispositivos como `sda`, `sda1`, `sdb`, etc., donde:
  - `sda` representa un disco duro.
  - `sda1` representa una partición de ese disco.
  - También podrías ver dispositivos como `sr0` (unidad de CD/DVD) o dispositivos de almacenamiento USB.

- **Estructura**: La salida puede mostrar una **jerarquía** de dispositivos, indicando qué particiones pertenecen a qué discos.

---

## 2. `lsusb`
Este comando lista **todos los dispositivos conectados a los puertos USB** del sistema. La salida incluye información sobre el **fabricante**, el **ID del dispositivo** y el **tipo de dispositivo**.

### Diferencia entre `lsusb` y `lspci`:
- **`lsusb`**: Se centra en los **dispositivos conectados a los puertos USB**.  
  Ejemplos: teclados, ratones, impresoras, unidades de almacenamiento USB.
- **`lspci`**: Muestra información sobre los **dispositivos conectados al bus PCI**.  
  Ejemplos: tarjetas gráficas, tarjetas de red, controladores de almacenamiento. Es más relevante para el **hardware interno** del sistema.

---

## 3. `dmesg | grep usb`
Este comando filtra los **mensajes del kernel** para mostrar únicamente aquellos relacionados con **dispositivos USB**.  
El comando `dmesg` muestra los mensajes del buffer del kernel, que incluyen información sobre el **arranque del sistema** y la **detección de hardware**.

**Información adicional proporcionada:**
- **Mensajes de conexión/desconexión**: Podrías ver mensajes que indican cuándo se conectó o desconectó un dispositivo USB.
- **Errores**: Si hay problemas con un dispositivo USB, como fallos de conexión o errores de lectura/escritura, estos mensajes pueden proporcionar pistas sobre lo que está sucediendo.
- **Detalles del dispositivo**: Información sobre la **identificación del dispositivo**, **controladores cargados** y otros **detalles técnicos** útiles para la resolución de problemas.

---

## Resumen
Estos comandos son **herramientas poderosas** para diagnosticar y entender el **hardware conectado** a un sistema Linux.  
Permiten obtener información sobre:
- **Dispositivos de almacenamiento** (`lsblk`)
- **Periféricos USB** (`lsusb`)
- **Componentes internos** (`lspci`)
- **Mensajes del kernel** relacionados con USB (`dmesg | grep usb`)
---
## Actividad 2: Verificar dispositivos de almacenamiento

### Objetivo
Aprender cómo identificar **discos duros**, **particiones** y su **configuración**.

---

### Instrucciones
1. Use el comando **`fdisk -l`** para **listar todos los discos y particiones**.
2. Utilice **`blkid`** para ver los **identificadores UUID** y los **tipos de sistema de archivos**.
3. Use **`df -h`** para **listar los dispositivos montados** y su **espacio disponible**.

---

### Conteste:
1. **¿Qué dispositivos de almacenamiento están conectados a su sistema?**

2. **¿Qué particiones están montadas actualmente?**

3. **¿Qué tipo de sistemas de archivos se usan en las particiones?**
---
## 1. `fdisk -l`
Este comando se utiliza para **listar todos los discos y sus particiones** en el sistema. Proporciona información detallada sobre cada disco, incluyendo el **tamaño**, el **tipo de particiones** y el **sistema de particiones** utilizado.

**Observaciones:**
- **Dispositivos de almacenamiento**: La salida mostrará todos los discos conectados, como `/dev/sda`, `/dev/sdb`, etc., junto con sus particiones (por ejemplo, `/dev/sda1`, `/dev/sda2`).
- **Tamaño y tipo de particiones**: También verás el **tamaño** de cada partición y el tipo de sistema de particiones (por ejemplo, **MBR** o **GPT**).

---

## 2. `blkid`
Este comando muestra información sobre los **dispositivos de bloque**, incluyendo sus **identificadores UUID** y el **tipo de sistema de archivos**.

**Observaciones:**
- **UUID**: Cada partición tendrá un **identificador único** (UUID) que se puede usar para montarla de manera confiable.
- **Tipos de sistema de archivos**: La salida incluirá el tipo de sistema de archivos para cada partición, como **ext4**, **xfs**, **ntfs**, etc.

---

## 3. `df -h`
Este comando lista los **sistemas de archivos montados** y muestra información sobre el **espacio utilizado** y **disponible** en cada uno de ellos. La opción `-h` hace que la salida sea **más legible**, mostrando tamaños en formato humano (por ejemplo, **GB**, **MB**).

**Observaciones:**
- **Particiones montadas**: La salida mostrará qué **particiones** están actualmente **montadas**, junto con sus **puntos de montaje** (por ejemplo, `/`, `/home`, etc.).
- **Espacio disponible**: También verás el **espacio total**, el **espacio utilizado** y el **espacio disponible** en cada partición montada.

---

## Respuestas a las preguntas

1. **¿Qué dispositivos de almacenamiento están conectados a su sistema?**  
   Al ejecutar `fdisk -l`, deberías ver una lista de dispositivos como **`/dev/sda`**, **`/dev/sdb`**, etc., junto con sus particiones.  
   Por ejemplo, podrías tener un **disco duro principal** (`/dev/sda`) y un **disco adicional** (`/dev/sdb`).

2. **¿Qué particiones están montadas actualmente?**  
   Al ejecutar `df -h`, podrás ver las **particiones montadas** actualmente, junto con sus **puntos de montaje**.  
   Por ejemplo, podrías ver **`/dev/sda1`** montada en **`/`** (raíz) y **`/dev/sda2`** montada en **`/home`**.

3. **¿Qué tipo de sistemas de archivos se usan en las particiones?**  
   Al ejecutar `blkid`, podrás identificar el **tipo de sistema de archivos** para cada partición.  
   Por ejemplo, podrías ver que **`/dev/sda1`** tiene un sistema de archivos **ext4** y **`/dev/sda2`** tiene un sistema de archivos **xfs**.

---

## Resumen
Estos comandos son **esenciales** para la administración de **discos y particiones** en Linux.  
Te permiten:
- Identificar los **dispositivos de almacenamiento**.
- Ver qué **particiones** están montadas.
- Conocer los **tipos de sistemas de archivos** que se utilizan.

Estas herramientas son fundamentales para **diagnosticar**, **configurar** y **gestionar** dispositivos de almacenamiento en un sistema Linux.
---
## Actividad 3: Explorar dispositivos de entrada

### Objetivo
Identificar dispositivos como **teclados**, **ratones** y **cámaras**.

---

### Instrucciones
1. Ejecute **`cat /proc/bus/input/devices`** para **listar los dispositivos de entrada**.
2. Use **`evtest`** para **monitorear eventos** de dispositivos de entrada (requiere permisos de superusuario).
3. Investigue los siguientes dispositivos:
   - **Teclado**
   - **Mouse**
   - **Controladores USB adicionales**

---

### Conteste:
1. **¿Qué eventos genera cada dispositivo al interactuar con ellos?**

2. **¿Cómo se identifican los dispositivos en `/proc/bus/input/devices`?**
---
## 1. `cat /proc/bus/input/devices`
Este comando muestra una lista de todos los **dispositivos de entrada** conectados al sistema, como **teclados**, **ratones** y otros periféricos. La información se encuentra en el archivo virtual **`/proc/bus/input/devices`**.

**Observaciones:**
- **Identificación de dispositivos**: Cada dispositivo listado tendrá información como:
  - El **nombre del dispositivo**.
  - Su **tipo** (teclado, ratón, etc.).
  - Su **ID de evento** (por ejemplo, `event0`, `event1`, etc.).
- **Detalles adicionales**: También se puede ver información sobre las **capacidades** del dispositivo, como si genera eventos de teclas, movimiento, etc.

---

## 2. `evtest`
Este comando se utiliza para **monitorear eventos** de dispositivos de entrada en **tiempo real**. Necesitarás **permisos de superusuario** para ejecutarlo.  
Al ejecutar `evtest`, podrás **seleccionar un dispositivo** y ver los eventos que genera al interactuar con él.

**Observaciones:**
- **Eventos generados**:  
   Al interactuar con un dispositivo (por ejemplo, presionar una tecla o mover el ratón), `evtest` mostrará:
   - El **tipo de evento** (por ejemplo, `EV_KEY` para teclas, `EV_REL` para movimiento del ratón).
   - El **código del evento** y su **estado** (presionado, liberado, etc.).

---

## Investigación de dispositivos

### **Teclado**
- **Eventos generados**:  
   Cuando presionas una tecla, se genera un evento de tipo **`EV_KEY`**. La salida de `evtest` mostrará:
   - El **código de la tecla** presionada.
   - El **estado**: **presionado** o **liberado**.
- **Identificación en `/proc/bus/input/devices`**:  
   El teclado se identifica por:
   - Su **nombre** (por ejemplo, *"ATML1000:00"*).
   - Su **ID de evento** (por ejemplo, `event0`).

---

### **Mouse**
- **Eventos generados**:  
   Al mover el ratón o hacer clic:
   - Se generan eventos **`EV_REL`** (para movimiento relativo).
   - También se generan eventos **`EV_KEY`** para los clics de los botones.
- **Identificación en `/proc/bus/input/devices`**:  
   El ratón se identifica por:
   - Su **nombre** (por ejemplo, *"Logitech USB Optical Mouse"*).
   - Su **ID de evento** (por ejemplo, `event1`).

---

### **Controladores USB adicionales**
- **Eventos generados**:  
   Dependiendo del tipo de dispositivo USB (como un joystick o gamepad), los eventos pueden incluir:
   - **`EV_KEY`** para botones.
   - **`EV_ABS`** para ejes de movimiento.
- **Identificación en `/proc/bus/input/devices`**:  
   Los dispositivos USB adicionales se identificarán de manera similar:
   - Por su **nombre**.
   - Su **ID de evento único** (por ejemplo, `event2`).

---

## Respuestas a las preguntas

1. **¿Qué eventos genera cada dispositivo al interactuar con ellos?**
   - **Teclado**: Genera eventos **`EV_KEY`** al presionar y soltar teclas.
   - **Mouse**: Genera eventos **`EV_REL`** para movimiento y **`EV_KEY`** para clics.
   - **Controladores USB adicionales**: Generan eventos como **`EV_KEY`** (botones) y **`EV_ABS`** (movimiento de ejes).

2. **¿Cómo se identifican los dispositivos en `/proc/bus/input/devices`?**
   - Los dispositivos se identifican por:
     - Su **nombre**.
     - El **tipo** de dispositivo.
     - Su **ID de evento** único (por ejemplo, `event0`, `event1`, etc.).
   - También se muestra información sobre las **capacidades** del dispositivo (teclas, movimiento, etc.).

---

## Resumen
Estos comandos son útiles para **explorar** y **monitorear** los dispositivos de entrada en un sistema Linux.  
Te permiten:
- Identificar los dispositivos conectados.
- Observar los **eventos** que generan al interactuar con ellos.
- Analizar las **capacidades** de cada dispositivo.

Estas herramientas son esenciales para diagnosticar problemas de hardware o verificar el funcionamiento de dispositivos periféricos.
---
## Actividad 4: Examinar dispositivos de salida

### **Objetivo**
Entender cómo identificar dispositivos de salida como **monitores** y **tarjetas de sonido**.

---

### **Instrucciones**

1. **`xrandr`**  
   Este comando se utiliza para **listar las pantallas conectadas** y sus **resoluciones**.

2. **`aplay -l`**  
   Este comando muestra una lista de las **tarjetas de sonido disponibles** en el sistema.

3. **`lsof /dev/snd/*`**  
   Este comando muestra qué **procesos están utilizando** la tarjeta de sonido.  
   La herramienta `lsof` lista archivos abiertos y dispositivos en uso.

---

## **Respuestas**

### **1. ¿Qué salidas de video están disponibles en su sistema?**
- Al ejecutar `xrandr`, obtendrás una lista de las **salidas de video** conectadas, como:
  - **HDMI-1**, **HDMI-2**: Salidas HDMI.
  - **DP-1**, **DP-2**: Salidas DisplayPort.
  - **eDP-1**: Pantalla integrada (típica en laptops).
- También muestra la **resolución actual** y las resoluciones disponibles para cada salida.

---

### **2. ¿Qué dispositivos de sonido se detectaron?**
- Al ejecutar `aplay -l`, se listarán las **tarjetas de sonido** y los **dispositivos de salida de audio** detectados.
  - Ejemplo de salida:
    ```
    **** List of PLAYBACK Hardware Devices ****
    card 0: PCH [HDA Intel PCH], device 0: ALC3234 Analog [ALC3234 Analog]
      Subdevices: 1/1
      Subdevice #0: subdevice #0
    ```
- La salida indica:
  - **Card 0**: Identificador de la tarjeta de sonido.
  - **Device 0**: Número del dispositivo.
  - **Nombre del controlador** (por ejemplo, `ALC3234 Analog`).

---

### **3. ¿Qué procesos están usando la tarjeta de sonido?**
- Al ejecutar `lsof /dev/snd/*`, se listarán los **procesos activos** que están utilizando la tarjeta de sonido.
  - Ejemplo de salida:
    ```
    COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    pulseaudi 1234 user   33u  CHR 116,5      0t0  1234 /dev/snd/controlC0
    firefox   5678 user   25u  CHR 116,5      0t0  1234 /dev/snd/pcmC0D0p
    ```
- La salida indica:
  - **COMMAND**: El nombre del proceso (por ejemplo, `pulseaudio` o `firefox`).
  - **PID**: El ID del proceso.
  - **NAME**: El dispositivo de sonido en uso (por ejemplo, `/dev/snd/controlC0`).

---

## **Resumen**
Estos comandos te permiten analizar los **dispositivos de salida** en un sistema Linux:
1. **`xrandr`** para pantallas conectadas y sus resoluciones.
2. **`aplay -l`** para tarjetas de sonido disponibles.
3. **`lsof /dev/snd/*`** para identificar los procesos que están utilizando la tarjeta de sonido.

Con esta información, puedes diagnosticar problemas de video y audio, verificar dispositivos conectados y analizar el uso de recursos por parte de los procesos.

## Actividad 5: Crear un script de resumen

---

### **Objetivo**
Automatizar la recopilación de información de dispositivos de **entrada** y **salida**.

---

### **Instrucciones**

1. Cree un archivo llamado **`dispositivos.sh`** y agregue el siguiente contenido:

   ```bash
   #!/bin/bash

   echo "Dispositivos de bloque:"
   lsblk

   echo "Dispositivos USB:"
   lsusb

   echo "Dispositivos PCI:"
   lspci

   echo "Dispositivos de entrada:"
   cat /proc/bus/input/devices

   echo "Salidas de video:"
   xrandr

   echo "Tarjetas de sonido:"
   aplay -l

2. Ejecute el script usando el siguiente comando:

   ```bash
   bash dispositivos.sh
3. Modifique el script para guardar la salida en un archivo llamado resumendispositivos.txt. Aquí está la versión modificada:

   ```bash
   #!/bin/bash
   echo "Dispositivos de bloque:" > resumendispositivos.txt
   lsblk >> resumendispositivos.txt
   echo -e "\nDispositivos USB:" >> resumendispositivos.txt
   lsusb >> resumendispositivos.txt
   echo -e "\nDispositivos PCI:" >> resumendispositivos.txt
   lspci >> resumendispositivos.txt
   echo -e "\nDispositivos de entrada:" >> resumendispositivos.txt
   cat /proc/bus/input/devices >> resumendispositivos.txt
   echo -e "\nSalidas de video:" >> resumendispositivos.txt
   xrandr >> resumendispositivos.txt
   echo -e "\nTarjetas de sonido:" >> resumendispositivos.txt
   aplay -l >> resumendispositivos.txt
   echo "Resumen guardado en resumendispositivos.txt"

4. Ejecute el script con:
   ```bash
   bash dispositivos.sh

### 1. ¿Qué ventajas tiene usar un script para recopilar esta información?

- **Automatización**: Ejecutar un solo comando recopila toda la información, evitando escribir comandos individuales cada vez.
- **Consistencia**: Garantiza que la misma información se recopile de forma uniforme.
- **Rapidez**: Ahorra tiempo al listar dispositivos y realizar diagnósticos rápidamente.
- **Registro**: Guardar la salida en un archivo permite revisar la información posteriormente o compartirla con otros.
- **Escalabilidad**: Puedes añadir más comandos según sea necesario sin repetir esfuerzos manuales.

### 2. ¿Qué cambios realizaría para personalizar el script?

Algunas mejoras y personalizaciones podrían incluir:

1. - **Opciones para ejecutar secciones específicas**: Permitir al usuario elegir qué información desea ver con argumentos como `-b` (bloques), `-u` (USB), etc.

```bash
if [[ $1 == "-b" ]]; then
    echo "Dispositivos de bloque:"
    lsblk
fi
```
2.  - Formato de salida más claro:
Utilizar separadores visuales (como líneas) para mejorar la legibilidad de la salida.

```bash
echo "===================="
echo "Dispositivos de bloque:"
lsblk
```
3. - Fecha y hora:
Incluir la fecha y hora en el nombre del archivo de salida para mantener un historial.
```bash
output="resumendispositivos_$(date +%F_%T).txt"
```
4. - Compresión de salida:
Comprimir el archivo de salida automáticamente si la información es extensa.
```bash
gzip $output
```
5. - Filtrado avanzado:
Agregar comandos adicionales para filtrar resultados, como mostrar solo dispositivos USB específicos o tarjetas de sonido activas.
---
# Resumen
Crear un script permite automatizar, organizar y guardar información clave sobre dispositivos de entrada y salida. Es flexible, fácil de ampliar y proporciona resultados rápidos, precisos y reutilizables.
---
# Actividad 6: Reflexión y discusión

## Objetivo
Analizar la importancia del manejo de dispositivos en sistemas Linux.

## Instrucciones
Reflexione sobre lo aprendido y discuta en equipo:
- ¿Qué comando encontró más útil y por qué?
- ¿Qué tan importante es conocer los dispositivos conectados al sistema?
- ¿Cómo podrían estos conocimientos aplicarse en la administración de sistemas?
# Reflexiones sobre los comandos

## Comando más útil:

**lsblk o fdisk -l**:  
Muchos podrían considerar que estos comandos son los más útiles, ya que proporcionan una visión clara de los dispositivos de almacenamiento y sus particiones. Conocer la estructura de los discos y particiones es esencial para la administración de datos, la instalación de sistemas operativos y la recuperación de información.  

**xrandr**:  
Para aquellos que trabajan con configuraciones de pantalla, *xrandr* es invaluable, ya que permite gestionar múltiples monitores y ajustar resoluciones de manera dinámica.  

**aplay -l**:  
Para los administradores de sistemas que manejan audio, este comando es crucial para identificar y gestionar dispositivos de sonido.

## Importancia de conocer los dispositivos conectados al sistema:

- **Diagnóstico y resolución de problemas**:  
  Conocer los dispositivos conectados permite a los administradores diagnosticar problemas de hardware y software de manera más efectiva. Por ejemplo, si un dispositivo no funciona correctamente, saber qué dispositivos están conectados y cómo se configuran puede ayudar a identificar la causa del problema.

- **Optimización del rendimiento**:  
  Entender cómo se utilizan los dispositivos puede ayudar a optimizar el rendimiento del sistema. Por ejemplo, si se sabe que un disco duro está casi lleno, se pueden tomar medidas para liberar espacio o agregar almacenamiento adicional.

- **Seguridad**:  
  Conocer los dispositivos conectados también es importante para la seguridad del sistema. Los administradores deben estar al tanto de cualquier dispositivo no autorizado que pueda estar conectado, lo que podría representar un riesgo de seguridad.

## Aplicaciones en la administración de sistemas:

- **Configuración y mantenimiento**:  
  Los conocimientos sobre dispositivos son esenciales para la configuración inicial de un sistema y su mantenimiento continuo. Esto incluye la instalación de controladores, la configuración de dispositivos de red y la gestión de dispositivos de almacenamiento.

- **Automatización de tareas**:  
  Los administradores pueden utilizar scripts que incorporen estos comandos para automatizar tareas relacionadas con la gestión de dispositivos, como la verificación de estado, la configuración de dispositivos de red o la monitorización del uso de recursos.

- **Planificación de capacidad**:  
  Conocer los dispositivos y su rendimiento permite a los administradores planificar la capacidad del sistema, asegurando que haya suficientes recursos para satisfacer las necesidades de los usuarios y las aplicaciones.

## Conclusión

El manejo de dispositivos en sistemas Linux es un aspecto crítico de la administración de sistemas. Los comandos que permiten explorar y gestionar dispositivos son herramientas esenciales para cualquier administrador de sistemas. La capacidad de diagnosticar problemas, optimizar el rendimiento y garantizar la seguridad del sistema depende en gran medida de un buen entendimiento de los dispositivos conectados.
---
# Comandos de Entrada y Salida, Discos y Archivos  

## Ejercicio 1: Montar y Desmontar Discos  
**Objetivo**: Aprender a montar y desmontar un dispositivo externo.  
Inserta una memoria USB en el sistema.  
Encuentra el dispositivo usando el comando:  

      lsblk  
o  

      fdisk -l  
Monta la memoria USB en un directorio, por ejemplo, `/mnt/usb`:  

      sudo mount /dev/sdX1 /mnt/usb  
Verifica que esté montado correctamente:  

      df -h  
Copia un archivo desde tu directorio personal al dispositivo USB:  

      cp archivo.txt /mnt/usb/  
Desmonta la memoria USB:  

      sudo umount /mnt/usb  

# Montar y Desmontar una Memoria USB en Linux  

## Paso 1: Insertar la memoria USB  
Inserta la memoria USB en uno de los puertos USB de tu computadora.  

## Paso 2: Encontrar el dispositivo  
Utiliza uno de los siguientes comandos para identificar el dispositivo USB:  

**Opción 1: lsblk**  
Este comando lista todos los dispositivos de bloque conectados al sistema.  

      lsblk  

**Opción 2: fdisk -l**  
Este comando muestra información sobre las particiones de los discos conectados.  

      sudo fdisk -l  

**Observaciones**:  
Busca una entrada que corresponda a tu memoria USB. Generalmente, será algo como `/dev/sdb1` o `/dev/sdc1`, dependiendo de cuántos dispositivos de almacenamiento tengas conectados.  

## Paso 3: Montar la memoria USB  
Crea un directorio donde montarás la memoria USB (si no existe ya):  

      sudo mkdir -p /mnt/usb  

Luego, monta la memoria USB en el directorio creado:  

      sudo mount /dev/sdX1 /mnt/usb  

**Nota**: Reemplaza `sdX1` con el identificador correcto de tu dispositivo USB (por ejemplo, `sdb1`).  

## Paso 4: Verificar que esté montado correctamente  
Utiliza el siguiente comando para verificar que la memoria USB esté montada:  

      df -h  

**Observaciones**:  
Busca una línea que muestre `/mnt/usb` y verifica que el tamaño y el uso del espacio sean correctos.  

## Paso 5: Copiar un archivo al dispositivo USB  
Copia un archivo desde tu directorio personal a la memoria USB. Por ejemplo, si tienes un archivo llamado `archivo.txt` en tu directorio personal:  

      cp ~/archivo.txt /mnt/usb/  

## Paso 6: Desmontar la memoria USB  
Una vez que hayas terminado de usar la memoria USB, es importante desmontarla correctamente para evitar la pérdida de datos:  

      sudo umount /mnt/usb  

## Resumen  
Estos pasos te permiten montar y desmontar un dispositivo externo, como una memoria USB, en un sistema Linux. Es fundamental seguir este proceso para asegurar que los datos se transfieran correctamente y que el dispositivo se desconecte de manera segura.  

# Ejercicio 2: Redirección de Entrada y Salida  

## Objetivo  
Usar redirección para guardar la salida de comandos en archivos.  

1. Lista los archivos de tu directorio actual y guarda el resultado en un archivo `listado.txt`:  
```bash
      ls -l > listado.txt  
```
2. Muestra el contenido del archivo en la terminal:  
```bash
      cat listado.txt  
```
3. Añade la fecha actual al final del archivo:  
```bash
      date >> listado.txt  
```
4. Muestra todo el contenido del archivo nuevamente:  
```bash
      cat listado.txt  
```
# Redirección de Entrada y Salida en Linux  

## Paso 1: Listar los archivos y guardar la salida en un archivo  
Utiliza el siguiente comando para listar los archivos en tu directorio actual y guardar el resultado en un archivo llamado `listado.txt`:  

      ls -l > listado.txt  

**Explicación**:  
- **ls -l**: Lista los archivos y directorios en el directorio actual en un formato detallado.  
- **>**: Redirige la salida del comando a un archivo. Si el archivo ya existe, se sobrescribirá.  
- **listado.txt**: Es el nombre del archivo donde se guardará la salida.  

## Paso 2: Mostrar el contenido del archivo en la terminal  
Para ver el contenido del archivo que acabas de crear, utiliza el siguiente comando:  

      cat listado.txt  

**Explicación**:  
- **cat**: Concatena y muestra el contenido de archivos. En este caso, mostrará el contenido de `listado.txt`.  

## Paso 3: Añadir la fecha actual al final del archivo  
Para agregar la fecha actual al final del archivo `listado.txt`, utiliza el siguiente comando:  

      date >> listado.txt  

**Explicación**:  
- **date**: Muestra la fecha y hora actuales.  
- **>>**: Redirige la salida del comando al final del archivo. A diferencia de `>`, que sobrescribe el archivo, `>>` añade la salida al final del archivo existente.  

## Paso 4: Mostrar todo el contenido del archivo nuevamente  
Para ver el contenido actualizado del archivo, que ahora incluye la lista de archivos y la fecha, utiliza el siguiente comando:  

      cat listado.txt  

## Resumen  
Estos pasos te permiten practicar la redirección de entrada y salida en un sistema Linux. Has aprendido a:  
- Listar archivos y guardar la salida en un archivo.  
- Mostrar el contenido de un archivo en la terminal.  
- Añadir información al final de un archivo existente.  

La redirección es una técnica muy útil en la administración de sistemas y en la automatización de tareas.  

# Ejercicio 3: Copiar y Mover Archivos  

## Objetivo  
Practicar copiar y mover archivos y directorios.  

1. Crea un archivo de texto llamado `archivo1.txt`:  
```bash
      echo "Este es un archivo de prueba" > archivo1.txt  
```
2. Copia este archivo a otro directorio, por ejemplo, `/tmp`:  
```bash
      cp archivo1.txt /tmp/  
```
3. Renombra el archivo copiado a `archivo2.txt` en `/tmp`:  
```bash
      mv /tmp/archivo1.txt /tmp/archivo2.txt  
```
4. Mueve el archivo `archivo2.txt` de vuelta a tu directorio actual:  
```bash
      mv /tmp/archivo2.txt .  
```
## Paso 1: Crear un archivo de texto  
Primero, vamos a crear un archivo de texto llamado `archivo1.txt` utilizando el comando `echo`:  

      echo "Este es un archivo de prueba" > archivo1.txt  

**Explicación**:  
- **echo "Este es un archivo de prueba"**: Este comando imprime el texto entre comillas.  
- **>**: Este operador redirige la salida del comando al archivo `archivo1.txt`. Si el archivo no existe, se creará; si ya existe, se sobrescribirá.  

## Paso 2: Copiar el archivo a otro directorio  
Ahora, copia el archivo `archivo1.txt` al directorio `/tmp`:  

      cp archivo1.txt /tmp/  

**Explicación**:  
- **cp**: Este comando se utiliza para copiar archivos y directorios.  
- **archivo1.txt**: Es el archivo que deseas copiar.  
- **/tmp/**: Es el destino donde se copiará el archivo.  

## Paso 3: Renombrar el archivo copiado  
Renombra el archivo copiado a `archivo2.txt` en el directorio `/tmp`:  

      mv /tmp/archivo1.txt /tmp/archivo2.txt  

**Explicación**:  
- **mv**: Este comando se utiliza para mover o renombrar archivos y directorios.  
- **/tmp/archivo1.txt**: Es la ruta del archivo que deseas renombrar.  
- **/tmp/archivo2.txt**: Es el nuevo nombre del archivo.  

## Paso 4: Mover el archivo de vuelta a tu directorio actual  
Finalmente, mueve el archivo `archivo2.txt` de vuelta a tu directorio actual:  

      mv /tmp/archivo2.txt .  

**Explicación**:  
- **.**: Este símbolo representa el directorio actual. Al usarlo como destino, estás indicando que deseas mover el archivo al directorio en el que te encuentras actualmente.  

## Resumen  
Estos pasos te permiten practicar cómo copiar y mover archivos en un sistema Linux. Has aprendido a:  
- Crear un archivo de texto.  
- Copiar un archivo a otro directorio.  
- Renombrar un archivo en un directorio.  
- Mover un archivo de un directorio a otro.  

La manipulación de archivos es una habilidad fundamental en la administración de sistemas y en el uso diario de Linux.  

# Ejercicio 4: Comprimir y Descomprimir Archivos

**Objetivo:** Aprender a trabajar con compresión de archivos.

1. Crea un directorio llamado `backup` y copia algunos archivos en él.

2. Comprime el directorio `backup` en un archivo `.tar.gz`:

   ```bash
   tar -czvf backup.tar.gz backup/
3. Borra el directorio original y extrae el contenido del archivo comprimido:
    ```bash
    tar -xzvf backup.tar.gz
## Paso 1: Crear un directorio llamado `backup`

Primero, crea un directorio llamado `backup` y copia algunos archivos en él. Puedes crear el directorio con el siguiente comando:
```bash
mkdir backup
```
Explicación:

- mkdir backup: Este comando crea un nuevo directorio llamado backup.

## Paso 2: Copiar algunos archivos al directorio backup
Para este paso, puedes copiar archivos existentes a tu nuevo directorio. Por ejemplo, si tienes un archivo llamado archivo1.txt, puedes copiarlo así:
```bash
cp archivo1.txt backup/
```
Explicación:

- cp archivo1.txt backup/: Este comando copia archivo1.txt al directorio backup.

## Paso 3: Comprimir el directorio backup en un archivo .tar.gz
Ahora, comprime el directorio backup en un archivo llamado backup.tar.gz utilizando el siguiente comando:
```bash
tar -czvf backup.tar.gz backup/
```
Explicación:

- tar: Este comando se utiliza para crear y manipular archivos tar.
- -c: Indica que deseas crear un nuevo archivo tar.
- -z: Indica que deseas comprimir el archivo utilizando gzip.
- -v: Muestra el progreso en la terminal (verbose).
- -f: Indica que el siguiente argumento es el nombre del archivo tar que se va a crear.
- backup/: Es el directorio que deseas comprimir.
## Paso 4: Borrar el directorio original
Una vez que hayas comprimido el directorio, puedes eliminar el directorio original backup:
```bash
rm -r backup
```
Explicación:

- rm -r backup: Este comando elimina el directorio backup y su contenido de forma recursiva. Ten cuidado al usar este comando, ya que eliminará permanentemente los archivos.
## Paso 5: Extraer el contenido del archivo comprimido
Finalmente, extrae el contenido del archivo comprimido backup.tar.gz utilizando el siguiente comando:
```bash
tar -xzvf backup.tar.gz
```
Explicación:

- -x: Indica que deseas extraer el contenido del archivo tar.
- -z: Indica que el archivo está comprimido con gzip.
- -v: Muestra el progreso en la terminal (verbose).
- -f: Indica que el siguiente argumento es el nombre del archivo tar que se va a extraer.
## Resumen
Estos pasos te permiten practicar cómo comprimir y descomprimir archivos en un sistema Linux. Has aprendido a:
- Crear un directorio y copiar archivos en él.
- Comprimir un directorio en un archivo .tar.gz.
- Eliminar un directorio y su contenido.
- Extraer el contenido de un archivo comprimido.

La compresión de archivos es una habilidad útil para ahorrar espacio en disco y facilitar la transferencia de archivos.






























































