from typing import cast, Tuple
import ast
import logging

import astor  # type: ignore

"""
Based on SICP section 2.3.2 Example: Symbolic Differentiation.
"""


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def is_num(v: ast.expr) -> bool:
    return isinstance(v, ast.Num)


def as_num(e: ast.expr) -> ast.Num:
    return cast(ast.Num, e)


def num_equals(v1: ast.expr, v2: ast.expr) -> bool:
    if not is_num(v1) or not is_num(v2):
        return False

    v1 = as_num(v1)
    v2 = as_num(v2)

    return v1.n == v2.n


def is_var(v: ast.expr) -> bool:
    return isinstance(v, ast.Name)


def as_var(e: ast.expr) -> ast.Name:
    return cast(ast.Name, e)


def var_equals(v1: ast.expr, v2: ast.expr) -> bool:
    if not is_var(v1) or not is_var(v2):
        return False

    v1 = as_var(v1)
    v2 = as_var(v2)

    return v1.id == v2.id


def as_binop(e: ast.expr) -> Tuple[ast.expr, ast.expr]:
    op = cast(ast.BinOp, e)
    return op.left, op.right


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
    logger.debug(f"make_sum: {ast.dump(a1)} + {ast.dump(a2)}")

    if num_equals(a1, ast.Num(0)):
        return a2
    if num_equals(a2, ast.Num(0)):
        return a1

    if is_num(a1) and is_num(a2):
        a1 = as_num(a1)
        a2 = as_num(a2)

        return ast.Num(a1.n + a2.n)

    if a1 == a2:
        return make_prod(ast.Num(2), a1)

    return ast.BinOp(op=ast.Add(), left=a1, right=a2)


def make_prod(m1: ast.expr, m2: ast.expr) -> ast.expr:
    logger.debug(f"make_prod: {ast.dump(m1)} * {ast.dump(m2)}")

    if num_equals(m1, ast.Num(1)):
        return m2
    if num_equals(m2, ast.Num(1)):
        return m1

    if is_num(m1) and is_num(m2):
        m1 = as_num(m1)
        m2 = as_num(m2)

        return ast.Num(m1.n * m2.n)

    if num_equals(m1, ast.Num(0)) or num_equals(m2, ast.Num(0)):
        return ast.Num(0)

    return ast.BinOp(op=ast.Mult(), left=m1, right=m2)


def make_pow(base: ast.expr, exp: ast.expr) -> ast.expr:
    logger.debug(f"make_pow: {ast.dump(base)} ** {ast.dump(exp)}")

    if num_equals(exp, ast.Num(0)):
        return ast.Num(1)

    if num_equals(exp, ast.Num(1)):
        return base

    return ast.BinOp(op=ast.Pow(), left=base, right=exp)


def derive(e: ast.expr, var: ast.expr) -> ast.expr:
    logger.debug(f"derive: {ast.dump(e)}, {ast.dump(var)}")

    if is_num(e):
        return ast.Num(0)

    if is_var(e):
        return ast.Num(1) if var_equals(e, var) else ast.Num(0)

    if is_sum(e):
        u, v = as_binop(e)
        return make_sum(
            derive(u, var),
            derive(v, var))

    if is_prod(e):
        u, v = as_binop(e)
        return make_sum(
            make_prod(u, derive(v, var)),
            make_prod(v, derive(u, var)))

    if is_pow_num(e):
        u, v = as_binop(e)
        n = as_num(v)
        return make_prod(
            make_prod(n, make_pow(u, ast.Num(n.n - 1))),
            derive(u, var)
        )

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
