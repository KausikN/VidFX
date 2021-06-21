"""
Stream lit GUI for hosting VidFX
"""

# Imports
import os
import cv2
import PIL
import importlib
import functools
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import json
from tqdm import tqdm

# from StreamLitGUI.webcam import webcam
# from webcam import webcam

import VidFX
# import ImageFX
# import ImageEffectTransistionFX

from Utils import VideoUtils
from EffectsLibrary import EffectsLibrary

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
DEFAULT_PATH_EXAMPLEIMAGE = 'TestImgs/Horse.PNG'
DEFAULT_PATH_EXAMPLEVIDEO = 'TestVids/Test_Animation.wmv'

DEFAULT_SAVEPATH_IMAGE = 'TestImgs/OutputImage.png'
DEFAULT_SAVEPATH_VIDEO = 'TestImgs/OutputVideo.mp4'
DEFAULT_SAVEPATH_GIF = 'TestImgs/OutputGIF.gif'

DEFAULT_CODE_PACKAGE = 'StreamLitGUI'

IMAGESIZE_MIN = [1, 1]
IMAGESIZE_MAX = [512, 512]
IMAGESIZE_DEFAULT = [100, 100]
IMAGESIZEINDICATORIMAGE_SIZE = [128, 128]

DISPLAY_IMAGESIZE = [512, 512]
DISPLAY_INTERPOLATION = cv2.INTER_NEAREST
DISPLAY_DELAY = 0.1

INPUTREADERS_VIDEO = {
    "Upload Video File": VideoUtils.ReadVideo,
    "Webcam": VideoUtils.WebcamVideo
}

# Util Vars


# Util Functions
def Hex_to_RGB(val):
    val = val.lstrip('#')
    lv = len(val)
    return tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def RGB_to_Hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

@st.cache
def GenerateImageSizeIndicatorImage(ImageSize):
    ### Image Size Indicator Image 
    ImageSizeIndicator_Image = np.zeros((IMAGESIZEINDICATORIMAGE_SIZE[0], IMAGESIZEINDICATORIMAGE_SIZE[1]), dtype=int)
    ImageSizeIndicator_Image[:int((ImageSize[0]/IMAGESIZE_MAX[0])*IMAGESIZEINDICATORIMAGE_SIZE[0]), :int((ImageSize[1]/IMAGESIZE_MAX[1])*IMAGESIZEINDICATORIMAGE_SIZE[1])] = 255
    return ImageSizeIndicator_Image

# Main Functions
def GetEffectsCode(CommonEffectsText, EffectFuncsText):
    ImportsCode = '''
import cv2
import functools
import numpy as np

from EffectsLibrary import EffectsLibrary

'''
    CommonEffectsCode = ImportsCode + "CommonEffects = " + VidFX.UICommonEffectsCodeParser(CommonEffectsText)
    open(os.path.join(DEFAULT_CODE_PACKAGE, "CommonEffects.py"), 'w').write(CommonEffectsCode)
    CommonEffects = importlib.import_module(DEFAULT_CODE_PACKAGE + ".CommonEffects").CommonEffects

    EffectFuncsCode = ImportsCode + "EffectFuncs = " + VidFX.UIMultiEffectsCodeParser(EffectFuncsText)
    open(os.path.join(DEFAULT_CODE_PACKAGE, "EffectFuncs.py"), 'w').write(EffectFuncsCode)
    EffectFuncs = importlib.import_module(DEFAULT_CODE_PACKAGE + ".EffectFuncs").EffectFuncs
    
    return CommonEffects, EffectFuncs

# UI Functions
def UI_Webcam():
    captured_image = webcam()
    if captured_image is None:
        st.write("Waiting for capture...")
    else:
        st.write("Got an image from the webcam:")
        st.image(captured_image)


def UI_VideoInputSource():
    USERINPUT_VideoInputChoice = st.selectbox("Select Video Input Source", list(INPUTREADERS_VIDEO.keys()))

    USERINPUT_VideoReader = None
    # Upload Video File
    if USERINPUT_VideoInputChoice == "Upload Video File":
        USERINPUT_VideoReader = INPUTREADERS_VIDEO[USERINPUT_VideoInputChoice]
        USERINPUT_VideoPath = st.file_uploader("Upload Video", ['avi', 'mp4', 'wmv'])
        if USERINPUT_VideoPath is None:
            USERINPUT_VideoPath = DEFAULT_PATH_EXAMPLEVIDEO
        USERINPUT_VideoReader = functools.partial(USERINPUT_VideoReader, USERINPUT_VideoPath)
    # Webcam
    else:
        USERINPUT_VideoReader = INPUTREADERS_VIDEO[USERINPUT_VideoInputChoice]

    USERINPUT_Video = USERINPUT_VideoReader()
    
    return USERINPUT_Video


def UI_TransistionFuncSelect(title='', col=st):
    TransistionFuncName = col.selectbox(title, list(TRANSISTIONFUNCS.keys()))
    TransistionFunc = TRANSISTIONFUNCS[TransistionFuncName]
    return TransistionFunc

def UI_CustomResize():
    col1, col2 = st.beta_columns(2)
    USERINPUT_ImageSizeX = col2.slider("Width Pixels", IMAGESIZE_MIN[0], IMAGESIZE_MAX[0], IMAGESIZE_DEFAULT[0], IMAGESIZE_MIN[0], key="USERINPUT_ImageSizeX")
    USERINPUT_ImageSizeY = col2.slider("Height Pixels", IMAGESIZE_MIN[1], IMAGESIZE_MAX[1], IMAGESIZE_DEFAULT[1], IMAGESIZE_MIN[1], key="USERINPUT_ImageSizeY")
    CustomSize = [int(USERINPUT_ImageSizeX), int(USERINPUT_ImageSizeY)]

    ImageSizeIndicator_Image = GenerateImageSizeIndicatorImage(CustomSize[::-1]) # Reversed due to dissimilarity in generating width and height
    col1.image(ImageSizeIndicator_Image, caption="Image Size (Max " + str(IMAGESIZE_MAX[0]) + " x " + str(IMAGESIZE_MAX[1]) + ")", use_column_width=False, clamp=False)
    
    return CustomSize

def UI_Resizer(USERINPUT_Image_1, USERINPUT_Image_2):
    ResizeFuncName = st.selectbox("Select Resize Method", list(RESIZEFUNCS.keys()))
    ResizeFunc = RESIZEFUNCS[ResizeFuncName]
    # Check for Custom Size
    if 'Custom Size' in ResizeFuncName:
        CustomSize = UI_CustomResize()
        ResizeFunc = functools.partial(ResizeFunc, Size=tuple(CustomSize))

    USERINPUT_Image_1, USERINPUT_Image_2 = ResizeFunc(USERINPUT_Image_1, USERINPUT_Image_2)
    col1, col2 = st.beta_columns(2)
    col1.image(USERINPUT_Image_1, caption="Resized Start Image", use_column_width=True)
    col2.image(USERINPUT_Image_2, caption="Resized End Image", use_column_width=True)

    return USERINPUT_Image_1, USERINPUT_Image_2

# Repo Based Functions
def videofx():
    # Title
    st.header("Video FX")

    # Load Inputs
    USERINPUT_Video = UI_VideoInputSource()
    CommonEffectsText = st.text_area("Common Effects Code")
    EffectFuncsText = st.text_area("Effects Code")
    CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=True)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=nCols, saveI_keys=saveI_keys)

    

    # Process Inputs
    if st.button("Generate"):
        pass

        # Display Outputs
        # UI_DisplayImageSequence_AsGIF(GeneratedImgs)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()