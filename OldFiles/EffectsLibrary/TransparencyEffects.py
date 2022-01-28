'''
Transparency Image Effects Library
'''

# Imports
import cv2
import numpy as np

# Main Functions
def ImageEffect_ColorKeyTransparent(I, keyColor=[0, 0, 0]):
    if I.shape[2] == 3:
        I = cv2.cvtColor(I, cv2.COLOR_RGB2RGBA)
    I_filtered = np.array(I, dtype=np.uint8)
    I_filtered[:, :, 3] = np.logical_not(np.all((I_filtered[:, :, :3] == keyColor), axis=-1)) * 255
    return I_filtered

# Driver Code