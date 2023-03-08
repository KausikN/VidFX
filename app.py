"""
Stream lit GUI for hosting VidFX
"""

# Imports
import os
import cv2
import json
import pickle
import functools
import numpy as np
from PIL import Image
from tqdm import tqdm
import streamlit as st
import graphviz

from VidFX import *

from Utils.EffectTransistionUtils import *
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
PATHS = {
    "cache": "StreamLitGUI/CacheData/Cache.json",
    "default": {
        "example": {
            "image": "TestFiles/TestImgs/Horse.PNG",
            "video": "TestFiles/TestVids/Test_Animation.wmv"
        },
        "save": {
            "image": "TestFiles/TestImgs/OutputImage.png",
            "video": "TestFiles/TestImgs/OutputVideo.mp4",
            "gif": "TestFiles/TestImgs/OutputGIF.gif"
        },
        "dir": {
            "frames": "StreamLitGUI/DefaultData/Frames/",
            "code_package": "StreamLitGUI/CacheData/"
        }
    },
    "available_effects": "StreamLitGUI/AvailableEffects.json",
    "tree_cache": "StreamLitGUI/CacheData/EffectTreeCache.p",
    "transistion_tree_cache": "StreamLitGUI/CacheData/TransistionEffectTreeCache.p"
}

OUTPUT_NCOLS = 5

IMAGESIZE_MIN = [1, 1]
IMAGESIZE_MAX = [512, 512]
IMAGESIZE_DEFAULT = [100, 100]
IMAGESIZEINDICATORIMAGE_SIZE = [128, 128]

DISPLAY_IMAGESIZE = [512, 512]
DISPLAY_INTERPOLATION = cv2.INTER_NEAREST
DISPLAY_DELAY = 0.1

TYPE_MAP = {
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "list": ParserUtils.ListParser
}

# Util Vars
CACHE = {}
FRAMES = []

# Util Functions
def GetNames(data):
    return [d["name"] for d in data]

def Hex_to_RGB(val):
    val = val.lstrip('#')
    lv = len(val)
    return tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def RGB_to_Hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def LoadCache():
    global CACHE
    CACHE = json.load(open(PATHS["cache"], 'r'))
def SaveCache():
    global CACHE
    json.dump(CACHE, open(PATHS["cache"], 'w'))

def LoadEffectTreeCache():
    global EFFECT_TREE
    if not os.path.exists(PATHS["tree_cache"]): return EFFECT_TREE
    EFFECT_TREE = pickle.load(open(PATHS["tree_cache"], 'rb'))
    return EFFECT_TREE
def SaveEffectTreeCache():
    global EFFECT_TREE
    pickle.dump(EFFECT_TREE, open(PATHS["tree_cache"], 'wb'))

def LoadTransistionEffectTreeCache():
    global EFFECT_TREE
    if not os.path.exists(PATHS["transistion_tree_cache"]): return EFFECT_TREE
    EFFECT_TREE = pickle.load(open(PATHS["transistion_tree_cache"], 'rb'))
    return EFFECT_TREE
def SaveTransistionEffectTreeCache():
    global EFFECT_TREE
    pickle.dump(EFFECT_TREE, open(PATHS["transistion_tree_cache"], 'wb'))

@st.cache
def GenerateImageSizeIndicatorImage(ImageSize):
    ### Image Size Indicator Image 
    ImageSizeIndicator_Image = np.zeros((IMAGESIZEINDICATORIMAGE_SIZE[0], IMAGESIZEINDICATORIMAGE_SIZE[1]), dtype=int)
    ImageSizeIndicator_Image[:int((ImageSize[0]/IMAGESIZE_MAX[0])*IMAGESIZEINDICATORIMAGE_SIZE[0]), :int((ImageSize[1]/IMAGESIZE_MAX[1])*IMAGESIZEINDICATORIMAGE_SIZE[1])] = 255
    return ImageSizeIndicator_Image

def Frames_Load():
    global FRAMES
    FRAMES = []
    for f in os.listdir(PATHS["default"]["dir"]["frames"]):
        FRAMES.append(f)

# Main Functions


