import tkinter as tk
from happiness.data_loader import load_data
from happiness.filters import find_country, filter_by_region, filter_by_score_range, to_float, filter_by_gdp
from happiness.ui_menu import attach_happiness_menu

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Index stesti')
        self.root.geometry('800x600')
        self.root.resizable(False, False)
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        if attach_happiness_menu:
            attach_happiness_menu(self.root,self.menubar)

    def run(self):
        self.root.mainloop()


def main():
    try:
        csv_path = "data/world_happiness_2023.csv"
        data = load_data(csv_path, delimiter=";")

        print(f"Načteno {len(data)} záznamů.")
        print(f"První záznam: {data[0]}")

        print("\n🔹 Vyhledání země 'Czechia':")
        country = find_country(data, "Czechia")
        print(country)

        print("\n🔹 Filtrování podle regionu 'Western Europe':")
        region = filter_by_region(data, "Western Europe")
        print(f"Nalezeno {len(region)} zemí v regionu Western Europe.")

        print("\n🔹 Filtrování podle skóre (7.0 – 8.0):")
        filtered = filter_by_score_range(data, 7.0, 8.0)
        print(f"Nalezeno {len(filtered)} zemí s hodnotou štěstí v rozmezí 7.0–8.0.")

        print("\n🔹 Filtrování podle GDP na obyvatele(9.0 - 10.0):")
        gdp = filter_by_gdp(data,9.5, 10.0)
        print(f"Nalezeno {len(gdp)} zemí které mají GDP na obyvatele(9.0 - 10.0).")
    except FileNotFoundError:
        print("Chyba: Soubor nebyl nalezen.")


if __name__ == "__main__":
    App().run()
    # main()
