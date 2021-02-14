'''
Image Effects Library
'''

# Imports
import cv2
import math
import numpy as np

from Utils import VideoUtils

Segmenter_Semantic = None
Segmenter_Instance = None

# Main Functions
# Loader Functions
def LoadSemanticSegmenter():
    from pixellib.semantic import semantic_segmentation
    global Segmenter_Semantic
    Segmenter_Semantic = semantic_segmentation()
    Segmenter_Semantic.load_pascalvoc_model("Models/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")

def LoadInstanceSegmenter():
    from pixellib.instance import instance_segmentation
    global Segmenter_Instance
    Segmenter_Instance = instance_segmentation()
    Segmenter_Instance.load_model("Models/mask_rcnn_coco.h5")

# Effect Applier Functions
def Image_MultipleImages(I, CommonEffects, EffectFuncs, nCols=2):
    for CommonEffect in CommonEffects:
        I = CommonEffect(I)

    if len(EffectFuncs) < nCols:
        nCols = len(EffectFuncs)
    nRows = int(math.ceil(len(EffectFuncs) / nCols))
    curPos = [0, 0]

    CommonSize = [0, 0]

    EffectedIs = []
    for EffectFuncs_Image in EffectFuncs:
        I_this = np.copy(I)
        for EffectFunc in EffectFuncs_Image:
            I_this = EffectFunc(I_this)
        if I_this.ndim == 2:
            I_this = cv2.cvtColor(I_this, cv2.COLOR_GRAY2RGB)
        # if not np.equal(I.shape[:2], I_this.shape[:2]).all():
        #     I_this = cv2.resize(I_this, (I.shape[1], I.shape[0]))
        EffectedIs.append(I_this)
        CommonSize = [max(CommonSize[0], I_this.shape[0]), max(CommonSize[1], I_this.shape[1])]

    # print("Common Size:", CommonSize)
    
    # Resize to CommonSize by appending 0s
    for i in range(len(EffectedIs)):
        PixelDiff = [CommonSize[0] - EffectedIs[i].shape[0], CommonSize[1] - EffectedIs[i].shape[1]]
        Offset = [int(PixelDiff[0]/2), int(PixelDiff[1]/2)]
        I_appended = np.zeros((CommonSize[0], CommonSize[1], 3), dtype=np.uint8)
        I_appended[Offset[0]:Offset[0]+EffectedIs[i].shape[0], Offset[1]:Offset[1]+EffectedIs[i].shape[1], :] = EffectedIs[i]
        EffectedIs[i] = I_appended

    # Append all images into 1 image
    I_full = np.zeros((CommonSize[0]*nRows, CommonSize[1]*nCols, 3), dtype=np.uint8)
    for I_this in EffectedIs:
        I_full[curPos[0]*CommonSize[0]:(curPos[0]+1)*CommonSize[0], curPos[1]*CommonSize[1]:(curPos[1]+1)*CommonSize[1], :] = I_this[:, :, :]
        curPos = [curPos[0], curPos[1]+1]
        if curPos[1] >= nCols:
            curPos = [curPos[0]+1, 0]

    return I_full

def Image_ApplyEffects(I, EffectFuncs):
    for EffectFunc in EffectFuncs:
        I = EffectFunc(I)
    return I

# Effect Functions
def ImageEffect_None(I):
    return I

def ImageEffect_Binarise(I, threshold=127):
    I = np.zeros(I.shape, dtype=np.uint8) + (I > threshold)*np.ones(I.shape, dtype=np.uint8)*255
    return I

