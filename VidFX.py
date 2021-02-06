'''
Set of tools for video editing and fun video effects
'''

# Imports
import functools
import numpy as np

from Utils import VideoUtils
from Utils import EffectsLibrary

# Main Functions

# Driver Code
# Params
webcamVideo = True
videoPath = 'TestVids/test.mp4'

CommonEffects = [
    functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240)),
]
EffectFuncs = [
    [
        functools.partial(EffectsLibrary.ImageEffect_MostDominantColor)
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_GreyScale),
        functools.partial(EffectsLibrary.ImageEffect_Binarise, threshold=100)
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_BinValues, bins=np.array([0, 64, 127, 200, 255]))
    ],
    [
        functools.partial(EffectsLibrary.ImageEffect_Binarise, threshold=200)
    ]
]

display = True
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