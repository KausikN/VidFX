'''
Set of tools for effect transistions on image
'''

# Imports
import os
import cv2
import functools
import numpy as np

from Utils import EffectTransistionUtils
from Utils import VideoUtils
from EffectsLibrary import EffectsLibrary

# Main Functions

# Driver Code
# Params
imgPath = 'TestImgs/Test.jpg' #TYPE: FILE

imgSize = None
keepAspectRatio = False

saveDir = 'GeneratedVisualisations/Effects/'
saveName = 'Rev.gif'

CommonEffects = [
    [
        functools.partial(EffectsLibrary.ImageEffect_None)
    ]
]
EffectFuncs = [
    [
        [
            EffectsLibrary.ImageEffect_ScaleValues, 
            {
                "scaleFactor": [
                functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=0, end=2),
                functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=0, end=2),
                functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=0, end=2)
            ]
            }
        ]
    ]
]
MainEffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages, nCols=2)

frameCount = 50

display = False
save = True
recursiveArgs = False
# Params

# RunCode
savePath = os.path.join(saveDir, saveName)
EffectFunctions = {
    "Main": MainEffectFunc,
    "Common": CommonEffects,
    "Effect": EffectFuncs
}

# Get Image
I = VideoUtils.ReadImage(imgPath, imgSize=imgSize, keepAspectRatio=keepAspectRatio)

# Apply Effects
EffectTransistionUtils.ImageEffectTransistion(I, EffectFunctions, pathOut=savePath, max_frames=frameCount, speedUp=1, fps=20.0, size=None, display=display, save=save, recursiveArgs=recursiveArgs)