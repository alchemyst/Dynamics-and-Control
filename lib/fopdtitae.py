"""
ITAE parameters for FOPDT system

This modole calculates the values of the PI/PID controller settings
based on Table 11.3 of Sebord, Edgar, Melichamp and Lewin (itself
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
table = {'Disturbance': {'PI': {'P': {'A': 0.859, 'B': -0.977, 'relation': f1},
                                'I': {'A': 0.674, 'B': -0.68, 'relation': f2}},
                         'PID': {'P': {'A': 1.357, 'B': -0.947, 'relation': f1},
                                 'I': {'A': 0.842, 'B': -0.738, 'relation': f2},
                                 'D': {'A': 0.381, 'B': 0.995, 'relation': f3}}},
         'Set point': {'PI': {'P': {'A': 0.586, 'B': -0.916, 'relation': f1},
                              'I': {'A': 1.03, 'B': -0.165, 'relation': f4}},
                       'PID': {'P': {'A': 0.965, 'B': -0.85, 'relation': f1},
                               'I': {'A': 0.796, 'B': -0.1465, 'relation': f4},
                               'D': {'A': 0.308, 'B': 0.929, 'relation': f3}}}}

def parameters(K, tau, theta, type_of_input='Disturbance', type_of_controller='PI'):
    retval = []
    for mode in type_of_controller:
        entry = table[type_of_input][type_of_controller][mode]
        f = entry['relation']
        value = f(K, tau, theta, entry['A'], entry['B'])
        retval.append(value)
    return retval
