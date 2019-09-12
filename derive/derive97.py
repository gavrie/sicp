import ast
import logging

import astor

"""
Based on SICP section 2.3.2 Example: Symbolic Differentiation.

- Remove math simplifications
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


def sum(a1, a2):
    return ast.BinOp(op=ast.Add(), left=a1, right=a2)


def product(m1, m2):
    return ast.BinOp(op=ast.Mult(), left=m1, right=m2)


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