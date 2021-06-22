"""
Stream lit GUI for hosting VidFX
"""

# Imports
import os
import cv2
import pickle
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
AVAILABLEEFFECTS_PATH = 'StreamLitGUI/AvailableEffects.txt'

DEFAULT_SAVEPATH_IMAGE = 'TestImgs/OutputImage.png'
DEFAULT_SAVEPATH_VIDEO = 'TestImgs/OutputVideo.mp4'
DEFAULT_SAVEPATH_GIF = 'TestImgs/OutputGIF.gif'

DEFAULT_CODE_PACKAGE = 'StreamLitGUI'

OUTPUT_NCOLS = 5

IMAGESIZE_MIN = [1, 1]
IMAGESIZE_MAX = [512, 512]
IMAGESIZE_DEFAULT = [100, 100]
IMAGESIZEINDICATORIMAGE_SIZE = [128, 128]

DISPLAY_IMAGESIZE = [512, 512]
DISPLAY_INTERPOLATION = cv2.INTER_NEAREST
DISPLAY_DELAY = 0.1

INPUTREADERS_VIDEO = {
    "Webcam": VideoUtils.WebcamVideo,
    "Upload Video File": VideoUtils.ReadVideo
}

INPUTREADERS_IMAGE = {
    "Webcam Snapshot": VideoUtils.WebcamVideo,
    "Upload Image File": None
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
import pickle

from EffectsLibrary import EffectsLibrary

'''
    SavePickleCode = '''
pickle.dump({EffectObj}, open('{DEFAULT_CODE_PACKAGE}' + '/{EffectObj}.p', 'wb'))
'''

    CommonEffectsCode = ImportsCode + "CommonEffects = " + VidFX.UICommonEffectsCodeParser(CommonEffectsText) + SavePickleCode.format(DEFAULT_CODE_PACKAGE=DEFAULT_CODE_PACKAGE, EffectObj='CommonEffects')
    # open(os.path.join(DEFAULT_CODE_PACKAGE, "CommonEffects.py"), 'w').write(CommonEffectsCode)
    # CommonEffectsModule = importlib.import_module(DEFAULT_CODE_PACKAGE + ".CommonEffects")
    # import StreamLitGUI.CommonEffects as CommonEffectsModule
    # CommonEffectsModule = importlib.reload(CommonEffectsModule)
    # CommonEffects = CommonEffectsModule.CommonEffects
    exec(CommonEffectsCode, globals())
    CommonEffects = pickle.load(open(os.path.join(DEFAULT_CODE_PACKAGE, "CommonEffects.p"), 'rb'))

    EffectFuncsCode = ImportsCode + "EffectFuncs = " + VidFX.UIMultiEffectsCodeParser(EffectFuncsText) + SavePickleCode.format(DEFAULT_CODE_PACKAGE=DEFAULT_CODE_PACKAGE, EffectObj='EffectFuncs')
    # open(os.path.join(DEFAULT_CODE_PACKAGE, "EffectFuncs.py"), 'w').write(EffectFuncsCode)
    # EffectFuncsModule = importlib.import_module(DEFAULT_CODE_PACKAGE + ".EffectFuncs")
    # import StreamLitGUI.EffectFuncs as EffectFuncsModule
    # EffectFuncsModule = importlib.reload(EffectFuncsModule)
    # EffectFuncs = EffectFuncsModule.EffectFuncs
    exec(EffectFuncsCode, globals())
    EffectFuncs = pickle.load(open(os.path.join(DEFAULT_CODE_PACKAGE, "EffectFuncs.p"), 'rb'))
    
    return CommonEffects, EffectFuncs

# UI Functions
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

def UI_DisplayEffectVideo(vid=None, max_frames=-1, EffectFunc=None, compactDisplay=False):
    frameCount = 0

    # Check if camera opened successfully
    if (vid.isOpened()== False): 
        print("Error opening video stream or file")

    col1, col2 = st, st
    if compactDisplay:
        col1, col2 = st.beta_columns(2)

    inputVideoDisplay = col1.empty()
    effectVideoDisplay = col2.empty()

    # Read until video is completed
    while(vid.isOpened() and ((not (frameCount == max_frames)) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        inputVideoDisplay.image(frame, caption='Input Video', use_column_width=compactDisplay)
        if ret == True:
            # Apply Effect if needed
            if EffectFunc is not None:
                frame = EffectFunc(frame)
            # Display the resulting frame
            effectVideoDisplay.image(frame, caption='Effect Video', use_column_width=compactDisplay)
            frameCount += 1
        # Break the loop
        else: 
            break
    # When everything done, release the video capture object
    vid.release()

def UI_LoadImage():
    USERINPUT_ImageInputChoice = st.selectbox("Select Image Input Source", list(INPUTREADERS_IMAGE.keys()))

    USERINPUT_Image = None
    # Upload Image File
    if USERINPUT_ImageInputChoice == "Upload Image File":
        USERINPUT_ImageReader = INPUTREADERS_IMAGE[USERINPUT_ImageInputChoice] # Unused Reader as image is loaded directly
        USERINPUT_ImageData = st.file_uploader("Upload Image", ['png', 'jpg', 'jpeg', 'bmp'])
        if USERINPUT_ImageData is not None:
            USERINPUT_ImageData = USERINPUT_ImageData.read()
        else:
            USERINPUT_ImageData = open(DEFAULT_PATH_EXAMPLEIMAGE, 'rb').read()
        USERINPUT_ImageData = cv2.imdecode(np.frombuffer(USERINPUT_ImageData, np.uint8), cv2.IMREAD_COLOR)
        USERINPUT_Image = cv2.cvtColor(USERINPUT_ImageData, cv2.COLOR_BGR2RGB)
    # Webcam Snapshot
    else:
        USERINPUT_ImageReader = INPUTREADERS_IMAGE[USERINPUT_ImageInputChoice]
        webcamVid = USERINPUT_ImageReader()
        RegenerateWebcameSnapshot = st.button("Retake")
        ret, USERINPUT_Image = webcamVid.read()
        USERINPUT_Image = cv2.cvtColor(USERINPUT_Image, cv2.COLOR_BGR2RGB)
    
    return USERINPUT_Image

def UI_DisplayEffectImage(USERINPUT_Image, EffectImage):
    st.image(USERINPUT_Image, "Input Image", use_column_width=True)
    st.image(EffectImage, "Effected Image", use_column_width=True)

def UI_AvailableEffects():
    AvailableEffectsData = open(AVAILABLEEFFECTS_PATH, 'r').read().split('\n')
    AvailableEffectsNames = []
    for data in AvailableEffectsData:
        AvailableEffectsNames.append((data.split('('))[0])
    st.markdown("## Available Effects")
    col1, col2 = st.beta_columns(2)
    USERINPUT_EffectName = col1.selectbox("", AvailableEffectsNames)
    USERINPUT_EffectIndex = AvailableEffectsNames.index(USERINPUT_EffectName)
    USERINPUT_EffectData = AvailableEffectsData[USERINPUT_EffectIndex]
    col2.markdown("```pythonn\n" + USERINPUT_EffectData)

    return USERINPUT_EffectData

# Repo Based Functions
def videofx():
    # Title
    st.header("Video FX")

    # Load Inputs
    USERINPUT_Video = UI_VideoInputSource()
    UI_AvailableEffects()
    st.markdown("## Enter Effect Codes")
    CommonEffectsText = st.text_area("Common Effects Code", "None")
    EffectFuncsText = st.text_area("Effects Code", "None")
    CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    # Process Inputs and Display Output
    st.markdown("## Videos")
    UI_DisplayEffectVideo(USERINPUT_Video, -1, EffectFunc)

def imagefx():
    # Title
    st.header("Image FX")

    # Load Inputs
    USERINPUT_Image = UI_LoadImage()
    UI_AvailableEffects()
    st.markdown("## Enter Effect Codes")
    CommonEffectsText = st.text_area("Common Effects Code", "None")
    EffectFuncsText = st.text_area("Effects Code", "None")
    CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    # Process Inputs
    EffectImage = EffectFunc(USERINPUT_Image)

    # Display Output
    st.markdown("## Images")
    UI_DisplayEffectImage(USERINPUT_Image, EffectImage)

def effects():
    # Title
    st.header("Effects")

    # Load Inputs
    USERINPUT_Video = UI_VideoInputSource()
    USERINPUT_ChosenEffectData = UI_AvailableEffects()
    st.markdown("## Edit Effect Parameters")
    EffectFuncText = st.text_input("Effect Code", USERINPUT_ChosenEffectData)
    CommonEffects, EffectFuncs = GetEffectsCode('None', EffectFuncText)

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    # Process Inputs and Display Output
    st.markdown("## Videos")
    UI_DisplayEffectVideo(USERINPUT_Video, -1, EffectFunc, compactDisplay=True)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()