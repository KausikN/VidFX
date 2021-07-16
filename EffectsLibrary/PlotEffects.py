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
figsize = (6.4, 4.8)
dpi = 100.0
fig = Figure(figsize=figsize, dpi=dpi)
canvas = FigureCanvasAgg(fig)

skipStart = 0

# Main Functions
# Loader Functions
def SetupPlots():
    global fig
    global canvas
    fig = Figure(dpi=dpi)
    canvas = FigureCanvasAgg(fig)

# Effect Functions
def ImageEffect_ValueCount_BarPlot(I, showAxis=True):
    global fig
    global canvas
    fig.clear(True)
    ax = fig.add_subplot(111)
    if not showAxis:
        ax.axis('off')
        ax.margins(0)
        fig.tight_layout(pad=0)

    I_g = np.mean(I, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.bar(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    return I_effect

def ImageEffect_ValueCount_LinePlot(I, showAxis=True):
    global fig
    global canvas
    fig.clear(True)
    ax = fig.add_subplot(111)
    if not showAxis:
        ax.axis('off')
        ax.margins(0)
        fig.tight_layout(pad=0)

    I_g = np.mean(I, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.plot(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    return I_effect

def ImageEffect_ValueCount_PointPlot(I, showAxis=True):
    global fig
    global canvas
    fig.clear(True)
    ax = fig.add_subplot(111)
    if not showAxis:
        ax.axis('off')
        ax.margins(0)
        fig.tight_layout(pad=0)

    I_g = np.mean(I, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.scatter(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    return I_effect

def ImageEffect_ValueCount_Plot(I, plots=['bar', 'point', 'line'], showAxis=True):
    global fig
    global canvas
    fig.clear(True)
    ax = fig.add_subplot(111)
    if not showAxis:
        ax.axis('off')
        ax.margins(0)
        fig.tight_layout(pad=0)

    I_g = np.mean(I, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1

    if 'bar' in plots:
        ax.bar(values[skipStart:], counts[skipStart:])
    if 'line' in plots:
        ax.plot(values[skipStart:], counts[skipStart:])
    if 'point' in plots:
        ax.scatter(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    return I_effect

# Driver Code
# Resize(size=(320, 240))
# GreyScale
# ,
# PlotValueCount
# fig = Figure()
# canvas = FigureCanvasAgg(fig)
# # print(dir(fig))
# print(fig.get_figwidth(), fig.get_dpi())