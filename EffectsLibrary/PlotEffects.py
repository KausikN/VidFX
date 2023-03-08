'''
Plot Effects Library
'''

# Imports
from .EffectUtils import *

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

    I_g = np.mean(I[:, :, :3] * 255, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.bar(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = np.asarray(buf)

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

    I_g = np.mean(I[:, :, :3] * 255, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.plot(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = np.asarray(buf)

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

    I_g = np.mean(I[:, :, :3] * 255, axis=2, dtype=int).reshape(-1)
    I_g = np.append(I_g, range(0, 255))

    values, counts = np.unique(I_g.reshape(-1), return_counts=True, axis=0)
    counts = counts - 1
    ax.scatter(values[skipStart:], counts[skipStart:])

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_effect = np.asarray(buf)

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

    I_g = np.mean(I[:, :, :3] * 255, axis=2, dtype=int).reshape(-1)
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
    I_effect = np.asarray(buf)

    return I_effect

# Main Vars
EFFECTFUNCS_PLOT = {
    "ValueCount_BarPlot": {
        "name": "ValueCount_BarPlot",
        "code": "ValueCount_BarPlot(showAxis=True)",
        "func": ImageEffect_ValueCount_BarPlot,
        "params": {
            "showAxis": True
        }
    },
    "ValueCount_LinePlot": {
        "name": "ValueCount_LinePlot",
        "code": "ValueCount_LinePlot(showAxis=True)",
        "func": ImageEffect_ValueCount_LinePlot,
        "params": {
            "showAxis": True
        }
    },
    "ValueCount_PointPlot": {
        "name": "ValueCount_PointPlot",
        "code": "ValueCount_PointPlot(showAxis=True)",
        "func": ImageEffect_ValueCount_PointPlot,
        "params": {
            "showAxis": True
        }
    },
    "ValueCount_Plot": {
        "name": "ValueCount_Plot",
        "code": "ValueCount_Plot(plots=['bar', 'point', 'line'], showAxis=True)",
        "func": ImageEffect_ValueCount_Plot,
        "params": {
            "plots": ['bar', 'point', 'line'],
            "showAxis": True
        }
    }
}