import ast
import logging

import astor

"""
Based on SICP section 2.3.2 Example: Symbolic Differentiation.

- Removed mypy annotations
"""


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def is_num(v):
    return isinstance(v, ast.Num)


def as_num(n):
    return n.n


def num(n):
    return ast.Num(n)


def num_equals(v1, v2):
    if not is_num(v1) or not is_num(v2):
        return False

    n1 = as_num(v1)
    n2 = as_num(v2)

    return n1 == n2


def is_var(v):
    return isinstance(v, ast.Name)


def same_var(v1, v2):
    if not is_var(v1) or not is_var(v2):
        return False

    return v1.id == v2.id


def operands(op):
    return op.left, op.right


def is_sum(v):
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Add))


def is_prod(v):
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Mult))


def is_pow_num(v):
    return (isinstance(v, ast.BinOp) and
            isinstance(v.op, ast.Pow) and
            isinstance(v.right, ast.Num))


def sum(a1, a2):
    if num_equals(a1, num(0)):
        return a2
    if num_equals(a2, num(0)):
        return a1

    if is_num(a1) and is_num(a2):
        n1 = as_num(a1)
        n2 = as_num(a2)
        return num(n1 + n2)

    if a1 == a2:
        return product(num(2), a1)

    return ast.BinOp(op=ast.Add(), left=a1, right=a2)


def product(m1, m2):
    if num_equals(m1, num(1)):
        return m2
    if num_equals(m2, num(1)):
        return m1

    if is_num(m1) and is_num(m2):
        n1 = as_num(m1)
        n2 = as_num(m2)
        return num(n1 * n2)

    if num_equals(m1, num(0)) or num_equals(m2, num(0)):
        return num(0)

    return ast.BinOp(op=ast.Mult(), left=m1, right=m2)


def make_pow(base, exp):
    if num_equals(exp, num(0)):
        return num(1)

    if num_equals(exp, num(1)):
        return base

    return ast.BinOp(op=ast.Pow(), left=base, right=exp)


def derive(e, var):
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

    if is_pow_num(e):
        u, v = operands(e)
        n = as_num(v)
        return product(
            product(v, make_pow(u, num(n - 1))),
            derive(u, var)
        )

    raise Exception("Unknown expression")


##########

def parse(s):
    """
    Parse a string into a Python AST.
    """
    body = ast.parse(s).body
    expr = body[0]

    if not isinstance(expr, ast.Expr):
        raise Exception("Expected an expression")

    return expr.value


##########

def derive_str(expr, var):
    result = derive(parse(expr), parse(var))
    return astor.to_source(ast.Expr(result)).strip()
