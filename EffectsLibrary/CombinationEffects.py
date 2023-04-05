'''
Image Effects Library
'''

# Imports
from .EffectUtils import *

# Main Functions
def ImageEffect_Substitute(I, key=EFFECT_TREE_ROOT_ID, **params):
    EFFECT_TREE = params["node"].parent.effect_tree_pointer
    # Substitute
    if key in EFFECT_TREE["nodes"].keys():
        return EFFECT_TREE["nodes"][key].I
    elif key == EFFECT_TREE_ROOT_ID:
        return EFFECT_TREE["root"].I
    else:
        # print(key)
        return I

# Combination Effects
def ImageEffect_Add(I, keys=[EFFECT_TREE_ROOT_ID], keepOriginalSizes=False, normaliseFit=False, **params):
    EFFECT_TREE = params["node"].parent.effect_tree_pointer
    # Check
    if len(keys) == 0: return I
    # Init
    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes, EFFECT_TREE=EFFECT_TREE)
    # Add
    I_effect = np.zeros(tuple(size), dtype=float)
    for key in keys:
        I_cur = I
        if key == EFFECT_TREE_ROOT_ID:
            I_cur = EFFECT_TREE["root"].I
        elif key in EFFECT_TREE["nodes"].keys():
            I_cur = EFFECT_TREE["nodes"][key].I
        I_alphaApplied = ApplyAlphaToImage(I_cur)
        I_effect = I_effect + cv2.resize(I_alphaApplied, tuple(size[:2][::-1])) # With Alpha
    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

def ImageEffect_Sub(I, keys=[EFFECT_TREE_ROOT_ID], keepOriginalSizes=False, normaliseFit=False, **params):
    EFFECT_TREE = params["node"].parent.effect_tree_pointer
    # Check
    if len(keys) == 0: return I
    # Init
    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes, EFFECT_TREE=EFFECT_TREE)
    # Subtract
    I_cur = I
    if keys[0] == EFFECT_TREE_ROOT_ID:
        I_cur = EFFECT_TREE["root"].I
    elif keys[0] in EFFECT_TREE["nodes"].keys():
        I_cur = EFFECT_TREE["nodes"][keys[0]].I
    I_alphaApplied = ApplyAlphaToImage(I_cur)
    I_effect = cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
    for i in range(1, len(keys)):
        key = keys[i]
        I_cur = I
        if key == EFFECT_TREE_ROOT_ID:
            I_cur = EFFECT_TREE["root"].I
        elif key in EFFECT_TREE["nodes"].keys():
            I_cur = EFFECT_TREE["nodes"][key].I
        I_alphaApplied = ApplyAlphaToImage(I_cur)
        I_effect = I_effect - cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

def ImageEffect_Avg(I, keys=[EFFECT_TREE_ROOT_ID], keepOriginalSizes=False, normaliseFit=False, **params):
    EFFECT_TREE = params["node"].parent.effect_tree_pointer
    # Check
    if len(keys) == 0: return I
    # Init
    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes, EFFECT_TREE=EFFECT_TREE)
    # Average
    I_effect = np.zeros(tuple(size), dtype=float)
    for key in keys:
        I_cur = I
        if key == EFFECT_TREE_ROOT_ID:
            I_cur = EFFECT_TREE["root"].I
        elif key in EFFECT_TREE["nodes"].keys():
            I_cur = EFFECT_TREE["nodes"][key].I
        I_alphaApplied = ApplyAlphaToImage(I_cur)
        I_effect = I_effect + cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
    I_effect = I_effect / max(1, len(keys))
    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

def ImageEffect_Mul(I, keys=[EFFECT_TREE_ROOT_ID], keepOriginalSizes=False, normaliseFit=False, **params):
    EFFECT_TREE = params["node"].parent.effect_tree_pointer
    # Check
    if len(keys) == 0: return I
    # Init
    size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes, EFFECT_TREE=EFFECT_TREE)
    # Multiply
    I_effect = np.ones(tuple(size), dtype=float)
    for key in keys:
        I_cur = I
        if key == EFFECT_TREE_ROOT_ID:
            I_cur = EFFECT_TREE["root"].I
        elif key in EFFECT_TREE["nodes"].keys():
            I_cur = EFFECT_TREE["nodes"][key].I
        I_alphaApplied = ApplyAlphaToImage(I_cur)
        I_effect = I_effect * cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
    I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

    return I_effect

# Main Vars
EFFECTFUNCS_COMBINATION = {
    "Substitute": {
        "name": "Substitute",
        "code": "Substitute(key='input')",
        "func": ImageEffect_Substitute,
        "params": {
            "key": "input"
        }
    },
    "Add": {
        "name": "Add",
        "code": "Add(keys=['input'], keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Add,
        "params": {
            "keys": ["input"],
            "keepOriginalSizes": False,
            "normaliseFit": False
        }
    },
    "Sub": {
        "name": "Sub",
        "code": "Sub(keys=['input'], keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Sub,
        "params": {
            "keys": ["input"],
            "keepOriginalSizes": False,
            "normaliseFit": False
        }
    },
    "Avg": {
        "name": "Avg",
        "code": "Avg(keys=['input'], keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Avg,
        "params": {
            "keys": ["input"],
            "keepOriginalSizes": False,
            "normaliseFit": False
        }
    },
    "Mul": {
        "name": "Mul",
        "code": "Mul(keys=['input'], keepOriginalSizes=False, normaliseFit=False)",
        "func": ImageEffect_Mul,
        "params": {
            "keys": ["input"],
            "keepOriginalSizes": False,
            "normaliseFit": False
        }
    }
}