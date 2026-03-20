import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


def test_basic_addition(calc):
    calc.append("2+3")
    assert calc.evaluate() == "5"


def test_basic_subtraction(calc):
    calc.append("10-4")
    assert calc.evaluate() == "6"


def test_multiplication(calc):
    calc.append("3*7")
    assert calc.evaluate() == "21"


def test_division(calc):
    calc.append("10/4")
    assert calc.evaluate() == "2.5"


def test_division_by_zero(calc):
    calc.append("5/0")
    assert calc.evaluate() == "div/0"


def test_clear(calc):
    calc.append("123")
    assert calc.clear() == "0"
    assert calc.expression == ""


def test_backspace(calc):
    calc.append("123")
    assert calc.backspace() == "12"


def test_backspace_empty(calc):
    assert calc.backspace() == "0"


def test_reset_next_on_new_number(calc):
    calc.append("5")
    calc.evaluate()
    calc.append("9")  # should start fresh, not append to result
    assert calc.expression == "9"


def test_chained_operations(calc):
    calc.append("2+3")
    calc.evaluate()
    calc.append("+4")
    assert calc.evaluate() == "9"


def test_invalid_expression(calc):
    calc.append("++")
    assert calc.evaluate() == "error"


def test_float_result(calc):
    calc.append("1/3")
    result = calc.evaluate()
    assert float(result) == pytest.approx(0.333, rel=1e-2)