def ImageEffect_GreyScale(I):
    return cv2.cvtColor(cv2.cvtColor(I, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)

def ImageEffect_Grey2RGB(I):
    return cv2.cvtColor(I, cv2.COLOR_GRAY2RGB)

def ImageEffect_RGB2BGR(I):
    return cv2.cvtColor(I, cv2.COLOR_RGB2BGR)

def ImageEffect_MostDominantColor(I):
    I_dom = np.max(I, axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    return (I)*(I_dom == I)

def ImageEffect_LeastDominantColor(I):
    I_dom = np.min(I, axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    return (I)*(I_dom == I)

def ImageEffect_ScaleValues(I, scaleFactor=[0, 0, 0]):
    I = np.multiply(I, np.array(scaleFactor, dtype=float)).astype(int)
    I = np.clip(I, 0, 255, dtype=int).astype(np.uint8)
    return I

def ImageEffect_ClipValues(I, threshold=[127, 128], replace=[127, 128]):
    I = np.clip(I, threshold[0], threshold[1])
    lowCheck = (I == threshold[0])
    highCheck = (I == threshold[1])
    I = lowCheck*np.ones(I.shape, dtype=np.uint8)*replace[0] + highCheck*np.ones(I.shape, dtype=np.uint8)*replace[1] + np.logical_not(np.logical_or(lowCheck, highCheck))*I
    return I

def ImageEffect_BinValues(I, bins=[0, 127, 255]):
    bins = np.array(bins)
    binMaps = np.digitize(I, bins)
    binMaps = np.clip(binMaps, 0, bins.shape[0]-1)
    return bins[binMaps]

def ImageEffect_Resize(I, size=(480, 640), interpolation=cv2.INTER_LINEAR):
    return cv2.resize(I, size, interpolation=interpolation)

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

def ImageEffect_GaussianNoise(I, mean=0, SD=1):
    return I + np.random.normal(mean, SD, size=I.shape).astype(int)

def ImageEffect_SpeckleNoise(I):
    noise = np.random.randn(I.shape[0], I.shape[1], I.shape[2]).astype(int)
    I = I + (I*noise)
    return I

def ImageEffect_SaltPepperNoise(I, prob=0.5):
    h, w, c = I.shape
    mask = np.random.choice((0, 1, 2), size=(h, w), p=[1-prob, prob/2., prob/2.])
    I[mask == 1] = 255
    I[mask == 2] = 0
    return I

def ImageEffect_SemanticSegmentation(I, overlay=False):
    if Segmenter_Semantic is None:
        LoadSemanticSegmenter()
    segmap, output = Segmenter_Semantic.segmentFrameAsPascalvoc(I, overlay=overlay)
    output = np.array(output)
    return output

def ImageEffect_InstanceSegmentation(I, show_bboxes=False):
    if Segmenter_Instance is None:
        LoadInstanceSegmenter()
    segmap, output = Segmenter_Instance.segmentFrame(I, show_bboxes=show_bboxes)
    output = np.array(output)
    return output

# Direct Video Effects
def VideoEffect_SemanticSegmentation(videoPath, outputPath, overlay=False, fps=20):
    if Segmenter_Semantic is None:
        LoadSemanticSegmenter()
    Segmenter_Semantic.process_video_pascalvoc(videoPath, overlay=overlay, frames_per_second=fps, output_video_name=outputPath)

def VideoEffect_InstanceSegmentation(videoPath, outputPath, show_bboxes=False, fps=20):
    if Segmenter_Instance is None:
        LoadInstanceSegmenter()
    Segmenter_Instance.process_video(videoPath, show_bboxes=show_bboxes, frames_per_second=fps, output_video_name=outputPath)

# Driver Code
# I = [[[100, 22, 3], [10, 1, 0], [0, 9, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
# I = np.array(I)

# bins = np.linspace(0, 255, 10, dtype=np.uint8)
# print(bins)
# ImageEffect_BinValues(I, bins=bins)

#AddFrame(FrameFileData={"imgPath": 'Frames/Frame_Nintendo_111_303_430_107_285_607.PNG'})

# I = cv2.imread('Test.png')
# cv2.imshow('', ImageEffect_SemanticSegmentation(I))
# cv2.waitKey(0)