'''
Set of tools for video editing and fun video effects
'''

# Imports
import cv2
import functools
import numpy as np

from Utils import VideoUtils
from EffectsLibrary import EffectsLibrary

# Main Vars
funcKeyVals = {}

# Main Functions
def UICommonEffectsCodeParser(data, funcKeyFuncs=['FrameDelay']):
    # INPUT FORMAT
    # <EffectFuncName>(<Param1Name>=<Param1Value>, <Param2Name>=<Param2Value>, ...)
    # OUTPUT FORMAT
    # functools.partial(<EffectFuncName>, <Param1Name>=<Param1Value>, <Param2Name>=<Param2Value>, ...)

    global funcKeyVals

    data = data.split('\n')

    parsedData = []
    for line in data:
        line = line.strip()
        if line in ['', '[', ']', ',']:
            continue
        else:
            funcnameShort = line.split('(')[0].strip()
            funcname = "EffectsLibrary.ImageEffect_" + funcnameShort
            paramText = '('.join(line.split('(')[1:]).rstrip(',')
            if paramText.endswith(')'):
                paramText = paramText[:-1]
            if not paramText.strip() == "":
                paramText = ", " + paramText

            # Check for funcKey needing Funcs
            if funcnameShort in funcKeyFuncs:
                if funcnameShort in funcKeyVals.keys():
                    funcKeyVals[funcnameShort] += 1
                else:
                    funcKeyVals[funcnameShort] = 0
                paramText = paramText + ", funcKey=" + "'" + funcnameShort + "_" + str(funcKeyVals[funcnameShort]) + "'"

            parsedData.append('functools.partial(' + funcname + paramText + ')')
    
    parsedData = "[\n" + ',\n'.join(parsedData) + "\n]"

    return parsedData

def UIMultiEffectsCodeParser(data):
    # GAP BETWEEN EFFECTS is a line with only ',' in it

    data = data.split('\n')

    parsedData = []
    parsedCurEffectData = []
    for line in data:
        line = line.strip()
        if line in ['[', ']']:
            continue
        elif line in ['', ',']:
            if len(parsedCurEffectData) > 0:
                parsedCurEffectData = UICommonEffectsCodeParser('\n'.join(parsedCurEffectData))
                parsedData.append(parsedCurEffectData)
                parsedCurEffectData = []
        else:
            parsedCurEffectData.append(line)
    if len(parsedCurEffectData) > 0:
        parsedCurEffectData = UICommonEffectsCodeParser('\n'.join(parsedCurEffectData))
        parsedData.append(parsedCurEffectData)
        parsedCurEffectData = []

    
    parsedData = "[\n" + ',\n'.join(parsedData) + "]"

    return parsedData

# Test Code
# data = '''None
# 123
# ,
# Resize
# 213
# ,
# Haha
# 12321'''
# print(UIMultiEffectsCodeParser(data))
# Driver Code
# # Params
# webcamVideo = True
# videoPath = 'TestVids/Test_Animation.wmv' #TYPE: FILE

# fps = 20.0
# max_frames = 500
# speedUp = 5

# savePath = 'TestVids/Test_Effect.gif'

# CommonEffects = [
#     functools.partial(EffectsLibrary.ImageEffect_Resize, size=(320, 240))
# ]
# EffectFuncs = [
#     [
#         functools.partial(EffectsLibrary.ImageEffect_GreyScale)
#     ], 
#     [
#         functools.partial(EffectsLibrary.ImageEffect_ValueCount_PointPlot, showAxis=False)
#     ]
# ]

# display = True
# save = False
# nCols = 2
# fastExec = True
# # Params

# # RunCode
# # Get Video Feed
# if fastExec:
#     EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=True)
#     EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=nCols, saveI_keys=saveI_keys)
# else:
#     EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=nCols)

# videoFeed = None
# if webcamVideo:
#     videoFeed = VideoUtils.WebcamVideo()
# else:
#     videoFeed = VideoUtils.ReadVideo(videoPath)

# if display:
#     VideoUtils.DisplayVideo(vid=videoFeed, EffectFunc=EffectFunc)

# if save:
#     VideoUtils.VideoEffect(videoPath, savePath, EffectFunc, max_frames=max_frames, speedUp=speedUp, fps=fps, size=None)