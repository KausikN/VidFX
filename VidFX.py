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
        functools.partial(EffectsLibrary.ImageEffect_Resize, size=(32*2, 24*2)),
        functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240), interpolation=cv2.INTER_NEAREST),
        functools.partial(EffectsLibrary.ImageEffect_BinValues, bins=list(range(0, 251, 50)))
    ]
]

display = False
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

VideoUtils.VideoEffect(videoPath, savePath, EffectFunc, max_frames=max_frames, speedUp=speedUp, fps=fps, size=None)