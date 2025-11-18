# 🧩 1. Práce se soubory CSV v Pythonu

## 🎯 Cíl lekce

* Seznámit se s formátem CSV.
* Umět v Pythonu načíst tabulková data ze souboru pomocí modulu `csv`.
* Porozumět tomu, jak lze data převést do struktury **seznamu slovníků**.
* Naučit se základní kontrolu existence souboru a práci s cestami pomocí `pathlib`.

---

## 📘 Co je CSV

**CSV (Comma Separated Values)** je jednoduchý textový formát, který ukládá tabulková data oddělená znakem – obvykle čárkou (`,`) nebo středníkem (`;`).

Příklad obsahu souboru `world_happiness.csv`:

```csv
Country;Regional indicator;Happiness score
Finland;Western Europe;7.8
Czechia;Central Europe;6.9
Afghanistan;South Asia;2.4
```

Každý řádek představuje **záznam** a každá položka v řádku **hodnotu sloupce**.

---

## 🧠 Jak Python zpracovává CSV

Python má vestavěný modul **`csv`**, který umožňuje snadné čtení i zápis těchto dat.
Nejčastěji používáme třídu **`csv.DictReader`**, která čte soubor a převádí každý řádek do **slovníku** (kde klíče odpovídají názvům sloupců v prvním řádku).

---

## 🧩 Ukázkový kód: `data_loader.py`

```python
import csv
from pathlib import Path

def load_data(csv_path="world_happiness_2024.csv", delimiter=';'):
    """
    Načte data ze souboru CSV a vrátí je jako seznam slovníků.
    Args:
        csv_path (str): Cesta k CSV souboru.
        delimiter (str): Oddělovač hodnot v souboru (např. ';' nebo ',').
    Returns:
        List[dict]: Seznam záznamů jako slovníky.
    """
    path = Path(csv_path)
    
    # 1️⃣ Kontrola, zda soubor existuje
    if not path.exists():
        raise FileNotFoundError(f"Soubor {csv_path} nebyl nalezen.")

    # 2️⃣ Otevření souboru s kódováním UTF-8
    with path.open(encoding="utf-8") as f:
        # 3️⃣ Čtení souboru jako seznamu slovníků
        reader = csv.DictReader(f, delimiter=delimiter)
        data = [row for row in reader]

    return data
```

---

## 🔍 Jak kód funguje krok za krokem

| Krok | Co se děje                                                               | Příklad                                 |
| ---- | ------------------------------------------------------------------------ | --------------------------------------- |
| 1️⃣  | Pomocí `Path(csv_path)` vytvoříme objekt cesty k souboru.                | `Path("data/world_happiness_2024.csv")` |
| 2️⃣  | Ověříme, že soubor existuje (`path.exists()`), jinak vyvoláme výjimku.   | `raise FileNotFoundError(...)`          |
| 3️⃣  | Otevřeme soubor (`path.open`) a čteme ho jako CSV.                       | `csv.DictReader`                        |
| 4️⃣  | Každý řádek se uloží jako slovník (např. `{'Country': 'Finland', ...}`). | výsledkem je list slovníků              |

---

## 💡 Výsledek načtení dat

Po zavolání:

```python
from data_loader import load_data

data = load_data("world_happiness_2024.csv")
print(data[0])
```

Dostaneme například:

```python
{
    'Country': 'Finland',
    'Regional indicator': 'Western Europe',
    'Happiness score': '7.8'
}
```

---

## ⚙️ Ošetření chyb

Pokud se pokusíme načíst neexistující soubor:

```python
data = load_data("neexistuje.csv")
```

Python vypíše:

```
FileNotFoundError: Soubor neexistuje.csv nebyl nalezen.
```

➡️ Díky konstrukci `raise FileNotFoundError(...)` dostane uživatel jasnou informaci, co se stalo.

---

## 🧭 Cvičení pro studenty

1. 🔹 Načti data ze souboru `world_happiness_2024.csv` a vypiš první tři řádky.
   *(Nápověda: využij `data[:3]`)*

