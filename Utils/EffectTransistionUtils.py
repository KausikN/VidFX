'''
Library for basic video functions
'''

# Imports
import os
import cv2
import functools
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from Utils import VideoUtils

# Main Functions
# Utils Functions
def ApplyArgsToFunction(func, args):
    return functools.partial(func, **args)

def GetTransistionedArgs(args, frame, recursive=False):
    argVals = {}
    for arg in args.keys():
        # Check if multiple transistions (list of values as arg)
        if type(args[arg]) in [list, tuple]:
            argVal = []
            for val in args[arg]:
                if recursive:
                    argVal.append(GetTransistionedArgs(val, frame))
                else:
                    argVal.append(val(frame))
            argVals[arg] = type(args[arg])(argVal)
        elif type(args[arg]) in [dict]:
            argVal = {}
            for val in args[arg].keys():
                if recursive:
                    argVal[val] = GetTransistionedArgs(args[arg][val], frame)
                else:
                    argVal[val] = args[arg][val](frame)
            argVals[arg] = type(args[arg])(argVal)
        else:
            argVals[arg] = args[arg](frame)
    return argVals

def GetTransistionedFunc(funcData, frame, recursive=False):
    func_tr = funcData[0]
    func = func_tr
    if len(funcData) >= 2:
        args_tr = funcData[1]
        args = GetTransistionedArgs(args_tr, frame, recursive=recursive)
        func = ApplyArgsToFunction(func_tr, args)
    return func

def GetMainFunc(MainEffectFunc, CommonEffects_Tr, EffectFuncs_Tr, frame, recursiveArgs=False):
    CommonEffects = []
    for ce in CommonEffects_Tr:
        CommonEffects.append(GetTransistionedFunc(ce, frame, recursive=recursiveArgs))
    EffectFuncs = []
    for efs in EffectFuncs_Tr:
        EFs = []
        for ef in efs:
            EFs.append(GetTransistionedFunc(ef, frame, recursive=recursiveArgs))
        EffectFuncs.append((EFs))
    MainFunc = functools.partial(MainEffectFunc, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs)
    return MainFunc

# Image Effect Transistions
def ImageEffectTransistion(I, EffectFunctions, pathOut=None, max_frames=-1, speedUp=1, fps=20.0, size=None, display=True, save=False, recursiveArgs=False):
    
    MainEffectFunc = EffectFunctions['Main']
    CommonEffects_Tr = EffectFunctions['Common']
    EffectFuncs_Tr = EffectFunctions['Effect']

    frames = np.linspace(0, 1, max_frames)

    frames = frames[::int(speedUp)]

    frames_effect = []
    for frame in tqdm(frames, disable=display):
        MainFunc = GetMainFunc(MainEffectFunc, CommonEffects_Tr, EffectFuncs_Tr, frame, recursiveArgs=recursiveArgs)

        outFrame = cv2.cvtColor(MainFunc(I), cv2.COLOR_BGR2RGB)
        frames_effect.append(Image.fromarray(outFrame))

        if display:
            cv2.imshow('Video', frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                display = False

    if save:
        if size is None:
            size = (640, 480)

        if os.path.splitext(pathOut)[-1] == '.gif':
            extraFrames = []
            if len(frames_effect) > 1:
                extraFrames = frames_effect[1:]
            frames_effect[0].save(pathOut, save_all=True, append_images=extraFrames, format='GIF', loop=0)
        else:
            out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'XVID'), fps, size)
            for frame in frames_effect:
                out.write(frame)
            out.release()

# Transistion Functions
def EffectTransistion_Linear(prop, start, end):
    return start + (end-start)*prop

# Driver Code
# Params
# path = 'TestVids/test.mp4'
# # Params

# # RunCode
# webcam = WebcamVideo()
# DisplayVideo(webcam)