"""Modul pro filtrování dat ze souboru Indexu štěstí."""


def to_float(x):
    """
    Převede hodnotu na float, pokud je to možné, jinak vrátí None.
    Args:
        x: Hodnota k převedení.
    Returns:
        float nebo None: Převedená hodnota nebo None při chybě.
    """
    # Použití výjimky pro bezpečné převedení na float
    # Pokusit se převést x na float
    try:
        return float(x)
    # Pokud dojde k ValueError nebo TypeError, vrátit None
    except (ValueError, TypeError):
        # Některé hodnoty mohou používat čárku jako desetinnou tečku
        # Zkusit nahradit čárku tečkou a znovu převést
        try:
            # Nahradit čárku tečkou a zkusit znovu převést na float
            return float(x.replace(",", "."))
        # Pokud opět dojde k chybě, vrátit None
        except (ValueError, AttributeError):
            return None


def find_country(data, name):
    """
    Vyhledá zemi podle názvu (case-insensitive).
    Args:
        data (list): Seznam záznamů jako slovníky.
        name (str): Název země k vyhledání.
    Returns:
        list: Seznam záznamů odpovídajících názvu země.
    """
    return [r for r in data if name.lower() in r["Country"].lower()]


def filter_by_region(data, region):
    """
    Vrátí všechny země v daném regionu.
    Args:
        data (list): Seznam záznamů jako slovníky.
        region (str): Název regionu.
    Returns:
        list: Seznam záznamů v daném regionu.
    """
    return [r for r in data if r["Regional indicator"] == region]


def filter_by_score_range(data, min_score, max_score, score_key="Happiness score"):
    """
    Filtr podle hodnoty štěstí.
    Args:
        data (list): Seznam záznamů jako slovníky.
        min_score (float): Minimální hodnota skóre.
        max_score (float): Maximální hodnota skóre.
    Returns:
        list: Seznam záznamů s hodnotou skóre v zadaném rozsahu.
    """
    return [r for r in data if (v := to_float(r[score_key])) and min_score <= v <= max_score]


def filter_by_gdp(data, min, max, score_key="GDP per capita"):
    return [r for r in data if (v := to_float(r[score_key])) and min <= v <= max]