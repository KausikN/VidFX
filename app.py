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
from PIL import Image
from tqdm import tqdm

# from StreamLitGUI.webcam import webcam
# from webcam import webcam

import VidFX
# import ImageFX
# import ImageEffectTransistionFX

from Utils import VideoUtils
from EffectsLibrary import EffectsLibrary
from Utils import ParserUtils
from Utils import EffectTransistionUtils

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
DEFAULT_PATH_EXAMPLEIMAGE = 'TestFiles/TestImgs/Horse.PNG'
DEFAULT_PATH_EXAMPLEVIDEO = 'TestFiles/TestVids/Test_Animation.wmv'
AVAILABLEEFFECTS_PATH = 'StreamLitGUI/AvailableEffects.json'

DEFAULT_SAVEPATH_IMAGE = 'TestFiles/TestImgs/OutputImage.png'
DEFAULT_SAVEPATH_VIDEO = 'TestFiles/TestImgs/OutputVideo.mp4'
DEFAULT_SAVEPATH_GIF = 'TestFiles/TestImgs/OutputGIF.gif'

DEFAULT_CODE_PACKAGE = 'StreamLitGUI/CacheData/'
DEFAULT_CACHEPATH = 'StreamLitGUI/CacheData/Cache.json'
DEFAULT_FRAMESPATH = 'StreamLitGUI/DefaultData/Frames/'

OUTPUT_NCOLS = 5

IMAGESIZE_MIN = [1, 1]
IMAGESIZE_MAX = [512, 512]
IMAGESIZE_DEFAULT = [100, 100]
IMAGESIZEINDICATORIMAGE_SIZE = [128, 128]

DISPLAY_IMAGESIZE = [512, 512]
DISPLAY_INTERPOLATION = cv2.INTER_NEAREST
DISPLAY_DELAY = 0.1

INPUTREADERS_VIDEO = VideoUtils.INPUTREADERS_VIDEO
INPUTREADERS_IMAGE = VideoUtils.INPUTREADERS_IMAGE

TYPE_MAP = {
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "list": ParserUtils.ListParser
}

