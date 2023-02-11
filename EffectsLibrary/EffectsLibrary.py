'''
Image Effects Library
'''

# Imports
import os
import cv2
import math
import functools
import numpy as np
# import skimage
# import skimage.feature

from Utils import VideoUtils

# Main Vars
savedIs = None
PIXELDATA_DIMENSIONS = 4 # RGB - 3, RGBA - 4

# Utils Functions
def LoadModule(moduleName="CombinationEffects"):
    global savedIs
    modulePath = os.path.dirname(os.path.relpath(__file__)) + "/" + moduleName + ".py"
    exec(open(modulePath).read(), globals())

# Load Effect Modules
AVAILABLE_EFFECTS = []
EFFECT_MODULES = [
    "BasicEffects",
    "CombinationEffects",
    "TimeEffects",
    "FrameEffects",
    "NoiseEffects",
    "FilterEffects",
    "SegmentationEffects",
    "MorphologicalEffects",
    "TerrainGenEffects",
    "PlotEffects",
    "TransparencyEffects",
    "ShufflingEffects",
    "QRBarEffects"
]
for module in EFFECT_MODULES:
    LoadModule(module)

# Main Functions
def ApplyAlphaToImage(I):
    I_ra = I[:, :, 0] * (I[:, :, 3])
    I_ga = I[:, :, 1] * (I[:, :, 3])
    I_ba = I[:, :, 2] * (I[:, :, 3])
    I_aa = np.dstack((I_ra, I_ga, I_ba, np.ones(I.shape[:2], dtype=float)))
    return np.array(I_aa, dtype=float)

def NormaliseSize(keys, keepOriginalSizes=False):
    global savedIs

    size = [100, 100, PIXELDATA_DIMENSIONS]
    if keepOriginalSizes:
        for key in keys:
            if key in savedIs.keys():
                size = [max(size[0], savedIs[key].shape[0]), max(size[1], savedIs[key].shape[1])] + [PIXELDATA_DIMENSIONS]
    else:
        if len(keys) > 0 and keys[0] in savedIs.keys():
            size = list(savedIs[keys[0]].shape)[:2] + [PIXELDATA_DIMENSIONS]

    return size

def NormaliseValues(I, normaliseFit=False):
    if normaliseFit:
        I_min = np.min(I[:, :, :2])
        I_max = np.max(I[:, :, :2])
        I[:, :, :2] = ((I[:, :, :2] - I_min) / (I_max - I_min))
    else:
        I = np.clip(I, a_min=0.0, a_max=1.0)
    I = np.array(I, dtype=float)
    return I

# Image Redundant Remove Functions
def StartSameFuncsCount(FD1, FD2):
    startsameCount = 0
    for f1, f2 in zip(FD1, FD2):
        if f1 == f2:
            startsameCount += 1
        else:
            break
    return startsameCount

def GetSaveIKeys(EffectFuncs=None, EffectFuncsData=None):
    saveI_keys = []

    # Get Funcs Data
    if EffectFuncs is not None:
        EffectFuncsData = []
        for EFs in EffectFuncs:
            EFKeys = []
            for e in EFs:
                data = {}
                data['name'] = str(e.func.__name__)
                data['params'] = e.keywords
                EFKeys.append(data)
            EffectFuncsData.append(EFKeys)

    # Get Keys
    for i in range(len(EffectFuncsData)):
        for j in range(len(EffectFuncsData[i])):
            if 'key' in EffectFuncsData[i][j]['params'].keys():
                saveI_keys.append(EffectFuncsData[i][j]['params']['key'])
            elif 'keys' in EffectFuncsData[i][j]['params'].keys():
                saveI_keys.extend(EffectFuncsData[i][j]['params']['keys'])

    return saveI_keys

