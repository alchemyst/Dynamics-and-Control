"""Control functions which operate symbolically using sympy"""

import sympy

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