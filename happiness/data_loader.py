""" Modul pro načítání dat Indexu štěstí ze souboru CSV. """
# import vestavěného modulu csv pro práci se soubory CSV
import csv
# import Path z modulu pathlib pro práci s cestami k souborům
from pathlib import Path


def load_data(csv_path="world_happiness_2024.csv", delimiter=';'):
    """
    Načte data ze souboru CSV a vrátí je jako seznam slovníků.
    Args:
        csv_path (str): Cesta k CSV souboru.
    Returns:
        List[dict]: Seznam záznamů jako slovníky.
    """
    # Vytvoření objektu Path pro zadanou cestu
    path = Path(csv_path)
    # Kontrola, zda soubor existuje
    if not path.exists():
        # Pokud neexistuje, vyvolá výjimku FileNotFoundError
        raise FileNotFoundError(f"Soubor {csv_path} nebyl nalezen.")

    # Otevření souboru pro čtení s kódováním UTF-8
    with path.open(encoding="utf-8") as f:
        # Vytvoření DictReader pro čtení CSV jako slovníků
        reader = csv.DictReader(f, delimiter=delimiter)
        # Načtení všech řádků do seznamu a uložení do proměnné data
        data = [row for row in reader]
    return data