# UI Functions
def UI_ShowAvailableEffects():
    '''
    UI - Show Available Effects
    '''
    # Init
    AvailableEffectsNames = list(AVAILABLE_EFFECTS.keys())
    # Display
    st.markdown("## Available Effects")
    col1, col2 = st.columns(2)
    USERINPUT_EffectName = st.selectbox("Select Effect", AvailableEffectsNames)
    USERINPUT_EffectCode = AVAILABLE_EFFECTS[USERINPUT_EffectName]["code"]
    st.markdown("<font size=\"2\">Code</font>", unsafe_allow_html=True)
    st.markdown("\n```python\n" + USERINPUT_EffectCode)

    return USERINPUT_EffectCode

## UI Load Functions
def UI_VideoInputSource():
    USERINPUT_VideoInputChoice = st.selectbox("Select Video Input Source", list(INPUTREADERS_VIDEO.keys()))
    USERINPUT_VideoReader = INPUTREADERS_VIDEO[USERINPUT_VideoInputChoice]

    # Upload Video File
    if USERINPUT_VideoInputChoice == "Upload Video File":
        USERINPUT_VideoPath = st.file_uploader("Upload Video", ["avi", "mp4", "wmv"])
        if USERINPUT_VideoPath is None:
            USERINPUT_VideoPath = PATHS["default"]["example"]["video"]
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

def UI_LoadImage():
    '''
    UI - Load Image
    '''
    # Select Image Input Source
    USERINPUT_ImageInputChoice = st.selectbox("Select Image Input Source", list(INPUTREADERS_IMAGE.keys()))
    # Load Image
    USERINPUT_Image = None
    # Upload Image File
    if USERINPUT_ImageInputChoice == "Upload Image File":
        USERINPUT_ImageReader = INPUTREADERS_IMAGE[USERINPUT_ImageInputChoice] # Unused Reader as image is loaded directly
        USERINPUT_ImageData = st.file_uploader("Upload Image", ['png', 'jpg', 'jpeg', 'bmp'])
        if USERINPUT_ImageData is not None:
            USERINPUT_ImageData = USERINPUT_ImageData.read()
        else:
            USERINPUT_ImageData = open(PATHS["default"]["example"]["image"], 'rb').read()
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

