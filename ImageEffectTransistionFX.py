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
imgPath = 'TestImgs/Horse.PNG' #TYPE: FILE

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
            EffectsLibrary.ImageEffect_Rotate,
            {
                "angle": functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=0.0, end=720.0)
            }
        ],
        [
            EffectsLibrary.ImageEffect_Scale,
            {
                "scale": [
                    functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=1.0, end=0.0),
                    functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=1.0, end=0.0)
                ]
            }
        ],
        [
            EffectsLibrary.ImageEffect_Translate,
            {
                "offset": [
                    functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=0, end=0.5),
                    functools.partial(EffectTransistionUtils.EffectTransistion_Linear, start=0, end=0.5)
                ]
            }
        ]
    ]
]
MainEffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages, nCols=2)

frameCount = 50

speedUp = 1
fps = 20.0

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
EffectTransistionUtils.ImageEffectTransistion(I, EffectFunctions, pathOut=savePath, max_frames=frameCount, speedUp=speedUp, fps=fps, size=None, display=display, save=save, recursiveArgs=recursiveArgs)