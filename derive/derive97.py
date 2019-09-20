from typing import cast, Tuple, Union
import ast
import logging

import astor  # type: ignore

"""
Based on SICP section 2.3.2 Example: Symbolic Differentiation.
"""


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


Number = Union[int, float, complex]


def is_num(v: ast.expr) -> bool:
    return isinstance(v, ast.Num)


def as_num(e: ast.expr) -> Number:
    n = cast(ast.Num, e)
    return n.n


def num(n: Number) -> ast.Num:
    return ast.Num(n)


def num_equals(v1: ast.expr, v2: ast.expr) -> bool:
    if not is_num(v1) or not is_num(v2):
        return False

    n1 = as_num(v1)
    n2 = as_num(v2)

    return n1 == n2


def is_var(v: ast.expr) -> bool:
    return isinstance(v, ast.Name)


def as_var(e: ast.expr) -> ast.Name:
    return cast(ast.Name, e)


def same_var(v1: ast.expr, v2: ast.expr) -> bool:
    if not is_var(v1) or not is_var(v2):
        return False

    v1 = as_var(v1)
    v2 = as_var(v2)

    return v1.id == v2.id


def operands(e: ast.expr) -> Tuple[ast.expr, ast.expr]:
    op = cast(ast.BinOp, e)
    return op.left, op.right


def is_sum(v: ast.expr) -> bool:
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Add))


def is_prod(v: ast.expr) -> bool:
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Mult))


def sum(a1: ast.expr, a2: ast.expr) -> ast.expr:
    logger.debug(f"make_sum: {ast.dump(a1)} + {ast.dump(a2)}")

    return ast.BinOp(op=ast.Add(), left=a1, right=a2)


def product(m1: ast.expr, m2: ast.expr) -> ast.expr:
    logger.debug(f"product: {ast.dump(m1)} * {ast.dump(m2)}")

    return ast.BinOp(op=ast.Mult(), left=m1, right=m2)


def derive(e: ast.expr, var: ast.expr) -> ast.expr:
    logger.debug(f"derive: {ast.dump(e)}, {ast.dump(var)}")

    if is_num(e):
        return num(0)

    if is_var(e):
        return num(1) if same_var(e, var) else num(0)

    if is_sum(e):
        u, v = operands(e)
        return sum(
            derive(u, var),
            derive(v, var))

    if is_prod(e):
        u, v = operands(e)
        return sum(
            product(u, derive(v, var)),
            product(v, derive(u, var)))

    raise Exception(f"Unknown expression: {ast.dump(e)}")


##########

def parse(s: str) -> ast.expr:
    """
    Parse a string into a Python AST.
    """
    body = ast.parse(s).body
    expr = body[0]

    if not isinstance(expr, ast.Expr):
        raise Exception("Expected an expression")

    return expr.value


##########

def derive_str(expr: str, var: str) -> str:
    logger.debug(f"derive_str: d({expr}) / d{var}")
    result = derive(parse(expr), parse(var))
    return cast(str, astor.to_source(ast.Expr(result)).strip())
