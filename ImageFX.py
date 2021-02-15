'''
Set of tools for fun effects on images
'''

# Imports
import os
import cv2
import functools
import numpy as np

from Utils import VideoUtils
from Utils import EffectsLibrary

# Main Functions

# Driver Code
# Params
imgPath = 'TestImgs/Test_Small.jpg' #TYPE: FILE

imgSize = None
keepAspectRatio = False

saveDir = 'GeneratedVisualisations/Effects/'
saveName = 'Effect_CannyEdges.jpg'

CommonEffects = [
    functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240))
]
EffectFuncs = [
    [
        functools.partial(EffectsLibrary.ImageEffect_None)
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_CannyEdges, sigma=0.0, low_threshold=0.1, high_threshold=0.9)
    ]
]

display = False
save = True
# Params

# RunCode
savePath = os.path.join(saveDir, saveName)
EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=2)

# Get Image
I = VideoUtils.ReadImage(imgPath, imgSize=imgSize, keepAspectRatio=keepAspectRatio)

# Apply Effects
I_effect = EffectFunc(I)

if display:
    VideoUtils.DisplayImage(I_effect, "Effect Image")

if save:
    VideoUtils.SaveImage(I_effect, savePath)