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
from Utils import ParserUtils

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
AVAILABLEEFFECTS_PATH = 'StreamLitGUI/AvailableEffects.json'

DEFAULT_SAVEPATH_IMAGE = 'TestImgs/OutputImage.png'
DEFAULT_SAVEPATH_VIDEO = 'TestImgs/OutputVideo.mp4'
DEFAULT_SAVEPATH_GIF = 'TestImgs/OutputGIF.gif'

DEFAULT_CODE_PACKAGE = 'StreamLitGUI/CacheData/'
DEFAULT_CACHEPATH = 'StreamLitGUI/CacheData/Cache.json'
DEFAULT_FRAMESPATH = 'Frames/'

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

TYPE_MAP = {
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "list": ParserUtils.ListParser
}

# Util Vars
CACHE_DATA = {}
AVAILABLE_EFFECTS = []
FRAMES = []

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

def LoadAvailableEffects():
    global AVAILABLE_EFFECTS
    AVAILABLE_EFFECTS = json.load(open(AVAILABLEEFFECTS_PATH, 'r'))["effects"]

def GetNames(data):
    names = []
    for d in data:
        names.append(d["name"])
    return names

def LoadCache():
    global CACHE_DATA
    CACHE_DATA = json.load(open(DEFAULT_CACHEPATH, 'r'))

def SaveCache():
    global CACHE_DATA
    json.dump(CACHE_DATA, open(DEFAULT_CACHEPATH, 'w'))

def LoadFrames():
    global FRAMES
    FRAMES = []
    for f in os.listdir(DEFAULT_FRAMESPATH):
        FRAMES.append(f)

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
    exec(CommonEffectsCode, globals())
    CommonEffects = pickle.load(open(os.path.join(DEFAULT_CODE_PACKAGE, "CommonEffects.p"), 'rb'))

    EffectFuncsCode = ImportsCode + "EffectFuncs = " + VidFX.UIMultiEffectsCodeParser(EffectFuncsText) + SavePickleCode.format(DEFAULT_CODE_PACKAGE=DEFAULT_CODE_PACKAGE, EffectObj='EffectFuncs')
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

def UI_ShowAvailableEffects():
    AvailableEffectsNames = GetNames(AVAILABLE_EFFECTS)
    st.markdown("## Available Effects")
    col1, col2 = st.beta_columns(2)
    USERINPUT_EffectName = st.selectbox("Select Effect", AvailableEffectsNames)
    USERINPUT_EffectIndex = AvailableEffectsNames.index(USERINPUT_EffectName)
    USERINPUT_EffectCode = AVAILABLE_EFFECTS[USERINPUT_EffectIndex]["code"]
    st.markdown("<font size=\"2\">Code</font>", unsafe_allow_html=True)
    st.markdown("\n```python\n" + USERINPUT_EffectCode)

    return USERINPUT_EffectCode

def UI_DisplayRepeater(AvailableEffectsNames):
    USERINPUT_DisplayCount = st.slider("Select Number of Displays", 1, 10, 1, key="Dn")

    EffectFuncsTextList = []
    for c in range(USERINPUT_DisplayCount):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Display " + str(c+1))
        EffectsListText = UI_EffectsRepeater(AvailableEffectsNames, str(c+1))
        st.markdown("<hr>", unsafe_allow_html=True)
        EffectFuncsTextList.append(EffectsListText)
    EffectFuncsText = "\n,\n".join(EffectFuncsTextList)

    return EffectFuncsText

def UI_EffectsRepeater(AvailableEffectsNames, displayKey=""):
    USERINPUT_EffectCount = st.slider("Select Number of Effects", 1, 10, 1, key="En_" + str(displayKey))

    EffectsList = []
    for e in range(USERINPUT_EffectCount):
        key = str(displayKey) + "_" + str(e)
        USERINPUT_EffectCode = UI_EffectSelector(AvailableEffectsNames, key)
        EffectsList.append(USERINPUT_EffectCode)
    EffectsListText = "\n".join(EffectsList)

    return EffectsListText
    
