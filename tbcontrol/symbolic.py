"""Control functions which operate symbolically using sympy"""

import sympy


def linearise(expr, variables, bars=None):
    """Linearise a nonlinear expression
    
    Parameters
    ----------
    expr: A sympy expression - this could be a single term or a sum of terms
    variables: The variables in the expression - all the other symbols in the expression will be treated as parameters
    bars: the "barred" versions of the variables. If bars is None, new barred versions will be built and returned
    
    Note: This function will *not work correctly with derivatives in expr*
    """
    if bars is None:
        returnbars = True
        bars = [sympy.Symbol(f"{variable.name}bar") for variable in variables]
    else:
        returnbars = False

    vars_and_bars = list(zip(variables, bars))

    # This is the constant term
    result = expr.subs(vars_and_bars)

    # now, we take the derivative with respect to each variable, evaluated at the steady state:
    for variable, bar in vars_and_bars:
        result += (variable - bar)*expr.diff(variable).subs(vars_and_bars)

    if returnbars:
        return bars, result
    else:
        return result


def routh(p):
    """ Construct the Routh-Hurwitz array given a polynomial in s

    Input: p - a sympy.Poly object
    Output: The Routh-Hurwitz array as a sympy.Matrix object
    """
    coefficients = p.all_coeffs()
    N = len(coefficients)
    M = sympy.zeros(N, (N+1)//2 + 1)

    r1 = coefficients[0::2]
    r2 = coefficients[1::2]
    M[0, :len(r1)] = [r1]
    M[1, :len(r2)] = [r2]
    for i in range(2, N):
        for j in range(N//2):
            S = M[[i-2, i-1], [0, j+1]]
            M[i, j] = sympy.simplify(-S.det()/M[i-1,0])
    return M[:, :-1]


def pade(G, s, M, N, p=0):
    """Return a Padé approximation of the function G in terms of variable s, of order M/N around point p"""
    M += 1
    N += 1
    b = sympy.symbols('b:{}'.format(M))
    a = sympy.symbols('a:{}'.format(N))
    approximation = sum(b[i]*s**i for i in range(M))/sum(a[i]*s**i for i in range(N))
    nder = M + N
    derivatives = [(G - approximation).diff(s, i).subs({s: p}) for i in range(nder-1)]
    denominator_constant = [a[0] - 1]  # set denom constant term = 1
    equations = derivatives + denominator_constant
    pars = sympy.solve(equations, a + b, dict=True)
    return approximation.subs(pars[0])


def ss2tf(A, B, C, D, s):
    """Convert state space matrices to a transfer function matrix

    Arguments:
    A, B, C, D : sympy.Matrix objects containing the state space matrices
    s : symbol to use for s

    Returns:
    G : Transfer function matrix
    """
    I = sympy.eye(A.shape[0])

    G = C*(s*I - A).inv()*B + D
    return G


def sampledvalues(fz, z, N):
    """Return the first N values of a z transform's inverse via Taylor series expansion

    Arguments:

        fz: sympy symbolic expression in terms of z
        z: the symbol used in fz for the z transform
        N: The number of time steps to return
    """
    q = sympy.Symbol('q')
    return sympy.poly(fz.subs(z, q**-1).series(q, 0, N).removeO(), q).all_coeffs()[::-1]


def evaluate_at_times(expression, t, ts):
    """Evaluate a sympy expression over time

    Arguments:
    
        expression: a sympy expression containing references to a time variable `t`
        t : a `sympy.Symbol` which is in `expression` and will be subsitituted from `ts`
        ts: an iterable containing times for evaluation. Should be only ints or floats

    versionadded: 0.1.3
    """

    return [expression.subs(t, ti).subs({sympy.Heaviside(float(0)): 1, 
                                         sympy.Heaviside(0): 1}) for ti in ts]
