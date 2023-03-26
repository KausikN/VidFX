'''
Time based Image Effects Library
'''

# Imports
from .EffectUtils import *

# Main Functions
# Effect Functions
def ImageEffect_FrameDelay(I, delay=12, **params):
    global EFFECT_TREE
    # Init
    if delay < 1: return I
    NODE = params["node"]
    PARENT_NODE = NODE.parent.start
    # Update History Length
    if PARENT_NODE.history_length < (delay+1): PARENT_NODE.history_length = delay+1
    # Get Delayed Frame
    output = None
    if len(PARENT_NODE.history) == 0: output = I
    elif len(PARENT_NODE.history) < (delay+1): output = PARENT_NODE.history[0]
    else: output = PARENT_NODE.history[-(delay+1)]

    return output

# Main Vars
EFFECTFUNCS_TIME = {
    "FrameDelay": {
        "name": "FrameDelay",
        "code": "FrameDelay(delay=12)",
        "func": ImageEffect_FrameDelay,
        "params": {
            "delay": 12
        }
    },
}