2. 🔹 Změň oddělovač z `';'` na `','` a sleduj, jak se změní výsledek.

3. 🔹 Vlož do funkce `print(f"Načteno {len(data)} záznamů.")` a ověř, kolik řádků se skutečně načetlo.

4. 🔹 Zkus úmyslně načíst neexistující soubor a sleduj, jak Python reaguje.

---

## 🧱 Shrnutí

| Klíčová myšlenka | Vysvětlení                                         |
| ---------------- | -------------------------------------------------- |
| `csv.DictReader` | převádí každý řádek CSV na slovník                 |
| `pathlib.Path`   | moderní způsob práce s cestami k souborům          |
| `try` / `raise`  | umožňují ošetřit chyby, když soubor chybí          |
| Výsledek         | seznam slovníků – ideální pro další zpracování dat |

---

# ⚙️ 2. Výjimky v Pythonu

*(Zpracování chyb a výjimečných situací při práci s daty)*

## 🎯 Cíl lekce

* Pochopit, co jsou **výjimky** a proč jsou důležité.
* Umět použít konstrukce `try`, `except`, `raise`.
* Naučit se ošetřit běžné chyby při čtení souborů a převodu dat.
* Vyzkoušet si psaní vlastních výjimek a testování jejich chování.

---

## 🧩 Co je výjimka

Během běhu programu může dojít k **chybě** – např. neexistuje soubor, dělení nulou, nebo špatný vstup.
Místo toho, aby program ihned spadl, Python vyvolá **výjimku** (*exception*), kterou můžeš zachytit a zpracovat.

Příklad jednoduché výjimky:

```python
x = int("abc")
```

➡️ Python odpoví:

```
ValueError: invalid literal for int() with base 10: 'abc'
```

---

## 🧠 Jak výjimky fungují

Základní struktura:

```python
try:
    # kód, který může způsobit chybu
    ...
except TypVyjimky:
    # co se má stát, když k chybě dojde
    ...
```

Rozšířená verze s více větvemi:

```python
try:
    ...
except FileNotFoundError:
    ...
except ValueError:
    ...
else:
    # spustí se, když žádná výjimka nenastala
    ...
finally:
    # spustí se vždy (např. uzavření souboru)
    ...
```

---

## 📘 Příklad 1: Výjimka při práci se souborem

Ve funkci `load_data()` z modulu `data_loader.py`:

```python
from pathlib import Path
import csv

def load_data(csv_path="world_happiness_2024.csv", delimiter=';'):
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Soubor {csv_path} nebyl nalezen.")
    
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        data = [row for row in reader]
    return data
```

🧩 Co se zde děje:

1. Ověřujeme, zda soubor **existuje**.
2. Pokud ne, vyvoláme (`raise`) výjimku `FileNotFoundError`.
3. Tím Python okamžitě ukončí běh funkce a předá informaci o chybě volajícímu kódu.

Takto vypadá ošetření na úrovni volajícího programu:

```python
try:
    data = load_data("neexistuje.csv")
except FileNotFoundError as e:
    print("Chyba:", e)
```

Výstup:

```
Chyba: Soubor neexistuje.csv nebyl nalezen.
```

---

## 📗 Příklad 2: Ošetření chyb při převodu dat

V modulu `filters.py` je funkce `to_float()`, která se snaží převést různé formáty čísel na `float`.

```python
def to_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        try:
            return float(x.replace(",", "."))
        except (ValueError, AttributeError):
            return None
```

🧩 Co se děje:

1. Pokus o převod `float(x)` – pokud se nepodaří, přejde se do `except`.
2. Pokud číslo obsahuje čárku (`"7,5"`), nahradí se tečkou a zkusí znovu.
3. Pokud i druhý pokus selže (např. `x=None` nebo `x="abc"`), vrátí `None`.

Tento příklad ukazuje **zřetězení dvou `try/except` bloků**, což je běžné při čištění dat.