def Image_ReplaceRedundantEffectChains(EffectFuncs, display=False):
    EffectFuncsData = []
    # Get Funcs Data
    for EFs in EffectFuncs:
        EFKeys = []
        for e in EFs:
            data = {}
            data['name'] = str(e.func.__name__)
            data['params'] = e.keywords
            EFKeys.append(data)
        EffectFuncsData.append(EFKeys)
    
    # Compare to identify redundancies
    reductionCounts = [0]
    reductionReferences = [-1]
    for i in range(1, len(EffectFuncsData)):
        max_red_j = -1
        max_red = 0
        for j in range(0, i):
            redCount = StartSameFuncsCount(EffectFuncsData[i], EffectFuncsData[j])
            if redCount > max_red:
                max_red_j = j
                max_red = redCount

        reductionCounts.append(max_red)
        reductionReferences.append(max_red_j)

    reducedStarts = []
    for i in range(len(reductionCounts)):
        if reductionReferences[i] >= 0:
            reducedStarts.append(reductionCounts[i] - reducedStarts[reductionReferences[i]])
        else:
            reducedStarts.append(reductionCounts[i])

    ReducedEffectFuncs = []

    # Preliminary Checking for keys in functions
    saveI_keys = GetSaveIKeys(EffectFuncsData=EffectFuncsData)
    # Add new keys
    for i in range(len(EffectFuncsData)):
        Funcs = []
        if reductionReferences[i] >= 0:
            key = str(reductionReferences[i]) + "_" + str(reducedStarts[i]-1)
            Funcs = [functools.partial(ImageEffect_Substitute, key=key)] + EffectFuncs[i][reductionCounts[i]:]
            saveI_keys.append(key)
        else:
            Funcs = EffectFuncs[i]
        ReducedEffectFuncs.append(Funcs)

    if display:
        print("EffectFuncs Original:")
        for i in range(len(EffectFuncs)):
            print(str(i+1) + ":")
            for e in EffectFuncs[i]:
                params = []
                for k in e.keywords.keys():
                    params.append(k + "=" + str(e.keywords[k]))
                Text = str(e.func.__name__) + '(' + ', '.join(params) + ")"
                print("\t", Text)
        print()
        print("EffectFuncs Reduced:")
        for i in range(len(ReducedEffectFuncs)):
            print(str(i+1) + ":")
            for e in ReducedEffectFuncs[i]:
                params = []
                for k in e.keywords.keys():
                    params.append(k + "=" + str(e.keywords[k]))
                Text = str(e.func.__name__) + '(' + ', '.join(params) + ")"
                print("\t", Text)
    
    return ReducedEffectFuncs, saveI_keys

# Effect Applier Functions
def Image_MultipleImages(I, CommonEffects, EffectFuncs, nCols=2):
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGBA)
    I = np.array(I, dtype=float) / 255.0

    for CommonEffect in CommonEffects:
        I = CommonEffect(I)

    nCols = min(nCols, len(EffectFuncs))
    nRows = int(math.ceil(len(EffectFuncs) / nCols))

    curPos = [0, 0]
    CommonSize = [0, 0]
    EffectedIs = []
    for EffectFuncs_Image in EffectFuncs:
        I_this = np.copy(I)
        for EffectFunc in EffectFuncs_Image:
            I_this = EffectFunc(I_this)
        EffectedIs.append(I_this)
        CommonSize = [max(CommonSize[0], I_this.shape[0]), max(CommonSize[1], I_this.shape[1])]
    # print("Common Size:", CommonSize)
    
    # Resize to CommonSize by appending 0s
    for i in range(len(EffectedIs)):
        PixelDiff = [CommonSize[0] - EffectedIs[i].shape[0], CommonSize[1] - EffectedIs[i].shape[1]]
        Offset = [int(PixelDiff[0]/2), int(PixelDiff[1]/2)]
        I_appended = np.zeros((CommonSize[0], CommonSize[1], PIXELDATA_DIMENSIONS), dtype=float)
        I_appended[Offset[0]:Offset[0]+EffectedIs[i].shape[0], Offset[1]:Offset[1]+EffectedIs[i].shape[1], :] = EffectedIs[i]
        EffectedIs[i] = I_appended

    # Append all images into 1 image
    I_full = np.zeros((CommonSize[0]*nRows, CommonSize[1]*nCols, PIXELDATA_DIMENSIONS), dtype=float)
    for I_this in EffectedIs:
        I_full[curPos[0]*CommonSize[0]:(curPos[0]+1)*CommonSize[0], curPos[1]*CommonSize[1]:(curPos[1]+1)*CommonSize[1], :] = I_this[:, :, :]
        curPos = [curPos[0], curPos[1]+1]
        if curPos[1] >= nCols:
            curPos = [curPos[0]+1, 0]

    I_full = np.array(I_full * 255, dtype=np.uint8)
    I_full = cv2.cvtColor(I_full, cv2.COLOR_RGBA2BGRA)

    return I_full

