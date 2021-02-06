'''
Set of tools for video editing and fun video effects
'''

# Imports
import cv2
import functools
import numpy as np

from Utils import VideoUtils
from Utils import EffectsLibrary

# Main Functions

# Driver Code
# Params
webcamVideo = False
videoPath = 'TestVids/Test_Animation.wmv'

fps = 20.0
max_frames = 500
speedUp = 5

savePath = 'TestVids/Test_Effect.gif'

CommonEffects = [
    functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240)),
]
EffectFuncs = [
    [
        functools.partial(EffectsLibrary.ImageEffect_None)
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_MostDominantColor)
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_Resize, size=(32, 24)),
        functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240)),
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_BinValues, bins=[0, 50, 100, 150, 200, 255])
    ]
]

display = False
save = True
# Params

# RunCode
# Get Video Feed
EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=2)

videoFeed = None
if webcamVideo:
    videoFeed = VideoUtils.WebcamVideo()
else:
    videoFeed = VideoUtils.ReadVideo(videoPath)

if display:
    VideoUtils.DisplayVideo(vid=videoFeed, EffectFunc=EffectFunc)

if save:
    VideoUtils.VideoEffect(videoPath, savePath, EffectFunc, max_frames=max_frames, speedUp=speedUp, fps=fps, size=None)