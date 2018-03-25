from collections import defaultdict
import scipy
import scipy.signal
import numpy

class Block:
    def __init__(self, name, inputname, outputname):
        self.name = name
        self.inputname = inputname
        self.outputname = outputname

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.inputname} →[ {self.name} ]→ {self.outputname}"


class LTI(Block):
    def __init__(self, name, inputname, outputname, numerator, denominator=1, delay=0):
        super().__init__(name, inputname, outputname)

        self.G = scipy.signal.lti(numerator, denominator)
        self.Gss = self.G.to_ss()
        if delay > 0:
            self.delay = Deadtime(None, None, None, delay)
        else:
            self.delay = None
        self.reset()

    def reset(self):
        self.change_state(numpy.zeros((self.Gss.A.shape[0], 1)))
        self.y = self.output = 0
        if self.delay:
            self.delay.reset()

    def change_input(self, t, u):
        self.y = (self.Gss.C.dot(self.x) + self.Gss.D.dot(u))[0, 0]
        if self.delay:
            self.y = self.delay.change_input(t, self.y)
        self.output = self.y
        return self.output

    def change_state(self, x):
        self.x = self.state = x

    def derivative(self, e):
        return self.Gss.A.dot(self.x) + self.Gss.B.dot(e)


class PI(LTI):
    def __init__(self, name, inputname, outputname, Kc, tau_i):
        super().__init__(name, inputname, outputname, [Kc*tau_i, Kc], [tau_i, 0])


class AE(Block):
    def __init__(self, name, inputname, outputname, f, delay=0):
        super().__init__(name, inputname, outputname)
        self.f = f # y = f(t, u)
        if delay > 0:
            self.delay = Deadtime(None, None, None, delay)
        else:
            self.delay = None
        self.reset()

    def reset(self):
        self.change_state(0)
        self.y = self.output = 0
        if self.delay:
            self.delay.reset()

    def change_input(self, t, u):
        self.y = self.f(t, u)
        if self.delay:
            self.y = self.delay.change_input(t, self.y)
        self.output = self.y
        return self.output

    def change_state(self, x):
        self.x = self.state = x

    def derivative(self, e):
        return 0


class Deadtime(Block):
    def __init__(self, name, inputname, outputname, delay):
        super().__init__(name, inputname, outputname)

        self.delay = delay
        self.reset()

    def reset(self):
        self.change_state(0)
        self.y = self.output = 0
        self.ts = [0]
        self.us = [0]

    def change_input(self, t, u):
        self.ts.append(t)
        self.us.append(u)
        if self.delay > 0:
            u = numpy.interp(t - self.delay, self.ts, self.us)

        self.y = u
        self.output = self.y
        return self.output

    def change_state(self, x):
        self.x = self.state = x

    def derivative(self, e):
        return 0


class Diagram:
    def __init__(self, blocks, sums, inputs):
        self.blocks = blocks
        self.sums = sums
        self.inputs = inputs
        self.reset()

    def reset(self):
        self.signals = {b.inputname: 0 for b in self.blocks}
        self.signals.update({b.outputname: 0 for b in self.blocks})
        for block in self.blocks:
            block.reset()

    def step(self, t, dt):
        signals = self.signals
        # Evaluate all inputs
        for signal, function in self.inputs.items():
            signals[signal] = function(t)
        # Evaluate sums
        for output, inputs in self.sums.items():
            signals[output] = sum(int(s[0]+'1')*signals[s[1:]] for s in inputs)
        # Evaluate blocks and integrate
        for block in self.blocks:
            u = signals[block.inputname]
            signals[block.outputname] = block.change_input(t, u)
            block.change_state(block.state + block.derivative(u)*dt)
        return signals

    def simulate(self, ts):
        dt = ts[1]
        outputs = defaultdict(list)
        self.reset()
        for t in ts:
            newoutputs = self.step(t, dt)
            for signal, value in newoutputs.items():
                outputs[signal].append(value)
        return outputs

    def __repr__(self):
        return '\n'.join(str(b) for b in self.blocks)