def Image_MultipleImages_RemovedRecompute(I, CommonEffects, EffectFuncs, nCols=2, saveI_keys=[]):
    # print("saveI_keys", saveI_keys)
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGBA)
    I = np.array(I, dtype=float) / 255.0

    for CommonEffect in CommonEffects:
        I = CommonEffect(I)

    nCols = min(nCols, len(EffectFuncs))
    nRows = int(math.ceil(len(EffectFuncs) / nCols))

    curPos = [0, 0]
    CommonSize = [0, 0]
    # Check Redundant Effects (Must be same effect with same parameters on same input image)
    # Reset Saved Images
    global savedIs
    savedIs = {}

    EffectedIs = []
    curIndex = [0, 0]
    for EffectFuncs_Image in EffectFuncs:
        I_this = np.copy(I)
        for EffectFunc in EffectFuncs_Image:
            I_this = EffectFunc(I_this)
            
            # Save Image if needed
            curIndexKey = str(curIndex[0]) + "_" + str(curIndex[1])
            if curIndexKey in saveI_keys:
                savedIs[curIndexKey] = np.copy(I_this)
            curIndex[1] += 1
        print(I_this.shape)
        EffectedIs.append(I_this)
        CommonSize = [max(CommonSize[0], I_this.shape[0]), max(CommonSize[1], I_this.shape[1])]
        curIndex = [curIndex[0]+1, 0]
    # print("Common Size:", CommonSize)
    
    # Resize to CommonSize by appending 0s
    for i in range(len(EffectedIs)):
        PixelDiff = [CommonSize[0] - EffectedIs[i].shape[0], CommonSize[1] - EffectedIs[i].shape[1]]
        Offset = [int(PixelDiff[0]/2), int(PixelDiff[1]/2)]
        I_appended = np.zeros((CommonSize[0], CommonSize[1], PIXELDATA_DIMENSIONS), dtype=float)
        I_appended[Offset[0]:Offset[0]+EffectedIs[i].shape[0], Offset[1]:Offset[1]+EffectedIs[i].shape[1], :] = EffectedIs[i]
        EffectedIs[i] = I_appended

    # Append all images into 1 image
    I_full = np.zeros((CommonSize[0]*nRows, CommonSize[1]*nCols, PIXELDATA_DIMENSIONS), dtype=float)
    for I_this in EffectedIs:
        I_full[curPos[0]*CommonSize[0]:(curPos[0]+1)*CommonSize[0], curPos[1]*CommonSize[1]:(curPos[1]+1)*CommonSize[1], :] = I_this[:, :, :]
        curPos = [curPos[0], curPos[1]+1]
        if curPos[1] >= nCols:
            curPos = [curPos[0]+1, 0]

    I_full = np.array(I_full * 255, dtype=np.uint8)
    I_full = cv2.cvtColor(I_full, cv2.COLOR_RGBA2BGRA)

    return I_full

def Image_ApplyEffects(I, EffectFuncs):
    for EffectFunc in EffectFuncs:
        I = EffectFunc(I)
    return I

# def ImageEffect_Substitute(I, key):
#     global savedIs
#     if key in savedIs.keys():
#         return savedIs[key]
#     else:
#         # print(key, savedIs.keys())
#         return I

# # Combination Effects
# def ImageEffect_Add(I, keys, keepOriginalSizes=False, normaliseFit=False):
#     global savedIs

#     size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

#     I_effect = np.zeros(tuple(size), dtype=float)
#     for key in keys:
#         if key in savedIs.keys():
#             I_alphaApplied = ApplyAlphaToImage(savedIs[key])
#             I_effect = I_effect + cv2.resize(I_alphaApplied, tuple(size[:2][::-1])) # With Alpha

#     I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

#     return I_effect

# def ImageEffect_Sub(I, keys, keepOriginalSizes=False, normaliseFit=False):
#     global savedIs

#     size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

#     I_effect = np.ones(tuple(size), dtype=float)
#     if len(keys) > 0:
#         I_alphaApplied = ApplyAlphaToImage(savedIs[keys[0]])
#         I_effect = cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
#     for i in range(1, len(keys)):
#         key = keys[i]
#         if key in savedIs.keys():
#             I_alphaApplied = ApplyAlphaToImage(savedIs[key])
#             I_effect = I_effect - cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))

#     I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

#     return I_effect

# def ImageEffect_Avg(I, keys, keepOriginalSizes=False, normaliseFit=False):
#     global savedIs

#     size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

#     I_effect = np.zeros(tuple(size), dtype=float)
#     for key in keys:
#         if key in savedIs.keys():
#             I_alphaApplied = ApplyAlphaToImage(savedIs[key])
#             I_effect = I_effect + cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))
#     I_effect = I_effect / max(1, len(keys))

#     I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

#     return I_effect

# def ImageEffect_Mul(I, keys, keepOriginalSizes=False, normaliseFit=False):
#     global savedIs

#     size = NormaliseSize(keys, keepOriginalSizes=keepOriginalSizes)

#     I_effect = np.ones(tuple(size), dtype=float)
#     for key in keys:
#         if key in savedIs.keys():
#             I_alphaApplied = ApplyAlphaToImage(savedIs[key])
#             I_effect = I_effect * cv2.resize(I_alphaApplied, tuple(size[:2][::-1]))

#     I_effect = NormaliseValues(I_effect, normaliseFit=normaliseFit)

#     return I_effect


# Driver Code