import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import json
from .data_loader import load_data
from .filters import find_country, filter_by_region, filter_by_score_range


class HappinessApp:
    def __init__(self, root):
        """
        konstruktor tridy HappinessApp
        """
        self.root = root
        self.data = []
        self.filtered = []
        self.tree = None

    def ensure_loaded(self):
        if not self.data:
            try:
                self.data = load_data()
            except FileNotFoundError:
                path = filedialog.askopenfilename(title="Vyber CSV soubor s daty štěstí", filetypes=[("CSV","*.csv")])
                if not path:
                    return False
                self.data = load_data(path)
            print(f"Načteno {self.data} záznamů.")
        return True

    def show_table(self):
        if not self.ensure_loaded():
            return
        win = tk.Toplevel(self.root)
        win.title("Tabulka Indexu štěstí")
        cols = ["Country", "Regional indicator", "Happiness score", "Healthy life expectancy", "GDP per capita"]
        self.tree = ttk.Treeview(win, columns=cols, show="headings")
        print(f"Zobrazování {len(self.data)} záznamů.")
        print(f"Sloupce: {cols}")
        print(f"První záznam: {self.data[0]}")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        for row in self.data:
            values = [row.get(c, "") for c in cols]
            self.tree.insert("", "end", values=values)
        self.tree.pack(fill="both", expand=True)
        self.filtered = self.data

    def search_country(self):
        if not self.ensure_loaded():
            return
        name = simpledialog.askstring("Hledat", "Zadej název země:")
        if not name:
            return
        result = find_country(self.data, name)
        if not result:
            messagebox.showinfo("Výsledek", "Země nebyla nalezena.")
        else:
            txt = "\n".join(f"{r['Country']} — {r['Happiness score']}" for r in result)
            messagebox.showinfo("Výsledek", txt)
            self.filtered = result

    def filter_region(self):
        if not self.ensure_loaded():
            return
        region = simpledialog.askstring("Filtr", "Zadej název regionu (např. Western Europe):")
        if not region:
            return
        result = filter_by_region(self.data, region)
        if not result:
            messagebox.showinfo("Výsledek", "Žádná země v daném regionu.")
        else:
            txt = "\n".join(f"{r['Country']} — {r['Happiness score']}" for r in result)
            messagebox.showinfo("Výsledek", txt)
            self.filtered = result

    def filter_score_range(self):
        if not self.ensure_loaded():
            return
        min_val = simpledialog.askfloat("Filtr", "Minimální hodnota štěstí:", minvalue=0, maxvalue=10)
        max_val = simpledialog.askfloat("Filtr", "Maximální hodnota štěstí:", minvalue=0, maxvalue=10)
        if min_val is None or max_val is None:
            return
        result = filter_by_score_range(self.data, min_val, max_val)
        messagebox.showinfo("Výsledek", f"Nalezeno {len(result)} zemí.")
        self.filtered = result

    def export_json(self):
        if not self.filtered:
            messagebox.showinfo("Info", "Nejprve vyhledej nebo filtruj data.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.filtered, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Hotovo", f"Soubor uložen: {path}")

def attach_happiness_menu(root, menubar):
    app = HappinessApp(root)
    m = tk.Menu(menubar, tearoff=False)
    m.add_command(label="Zobrazit tabulku", command=app.show_table)
    m.add_command(label="Hledat zemi", command=app.search_country)
    m.add_command(label="Filtrovat podle regionu", command=app.filter_region)
    m.add_command(label="Filtrovat podle indexu štěstí", command=app.filter_score_range)
    m.add_separator()
    m.add_command(label="Exportovat do JSON", command=app.export_json)
    menubar.add_cascade(label="Happiness", menu=m)
    return app