---

## 🔍 Příklad 3: Vlastní ošetření výjimky při testech

Ve tvém modulu `tests.py` se využívá výjimka k zachycení chyb při načítání dat:

```python
if __name__ == "__main__":
    try:
        csv_data = load_data("happiness/world_happiness_2023.csv", delimiter=';')
        test_load_data(csv_data)
        test_find_country(csv_data)
        test_filter_by_region(csv_data)
        test_filter_by_score_range(csv_data, score_key="Happiness score")
        print("Všechny testy proběhly úspěšně.")
    except FileNotFoundError:
        print("Chyba: Soubor nebyl nalezen.")
```

Zde `try` chrání všechny testy.
Pokud selže už načtení dat, program nespadne, ale vypíše **srozumitelnou hlášku**.

---

## ⚠️ Časté chyby studentů

| Chyba                       | Co se stane            | Řešení                                      |
| --------------------------- | ---------------------- | ------------------------------------------- |
| Neexistující soubor         | `FileNotFoundError`    | Ošetři pomocí `try/except`                  |
| Prázdný řetězec při převodu | `ValueError`           | Zachytit v `except (ValueError, TypeError)` |
| `None.replace()`            | `AttributeError`       | Přidat další `except` blok                  |
| Chybí `raise`               | Funkce mlčky pokračuje | Použij `raise` k vyvolání chyby             |

---

## 🧭 Cvičení pro studenty

1. 🔹 Zkus načíst neexistující CSV soubor bez `try/except` a sleduj, jak program spadne.
2. 🔹 Ošetři stejný kód pomocí `try/except` a zobraz přívětivou zprávu.
3. 🔹 Vytvoř vlastní funkci:

   ```python
   def safe_divide(a, b):
       ...
   ```

   která ošetří dělení nulou (`ZeroDivisionError`) a vypíše upozornění.
4. 🔹 Doplň do `to_float()` tiskovou zprávu:

   ```python
   print(f"Chybná hodnota: {x}")
   ```

   a sleduj, kolikrát se objeví při zpracování datasetu.

---

## 🧱 Shrnutí

| Klíčový pojem                                  | Význam                                                                    |
| ---------------------------------------------- | ------------------------------------------------------------------------- |
| `try`                                          | blok s rizikovým kódem                                                    |
| `except`                                       | zachycení konkrétní výjimky                                               |
| `raise`                                        | vyvolání výjimky v případě chyby                                          |
| `FileNotFoundError`, `ValueError`, `TypeError` | běžné typy výjimek                                                        |
| Dobrá praxe                                    | výjimky mají uživateli **vysvětlit**, co se stalo, ne jen program ukončit |

---

Skvěle, tady je závěrečná část výukového bloku:
📘 **Kapitola 3 – Tvorba a spouštění testů v Pythonu**

---

# 🧪 3. Tvorba a spouštění testů v Pythonu

## 🎯 Cíl lekce

* Pochopit, **proč testujeme kód** a jaké chyby tím odhalíme.
* Naučit se psát **základní testovací funkce** s příkazem `assert`.
* Umět testy **spustit ručně** i pomocí nástroje `pytest`.
* Procvičit psaní jednoduchých testů pro načítání a filtrování dat.

---

## 💡 Proč testovat kód?

Testování není jen pro „profesionální vývojáře“.
Pomáhá:

* odhalit chyby hned po změně kódu,
* ověřit, že program dělá to, co má,
* zajistit, že pozdější úpravy nic nerozbijí,
* udržovat přehlednost a důvěru v kód.

---

## 🧩 Typy testování (stručně)

| Typ testu             | Co kontroluje          | Příklad                              |
| --------------------- | ---------------------- | ------------------------------------ |
| **Jednotkový (unit)** | Jednu konkrétní funkci | `test_to_float()`                    |
| **Integrační**        | Spolupráci více funkcí | `load_data()` + `filter_by_region()` |
| **Systémový**         | Celou aplikaci         | spuštění programu jako celek         |