TRANSISTION_FUNCS = {
    "Constant": EffectTransistionUtils.EffectTransistion_Constant,
    "Linear": EffectTransistionUtils.EffectTransistion_Linear
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
    # Load from JSON
    # AVAILABLE_EFFECTS = json.load(open(AVAILABLEEFFECTS_PATH, 'r'))["effects"]
    # Load from EffectLibrary
    AVAILABLE_EFFECTS = EffectsLibrary.AVAILABLE_EFFECTS

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

from Utils import EffectTransistionUtils
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
def UI_SelectNCols():
    global OUTPUT_NCOLS
    OUTPUT_NCOLS = st.sidebar.slider('Number of Columns', 1, 10, 5)

def UI_VideoInputSource():
    USERINPUT_VideoInputChoice = st.selectbox("Select Video Input Source", list(INPUTREADERS_VIDEO.keys()))
    USERINPUT_VideoReader = INPUTREADERS_VIDEO[USERINPUT_VideoInputChoice]

    # Upload Video File
    if USERINPUT_VideoInputChoice == "Upload Video File":
        USERINPUT_VideoPath = st.file_uploader("Upload Video", ['avi', 'mp4', 'wmv'])
        if USERINPUT_VideoPath is None:
            USERINPUT_VideoPath = DEFAULT_PATH_EXAMPLEVIDEO
        USERINPUT_VideoReader = functools.partial(USERINPUT_VideoReader, USERINPUT_VideoPath)
    # Video URL
    elif USERINPUT_VideoInputChoice == "Video URL":
        USERINPUT_VideoURL = st.text_input("Video URL", "http://192.168.0.102:8080/shot.jpg")
        USERINPUT_VideoReader = functools.partial(USERINPUT_VideoReader, USERINPUT_VideoURL)
    # Webcam
    else:
        pass

    USERINPUT_Video = USERINPUT_VideoReader()
    
    return USERINPUT_Video

def UI_DisplayEffectVideo(vid=None, max_frames=-1, EffectFunc=None, compactDisplay=False):
    frameCount = 0

    # Check if camera opened successfully
    if (vid.isOpened()== False):
        print("Error opening video stream or file")

    col1, col2 = st, st
    if compactDisplay:
        col1, col2 = st.columns(2)

    inputVideoDisplay = col1.empty()
    effectVideoDisplay = col2.empty()

    # Read until video is completed
    while(vid.isOpened() and ((not (frameCount == max_frames)) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            inputVideoDisplay.image(frame, caption='Input Video', use_column_width=compactDisplay)
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
    # Upload Image URL
    elif USERINPUT_ImageInputChoice == "Image URL":
        USERINPUT_ImageReader = INPUTREADERS_IMAGE[USERINPUT_ImageInputChoice]
        USERINPUT_ImageURL = st.text_input("Enter Video URL", "http://192.168.0.102:8080/shot.jpg")
        urlVid = USERINPUT_ImageReader(USERINPUT_ImageURL)
        RegenerateWebcameSnapshot = st.button("Retake")
        ret, USERINPUT_Image = urlVid.read()
        USERINPUT_Image = cv2.cvtColor(USERINPUT_Image, cv2.COLOR_BGR2RGB)
    # Webcam Snapshot
    else:
        USERINPUT_ImageReader = INPUTREADERS_IMAGE[USERINPUT_ImageInputChoice]
        webcamVid = USERINPUT_ImageReader()
        RegenerateWebcameSnapshot = st.button("Retake")
        ret, USERINPUT_Image = webcamVid.read()
        USERINPUT_Image = cv2.cvtColor(USERINPUT_Image, cv2.COLOR_BGR2RGB)
    
    return USERINPUT_Image

def UI_DisplayEffectImage(USERINPUT_Image, EffectImage, compactDisplay=False):
    col1, col2 = st, st
    if compactDisplay:
        col1, col2 = st.columns(2)
    col1.image(USERINPUT_Image, "Input Image", use_column_width=True)
    col2.image(EffectImage, "Effected Image", use_column_width=True)

def UI_ShowAvailableEffects():
    AvailableEffectsNames = GetNames(AVAILABLE_EFFECTS)
    st.markdown("## Available Effects")
    col1, col2 = st.columns(2)
    USERINPUT_EffectName = st.selectbox("Select Effect", AvailableEffectsNames)
    USERINPUT_EffectIndex = AvailableEffectsNames.index(USERINPUT_EffectName)
    USERINPUT_EffectCode = AVAILABLE_EFFECTS[USERINPUT_EffectIndex]["code"]
    st.markdown("<font size=\"2\">Code</font>", unsafe_allow_html=True)
    st.markdown("\n```python\n" + USERINPUT_EffectCode)

    return USERINPUT_EffectCode

# UI TRANSISTION EFFECT FUNCTIONS ###################################################################################################################
def UI_DisplayEffectTransistionVideo(I=None, max_frames=-1, EffectFuncs=None, compactDisplay=False):
    MainEffectFunc = EffectFuncs['Main']
    CommonEffects_Tr = EffectFuncs['Common']
    EffectFuncs_Tr = EffectFuncs['Effect']

    frames = np.linspace(0, 1, max_frames)

    col1, col2 = st, st
    if compactDisplay:
        col1, col2 = st.columns(2)

    col1.image(I, "Input Image", use_column_width=True)
    effectVideoDisplay = col2.empty()

    # Generate
    frames_effect = []
    for frame in frames:
        MainFunc = EffectTransistionUtils.GetMainFunc(MainEffectFunc, CommonEffects_Tr, EffectFuncs_Tr, frame, recursiveArgs=False)
        outFrame = MainFunc(I)
        frames_effect.append(outFrame)
        effectVideoDisplay.image(outFrame, caption='Effect Video', use_column_width=True)

    # Save
    frames_effect = list(map(Image.fromarray, frames_effect))
    extraFrames = []
    if len(frames_effect) > 1:
        extraFrames = frames_effect[1:]
    frames_effect[0].save(DEFAULT_SAVEPATH_GIF, save_all=True, append_images=extraFrames, format='GIF', loop=0)
    effectVideoDisplay.image(DEFAULT_SAVEPATH_GIF, caption='Effect Video', use_column_width=True)

def UI_Param_EffectTransistions(p, col1=st, col2=st, col3=st, key=""):
    # Parse type
    inp_start = None
    inp_end = None
    TransistionFunc = None
    inp_type = p["type"]
    if p["type"] == "bool":
        inp_start = col1.checkbox(p["name"] + " Start", p["default"], key=p["name"] + "_start_" + key)
        inp_end = col2.checkbox(p["name"] + " End", p["default"], key=p["name"] + "_end_" + key)
    elif p["type"] == "int":
        inp_start = col1.slider(p["name"] + " Start", p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_start_" + key)
        inp_end = col2.slider(p["name"] + " End", p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_end_" + key)
    elif p["type"] == "float":
        inp_start = col1.slider(p["name"] + " Start", p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_start_" + key)
        inp_end = col2.slider(p["name"] + " End", p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_end_" + key)
    elif p["type"] == "str":
        inp_start = col1.text_input(p["name"], p["default"], key=p["name"] + "_" + key)
        inp_end = inp_start
    elif p["type"].startswith("list"):
        typeSplit = p["type"].split(":")
        if typeSplit[1] in ["str", "key", "frame"]:
            inp_start = col1.text_area(p["name"], '\n'.join(list(map(str, p["default"]))), key=p["name"] + "_start_" + key)
            inp_end = inp_start
        else:
            inp_start = col1.text_area(p["name"] + " Start", '\n'.join(list(map(str, p["default"]))), key=p["name"] + "_start_" + key)
            inp_end = col2.text_area(p["name"] + " End", '\n'.join(list(map(str, p["default"]))), key=p["name"] + "_end_" + key)
        
        inp_start = TYPE_MAP[typeSplit[0]](inp_start, TYPE_MAP[typeSplit[1]])
        inp_end = TYPE_MAP[typeSplit[0]](inp_end, TYPE_MAP[typeSplit[1]])
    elif p["type"] == "frame":
        frameName = col1.selectbox("Select Frame", ["Select Frame"] + FRAMES, key=p["name"] + "_frametr_" + key)
        inp_start = None
        if not (frameName == "Select Frame"):
            inp_start = os.path.join(DEFAULT_FRAMESPATH, frameName)
            inp_start = inp_start.replace('"', '\\"')
            inp_start = '"' + inp_start + '"'
    else:
        return None, None, None

    if inp_end is not None:
        TransistionFunc = TRANSISTION_FUNCS[col3.selectbox(p["name"] + " Transistion", list(TRANSISTION_FUNCS.keys()), key=p["name"] + "_trf_" + key)]
    else:
        inp_end = inp_start
        TransistionFunc = TRANSISTION_FUNCS['Constant']

    return inp_start, inp_end, TransistionFunc
    
def UI_EffectSelector_EffectTransistions(AvailableEffectsNames, key=""):
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    USERINPUT_EffectName = col1.selectbox("", AvailableEffectsNames, key="EN_" + key)
    USERINPUT_EffectIndex = AvailableEffectsNames.index(USERINPUT_EffectName)
    USERINPUT_EffectData = AVAILABLE_EFFECTS[USERINPUT_EffectIndex]
    ParamsInputs = UI_Params_EffectTransistions(USERINPUT_EffectData["params"], col1=col2, col2=col3, col3=col4, key=key)
    USERINPUT_EffectFunc = functools.partial(USERINPUT_EffectData["func"]) # Params Tranisiton is applied later
    USERINPUT_EffectCode = USERINPUT_EffectData["name"]
    return USERINPUT_EffectCode, ParamsInputs, USERINPUT_EffectFunc

def UI_Params_EffectTransistions(paramsData, col1=st, col2=st, col3=st, key=""):
    ParamsInputs = {}
    for p in paramsData:
        inp_start, inp_end, TransistionFunc = UI_Param_EffectTransistions(p, col1, col2, col3, key)
        ParamsInputs[p["name"]] = {"start": inp_start, "end": inp_end, "func": TransistionFunc}
    return ParamsInputs

# UI EFFECT FUNCTIONS ###########################################################################################################################
def UI_Param_Effects(p, col=st, key=""):
    # Parse type
    inp = None
    if p["type"] == "bool":
        inp = col.checkbox(p["name"], p["default"], key=p["name"] + "_" + key)
    elif p["type"] == "int":
        inp = col.slider(p["name"], p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_" + key)
    elif p["type"] == "float":
        inp = col.slider(p["name"], p["min"], p["max"], p["default"], p["step"], key=p["name"] + "_" + key)
    elif p["type"] == "str":
        inp = col.text_input(p["name"], p["default"], key=p["name"] + "_" + key)
    elif p["type"].startswith("list"):
        inp = col.text_area(p["name"], '\n'.join(list(map(str, p["default"]))), key=p["name"] + "_" + key)
        typeSplit = p["type"].split(":")
        inp = TYPE_MAP[typeSplit[0]](inp, TYPE_MAP[typeSplit[1]])
    elif p["type"] == "frame":
        frameName = col.selectbox("Select Frame", ["Select Frame"] + FRAMES, key=p["name"] + "_framen_" + key)
        inp = None
        if not (frameName == "Select Frame"):
            inp = os.path.join(DEFAULT_FRAMESPATH, frameName)
    else:
        return None

    return inp
    
def UI_EffectSelector_Effects(AvailableEffectsNames, key=""):
    col1, col2 = st.columns(2)
    USERINPUT_EffectName = col1.selectbox("", AvailableEffectsNames, key="EN_" + key)
    USERINPUT_EffectIndex = AvailableEffectsNames.index(USERINPUT_EffectName)
    USERINPUT_EffectData = AVAILABLE_EFFECTS[USERINPUT_EffectIndex]
    ParamsInputs = UI_Params_Effects(USERINPUT_EffectData["params"], col=col2, key=key)
    USERINPUT_EffectFunc = functools.partial(USERINPUT_EffectData["func"]) # Params are applied later
    USERINPUT_EffectCode = USERINPUT_EffectData["name"]
    return USERINPUT_EffectCode, ParamsInputs, USERINPUT_EffectFunc

def UI_Params_Effects(paramsData, col=st, key=""):
    ParamsInputs = {}
    for p in paramsData:
        inp = UI_Param_Effects(p, col, key)
        if inp is not None:
            ParamsInputs[p["name"]] = inp
    return ParamsInputs
####################################################################################################################
def UI_DisplayRepeater(AvailableEffectsNames, EffectMode=UI_EffectSelector_Effects):
    USERINPUT_DisplayCount = st.slider("Select Number of Displays", 1, 10, 1, key="Dn")

    EffectFuncsTextList = []
    EffectFuncsParamsInputs = []
    EffectFuncsGroup = []
    for c in range(USERINPUT_DisplayCount):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Display " + str(c+1))
        EffectsListText, EffectsParamsInputs, EffectFuncs = UI_EffectsRepeater(AvailableEffectsNames, str(c+1), EffectMode=EffectMode)
        st.markdown("<hr>", unsafe_allow_html=True)
        EffectFuncsTextList.append(EffectsListText)
        EffectFuncsParamsInputs.append(EffectsParamsInputs)
        EffectFuncsGroup.append(EffectFuncs)
    EffectFuncsText = "\n,\n".join(EffectFuncsTextList)
    
    return EffectFuncsText, EffectFuncsParamsInputs, EffectFuncsGroup

def UI_EffectsRepeater(AvailableEffectsNames, displayKey="", EffectMode=UI_EffectSelector_Effects):
    USERINPUT_EffectCount = st.slider("Select Number of Effects", 1, 10, 1, key="En_" + str(displayKey))

    EffectsList = []
    EffectsParamsInputs = []
    EffectFuncs = []
    for e in range(USERINPUT_EffectCount):
        key = str(displayKey) + "_" + str(e)
        EffectCode, ParamsInputs, EffectFunc = EffectMode(AvailableEffectsNames, key)
        EffectsList.append(EffectCode)
        EffectsParamsInputs.append(ParamsInputs)
        EffectFuncs.append(EffectFunc)
    EffectsListText = "\n".join(EffectsList)

    return EffectsListText, EffectsParamsInputs, EffectFuncs

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
    CommonEffectsText, ParamInputs_Common, CommonEffects = UI_EffectsRepeater(AvailableEffectsNames, displayKey="CE", EffectMode=UI_EffectSelector_Effects)

    st.markdown("## Choose Display Effects")
    EffectFuncsText, ParamInputs_Effects, EffectFuncs = UI_DisplayRepeater(AvailableEffectsNames, EffectMode=UI_EffectSelector_Effects)

    UI_SelectNCols()

    # CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    # Apply Params
    EffectFuncs_PA = []
    CommonFuncs_PA = []
    for i in range(len(EffectFuncs)):
        efs = EffectFuncs[i]
        efs_tr = []
        for j in range(len(efs)):
            ef = efs[j]
            paramsData = ParamInputs_Effects[i][j]
            funcData = functools.partial(ef.func, **paramsData)
            efs_tr.append(funcData)
        EffectFuncs_PA.append(efs_tr)
    for i in range(len(CommonEffects)):
        efs = CommonEffects[i]
        paramsData = ParamInputs_Common[i]
        funcData = functools.partial(efs.func, **paramsData)
        CommonFuncs_PA.append(funcData)
    CommonEffects = CommonFuncs_PA
    EffectFuncs = EffectFuncs_PA

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    USERINPUT_CompactDisplay = st.sidebar.checkbox("Compact Display", False)

    # Process Inputs and Display Output
    st.markdown("## Videos")
    UI_DisplayEffectVideo(USERINPUT_Video, -1, EffectFunc, USERINPUT_CompactDisplay)

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
    CommonEffectsText, ParamInputs_Common, CommonEffects = UI_EffectsRepeater(AvailableEffectsNames, displayKey="CE", EffectMode=UI_EffectSelector_Effects)

    st.markdown("## Choose Display Effects")
    EffectFuncsText, ParamInputs_Effects, EffectFuncs = UI_DisplayRepeater(AvailableEffectsNames, EffectMode=UI_EffectSelector_Effects)

    UI_SelectNCols()

    # CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    # Apply Params
    EffectFuncs_PA = []
    CommonFuncs_PA = []
    for i in range(len(EffectFuncs)):
        efs = EffectFuncs[i]
        efs_tr = []
        for j in range(len(efs)):
            ef = efs[j]
            paramsData = ParamInputs_Effects[i][j]
            funcData = functools.partial(ef.func, **paramsData)
            efs_tr.append(funcData)
        EffectFuncs_PA.append(efs_tr)
    for i in range(len(CommonEffects)):
        efs = CommonEffects[i]
        paramsData = ParamInputs_Common[i]
        funcData = functools.partial(efs.func, **paramsData)
        CommonFuncs_PA.append(funcData)
    CommonEffects = CommonFuncs_PA
    EffectFuncs = EffectFuncs_PA

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    USERINPUT_CompactDisplay = st.sidebar.checkbox("Compact Display", False)

    # Process Inputs
    EffectImage = EffectFunc(USERINPUT_Image)

    # Display Output
    st.markdown("## Images")
    UI_DisplayEffectImage(USERINPUT_Image, EffectImage, USERINPUT_CompactDisplay)

def image_effect_transistion():
    # Title
    st.header("Image Effect Transistion")

    # Load Inputs
    USERINPUT_Image = UI_LoadImage()

    LoadAvailableEffects()
    LoadFrames()

    UI_ShowAvailableEffects()
    AvailableEffectsNames = GetNames(AVAILABLE_EFFECTS)
    
    st.markdown("## Choose Common Effects")
    CommonEffectsText, ParamsInputs_Common, CommonEffects = UI_EffectsRepeater(AvailableEffectsNames, displayKey="CE", EffectMode=UI_EffectSelector_EffectTransistions)

    st.markdown("## Choose Effects Transistions")
    EffectFuncsText, ParamsInputs_Effects, EffectFuncs = UI_DisplayRepeater(AvailableEffectsNames, EffectMode=UI_EffectSelector_EffectTransistions)

    UI_SelectNCols()

    # CommonEffects, EffectFuncs = GetEffectsCode(CommonEffectsText, EffectFuncsText)

    EffectFuncs_Tr = []
    CommonFuncs_Tr = []
    for i in range(len(EffectFuncs)):
        efs = EffectFuncs[i]
        efs_tr = []
        for j in range(len(efs)):
            ef = efs[j]
            paramsData = {}
            for k in ParamsInputs_Effects[i][j].keys():
                pD = ParamsInputs_Effects[i][j][k]
                if pD["func"] is not None:
                    paramsData[k] = functools.partial(pD["func"], start=pD["start"], end=pD["end"])
            trData = [ef, paramsData]
            efs_tr.append(trData)
        EffectFuncs_Tr.append(efs_tr)
    for i in range(len(CommonEffects)):
        efs = CommonEffects[i]
        paramsData = {}
        for k in ParamsInputs_Common[i].keys():
            pD = ParamsInputs_Common[i][k]
            if pD["func"] is not None:
                paramsData[k] = functools.partial(pD["func"], start=pD["start"], end=pD["end"])
        trData = [efs, paramsData]
        CommonFuncs_Tr.append(trData)

    saveI_keys = EffectsLibrary.GetSaveIKeys(EffectFuncs)
    MainFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)
    
    EffectFunctions = {
        "Main": MainFunc,
        "Common": CommonFuncs_Tr,
        "Effect": EffectFuncs_Tr
    }

    USERINPUT_FrameCount = st.slider("Frames Count", 1, 100, 20, 1)
    USERINPUT_CompactDisplay = st.sidebar.checkbox("Compact Display", False)
    
    # Process Inputs and Display Output
    UI_DisplayEffectTransistionVideo(USERINPUT_Image, USERINPUT_FrameCount, EffectFunctions, USERINPUT_CompactDisplay)

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

    UI_SelectNCols()

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    USERINPUT_CompactDisplay = st.sidebar.checkbox("Compact Display", False)

    # Process Inputs and Display Output
    st.markdown("## Videos")
    UI_DisplayEffectVideo(USERINPUT_Video, -1, EffectFunc, USERINPUT_CompactDisplay)

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

    UI_SelectNCols()

    EffectFuncs, saveI_keys = EffectsLibrary.Image_ReplaceRedundantEffectChains(EffectFuncs, display=False)
    EffectFunc = functools.partial(EffectsLibrary.Image_MultipleImages_RemovedRecompute, CommonEffects=CommonEffects, EffectFuncs=EffectFuncs, nCols=OUTPUT_NCOLS, saveI_keys=saveI_keys)

    USERINPUT_CompactDisplay = st.sidebar.checkbox("Compact Display", False)

    # Process Inputs
    EffectImage = EffectFunc(USERINPUT_Image)

    # Display Output
    st.markdown("## Images")
    UI_DisplayEffectImage(USERINPUT_Image, EffectImage, USERINPUT_CompactDisplay)

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