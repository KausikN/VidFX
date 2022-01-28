'''
Image Effects Library
'''

# Imports
import cv2
import math
import functools
import numpy as np
# import skimage
# import skimage.feature

# Main Vars
# savedIs = None

# Main Functions
def ImageEffect_Substitute(I, key):
    global savedIs
    if key in savedIs.keys():
        return savedIs[key]
    else:
        # print(key, savedIs.keys())
        return I

# Combination Effects
def ImageEffect_Add(I, keys, keepOriginalSizes=False, normaliseFit=False):
    global savedIs

    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

    I_effect = np.zeros(tuple(size), dtype=float)
    for key in keys:
        if key in savedIs.keys():
            I_alphaApplied = ApplyAlphaToImage(savedIs[key])
            I_effect = I_effect + cv2.resize(I_alphaApplied, tuple(size[:2][::-1])) # With Alpha

    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

def ImageEffect_Sub(I, keys, keepOriginalSizes=False, normaliseFit=False):
    global savedIs

    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

    I_effect = np.ones(tuple(size), dtype=float)
    if len(keys) > 0:
        I_alphaApplied = ApplyAlphaToImage(savedIs[keys[0]])
        I_effect = cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
    for i in range(1, len(keys)):
        key = keys[i]
        if key in savedIs.keys():
            I_alphaApplied = ApplyAlphaToImage(savedIs[key])
            I_effect = I_effect - cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))

    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

def ImageEffect_Avg(I, keys, keepOriginalSizes=False, normaliseFit=False):
    global savedIs

    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

    I_effect = np.zeros(tuple(size), dtype=float)
    for key in keys:
        if key in savedIs.keys():
            I_alphaApplied = ApplyAlphaToImage(savedIs[key])
            I_effect = I_effect + cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
    I_effect = I_effect / max(1, len(keys))

    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

def ImageEffect_Mul(I, keys, keepOriginalSizes=False, normaliseFit=False):
    global savedIs

    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

    I_effect = np.ones(tuple(size), dtype=float)
    for key in keys:
        if key in savedIs.keys():
            I_alphaApplied = ApplyAlphaToImage(savedIs[key])
            I_effect = I_effect * cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))

    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

# Main Vars
EFFECTFUNCS_COMBINATION = [
    {
        "name": "Substitute",
        "code": "Substitute(key)",
        "func": ImageEffect_Substitute,
        "params": [
            {
                "name": "key",
                "type": "str",
                "default": "0_0",
            }
        ]
    },
    {
        "name": "Add",
        "code": "Add(keys, keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Add,
        "params": [
            {
                "name": "keys",
                "type": "list:str",
                "default": ["0_0", "0_1"]
            },
            {
                "name": "keepOriginalSizes",
                "type": "bool",
                "default": False
            },
            {
                "name": "normaliseFit",
                "type": "bool",
                "default": False
            }
        ]
    },
    {
        "name": "Sub",
        "code": "Sub(keys, keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Sub,
        "params": [
            {
                "name": "keys",
                "type": "list:str",
                "default": ["0_0", "0_1"]
            },
            {
                "name": "keepOriginalSizes",
                "type": "bool",
                "default": False
            },
            {
                "name": "normaliseFit",
                "type": "bool",
                "default": False
            }
        ]
    },
    {
        "name": "Avg",
        "code": "Avg(keys, keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Avg,
        "params": [
            {
                "name": "keys",
                "type": "list:str",
                "default": ["0_0", "0_1"]
            },
            {
                "name": "keepOriginalSizes",
                "type": "bool",
                "default": False
            },
            {
                "name": "normaliseFit",
                "type": "bool",
                "default": False
            }
        ]
    },
    {
        "name": "Mul",
        "code": "Mul(keys, keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Mul,
        "params": [
            {
                "name": "keys",
                "type": "list:str",
                "default": ["0_0", "0_1"]
            },
            {
                "name": "keepOriginalSizes",
                "type": "bool",
                "default": False
            },
            {
                "name": "normaliseFit",
                "type": "bool",
                "default": False
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_COMBINATION)

# Driver Code