V této kapitole se zaměříme na **jednotkové testy** – základní krok pro všechny programátory.

---

## 📘 Základní princip: `assert`

Příkaz **`assert`** říká:

> „Očekávám, že tento výraz je pravdivý. Pokud ne, program skončí chybou.“

Příklad:

```python
x = 10
assert x > 0          # OK
assert x < 0          # AssertionError
```

Když test neprojde, Python vypíše:

```
AssertionError
```

---

## 🧠 Struktura testovací funkce

Každý test má mít **popisný název** a testuje jen **jednu konkrétní věc**.

```python
def test_addition():
    result = 2 + 3
    assert result == 5
```

Tento princip využívá i tvůj soubor `tests.py`.

---

## 📗 Ukázkový testovací modul

Zjednodušená verze tvého `tests.py`:

```python
from happiness.data_loader import load_data
from happiness.filters import find_country, filter_by_region, filter_by_score_range, to_float

def test_load_data(data):
    assert isinstance(data, list)
    assert len(data) > 0
    assert "Country" in data[0]
    assert "Happiness score" in data[0]

def test_find_country(data, country_name="Czechia"):
    result = find_country(data, country_name)
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["Country"] == country_name

def test_filter_by_score_range(data, min_score=7.0, max_score=8.0, score_key="Happiness score"):
    result = filter_by_score_range(data, min_score, max_score, score_key)
    assert all(min_score <= to_float(r[score_key]) <= max_score for r in result)

if __name__ == "__main__":
    try:
        csv_data = load_data("happiness/world_happiness_2023.csv", delimiter=';')
        test_load_data(csv_data)
        test_find_country(csv_data)
        test_filter_by_score_range(csv_data)
        print("✅ Všechny testy proběhly úspěšně.")
    except FileNotFoundError:
        print("❌ Soubor nebyl nalezen.")
```

---

## 🔍 Jak test funguje krok za krokem

1. **Načte se dataset** pomocí `load_data()`.
2. Každá testovací funkce obdrží tato data jako argument.
3. Příkazy `assert` ověří, že:

   * data mají správný typ,
   * obsahují očekávané klíče,
   * filtrování funguje správně.
4. Pokud všechny testy projdou, vypíše se potvrzení.
5. Pokud některý test selže, Python vyvolá `AssertionError` a test se zastaví.

---

## ⚙️ Spouštění testů

### 🔸 Varianta 1 – ručně

Stačí spustit soubor přímo:

```bash
python tests.py
```

### 🔸 Varianta 2 – pomocí `pytest`

`pytest` je externí nástroj, který testy automaticky vyhledá a spustí.

Instalace:

```bash
pip install pytest
```

Spuštění testů:

```bash
pytest
```

Výsledek bude přehlednější:

```
collected 3 items
tests.py ...                                      [100%]
```

Tečky (`.`) znamenají úspěšné testy.

---

## 🧩 Příklad selhání testu

Zkus úmyslně změnit hodnotu v testu:

```python
assert "Region" in data[0]
```

Spuštění testu:

```
AssertionError: assert 'Region' in data[0]
```

➡️ Vidíš, jak test okamžitě upozorní, že se něco změnilo ve struktuře dat.

---

## 💡 Tipy pro praxi

| Doporučení                                    | Proč                                      |
| --------------------------------------------- | ----------------------------------------- |
| Testy ukládej do samostatné složky `tests/`   | přehlednost projektu                      |
| Každá funkce má mít svůj test                 | snadné dohledání chyby                    |
| Používej mluvící názvy: `test_nazev_funkce()` | čitelnost                                 |
| Při selhání testu přidej vysvětlení           | např. `assert x > 0, "x musí být kladné"` |

---

## 🧭 Cvičení pro studenty

