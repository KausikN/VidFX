'''
Plot Effects Library
'''

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Main Vars
fig = Figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
# Loader Functions
def SetupPlots():
    global fig
    global canvas
    fig = Figure()
    canvas = FigureCanvasAgg(fig)

# Effect Functions
def ImageEffect_PlotValueCount(I, showAxis=True):
    global fig
    global canvas
    fig.clear(True)
    ax = fig.add_subplot(111)
    if not showAxis:
        ax.axis('off')
    fig.tight_layout(pad=0)

    I_g = np.mean(I, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.bar(values, counts)

    ax.margins(0)
    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    return I_effect

# Driver Code
# Resize(size=(320, 240))