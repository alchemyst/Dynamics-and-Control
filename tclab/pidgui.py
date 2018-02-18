from ipywidgets import Button, Label, FloatSlider, HBox, VBox, Checkbox, IntText
import tornado
from tclab import Plotter, Historian, TCLab, TCLabModel
from tclab.gui import actionbutton, labelledvalue, slider, NotebookInteraction

import matplotlib.pyplot as plt

class PID:
    def __init__(self):
        self.K = 1
        self.taui = 100
        self.taud = 0

        self.e = 0
        self.dedt = 0
        self.eint = 0
        self.output = 0

    def update(self, setpoint, mv):
        e = setpoint - mv
        self.dedt = self.e - e
        self.eint += e
        self.e = e

        self.output = self.K * (self.e + 1/self.taui*self.eint + self.taud*self.dedt)
        return self.output


class PIDGUI(NotebookInteraction):
    def __init__(self):
        self.lab = None
        self.layout = (('T1', 'setpoint'),
                       ('error',),
                       ('eint',),
                       ('dedt',),
                       ('Q1', 'output'))

        self.pid = PID()

        self.mode = 'manual'

        self.manual = actionbutton('Manual', self.action_manual)
        self.auto = actionbutton('Auto', self.action_auto)
        
        buttons = HBox([self.auto, self.manual])

        # Sliders for heaters
        self.gain = slider('Gain', self.action_gain, maxvalue=100)
        self.gain.value = 1
        self.tau_i = slider(r'$\tau_I$', self.action_tau_i, minvalue=0)
        self.tau_i.value = 100
        self.tau_d = slider(r'$\tau_D$', self.action_tau_d, maxvalue=10)

        parameters = HBox([self.gain, self.tau_i, self.tau_d])

        # Setpoint
        self.setpoint = slider('Setpoint', minvalue=20, maxvalue=70)
        self.setpoint.value = 30
        self.Q1 = slider('Q1')

        self.ui = VBox([buttons,
                        parameters,
                        HBox([self.setpoint, self.Q1]),
                       ])

    def update(self, t):
        if self.mode == 'auto':
            Q1 = self.pid.update(self.setpoint.value, self.lab.T1)
        else:
            Q1 = self.Q1.value

        self.lab.Q1(Q1)

    def connect(self, lab):
        super().connect(lab)
        self.sources = [('T1', lambda: self.lab.T1),
                        ('Q1', self.lab.Q1),
                        ('setpoint', lambda: self.setpoint.value),
                        ('error', lambda: self.pid.e),
                        ('eint', lambda: self.pid.eint),
                        ('dedt', lambda: self.pid.dedt),
                        ('output', lambda: self.pid.output),
                        ('gain', lambda: self.gain.value),
                        ('taui', lambda: self.tau_i.value),
                        ('taud', lambda: self.tau_d.value),
                        ]

    def start(self):
        self.action_manual()

    def stop(self):
        self.auto.disabled = True
        self.manual.disabled = True

    def action_auto(self, w=None):
        self.mode = 'auto'
        self.manual.disabled = False
        self.auto.disabled = True

        self.Q1.disabled = True
        self.setpoint.disabled = False
        self.gain.disabled = False
        self.tau_i.disabled = False
        self.tau_d.disabled = False

    def action_manual(self, w=None):
        self.mode = 'manual'
        self.manual.disabled = True
        self.auto.disabled = False

        self.Q1.disabled = False
        self.setpoint.disabled = True
        self.gain.disabled = True
        self.tau_i.disabled = True
        self.tau_d.disabled = True

    def action_gain(self, w):
        self.pid.K = self.gain.value

    def action_tau_i(self, w):
        self.pid.taui = self.tau_i.value

    def action_tau_d(self, w):
        self.pid.taud = self.tau_d.value