1. 🔹 Vytvoř test `test_empty_search()`, který ověří, že `find_country(data, "Atlantis")` vrátí **prázdný seznam**.
2. 🔹 Přidej do `test_filter_by_region()` kontrolu, že všechny výsledky obsahují klíč `"Regional indicator"`.
3. 🔹 Vyzkoušej spustit testy pomocí `pytest` a zjisti, kolik testů bylo nalezeno.
4. 🔹 Zkus záměrně přepsat jeden klíč v CSV (např. `Country` → `Nation`) a sleduj, jak test reaguje.
5. 🔹 Napiš vlastní test, který ověří, že všechny hodnoty v `Happiness score` lze převést na `float`.
6. 🔹 Napiš vlastní funkci, která bude filtrovat země podle minimálního skóre štěstí, a vytvoř pro ni testovací funkci.

---

## 🧱 Shrnutí

| Klíčová myšlenka   | Vysvětlení                                    |
| ------------------ | --------------------------------------------- |
| `assert`           | kontroluje, že podmínka je splněna            |
| testovací funkce   | ověřuje chování konkrétní části programu      |
| `pytest`           | automaticky vyhledá a spustí všechny testy    |
| test = dokumentace | testy slouží i jako popis funkčnosti programu |

---

## 💬 Závěrečné doporučení

Dobře napsané testy jsou jako **bezpečnostní síť** – dovolují experimentovat s kódem, protože okamžitě odhalí, kdy se něco pokazí.
Při práci s daty (např. CSV soubory) pomáhají odhalit překlepy, špatné typy hodnot i chybějící klíče dřív, než chyba poškodí výsledky.

---

# 🧪 4. Jak používat pytest

## 🎯 Cíl lekce
- Seznámit se s nástrojem **pytest**, který slouží pro testování kódu v Pythonu.  
- Naučit se psát a spouštět testy pomocí `pytest`.  
- Porozumět principu **fixtures**, výpisu výsledků a typickým chybovým hláškám.  
- Vyzkoušet si prakticky napsat vlastní testovací modul.

---

## 🧩 Co je pytest

**pytest** je moderní a jednoduchý nástroj pro testování Python kódu.  
Umí automaticky vyhledávat testovací soubory, spouštět testy a zobrazovat přehledné výsledky.  
Na rozdíl od `unittest` nevyžaduje třídy ani složitou strukturu.

---

## 💻 Instalace

pytest není součástí standardní knihovny Pythonu, takže ho nainstalujeme pomocí pipu:

```bash
pip install pytest
````

Po instalaci lze testy spustit příkazem:

```bash
pytest
```

nebo zkráceně:

```bash
py -m pytest
```

---

## 📘 Jak pytest funguje

pytest automaticky najde všechny soubory a funkce, které:

* mají název začínající na `test_` (např. `test_math.py`)
* obsahují funkce začínající na `test_` (např. `def test_addition():`)

Každý `assert` uvnitř těchto funkcí je testovací tvrzení.

---

## 💡 První test s pytestem

Vytvoř nový soubor `test_math.py`:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

Spusť v terminálu:

```bash
pytest -q
```

Výstup:

```
...                                                                   [100%]
3 passed in 0.01s
```

Každá tečka (`.`) znamená úspěšný test.
Pokud by některý selhal, zobrazí se `F` (*failure*).

---

## ⚠️ Příklad selhání

Zkus záměrně chybný test:

```python
def test_add():
    assert add(2, 3) == 6
```

Spuštění:

```
F                                                                    [100%]
================================== FAILURES ==================================
__________________________________ test_add __________________________________
>       assert add(2, 3) == 6
E       assert 5 == 6
E        +  where 5 = add(2, 3)
```

pytest okamžitě ukáže, **co bylo očekáváno** a **co skutečně dostal** – to je obrovská výhoda oproti běžnému `assert`.

---

## 🧱 Struktura projektu

Doporučená struktura projektu s pytestem:

```
projekt/
│
├── happiness/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── filters.py
│
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   └── test_filters.py
│
└── requirements.txt
```

pytest automaticky najde všechny testy ve složce `tests/`.

---

## 🧩 Fixture – sdílená data pro testy

Fixtures slouží k **přípravě dat nebo prostředí**, které testy využívají.
Např. načtení CSV souboru, připojení k databázi, vytvoření objektu apod.

### 💻 Příklad

```python
import pytest
from happiness.data_loader import load_data

