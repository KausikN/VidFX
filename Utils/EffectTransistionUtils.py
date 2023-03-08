'''
Library for basic video functions
'''

# Imports
import os
import cv2
import functools
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from Utils import VideoUtils

# Main Functions
# Utils Functions

# Image Effect Transistions
def EffectTransistion_Apply(I, EFFECT_TREE, TREE_APPLY_FUNC, n_frames=2, PROGRESS_BAR=None):
    '''
    Effect Transistion - Apply
    '''
    # Init
    Transistion_Is = []
    FRAME_PROPS = np.linspace(0.0, 1.0, n_frames)
    # Loop
    for i in range(n_frames):
        ## Update Current Params for each node
        for nk in EFFECT_TREE["nodes"].keys():
            CurParams = {
                pk: EFFECT_TREE["nodes"][nk].parent.effect["transistion"][pk]["transistion"]["func"](
                    FRAME_PROPS[i],
                    EFFECT_TREE["nodes"][nk].parent.effect["transistion"][pk]["start"],
                    EFFECT_TREE["nodes"][nk].parent.effect["transistion"][pk]["end"],
                    **EFFECT_TREE["nodes"][nk].parent.effect["transistion"][pk]["transistion"]["params"]
                )
                for pk in EFFECT_TREE["nodes"][nk].parent.effect["params"].keys()
            }
            EFFECT_TREE["nodes"][nk].parent.effect["params"] = CurParams
            print(i, nk, EFFECT_TREE["nodes"][nk].parent.effect["params"])
        ## Apply and Record
        frame = TREE_APPLY_FUNC(I, EFFECT_TREE=EFFECT_TREE)
        Transistion_Is.append(frame)
        ## Update Progress Bar
        if not PROGRESS_BAR == None: PROGRESS_BAR((i+1)/n_frames)
    
    return Transistion_Is

# Transistion Selector Functions
def EffectTransistionSelect_Basic(param_start, param_end):
    '''
    Effect Transistion Select - Basic
    '''
    # Select Based on param type
    # Non Numeric
    if param_start is None or param_end is None:
        return ["Constant", "Switch"]
    if isinstance(param_start, str) or isinstance(param_end, str):
        return ["Constant", "Switch"]
    # Numeric
    if isinstance(param_start, int) and isinstance(param_end, int):
        return list(TRANSISTION_FUNCS.keys())
    if isinstance(param_start, float) and isinstance(param_end, float):
        return list(TRANSISTION_FUNCS.keys())
    # N-D Array
    if isinstance(param_start, list) and isinstance(param_end, list):
        param_start_elem = param_start
        while isinstance(param_start_elem, list): param_start_elem = param_start_elem[0]
        param_end_elem = param_end
        while isinstance(param_end_elem, list): param_end_elem = param_end_elem[0]
        return EffectTransistionSelect_Basic(param_start_elem, param_end_elem)
    # Unknown
    return ["Constant", "Switch"]

# Transistion Functions
def EffectTransistion_Constant(prop, start, end):
    '''
    Effect Transistion - Constant
    '''
    return start

def EffectTransistion_Switch(prop, start, end, threshold=0.5):
    '''
    Effect Transistion - Switch
    '''
    return start if prop < threshold else end

def EffectTransistion_Linear(prop, start, end):
    '''
    Effect Transistion - Linear
    '''
    return start + (end-start)*prop

def EffectTransistion_Sin(prop, start, end, frequency=1.0):
    '''
    Effect Transistion - Sin
    '''
    return start + (end-start)*np.sin(prop*(2*np.pi)*frequency)

# Main Vars
TRANSISTION_FUNCS = {
    "Constant": {
        "func": EffectTransistion_Constant,
        "params": {}
    },
    "Switch": {
        "func": EffectTransistion_Switch,
        "params": {
            "threshold": 0.5
        }
    },
    "Linear": {
        "func": EffectTransistion_Linear,
        "params": {}
    },
    "Sin": {
        "func": EffectTransistion_Sin,
        "params": {
            "frequency": 1.0
        }
    }
}