"""
ITAE parameters for FOPDT system

This module calculates the values of the PI/PID controller settings
based on Table 11.3 of Seborg, Edgar, Melichamp and Lewin (itself
based on Smith and Corripio, 1997).
"""

# There are four different design relationships
def f1(K, tau, theta, A, B):
    Y = A*(theta/tau)**B
    Kc = Y/K
    return Kc


def f2(K, tau, theta, A, B):
    Y = A*(theta/tau)**B
    tau_I = tau/Y
    return tau_I


def f3(K, tau, theta, A, B):
    Y = A*(theta/tau)**B
    tau_D = Y*tau
    return tau_D


def f4(K, tau, theta, A, B):
    Y = A + B*(theta/tau)
    tau_I = tau/Y
    return tau_I


# dictionary to allow lookup of the coefficients and the relation to use
table = {'Disturbance': {'PI': {'P': (0.859, -0.977, f1),
                                'I': (0.674, -0.68, f2)},
                         'PID': {'P': (1.357, -0.947, f1),
                                 'I': (0.842, -0.738, f2),
                                 'D': (0.381, 0.995, f3)}},
         'Set point': {'PI': {'P': (0.586, -0.916, f1),
                              'I': (1.03, -0.165, f4)},
                       'PID': {'P': (0.965, -0.85, f1),
                               'I': (0.796, -0.1465, f4),
                               'D': (0.308, 0.929, f3)}}}


def parameters(K, tau, theta, type_of_input='Disturbance', type_of_controller='PI'):
    retval = []
    for mode in type_of_controller:
        A, B, f = table[type_of_input][type_of_controller][mode]
        value = f(K, tau, theta, A, B)
        retval.append(value)
    return retval
