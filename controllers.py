import numpy
import scipy.signal

# Define controller classses

class PController:
    def __init__(self, K_c, bias):
        self.G = K_c
        self.bias = self.output = bias
        self.y = self.bias

    def change_input(self, t, u):
        self.output = self.y = self.G * u + self.bias


class PIController:
    def __init__(self, K_c, tau_I, bias):
        self.G = scipy.signal.lti([K_c * tau_I, K_c], [tau_I, 0])

        self.change_state(numpy.zeros((self.G.A.shape[0], 1)))
        self.bias = self.output = bias
        self.y = self.bias

    def change_input(self, t, u):
        self.y = self.G.C.dot(self.x) + self.G.D.dot(u) + self.bias
        self.derivative = self.dxdt = self.G.A.dot(self.x) + self.G.B.dot(u)
        self.output = self.y[0, 0]

    def change_state(self, x):
        self.x = self.state = x

        
class PIDController:
    def __init__(self, K_c, tau_I, tau_D, bias, alpha_f=0.1):
        self.G = scipy.signal.lti([K_c*alpha_f*tau_D*tau_I + K_c*tau_D*tau_I,
                                   K_c*alpha_f*tau_D + K_c*tau_I, K_c],
                                  [alpha_f*tau_D*tau_I, tau_I, 0.0])

        self.change_state(numpy.zeros((self.G.A.shape[0], 1)))
        self.bias = self.output = bias
        self.y = self.bias

    def change_input(self, t, u):
        self.y = self.G.C.dot(self.x) + self.G.D.dot(u) + self.bias
        self.derivative = self.dxdt = self.G.A.dot(self.x) + self.G.B.dot(u)
        self.output = self.y[0, 0]

    def change_state(self, x):
        self.x = self.state = x

def limit(signal, lower, upper):
    if signal > upper:
        return upper
    if signal < lower:  # x < 0.0
        return lower
    return signal
