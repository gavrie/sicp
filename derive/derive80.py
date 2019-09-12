"""
Based on SICP section 2.3.2 Example: Symbolic Differentiation.
-
"""

def derive(expr, var):
    if is_num(expr):
        return num(0)

    if is_var(expr):
        return num(1) if same_var(expr, var) else num(0)

    if is_sum(expr):
        u, v = operands(expr)
        return sum(
            derive(u, var),
            derive(v, var))

    if is_product(expr):
        u, v = operands(expr)
        return sum(
            product(u, derive(v, var)),
            product(v, derive(u, var)))

    raise Exception("Unknown expression")
