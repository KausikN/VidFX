'''
Image Effects Library
'''

# Imports
import cv2
import math
import numpy as np
import skimage
import skimage.feature

from Utils import VideoUtils

from EffectsLibrary.BasicEffects import *
from EffectsLibrary.FrameEffects import *
from EffectsLibrary.NoiseEffects import *
from EffectsLibrary.FilterEffects import *
from EffectsLibrary.SegmentationEffects import *

# Main Functions
# Effect Applier Functions
def Image_MultipleImages(I, CommonEffects, EffectFuncs, nCols=2):
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)

    for CommonEffect in CommonEffects:
        I = CommonEffect(I)

    if len(EffectFuncs) < nCols:
        nCols = len(EffectFuncs)
    nRows = int(math.ceil(len(EffectFuncs) / nCols))
    curPos = [0, 0]

    CommonSize = [0, 0]

    EffectedIs = []
    for EffectFuncs_Image in EffectFuncs:
        I_this = np.copy(I)
        for EffectFunc in EffectFuncs_Image:
            I_this = EffectFunc(I_this)
        if I_this.ndim == 2:
            I_this = cv2.cvtColor(I_this, cv2.COLOR_GRAY2RGB)
        # if not np.equal(I.shape[:2], I_this.shape[:2]).all():
        #     I_this = cv2.resize(I_this, (I.shape[1], I.shape[0]))
        EffectedIs.append(I_this)
        CommonSize = [max(CommonSize[0], I_this.shape[0]), max(CommonSize[1], I_this.shape[1])]

    # print("Common Size:", CommonSize)
    
    # Resize to CommonSize by appending 0s
    for i in range(len(EffectedIs)):
        PixelDiff = [CommonSize[0] - EffectedIs[i].shape[0], CommonSize[1] - EffectedIs[i].shape[1]]
        Offset = [int(PixelDiff[0]/2), int(PixelDiff[1]/2)]
        I_appended = np.zeros((CommonSize[0], CommonSize[1], 3), dtype=np.uint8)
        I_appended[Offset[0]:Offset[0]+EffectedIs[i].shape[0], Offset[1]:Offset[1]+EffectedIs[i].shape[1], :] = EffectedIs[i]
        EffectedIs[i] = I_appended

    # Append all images into 1 image
    I_full = np.zeros((CommonSize[0]*nRows, CommonSize[1]*nCols, 3), dtype=np.uint8)
    for I_this in EffectedIs:
        I_full[curPos[0]*CommonSize[0]:(curPos[0]+1)*CommonSize[0], curPos[1]*CommonSize[1]:(curPos[1]+1)*CommonSize[1], :] = I_this[:, :, :]
        curPos = [curPos[0], curPos[1]+1]
        if curPos[1] >= nCols:
            curPos = [curPos[0]+1, 0]

    I_full = cv2.cvtColor(I_full, cv2.COLOR_RGB2BGR)

    return I_full

def Image_ApplyEffects(I, EffectFuncs):
    for EffectFunc in EffectFuncs:
        I = EffectFunc(I)
    return I

# Driver Code
# I = [[[100, 22, 3], [10, 1, 0], [0, 9, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
# I = np.array(I)

# bins = np.linspace(0, 255, 10, dtype=np.uint8)
# print(bins)
# ImageEffect_BinValues(I, bins=bins)

#AddFrame(FrameFileData={"imgPath": 'Frames/Frame_Nintendo_111_303_430_107_285_607.PNG'})

# I = cv2.imread('Test.png')
# cv2.imshow('', ImageEffect_SemanticSegmentation(I))
# cv2.waitKey(0)