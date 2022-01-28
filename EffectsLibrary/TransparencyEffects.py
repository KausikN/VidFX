'''
Transparency Image Effects Library
'''

# Imports
import cv2
import numpy as np

# Main Functions
def ImageEffect_ColorKeyTransparent(I, keyColor=[0.0, 0.0, 0.0]):
    I_filtered = np.array(I)
    I_filtered[:, :, 3] = np.logical_not(np.all((I_filtered[:, :, :3] == keyColor), axis=-1))
    return I_filtered

# Main Vars
EFFECTFUNCS_TRANSPARENCY = [
    {
        "name": "ColorKeyTransparent",
        "code": "ColorKeyTransparent(keyColor=[0.0, 0.0, 0.0])",
        "func": ImageEffect_ColorKeyTransparent,
        "params": [
            {
                "name": "keyColor",
                "default": [0.0, 0.0, 0.0],
                "type": "list:float"
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_TRANSPARENCY)

# Driver Code