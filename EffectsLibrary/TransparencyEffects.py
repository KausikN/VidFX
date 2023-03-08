'''
Transparency Image Effects Library
'''

# Imports
from .EffectUtils import *

# Main Functions
def ImageEffect_ColorKeyTransparent(I, keyColor=[0.0, 0.0, 0.0]):
    I_filtered = np.array(I)
    I_filtered[:, :, 3] = np.logical_not(np.all((I_filtered[:, :, :3] == keyColor), axis=-1))
    return I_filtered

# Main Vars
EFFECTFUNCS_TRANSPARENCY = {
    "ColorKeyTransparent": {
        "name": "ColorKeyTransparent",
        "code": "ColorKeyTransparent(keyColor=[0.0, 0.0, 0.0])",
        "func": ImageEffect_ColorKeyTransparent,
        "params": {
            "keyColor": [0.0, 0.0, 0.0]
        }
    }
}