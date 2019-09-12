from .derive98 import derive_str


def test_derive_num() -> None:
    assert derive_str("7", "x") == "0"


def test_derive_var() -> None:
    assert derive_str("x", "x") == "1"


def test_derive_var_sum() -> None:
    assert derive_str("x+3", "x") == "1"


def test_derive_var_mul() -> None:
    assert derive_str("x*y", "x") == "y"


def test_derive_poly_mul() -> None:
    assert derive_str("a*x*x + b*x + c", "x") == "a * x + x * a + b"  # -> 2*a*x + b

