'''
Frame Image Effects Library
'''

# Imports
import cv2
import numpy as np

from Utils import VideoUtils

# Main Functions
def ImageEffect_AddFrameOLD(I, FrameFileData=None, FrameImage=None, ImageReplaceBox=[[0, 0], [0, 0]]):
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

    FrameImage = np.array(FrameImage, dtype=float) / 255.0
    FrameImage = np.dstack((FrameImage[:, :, 0], FrameImage[:, :, 1], FrameImage[:, :, 2], np.ones(FrameImage.shape[:2])))

    FrameImage[ImageReplaceBox[1][0]:ImageReplaceBox[1][1], ImageReplaceBox[0][0]:ImageReplaceBox[0][1]] = I
    return FrameImage

def ImageEffect_AddFrame(I, imgPath=None):
    if imgPath is None:
        return I
    FrameImage = VideoUtils.ReadImage(imgPath, imgSize=None, keepAspectRatio=True)
    ImageReplaceBox = VideoUtils.GetFillBoxFromFrameName(imgPath)

    ImageReplaceBox = [
        [int(ImageReplaceBox[0][0]*FrameImage.shape[1]), int(ImageReplaceBox[0][1]*FrameImage.shape[1])],
        [int(ImageReplaceBox[1][0]*FrameImage.shape[0]), int(ImageReplaceBox[1][1]*FrameImage.shape[0])]
    ]
    FitSize = (ImageReplaceBox[0][1] - ImageReplaceBox[0][0], ImageReplaceBox[1][1] - ImageReplaceBox[1][0])
    I = cv2.resize(I, FitSize)
    
    FrameImage = np.array(FrameImage, dtype=float) / 255.0
    FrameImage = np.dstack((FrameImage[:, :, 0], FrameImage[:, :, 1], FrameImage[:, :, 2], np.ones(FrameImage.shape[:2])))
    
    FrameImage[ImageReplaceBox[1][0]:ImageReplaceBox[1][1], ImageReplaceBox[0][0]:ImageReplaceBox[0][1]] = I
    return FrameImage

# Main Vars
EFFECTFUNCS_FRAME = [
    {
        "name": "AddFrame",
        "code": "AddFrame(imgPath='Frames/Frame_Nintendo_111_303_430_107_285_607.PNG')",
        "func": ImageEffect_AddFrame,
        "params": [
            {
                "name": "imgPath",
                "default": "Frames/Frame_Nintendo_111_303_430_107_285_607.PNG",
                "type": "frame"
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_FRAME)

# Driver Code