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

def DisplayImage(I, title=''):
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    plt.imshow(I, 'gray')
    plt.title(title)
    plt.show()

def SaveImage(I, path):
    cv2.imwrite(path, I)

def GetFramesFromVideo(vid=None, path=None, max_frames=-1):
    if vid is None:
        vid = ReadVideo(path)
    
    frames = []
    frameCount = 0

    # Check if camera opened successfully
    if (vid.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(vid.isOpened() and ((not (frameCount == max_frames)) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            frames.append(frame)
            frameCount += 1
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    vid.release()

    return frames

def DisplayVideo(vid=None, path=None, max_frames=-1, EffectFunc=None):
    if vid is None:
        vid = ReadVideo(path)
    
    frameCount = 0

    # Check if camera opened successfully
    if (vid.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(vid.isOpened() and ((not (frameCount == max_frames)) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            # Apply Effect if needed
            if EffectFunc is not None:
                frame = EffectFunc(frame)
            # Display the resulting frame
            cv2.imshow('Video', frame)
            frameCount += 1
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    vid.release()

    cv2.destroyAllWindows()

def VideoEffect(pathIn, pathOut, EffectFunc, max_frames=-1, speedUp=1, fps=20.0, size=None):
    frames = GetFramesFromVideo(path=pathIn, max_frames=max_frames)
    frames = frames[::int(speedUp)]

    frames_effect = []
    for frame in tqdm(frames):
        frame = cv2.cvtColor(EffectFunc(frame), cv2.COLOR_BGR2RGB)
        frames_effect.append(Image.fromarray(frame))

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

# Frame Functions
def GetFillBoxFromFrameName(framePath):
    frameName = os.path.splitext(os.path.basename(framePath))[0]
    frameData = frameName.split('_')[2:]
    FillBox = [[int(frameData[0])/int(frameData[2]), int(frameData[1])/int(frameData[2])], [int(frameData[3])/int(frameData[5]), int(frameData[4])/int(frameData[5])]]
    return FillBox

# Driver Code
# Params
# path = 'TestVids/test.mp4'
# # Params

# # RunCode
# webcam = WebcamVideo()
# DisplayVideo(webcam)