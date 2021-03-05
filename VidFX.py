'''
Set of tools for video editing and fun video effects
'''

# Imports
import cv2
import functools
import numpy as np

from Utils import VideoUtils
from EffectsLibrary import EffectsLibrary

# Main Functions

# Driver Code
# Params
webcamVideo = True
videoPath = 'TestVids/Test_Animation.wmv' #TYPE: FILE

fps = 20.0
max_frames = 500
speedUp = 5

savePath = 'TestVids/Test_Effect.gif'

CommonEffects = [
    functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240))
]
EffectFuncs = [
    [
        functools.partial(EffectsLibrary.ImageEffect_Binarise, threshold=127)
    ], 
    [
        functools.partial(EffectsLibrary.ImageEffect_Binarise, threshold=127)
    ]
]

display = True
save = False
nCols = 2
fastExec = True
# Params

# RunCode
# Get Video Feed
if fastExec:
    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=True)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=nCols, saveI_keys=saveI_keys)
else:
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=nCols)

videoFeed = None
if webcamVideo:
    videoFeed = VideoUtils.WebcamVideo()
else:
    videoFeed = VideoUtils.ReadVideo(videoPath)

if display:
    VideoUtils.DisplayVideo(vid=videoFeed, EffectFunc=EffectFunc)

if save:
    VideoUtils.VideoEffect(videoPath, savePath, EffectFunc, max_frames=max_frames, speedUp=speedUp, fps=fps, size=None)