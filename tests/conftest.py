import pytest
from pathlib import Path
from happiness.data_loader import load_data

@pytest.fixture(scope="session")
def data():
    """Fixture pro načtení CSV dat – spustí se jen jednou za celou testovací relaci."""
    csv_path = Path(__file__).parent.parent / "data" / "world_happiness_2022.csv"
    return load_data(csv_path, delimiter=";")
