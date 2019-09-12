from .derive97 import derive_str


def test_derive_num() -> None:
    assert derive_str("7", "x") == "0"


def test_derive_var() -> None:
    assert derive_str("x", "x") == "1"


def test_derive_var_sum() -> None:
    assert derive_str("x+3", "x") == "1 + 0"


def test_derive_var_mul() -> None:
    assert derive_str("x*y", "x") == "x * 0 + y * 1"


def test_derive_poly_mul() -> None:
    assert derive_str("a*x*x + b*x + c", "x") == "a * x * 1 + x * (a * 1 + x * 0) + (b * 1 + x * 0) + 0"  # -> 2*a*x + b

