'''
Library for basic video functions
'''

# Imports
import os
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from .VideoInputs import *

# Main Vars
INPUTREADERS_VIDEO = {
    "Webcam": WebcamVideo,
    "Upload Video File": ReadVideo,
    "Video URL": ReadVideo_URL
}

INPUTREADERS_IMAGE = {
    "Webcam Snapshot": WebcamVideo,
    "Upload Image File": ReadVideo,
    "Image URL": ReadVideo_URL
}

# Main Functions
def ReadImage(imgPath, imgSize=None, keepAspectRatio=False):
    '''
    Read Image
    '''
    I = cv2.imread(imgPath)
    if not imgSize == None:
        size_original = [I.shape[0], I.shape[1]]
        print(size_original)
        if keepAspectRatio:
            if imgSize[1] > imgSize[0]:
                imgSize = (size_original[0] * (imgSize[1] / size_original[1]), imgSize[1])
            elif imgSize[0] > imgSize[1]:
                imgSize = (imgSize[0], size_original[1] * (imgSize[0] / size_original[0]))
            else:
                if size_original[1] > size_original[0]:
                    imgSize = (size_original[0] * (imgSize[1] / size_original[1]), imgSize[1])
                else:
                    imgSize = (imgSize[0], size_original[1] * (imgSize[0] / size_original[0]))
            imgSize = (int(round(imgSize[1])), int(round(imgSize[0])))
        I = cv2.resize(I, imgSize)
    # I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)

    return I

def VideoUtils_SaveFrames2Video(frames, pathOut, fps=20, size=None):
    '''
    VideoUtils - Save Frames to Video
    '''
    if os.path.splitext(pathOut)[-1] == ".gif":
        
        frames_images = [Image.fromarray(np.array(frame*255, dtype=np.uint8)) for frame in frames]
        extraFrames = []
        if len(frames_images) > 1: extraFrames = frames_images[1:]
        frames_images[0].save(pathOut, save_all=True, append_images=extraFrames, format="GIF", loop=0)
    else:
        # if size is None: size = (640, 480)
        # frames = [np.array(frame*255, dtype=int) for frame in frames]
        # frames = [ResizeImage_Pad(frame, size=size[::-1]) for frame in frames]
        if size is None: size = (frames[0].shape[1], frames[0].shape[0])
        frames = [np.array(frame*255, dtype=np.uint8) for frame in frames]
        codec = cv2.VideoWriter_fourcc(*'AVC1')
        out = cv2.VideoWriter(pathOut, codec, fps, size)
        for frame in frames:
            out.write(frame)
        # out.close()
        out.release()

# Frame Functions
def GetFillBoxFromFrameName(framePath):
    '''
    Get Fill Box From Frame Name
    '''
    frameName = os.path.splitext(os.path.basename(framePath))[0]
    frameData = frameName.split('_')[2:]
    FillBox = [[int(frameData[0])/int(frameData[2]), int(frameData[1])/int(frameData[2])], [int(frameData[3])/int(frameData[5]), int(frameData[4])/int(frameData[5])]]
    
    return FillBox