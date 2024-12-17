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