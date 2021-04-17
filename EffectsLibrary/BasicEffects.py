'''
Basic Image Effects Library
'''

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Main Functions
def ImageEffect_None(I):
    return I

def ImageEffect_Binarise(I, threshold=127):
    # threshold = int(threshold)
    I = np.zeros(I.shape, dtype=np.uint8) + (I >= threshold)*np.ones(I.shape, dtype=np.uint8)*255
    return I

def ImageEffect_GreyScale(I):
    # I_effect = cv2.cvtColor(cv2.cvtColor(I, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
    I_effect = np.mean(I, axis=2)
    I_effect = np.dstack((I_effect, I_effect, I_effect))
    return I_effect

def ImageEffect_Grey2RGB(I):
    return cv2.cvtColor(I, cv2.COLOR_GRAY2RGB)

def ImageEffect_RGB2BGR(I):
    return cv2.cvtColor(I, cv2.COLOR_RGB2BGR)

def ImageEffect_RedChannel(I):
    return I[:, :, :] * np.array([1, 0, 0])

def ImageEffect_BlueChannel(I):
    return I[:, :, :] * np.array([0, 0, 1])

def ImageEffect_GreenChannel(I):
    return I[:, :, :] * np.array([0, 1, 0])

def ImageEffect_Invert(I):
    return 255 - I

def ImageEffect_MostDominantColor(I):
    I_dom = np.max(I, axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    return (I)*(I_dom == I)

def ImageEffect_LeastDominantColor(I):
    I_dom = np.min(I, axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    return (I)*(I_dom == I)

def ImageEffect_ScaleValues(I, scaleFactor=[0, 0, 0]):
    I = np.multiply(I, np.array(scaleFactor, dtype=float)).astype(int)
    I = np.clip(I, 0, 255, dtype=int).astype(np.uint8)
    return I

def ImageEffect_ClipValues(I, threshold=[127, 128], replace=[127, 128]):
    I = np.clip(I, threshold[0], threshold[1])
    lowCheck = (I == threshold[0])
    highCheck = (I == threshold[1])
    I = lowCheck*np.ones(I.shape, dtype=np.uint8)*replace[0] + highCheck*np.ones(I.shape, dtype=np.uint8)*replace[1] + np.logical_not(np.logical_or(lowCheck, highCheck))*I
    return I

def ImageEffect_BinValues(I, bins=[0, 127, 255]):
    bins = np.array(bins)
    binMaps = np.digitize(I, bins)
    binMaps = np.clip(binMaps, 0, bins.shape[0]-1)
    return bins[binMaps]

def ImageEffect_Resize(I, size=(480, 640), interpolation=cv2.INTER_LINEAR):
    return cv2.resize(I, size, interpolation=interpolation)

def ImageEffect_Mirror(I):
    I_effect = I[:, ::-1]
    return I_effect

# Driver Code