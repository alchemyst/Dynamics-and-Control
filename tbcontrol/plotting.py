"""Commonly used plotting functions"""

import matplotlib.pyplot as plt

def cross_axis(size=5, ax=None):
    """Change to cross-style axes through the origin and fix size

    :param size: either a single number or a collection with 4 elements
                 suitable for a call to plt.axis. If a single number is given
                 it is the size of the axis on all sides of the origin

    :param ax:   the axis to set. If None, the current axis is used.
    """

    if ax is None:
        ax = plt.gca()
    if not isinstance(size, (list, tuple)):
        size = [-size, size, -size, size]
    ax.axis(size)
    # from http://stackoverflow.com/questions/25689238/show-origin-axis-x-y-in-matplotlib-plot
    ax.spines['left'].set_position('zero')

    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()

    # set the y-spine
    ax.spines['bottom'].set_position('zero')

    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()
    
    # Set axis to equal aspect ratio
    ax.set_aspect('equal')
