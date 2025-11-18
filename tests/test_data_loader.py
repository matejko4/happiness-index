def test_load_data(data):
    """Test načítání dat ze souboru CSV."""
    # Ověření, že data jsou načtena jako seznam
    assert isinstance(data, list)
    # Ověření, že seznam není prázdný
    assert len(data) > 0
    # Ověření, že první prvek seznamu je slovník s očekávanými klíči
    assert isinstance(data[0], dict)
    # Ověření, že klíče "Country" a "Happiness score" jsou přítomny
    assert "Country" in data[0]
    # Ověření, že klíč "Happiness score" je přítomen
    assert "Happiness score" in data[0]
    assert "GDP per capita" in data[0]
