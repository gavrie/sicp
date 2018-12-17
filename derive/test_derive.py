from .derive import derive


def test_derive_basic() -> None:
    assert derive("x+3", "x") == "1"
    assert derive("x*y", "x") == "y"


def test_derive_poly_mult() -> None:
    assert derive("a*x*x + b*x + c", "x") == "(((a * x) + (x * a)) + b)"  # -> 2*a*x + b


def test_derive_poly_2() -> None:
    assert derive("a*x**2 + b*x + c", "x") == "((a * (2 * x)) + b)"  # -> 2*a*x + b


def test_derive_poly_3() -> None:
    assert derive("a*x**3 + b*x**2 + c*x + d", "x") == \
           "(((a * (3 * (x ** 2))) + (b * (2 * x))) + c)"


def test_derive_poly_4() -> None:
    assert derive("x**0.5", "x") == "(0.5 * (x ** -0.5))"
