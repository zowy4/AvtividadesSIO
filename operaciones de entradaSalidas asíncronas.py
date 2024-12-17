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