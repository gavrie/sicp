from .derive import derive_str


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


def test_derive_poly_2() -> None:
    assert derive_str("a*x**2 + b*x + c", "x") == "a * (2 * x) + b"  # -> 2*a*x + b


def test_derive_poly_3() -> None:
    assert derive_str("a*x**3 + b*x**2 + c*x + d", "x") == \
        "a * (3 * x ** 2) + b * (2 * x) + c"  # -> 3*a*x**2 + 2*b*x + c


def test_derive_poly_4() -> None:
    assert derive_str("x**0.5", "x") == "0.5 * x ** -0.5"