def UI_EffectSelector(AvailableEffectsNames, key=""):
    col1, col2 = st.beta_columns(2)
    USERINPUT_EffectName = col1.selectbox("", AvailableEffectsNames, key="EN_" + key)
    USERINPUT_EffectIndex = AvailableEffectsNames.index(USERINPUT_EffectName)
    USERINPUT_EffectData = AVAILABLE_EFFECTS[USERINPUT_EffectIndex]
    ParamsInputs = UI_Params(USERINPUT_EffectData["params"], col=col2, key=key)
    USERINPUT_EffectCode = USERINPUT_EffectData["name"] + "(" + ParamsInputs + ")"
    return USERINPUT_EffectCode

def UI_Params(paramsData, col=st, key=""):
    ParamsInputs = []
    for p in paramsData:
        inp = UI_Param(p, col, key)
        ParamsInputs.append(p["name"] + "=" + str(inp))
    ParamsInputsText = ", ".join(ParamsInputs)
    return ParamsInputsText

def UI_Param(p, col=st, key=""):
    # Parse type
    inp = None
    inp_type = p["type"]
    if p["type"] == "bool":
        inp = col.checkbox(p["name"], p["default"], key=p["name"] + "_" + key)
    elif p["type"] == "int":
        inp = col.slider(p["name"], p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_" + key)
    elif p["type"] == "float":
        inp = col.slider(p["name"], p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_" + key)
    elif p["type"] == "str":
        inp = col.text_input(p["name"], p["default"], key=p["name"] + "_" + key)
        inp = inp.replace('"', '\\"')
        inp = '"' + inp + '"'
    elif p["type"].startswith("list"):
        inp = col.text_area(p["name"], '\n'.join(list(map(str, p["default"]))), key=p["name"] + "_" + key)
        typeSplit = p["type"].split(":")
        inp = TYPE_MAP[typeSplit[0]](inp, TYPE_MAP[typeSplit[1]])
    elif p["type"] == "frame":
        frameName = st.selectbox("Select Frame", ["Select Frame"] + FRAMES)
        inp = None
        if not (frameName == "Select Frame"):
            inp = os.path.join(DEFAULT_FRAMESPATH, frameName)
            inp = inp.replace('"', '\\"')
            inp = '"' + inp + '"'

    return inp

# Repo Based Functions
def videofx():
    # Title
    st.header("Video FX")

    # Load Inputs
    USERINPUT_Video = UI_VideoInputSource()

    LoadAvailableEffects()
    LoadFrames()

    UI_ShowAvailableEffects()
    AvailableEffectsNames = GetNames(AVAILABLE_EFFECTS)
    
    st.markdown("## Choose Common Effects")
    CommonEffectsText = UI_EffectSelector(AvailableEffectsNames, key="CE")

    st.markdown("## Choose Display Effects")
    EffectFuncsText = UI_DisplayRepeater(AvailableEffectsNames)

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

    LoadAvailableEffects()
    LoadFrames()

    UI_ShowAvailableEffects()
    AvailableEffectsNames = GetNames(AVAILABLE_EFFECTS)
    
    st.markdown("## Choose Common Effects")
    CommonEffectsText = UI_EffectSelector(AvailableEffectsNames, key="CE")

    st.markdown("## Choose Display Effects")
    EffectFuncsText = UI_DisplayRepeater(AvailableEffectsNames)

    CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    # Process Inputs
    EffectImage = EffectFunc(USERINPUT_Image)

    # Display Output
    st.markdown("## Images")
    UI_DisplayEffectImage(USERINPUT_Image, EffectImage)

def videofx_text_based():
    # Title
    st.header("Video FX (Text Based)")

    # Load Inputs
    USERINPUT_Video = UI_VideoInputSource()
    LoadAvailableEffects()
    UI_ShowAvailableEffects()
    st.markdown("## Enter Effect Codes")
    CommonEffectsText = st.text_area("Common Effects Code", "None")
    EffectFuncsText = st.text_area("Effects Code", "None")
    CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    # Process Inputs and Display Output
    st.markdown("## Videos")
    UI_DisplayEffectVideo(USERINPUT_Video, -1, EffectFunc)

def imagefx_text_based():
    # Title
    st.header("Image FX (Text Based)")

    # Load Inputs
    USERINPUT_Image = UI_LoadImage()
    LoadAvailableEffects()
    UI_ShowAvailableEffects()
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
    LoadAvailableEffects()
    USERINPUT_ChosenEffectData = UI_ShowAvailableEffects()
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