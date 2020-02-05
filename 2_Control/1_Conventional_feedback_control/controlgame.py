import tornado
import time
import numpy

import matplotlib.pyplot as plt

from ipywidgets import FloatProgress, FloatSlider, HBox, VBox, Button, Text

K = 2
tau = 2

LIMIT = 100  # Limits for CV
SLEEP = 150  # Sleep time - make smaller for more responsive simulation

MINIMUM = 5  # minimum length the setpoint stays in one place
EXTRA = 5  # maximum additional length that is added randomly
SEED = 1  # control the game - everyone sees the same sequence


class SetPointGenerator:
    def __init__(self):
        self.nextt = 0
        self.output = 0
        
    def generate(self, t):
        if t > self.nextt:
            self.nextt = t + MINIMUM + numpy.random.random()*EXTRA
            self.output = LIMIT*(2*numpy.random.random() - 1)
        
        return self.output


class ControlledSystem:
    def __init__(self):
        self.state = 0
        self.manipulated = 0
        self.controlled = 0
        
    def update(self, t, manipulated):
        dt = SLEEP/1000
        
        dxdt = K/tau*manipulated
        self.state += dxdt*dt
        self.controlled = self.state
        
        return self.controlled

    
class ControlGame:
    def __init__(self, runtime):
        """Initialise the game
        
        :param runtime: runtime in seconds
        """
        self.runtime = runtime
        
        self.startbutton = Button(description='Run')
        self.startbutton.on_click(self.run)

        self.timeprogress = FloatProgress(value=0, min=0, max=self.runtime, description='Time')
        self.setpoint = FloatSlider(value=0, min=-LIMIT, max=LIMIT, description='Setpoint')
        self.controlled = FloatSlider(value=0, min=-LIMIT, max=LIMIT, description='Controlled')
        self.controlled.disabled = True
        self.manipulated = FloatSlider(value=0, min=-LIMIT, max=LIMIT, description= 'MV')
        self.scoretext = Text(value='0', description='Score')
        self.score = 0
        
        self.timer = tornado.ioloop.PeriodicCallback(self.update, SLEEP)
        
        self.running = False
        self.reset()

    def reset(self):
        self.ts = []
        self.sps = []
        self.mvs = []
        self.cvs = []

        self.t = 0
        self.score = 0
        self.scoretext.value = '0'


    def run(self, args):
        numpy.random.seed(SEED)

        self.running = True
        self.startbutton.disabled = True
        self.setpointgenerator = SetPointGenerator()
        self.system = ControlledSystem()

        self.reset()

        self.timer.start()
        
    def update(self):
        if not self.running:
            return
        
        t = self.t = self.t + SLEEP/1000
        
        if t >= self.runtime:
            self.running = False
            self.timer.stop()
            self.startbutton.disabled = False
            return

        self.timeprogress.value = t
        
        sp = self.setpoint.value = self.setpointgenerator.generate(t)
        mv = self.manipulated.value
        cv = self.controlled.value = self.system.update(t, mv)
        
        score = 1 - min(abs(sp - cv), LIMIT)/LIMIT
        
        self.score += score
                 
        self.scoretext.value = f'{self.score:0.1f}'
    
        self.ts.append(t)
        self.sps.append(sp)
        self.mvs.append(mv)
        self.cvs.append(cv)
        
        
    def ui(self):
        return VBox([
            HBox([self.startbutton, self.scoretext]),
            self.timeprogress, 
            self.setpoint, 
            self.controlled, 
            self.manipulated,
        ])
        

    def plot(self):
        fig, [axcv, axmv] = plt.subplots(2, 1)
        axcv.plot(self.ts, self.sps, self.ts, self.cvs)
        axmv.plot(self.ts, self.mvs)
