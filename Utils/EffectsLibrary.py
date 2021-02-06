'''
Image Effects Library
'''

# Imports
import cv2
import math
import numpy as np

# Main Functions
# Effect Applier Functions
def Image_MultipleImages(I, CommonEffects, EffectFuncs, nCols=2):
    for CommonEffect in CommonEffects:
        I = CommonEffect(I)

    if len(EffectFuncs) < nCols:
        nCols = len(EffectFuncs)
    nRows = int(math.ceil(len(EffectFuncs) / nCols))
    I_full = np.zeros((I.shape[0]*nRows, I.shape[1]*nCols, 3), dtype=np.uint8)
    curPos = [0, 0]

    for EffectFuncs_Image in EffectFuncs:
        I_this = np.copy(I)
        for EffectFunc in EffectFuncs_Image:
            I_this = EffectFunc(I_this)
        if I_this.ndim == 2:
            I_this = cv2.cvtColor(I_this, cv2.COLOR_GRAY2RGB)
        if not np.equal(I.shape[:2], I_this.shape[:2]).all():
            I_this = cv2.resize(I_this, (I.shape[0], I.shape[1]))
        I_full[curPos[0]*I.shape[0]:(curPos[0]+1)*I.shape[0], curPos[1]*I.shape[1]:(curPos[1]+1)*I.shape[1], :] = I_this[:, :, :]
        curPos = [curPos[0], curPos[1]+1]
        if curPos[1] >= nCols:
            curPos = [curPos[0]+1, 0]
    return I_full

def Image_ApplyEffects(I, EffectFuncs):
    for EffectFunc in EffectFuncs:
        I = EffectFunc(I)
    return I

# Effect Functions
def ImageEffect_None(I):
    return I

def ImageEffect_Binarise(I, threshold=127):
    I = np.zeros(I.shape, dtype=np.uint8) + (I > threshold)*np.ones(I.shape, dtype=np.uint8)*255
    return I

def ImageEffect_GreyScale(I):
    return cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)

def ImageEffect_BGR(I):
    return cv2.cvtColor(I, cv2.COLOR_RGB2BGR)

def ImageEffect_MostDominantColor(I):
    I_dom = np.max(I, axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    return (I)*(I_dom == I)

def ImageEffect_LeastDominantColor(I):
    I_dom = np.min(I, axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    return (I)*(I_dom == I)

def ImageEffect_ClipValues(I, threshold=[127, 128], replace=[127, 128]):
    I = np.clip(I, threshold[0], threshold[1])
    lowCheck = (I == threshold[0])
    highCheck = (I == threshold[1])
    I = lowCheck*np.ones(I.shape, dtype=np.uint8)*replace[0] + highCheck*np.ones(I.shape, dtype=np.uint8)*replace[1] + np.logical_not(np.logical_or(lowCheck, highCheck))*I
    return I

def ImageEffect_BinValues(I, bins=np.array([0, 127, 255])):
    bins = np.array(bins)
    binMaps = np.digitize(I, bins)
    binMaps = np.clip(binMaps, 0, bins.shape[0]-1)
    return bins[binMaps]

def ImageEffect_Resize(I, size=(480, 640)):
    return cv2.resize(I, size)

# Driver Code
# I = [[[100, 22, 3], [10, 1, 0], [0, 9, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
# I = np.array(I)

# bins = np.linspace(0, 255, 10, dtype=np.uint8)
# print(bins)
# ImageEffect_BinValues(I, bins=bins)