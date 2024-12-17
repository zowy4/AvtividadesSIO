import pyodbc

# Configuración del DSN (nombre definido en el Administrador ODBC)
dsn = 'MiBaseODBC'
user = 'zowy'
password = '1234'

# Conexión a la base de datos
try:
    conexion = pyodbc.connect(f'DSN={dsn};UID={user};PWD={password}')
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar: {e}")
    exit()

# Cursor para ejecutar consultas
cursor = conexion.cursor()

# 1. Seleccionar la base de datos antes de las consultas
cursor.execute("USE nombre_de_base_de_datos;")  # Asegúrate de reemplazar 'nombre_de_base_de_datos' con tu base de datos real

# 2. Ejecutar consultas predefinidas
print("\n--- Resultados de Consultas Predefinidas ---")

# Consulta 1: Mostrar datos de una tabla
consulta1 = "SELECT * FROM tu_tabla LIMIT 5;"  # Modifica 'tu_tabla' con el nombre de tu tabla
cursor.execute(consulta1)
for fila in cursor.fetchall():
    print(fila)

# Consulta 2: Contar registros
consulta2 = "SELECT COUNT(*) AS Total FROM tu_tabla;"  # Modifica 'tu_tabla' con el nombre de tu tabla
cursor.execute(consulta2)
resultado = cursor.fetchone()
print(f"Total de registros: {resultado.Total}")

# 3. Insertar datos proporcionados por el usuario
print("\n--- Inserción de Datos ---")
try:
    # Solicitar datos al usuario
    campo1 = input("Ingresa el valor para el campo1: ")
    campo2 = input("Ingresa el valor para el campo2: ")
    # Modifica los campos y tabla según tu estructura
    insercion = f"INSERT INTO tu_tabla (campo1, campo2) VALUES (?, ?);"
    cursor.execute(insercion, (campo1, campo2))
    conexion.commit()  # Confirmar cambios
    print("Datos insertados correctamente.")
except Exception as e:
    print(f"Error al insertar datos: {e}")

# Cerrar la conexión
conexion.close()
print("\nConexión cerrada.")
