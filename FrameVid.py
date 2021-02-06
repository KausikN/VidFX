'''
Put a video inside a frame
'''

# Imports
import os
import functools
import numpy as np

from Utils import VideoUtils
from Utils import EffectsLibrary

# Main Functions
def GetFillBoxFromFrameName(framePath):
    frameName = os.path.splitext(os.path.basename(framePath))[0]
    frameData = frameName.split('_')[2:]
    FillBox = [[int(frameData[0])/int(frameData[2]), int(frameData[1])/int(frameData[2])], [int(frameData[3])/int(frameData[5]), int(frameData[4])/int(frameData[5])]]
    return FillBox

# Driver Code
# Params
webcamVideo = True
videoPath = 'TestVids/Test_Earth.wmv'

fps = 20.0
max_frames = 500
speedUp = 5

savePath = 'TestVids/Test_Effect.gif'

framePath = 'Frames/Frame_Nintendo_111_303_430_107_285_607.PNG'
frameSize = None

EffectFuncs = [
    functools.partial(EffectsLibrary.ImageEffect_Resize, size=(32*2, 24*2)),
    functools.partial(EffectsLibrary.ImageEffect_GreyScale),
    functools.partial(EffectsLibrary.ImageEffect_ScaleValues, scaleFactor=[0, 1, 0])
]

display = False
save = True
# Params

# RunCode
Frame = VideoUtils.ReadImage(framePath, imgSize=frameSize, keepAspectRatio=False)
fillBox = GetFillBoxFromFrameName(framePath)
EffectFuncs = EffectFuncs + [
    functools.partial(EffectsLibrary.ImageEffect_AddFrame, FrameImage=Frame, ImageReplaceBox=fillBox)
]
EffectFunc = functools.partial(EffectsLibrary.Image_ApplyEffects, EffectFuncs=EffectFuncs)

# Get Video Feed
videoFeed = None
if webcamVideo:
    videoFeed = VideoUtils.WebcamVideo()
else:
    videoFeed = VideoUtils.ReadVideo(videoPath)

if display:
    VideoUtils.DisplayVideo(vid=videoFeed, EffectFunc=EffectFunc)

if save:
    VideoUtils.VideoEffect(videoPath, savePath, EffectFunc, max_frames=max_frames, speedUp=speedUp, fps=fps, size=None)