## UI - Display Functions
def UI_DisplayEffectVideo(vid, EffectFunc, max_frames=-1, compact_display=False):
    '''
    UI - Display Effect Video
    '''
    # Check if camera opened successfully
    if (vid.isOpened()== False): st.error("Error opening video stream or file")
    # Set up display
    col1, col2 = st, st
    if compact_display: col1, col2 = st.columns(2)
    inputVideoDisplay = col1.empty()
    effectVideoDisplay = col2.empty()
    # Read until video is completed
    FRAME_COUNT = 0
    while(vid.isOpened() and ((not (FRAME_COUNT == max_frames)) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            inputVideoDisplay.image(frame, caption='Input Video', use_column_width=compact_display)
            # Apply Effect if needed
            if EffectFunc is not None:
                frame = EffectFunc(frame)
            # Display the resulting frame
            effectVideoDisplay.image(frame, caption='Effect Video', use_column_width=compact_display)
            FRAME_COUNT += 1
        # Break the loop
        else: 
            break
    # When everything done, release the video capture object
    vid.release()

def UI_DisplayEffectImage(USERINPUT_Image, EffectImage, compact_display=False):
    '''
    UI - Display Effect Image
    '''
    # Set up display
    col1, col2 = st, st
    if compact_display: col1, col2 = st.columns(2)
    # Display Images
    col1.image(USERINPUT_Image, "Input Image", use_column_width=True)
    col2.image(EffectImage, "Effected Image", use_column_width=True)

## UI - Effect Tree Functions
def UI_DisplayEffectTree(ROOT_NODE, EFFECT_TREE_NODES):
    '''
    UI - Display Effect Tree
    '''
    # Construct Tree Graph
    G = graphviz.Digraph(graph_attr={"rankdir": "LR"})
    ## Add Nodes
    G.node(ROOT_NODE.id, ROOT_NODE.id)
    for node_id in EFFECT_TREE_NODES.keys():
        G.node(node_id, node_id)
    ## Add Edges
    for child_conn_k in ROOT_NODE.children.keys():
        child_conn = ROOT_NODE.children[child_conn_k]
        conn_id = child_conn.start.id + "_" + child_conn.end.id
        G.node(conn_id, child_conn.effect["name"], shape="box")
        G.edge(ROOT_NODE.id, conn_id)
        G.edge(conn_id, child_conn.end.id)
    for node_id in EFFECT_TREE_NODES.keys():
        node = EFFECT_TREE_NODES[node_id]
        for child_conn_k in node.children.keys():
            child_conn = node.children[child_conn_k]
            conn_id = child_conn.start.id + "_" + child_conn.end.id
            G.node(conn_id, child_conn.effect["name"], shape="box")
            G.edge(node_id, conn_id)
            G.edge(conn_id, child_conn.end.id)
        # Display Tree Graph
    st.markdown("## Effect Tree")
    Graph_I = G.pipe(format="png")
    st.image(Graph_I, use_column_width=False)
    # st.write(G)

def UI_AddEffectTreeNode():
    '''
    UI - Add Effect Tree Node
    '''
    global EFFECT_TREE
    # Init
    PARENT_NODE_IDS = [EFFECT_TREE_ROOT_ID] + list(EFFECT_TREE["nodes"].keys())
    EFFECT_NAMES = list(AVAILABLE_EFFECTS.keys())
    # Load Inputs
    USERINPUT_ParentID = st.selectbox("Parent Node", PARENT_NODE_IDS)
    cols = st.columns((1, 3))
    USERINPUT_EffectName = cols[0].selectbox("New Effect", EFFECT_NAMES)
    USERINPUT_EffectParams = json.loads(cols[1].text_area(
        "New Effect Params", 
        json.dumps(AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"], indent=4),
        height=200
    ))
    # Add Node
    if st.button("Add"):
        ParentNode = EFFECT_TREE["root"] if USERINPUT_ParentID == EFFECT_TREE_ROOT_ID else EFFECT_TREE["nodes"][USERINPUT_ParentID]
        ## Set Connection Data
        NEW_CONNECTION_DATA = {
            "start": ParentNode,
            "end": None,
            "effect": dict(AVAILABLE_EFFECTS[USERINPUT_EffectName])
        }
        NEW_CONNECTION_DATA["effect"]["params"] = USERINPUT_EffectParams
        NEW_CONNECTION = EFFECT_TREE_CONNECTION(**NEW_CONNECTION_DATA)
        ## Set Node Data
        NEW_NODE_DATA = {
            "id": str(EFFECT_TREE["node_id_counter"]),
            "parent": NEW_CONNECTION,
        }
        EFFECT_TREE["nodes"][NEW_NODE_DATA["id"]] = EFFECT_TREE_NODE(**NEW_NODE_DATA)
        NEW_CONNECTION.end = EFFECT_TREE["nodes"][NEW_NODE_DATA["id"]]
        EFFECT_TREE["node_id_counter"] += 1
        ## Set Parent Data
        NEW_NODE_DATA["parent"].start.children[NEW_NODE_DATA["id"]] = NEW_CONNECTION

def UI_EditEffectTreeNode():
    '''
    UI - Edit Effect Tree Node
    '''
    global EFFECT_TREE
    # Init
    NODE_IDS = list(EFFECT_TREE["nodes"].keys())
    PARENT_NODE_IDS = [EFFECT_TREE_ROOT_ID] + list(EFFECT_TREE["nodes"].keys())
    EFFECT_NAMES = list(AVAILABLE_EFFECTS.keys())
    # Load Inputs
    ## Select Node
    USERINPUT_NodeID = st.selectbox("Select Node", NODE_IDS)
    CurNode = EFFECT_TREE["nodes"][USERINPUT_NodeID]
    CurConnection = CurNode.parent
    ## Edit
    USERINPUT_ParentID = st.selectbox(
        "Edit Parent Node", PARENT_NODE_IDS, 
        index=PARENT_NODE_IDS.index(CurConnection.start.id)
    )
    cols = st.columns((1, 3))
    USERINPUT_EffectName = cols[0].selectbox(
        "Edit Effect", EFFECT_NAMES,
        index=EFFECT_NAMES.index(CurConnection.effect["name"])
    )
    USERINPUT_EffectParams = json.loads(cols[1].text_area(
        "Edit Effect Params", 
        json.dumps(CurConnection.effect["params"], indent=4),
        height=200
    ))
    # Edit Node
    cols = st.columns(2)
    if cols[0].button("Edit"):
        ParentNode = EFFECT_TREE["root"] if USERINPUT_ParentID == EFFECT_TREE_ROOT_ID else EFFECT_TREE["nodes"][USERINPUT_ParentID]
        ## Set Connection Data
        CurConnection.start = ParentNode
        CurConnection.effect = dict(AVAILABLE_EFFECTS[USERINPUT_EffectName])
        CurConnection.effect["params"] = USERINPUT_EffectParams
        ## Set Node Data
        CurNode.parent = CurConnection
        ## Set Parent Data
        CurConnection.start.children[CurNode.id] = CurConnection
    if cols[1].button("Delete"):
        del CurConnection.start.children[CurNode.id]
        del EFFECT_TREE["nodes"][CurNode.id]

def UI_ConstructEffectTree():
    '''
    UI - Construct Effect Tree
    '''
    global EFFECT_TREE
    # Init
    st.markdown("## Construct Effect Tree")
    ## Load Tree Cache
    EFFECT_TREE = LoadEffectTreeCache()
    ## Display
    UI_DisplayEffectTree(EFFECT_TREE["root"], EFFECT_TREE["nodes"])
    # Node Operations
    USERINPUT_NodeOp = st.selectbox("Node Operations", ["-", "Add", "Edit", "Clear"])
    if USERINPUT_NodeOp == "Clear":
        if st.button("Clear Effect Tree"):
            EFFECT_TREE.update({
                "root": EFFECT_TREE_NODE(EFFECT_TREE_ROOT_ID),
                "nodes": {}
            })
            SaveEffectTreeCache()
    elif USERINPUT_NodeOp == "Add":
        UI_AddEffectTreeNode()
        SaveEffectTreeCache()
    elif USERINPUT_NodeOp == "Edit":
        UI_EditEffectTreeNode()
        SaveEffectTreeCache()
    st.button("Refresh")

    return EFFECT_TREE

def UI_ConstructDisplayGrid():
    '''
    UI - Construct Display Grid
    '''
    global DISPLAY_GRID
    # Init
    st.markdown("## Construct Display Grid")
    # Construct Grid
    cols = st.columns(2)
    USERINPUT_Grid = json.loads(cols[0].text_area(
        "Grid", 
        value=json.dumps(DISPLAY_GRID["grid"], indent=4), 
        height=200
    ))
    USERINPUT_GridParams = json.loads(cols[1].text_area(
        "Grid Params", 
        value=json.dumps(DISPLAY_GRID["params"], indent=4), 
        height=200
    ))
    # Update Grid
    DISPLAY_GRID.update({
        "grid": USERINPUT_Grid,
        "params": USERINPUT_GridParams
    })

    return DISPLAY_GRID

## UI - Effect Transistion Functions
def UI_LoadTransistionEffectParams(DefaultTransistionParams):
    '''
    UI - Load Transistion Effect Params
    '''
    global EFFECT_TREE
    # Load Inputs
    USERINPUT_TransistionEffectParams = {}
    for pk in DefaultTransistionParams.keys():
        st.markdown("---")
        ## Load Params
        cols = st.columns(2)
        USERINPUT_EffectParamStart = json.loads(cols[0].text_area(
            f"{pk} - start", 
            json.dumps({pk: DefaultTransistionParams[pk]["start"]}, indent=4),
            height=200
        ))[pk]
        USERINPUT_EffectParamEnd = json.loads(cols[1].text_area(
            f"{pk} - end", 
            json.dumps({pk: DefaultTransistionParams[pk]["end"]}, indent=4),
            height=200
        ))[pk]
        ## Load Transistion
        AvailableTransistionFuncs = EffectTransistionSelect_Basic(USERINPUT_EffectParamStart, USERINPUT_EffectParamEnd)
        cols = st.columns((1, 2))
        USERINPUT_TransistionType = cols[0].selectbox(
            "Transistion Type", 
            AvailableTransistionFuncs
        )
        USERINPUT_TransistionParams = json.loads(cols[1].text_area(
            f"Transistion Params", 
            json.dumps(TRANSISTION_FUNCS[USERINPUT_TransistionType]["params"], indent=4),
            height=200
        ))
        TransistionFunc = dict(TRANSISTION_FUNCS[USERINPUT_TransistionType])
        TransistionFunc["params"] = USERINPUT_TransistionParams
        USERINPUT_TransistionEffectParams[pk] = {
            "start": USERINPUT_EffectParamStart,
            "end": USERINPUT_EffectParamEnd,
            "transistion": TransistionFunc
        }
    st.markdown("---")

    return USERINPUT_TransistionEffectParams


def UI_AddEffectTreeNode_Transistion():
    '''
    UI - Add Effect Tree Node - Transistion
    '''
    global EFFECT_TREE
    # Init
    PARENT_NODE_IDS = [EFFECT_TREE_ROOT_ID] + list(EFFECT_TREE["nodes"].keys())
    EFFECT_NAMES = list(AVAILABLE_EFFECTS.keys())
    # Load Inputs
    USERINPUT_ParentID = st.selectbox("Parent Node", PARENT_NODE_IDS)
    USERINPUT_EffectName = st.selectbox("New Effect", EFFECT_NAMES)
    DefaultTransistionParams = {
        pk: {
            "start": AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"][pk],
            "end": AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"][pk]
        }
        for pk in AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"].keys()
    }
    USERINPUT_EffectParams = UI_LoadTransistionEffectParams(DefaultTransistionParams)
    # Add Node
    if st.button("Add"):
        ParentNode = EFFECT_TREE["root"] if USERINPUT_ParentID == EFFECT_TREE_ROOT_ID else EFFECT_TREE["nodes"][USERINPUT_ParentID]
        ## Set Connection Data
        NEW_CONNECTION_DATA = {
            "start": ParentNode,
            "end": None,
            "effect": dict(AVAILABLE_EFFECTS[USERINPUT_EffectName])
        }
        NEW_CONNECTION_DATA["effect"]["transistion"] = USERINPUT_EffectParams
        NEW_CONNECTION = EFFECT_TREE_CONNECTION(**NEW_CONNECTION_DATA)
        ## Set Node Data
        NEW_NODE_DATA = {
            "id": str(EFFECT_TREE["node_id_counter"]),
            "parent": NEW_CONNECTION,
        }
        EFFECT_TREE["nodes"][NEW_NODE_DATA["id"]] = EFFECT_TREE_NODE(**NEW_NODE_DATA)
        NEW_CONNECTION.end = EFFECT_TREE["nodes"][NEW_NODE_DATA["id"]]
        EFFECT_TREE["node_id_counter"] += 1
        ## Set Parent Data
        NEW_NODE_DATA["parent"].start.children[NEW_NODE_DATA["id"]] = NEW_CONNECTION

def UI_EditEffectTreeNode_Transistion():
    '''
    UI - Edit Effect Tree Node - Transistion
    '''
    global EFFECT_TREE
    # Init
    NODE_IDS = list(EFFECT_TREE["nodes"].keys())
    PARENT_NODE_IDS = [EFFECT_TREE_ROOT_ID] + list(EFFECT_TREE["nodes"].keys())
    EFFECT_NAMES = list(AVAILABLE_EFFECTS.keys())
    # Load Inputs
    ## Select Node
    USERINPUT_NodeID = st.selectbox("Select Node", NODE_IDS)
    CurNode = EFFECT_TREE["nodes"][USERINPUT_NodeID]
    CurConnection = CurNode.parent
    ## Edit
    USERINPUT_ParentID = st.selectbox(
        "Edit Parent Node", PARENT_NODE_IDS, 
        index=PARENT_NODE_IDS.index(CurConnection.start.id)
    )
    USERINPUT_EffectName = st.selectbox(
        "Edit Effect", EFFECT_NAMES,
        index=EFFECT_NAMES.index(CurConnection.effect["name"])
    )
    DefaultTransistionParams = CurConnection.effect["transistion"]
    if USERINPUT_EffectName != CurConnection.effect["name"]:
        DefaultTransistionParams = {
            pk: {
                "start": AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"][pk],
                "end": AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"][pk]
            }
            for pk in AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"].keys()
        }
    USERINPUT_EffectParams = UI_LoadTransistionEffectParams(DefaultTransistionParams)
    # Edit Node
    cols = st.columns(2)
    if cols[0].button("Edit"):
        ParentNode = EFFECT_TREE["root"] if USERINPUT_ParentID == EFFECT_TREE_ROOT_ID else EFFECT_TREE["nodes"][USERINPUT_ParentID]
        ## Set Connection Data
        CurConnection.start = ParentNode
        CurConnection.effect = dict(AVAILABLE_EFFECTS[USERINPUT_EffectName])
        CurConnection.effect["transistion"] = USERINPUT_EffectParams
        ## Set Node Data
        CurNode.parent = CurConnection
        ## Set Parent Data
        CurConnection.start.children[CurNode.id] = CurConnection
    if cols[1].button("Delete"):
        ## Delete Node
        deleted_node_ids = EFFECT_TREE["nodes"][CurNode.id].delete(propogate=True)
        for deleted_node_id in deleted_node_ids:
            del EFFECT_TREE["nodes"][deleted_node_id]

def UI_ConstructEffectTree_Transistion():
    '''
    UI - Construct Effect Tree - Transistion
    '''
    global EFFECT_TREE
    # Init
    st.markdown("## Construct Effect Tree (Transistion)")
    ## Load Tree Cache
    EFFECT_TREE = LoadTransistionEffectTreeCache()
    ## Display
    UI_DisplayEffectTree(EFFECT_TREE["root"], EFFECT_TREE["nodes"])
    # Node Operations
    USERINPUT_NodeOp = st.selectbox("Node Operations", ["-", "Add", "Edit", "Clear"])
    if USERINPUT_NodeOp == "Clear":
        if st.button("Clear Effect Tree"):
            EFFECT_TREE.update({
                "root": EFFECT_TREE_NODE(EFFECT_TREE_ROOT_ID),
                "nodes": {},
                "node_id_counter": 1
            })
            SaveTransistionEffectTreeCache()
    elif USERINPUT_NodeOp == "Add":
        UI_AddEffectTreeNode_Transistion()
        SaveTransistionEffectTreeCache()
    elif USERINPUT_NodeOp == "Edit":
        UI_EditEffectTreeNode_Transistion()
        SaveTransistionEffectTreeCache()
    st.button("Refresh")

    return EFFECT_TREE

# Repo Based Functions
def videofx():
    global EFFECT_TREE
    global DISPLAY_GRID
    # Title
    st.header("Video FX")

    # Load Prereq Inputs
    USERINPUT_Video = UI_VideoInputSource()
    Frames_Load()
    # UI_ShowAvailableEffects()
    # Load Inputs
    ## Effect Tree
    EFFECT_TREE = UI_ConstructEffectTree()
    ## Display Grid
    DISPLAY_GRID = UI_ConstructDisplayGrid()
    USERINPUT_DisplayParams = {
        "max_frames": -1,
        "compact_display": st.sidebar.checkbox("Compact Display", False)
    }

    # Process Inputs
    cols = st.columns(2)
    USERINPUT_StreamProcess = cols[0].checkbox("Stream Process", False)
    if not USERINPUT_StreamProcess: USERINPUT_StreamProcess = cols[1].button("Process")
    if USERINPUT_StreamProcess:
        EffectFunc = functools.partial(EffectFunc_TreeApply, EFFECT_TREE=EFFECT_TREE, DISPLAY_GRID=DISPLAY_GRID)
        # Display Output
        st.markdown("## Video")
        UI_DisplayEffectVideo(USERINPUT_Video, EffectFunc, **USERINPUT_DisplayParams)

def imagefx():
    global EFFECT_TREE
    global DISPLAY_GRID
    # Title
    st.header("Image FX")

    # Load Prereq Inputs
    USERINPUT_Image = UI_LoadImage()
    Frames_Load()
    # UI_ShowAvailableEffects()
    # Load Inputs
    ## Effect Graph
    EFFECT_TREE = UI_ConstructEffectTree()
    ## Display Grid
    DISPLAY_GRID = UI_ConstructDisplayGrid()
    USERINPUT_DisplayParams = {
        "compact_display": st.sidebar.checkbox("Compact Display", False)
    }

    # Process Inputs
    cols = st.columns(2)
    USERINPUT_StreamProcess = cols[0].checkbox("Stream Process", False)
    if not USERINPUT_StreamProcess: USERINPUT_StreamProcess = cols[1].button("Process")
    if USERINPUT_StreamProcess:
        EffectImage = EffectFunc_TreeApply(
            USERINPUT_Image, 
            EFFECT_TREE=EFFECT_TREE, DISPLAY_GRID=DISPLAY_GRID
        )
        # Display Output
        st.markdown("## Images")
        UI_DisplayEffectImage(USERINPUT_Image, EffectImage, **USERINPUT_DisplayParams)

def image_effect_transistion():
    global EFFECT_TREE
    global DISPLAY_GRID
    # Title
    st.header("Image Effect Transistion")

    # Load Prereq Inputs
    USERINPUT_Image = UI_LoadImage()
    Frames_Load()
    # UI_ShowAvailableEffects()
    # Load Inputs
    ## Effect Graph Transistion
    EFFECT_TREE = UI_ConstructEffectTree_Transistion()
    ## Other Inputs
    cols = st.columns(2)
    USERINPUT_FinalNodeID = cols[0].selectbox("Select Final Effect Node", EFFECT_TREE["nodes"].keys())
    USERINPUT_NFrames = cols[1].number_input("Select N Frames", min_value=1, max_value=100, value=10)
    USERINPUT_FPS = st.sidebar.number_input("FPS", min_value=1, max_value=120, value=10)

    # Process Inputs
    cols = st.columns(2)
    USERINPUT_StreamProcess = cols[0].checkbox("Stream Process", False)
    if not USERINPUT_StreamProcess: USERINPUT_StreamProcess = cols[1].button("Process")
    if USERINPUT_StreamProcess:
        DISPLAY_GRID.update({
            "grid": [[USERINPUT_FinalNodeID]],
            "params": {
                "grid_cell_space": [0, 0],
                "grid_border_space": [0, 0]
            },
        })
        TREE_APPLY_FUNC = functools.partial(
            EffectFunc_TreeApply, 
            DISPLAY_GRID=DISPLAY_GRID
        )
        PROGRESS_BAR = st.progress(0)
        TransistionEffectImages = EffectTransistion_Apply(
            USERINPUT_Image, 
            EFFECT_TREE=EFFECT_TREE, TREE_APPLY_FUNC=TREE_APPLY_FUNC,
            n_frames=USERINPUT_NFrames,
            PROGRESS_BAR=PROGRESS_BAR.progress
        )
        # Display Output
        st.markdown("## Video")
        VideoUtils_SaveFrames2Video(TransistionEffectImages, PATHS["default"]["save"]["video"], fps=USERINPUT_FPS)
        st.video(PATHS["default"]["save"]["video"])

def effects():
    # Title
    st.header("Effects")

    # Load Prereq Inputs
    USERINPUT_Video = UI_VideoInputSource()
    Frames_Load()
    # USERINPUT_ChosenEffectData = UI_ShowAvailableEffects()
    # Load Inputs
    st.markdown("## Select Effect")
    EFFECT_NAMES = list(AVAILABLE_EFFECTS.keys())
    cols = st.columns(2)
    USERINPUT_EffectName = cols[0].selectbox("Effect", EFFECT_NAMES)
    USERINPUT_EffectParams = json.loads(cols[1].text_area(
        "New Effect Params", 
        json.dumps(AVAILABLE_EFFECTS[USERINPUT_EffectName]["params"], indent=4),
        height=200
    ))

    # Process Inputs
    cols = st.columns(2)
    USERINPUT_StreamProcess = cols[0].checkbox("Stream Process", False)
    if not USERINPUT_StreamProcess: USERINPUT_StreamProcess = cols[1].button("Process")
    if USERINPUT_StreamProcess:
        EffectFunc = functools.partial(
            EffectFunc_SingleEffect, 
            EffectFunc=functools.partial(AVAILABLE_EFFECTS[USERINPUT_EffectName]["func"], **USERINPUT_EffectParams)
        )
        # Display Output
        st.markdown("## Video")
        UI_DisplayEffectVideo(USERINPUT_Video, EffectFunc, max_frames=-1, compact_display=True)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()