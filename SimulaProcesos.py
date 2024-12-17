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