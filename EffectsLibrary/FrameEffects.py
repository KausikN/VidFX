'''
Frame Image Effects Library
'''

# Imports
import cv2
import numpy as np

from Utils import VideoUtils

# Main Functions
def ImageEffect_AddFrame(I, FrameFileData=None, FrameImage=None, ImageReplaceBox=[[0, 0], [0, 0]]):
    if FrameFileData is not None:
        if not ('imgSize' in FrameFileData.keys()):
            FrameFileData['imgSize'] = None
        if not ('keepAspectRatio' in FrameFileData.keys()):
            FrameFileData['keepAspectRatio'] = False
        FrameImage = VideoUtils.ReadImage(FrameFileData['imgPath'], imgSize=FrameFileData['imgSize'], keepAspectRatio=FrameFileData['keepAspectRatio'])
        ImageReplaceBox = VideoUtils.GetFillBoxFromFrameName(FrameFileData['imgPath'])

    ImageReplaceBox = [
        [int(ImageReplaceBox[0][0]*FrameImage.shape[1]), int(ImageReplaceBox[0][1]*FrameImage.shape[1])],
        [int(ImageReplaceBox[1][0]*FrameImage.shape[0]), int(ImageReplaceBox[1][1]*FrameImage.shape[0])]
    ]
    FitSize = (ImageReplaceBox[0][1] - ImageReplaceBox[0][0], ImageReplaceBox[1][1] - ImageReplaceBox[1][0])
    I = cv2.resize(I, FitSize)
    if I.ndim == 2:
        I = cv2.cvtColor(I, cv2.COLOR_GRAY2RGB)
    FrameImage[ImageReplaceBox[1][0]:ImageReplaceBox[1][1], ImageReplaceBox[0][0]:ImageReplaceBox[0][1]] = I
    return FrameImage

# Driver Code