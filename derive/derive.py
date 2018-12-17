from typing import cast
import ast
import logging

import astunparse  # type: ignore

"""
Based on SICP section 2.3.2 Example: Symbolic Differentiation.
"""


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def is_num(v: ast.expr) -> bool:
    logger.debug(f"is_num: {ast.dump(v)}")
    return isinstance(v, ast.Num)


def num_equals(v1: ast.expr, v2: ast.expr) -> bool:
    logger.debug(f"num_equals: {ast.dump(v1)} == {ast.dump(v2)} ?")

    if not is_num(v1) or not is_num(v2):
        return False

    v1 = cast(ast.Num, v1)
    v2 = cast(ast.Num, v2)

    return v1.n == v2.n


def is_var(v: ast.expr) -> bool:
    logger.debug(f"is_var: {ast.dump(v)}")
    return isinstance(v, ast.Name)


def var_equals(v1: ast.expr, v2: ast.expr) -> bool:
    logger.debug(f"var_equals: {ast.dump(v1)}, {ast.dump(v2)}")

    if not is_var(v1) or not is_var(v2):
        return False

    v1 = cast(ast.Name, v1)
    v2 = cast(ast.Name, v2)

    return v1.id == v2.id


def is_sum(v: ast.expr) -> bool:
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Add))


def is_prod(v: ast.expr) -> bool:
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Mult))


def is_pow_num(v: ast.expr) -> bool:
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Pow) and
            isinstance(v.right, ast.Num))


def make_sum(a1: ast.expr, a2: ast.expr) -> ast.expr:
    if num_equals(a1, ast.Num(0)):
        return a2
    if num_equals(a2, ast.Num(0)):
        return a1

    if is_num(a1) and is_num(a2):
        a1 = cast(ast.Num, a1)
        a2 = cast(ast.Num, a2)

        return ast.Num(a1.n + a2.n)

    if a1 == a2:
        return make_prod(ast.Num(2), a1)

    return ast.BinOp(op=ast.Add(), left=a1, right=a2)


def make_prod(m1: ast.expr, m2: ast.expr) -> ast.expr:
    if num_equals(m1, ast.Num(1)):
        return m2
    if num_equals(m2, ast.Num(1)):
        return m1

    if is_num(m1) and is_num(m2):
        m1 = cast(ast.Num, m1)
        m2 = cast(ast.Num, m2)

        return ast.Num(m1.n * m2.n)

    if num_equals(m1, ast.Num(0)) or num_equals(m2, ast.Num(0)):
        return ast.Num(0)

    return ast.BinOp(op=ast.Mult(), left=m1, right=m2)


def make_pow(base: ast.expr, exp: ast.expr) -> ast.expr:
    logger.info(f"make_pow: {ast.dump(base)} ** {ast.dump(exp)}")

    if num_equals(exp, ast.Num(0)):
        return ast.Num(1)

    if num_equals(exp, ast.Num(1)):
        return base

    return ast.BinOp(op=ast.Pow(), left=base, right=exp)


def _derive(e: ast.expr, var: ast.expr) -> ast.expr:
    logger.debug(f"deriv: {ast.dump(e)}, {ast.dump(var)}")

    if is_num(e):
        return ast.Num(0)

    if is_var(e):
        return ast.Num(1) if var_equals(e, var) else ast.Num(0)

    if is_sum(e):
        u = cast(ast.BinOp, e).left
        v = cast(ast.BinOp, e).right
        return make_sum(
            _derive(u, var),
            _derive(v, var))

    if is_prod(e):
        u = cast(ast.BinOp, e).left
        v = cast(ast.BinOp, e).right
        return make_sum(
            make_prod(u, _derive(v, var)),
            make_prod(v, _derive(u, var)))

    if is_pow_num(e):
        u = cast(ast.BinOp, e).left
        n = cast(ast.Num, cast(ast.BinOp, e).right)
        return make_prod(
            make_prod(n, make_pow(u, ast.Num(n.n - 1))),
            _derive(u, var)
        )

    raise Exception(f"Unknown expression: {ast.dump(e)}")


##########

def _parse(s: str) -> ast.expr:
    """
    Parse a string into a Python AST.
    """
    body = ast.parse(s).body
    expr = body[0]

    if not isinstance(expr, ast.Expr):
        raise Exception("Expected an expression")

    return expr.value


##########

def derive(expr: str, var: str) -> str:
    result = _derive(_parse(expr), _parse(var))
    return cast(str, astunparse.unparse(result).strip())