@pytest.fixture(scope="module")
def data():
    """Fixture pro načtení CSV dat pouze jednou pro celý modul."""
    return load_data("happiness/world_happiness_2023.csv", delimiter=";")

def test_load_data(data):
    assert isinstance(data, list)
    assert len(data) > 0
    assert "Country" in data[0]
```

* Fixture `data` se předá do testů jako argument.
* pytest ji automaticky rozpozná a spustí před testem.
* Parametr `scope="module"` znamená, že se vytvoří **jen jednou pro všechny testy** v daném souboru.

---

## 🧠 Užitočné příkazy pytestu

| Příkaz                         | Význam                                    |
| ------------------------------ | ----------------------------------------- |
| `pytest`                       | Spustí všechny testy                      |
| `pytest -q`                    | „Tichý“ režim (zobrazí jen výsledek)      |
| `pytest -v`                    | Podrobný výpis                            |
| `pytest tests/test_filters.py` | Spustí testy v konkrétním souboru         |
| `pytest -k "score"`            | Spustí jen testy obsahující slovo „score“ |
| `pytest --maxfail=1`           | Ukončí po prvním selhání                  |
| `pytest --disable-warnings`    | Skryje varování                           |

---

## 🧰 Rozšíření pytestu

pytest má mnoho užitečných doplňků (pluginů):

| Plugin           | Popis                                           |
| ---------------- | ----------------------------------------------- |
| **pytest-cov**   | měření pokrytí testy (`pip install pytest-cov`) |
| **pytest-xdist** | paralelní běh testů na vícejádrovém procesoru   |
| **pytest-html**  | generování HTML reportů                         |
| **pytest-mock**  | snadné vytváření simulací objektů (mockování)   |

Příklad spuštění s měřením pokrytí:

```bash
pytest --cov=happiness
```

---

## 💬 Výhody pytestu

✅ Minimální kód
✅ Automatické hledání testů
✅ Přehledný výstup chyb
✅ Fixture systém pro přípravu dat
✅ Rozšiřitelný pomocí pluginů
✅ Kompatibilní s `unittest` i `doctest`

---

## 🧭 Cvičení pro studenty

1. 🔹 Nainstaluj `pytest` a ověř instalaci příkazem `pytest --version`.
2. 🔹 Vytvoř soubor `test_math.py` s funkcí `add(a, b)` a třemi testy.
3. 🔹 Přidej test, který záměrně selže, a sleduj výstup pytestu.
4. 🔹 Vytvoř fixture `data()` pro načtení CSV a otestuj, že soubor obsahuje alespoň 100 záznamů.
5. 🔹 Spusť testy s volbou `-v` a pozoruj podrobnosti výstupu.
6. 🔹 Vyzkoušej plugin `pytest-cov` a zjisti, jaké procento kódu je pokryto testy.

---

## 🧱 Shrnutí

| Klíčový pojem    | Význam                                |
| ---------------- | ------------------------------------- |
| `pytest`         | nástroj pro testování Python kódu     |
| testovací funkce | funkce začínající na `test_`          |
| `assert`         | tvrzení, které musí být pravdivé      |
| fixture          | sdílená data nebo nastavení pro testy |
| `pytest -v`      | podrobný výpis výsledků testů         |

---

## 💡 Doporučení

* Testy umísťuj do složky `tests/`.
* Každý modul by měl mít odpovídající testovací soubor (`test_nazev_modulu.py`).
* Při chybě si projdi chybový výstup pytestu — ukazuje přesně, **co bylo očekáváno** a **co skutečně nastalo**.
* Zvykni si testy spouštět často — třeba po každé úpravě funkce.

