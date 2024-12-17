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