from project import validate_response, add_shop, get_shopping_list
import pytest

def test_validate_response():
    assert validate_response("3") == 3
    with pytest.raises(ValueError):
        validate_response("tomato")

def test_add_shop():
    assert add_shop("aldi") == "\nALDI added!\n"
    assert add_shop("carrefour") == "\nCARREFOUR added!\n"

def test_get_shopping_list():
    assert get_shopping_list(1) == ["- coffee table", "- candles", "- pillow cases", "- new pillow for lena"]
