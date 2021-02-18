'''
Set of tools for fun effects on images
'''

# Imports
import os
import cv2
import functools
import numpy as np

from Utils import VideoUtils
from EffectsLibrary import EffectsLibrary

# Main Functions

# Driver Code
# Params
imgPath = 'TestImgs/Horse.PNG' #TYPE: FILE

imgSize = None
keepAspectRatio = False

saveDir = 'GeneratedVisualisations/Effects/'
saveName = 'Effect_GaussianFilter.jpg'

CommonEffects = [
    functools.partial(EffectsLibrary.ImageEffect_None)
]
EffectFuncs = [
    [
        functools.partial(EffectsLibrary.ImageEffect_GreyScale),
        functools.partial(EffectsLibrary.ImageEffect_Binarise, threshold=127)
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_Skeleton)
    ]
]

display = True
save = False
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