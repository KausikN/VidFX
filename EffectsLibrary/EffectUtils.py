'''
Effect Utils
'''

# Imports
import os
import cv2
import math
import functools
import numpy as np

from Utils.VideoUtils import *
from .EffectVars import *

# Utils Functions
def LoadModule(moduleName="CombinationEffects"):
    modulePath = os.path.dirname(os.path.relpath(__file__)) + "/" + moduleName + ".py"
    exec(open(modulePath).read(), globals())

# Main Functions
def ApplyAlphaToImage(I):
    I_ra = I[:, :, 0] * (I[:, :, 3])
    I_ga = I[:, :, 1] * (I[:, :, 3])
    I_ba = I[:, :, 2] * (I[:, :, 3])
    I_aa = np.dstack((I_ra, I_ga, I_ba, np.ones(I.shape[:2], dtype=float)))
    return np.array(I_aa, dtype=float)

def NormaliseSize(keys, keepOriginalSizes=False, EFFECT_TREE=None):
    # Init
    size = [100, 100, PIXELDATA_DIMENSIONS]
    # Check
    if len(keys) == 0: return size
    # Normalise Sizes
    if keepOriginalSizes:
        for key in keys:
            I_cur = None
            if key == EFFECT_TREE_ROOT_ID:
                I_cur = EFFECT_TREE["root"].I
            elif key in EFFECT_TREE["nodes"].keys():
                I_cur = EFFECT_TREE["nodes"][key].I
            if I_cur is not None:
                size = [max(size[0], I_cur.shape[0]), max(size[1], I_cur.shape[1])] + [PIXELDATA_DIMENSIONS]
    else:
        I_cur = None
        if keys[0] == EFFECT_TREE_ROOT_ID:
            I_cur = EFFECT_TREE["root"].I
        elif keys[0] in EFFECT_TREE["nodes"].keys():
            I_cur = EFFECT_TREE["nodes"][keys[0]].I
        if I_cur is not None:
            size = list(I_cur.shape)[:2] + [PIXELDATA_DIMENSIONS]

    return size

def NormaliseValues(I, normaliseFit=False):
    if normaliseFit:
        I_min = np.min(I[:, :, :2])
        I_max = np.max(I[:, :, :2])
        I[:, :, :2] = ((I[:, :, :2] - I_min) / (I_max - I_min))
    else:
        I = np.clip(I, a_min=0.0, a_max=1.0)
    I = np.array(I, dtype=float)
    return I

# Effect Apply Functions
def EffectTree_GenerateNodeImages_BFS(EFFECT_TREE):
    '''
    Effect Tree - Generate Images for all nodes in BFS order
    '''
    # Init
    QUEUE = [EFFECT_TREE["root"].children[ck].end for ck in EFFECT_TREE["root"].children.keys()]
    # BFS
    while len(QUEUE) > 0:
        # Get Node
        node = QUEUE.pop(0)
        # Generate Image
        node.generate()
        # Add Children to Queue
        for ck in node.children.keys():
            QUEUE.append(node.children[ck].end)

def EffectFunc_TreeApply(frame, EFFECT_TREE=None, DISPLAY_GRID=None):
    '''
    Effect Tree - Apply
    '''
    # Check
    if EFFECT_TREE is None or DISPLAY_GRID is None: return frame
    # Check input image
    if frame.shape[2] < PIXELDATA_DIMENSIONS:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame = np.array(frame, dtype=np.float32) / 255.0
    # Run Effect Tree
    ## Set frame to root
    EFFECT_TREE["root"].I = frame
    EFFECT_TREE["root"].updateHistory()
    ## Generate Images for all nodes
    EffectTree_GenerateNodeImages_BFS(EFFECT_TREE)

    # Get Output Image
    ## Form Image Grid
    OVERALL_IMAGE_SIZE = [0, 0]
    ROW_WISE_DATA = []
    GRID_Is = []
    for i in range(len(DISPLAY_GRID["grid"])):
        GRID_Is.append([])
        for j in range(len(DISPLAY_GRID["grid"][i])):
            key = DISPLAY_GRID["grid"][i][j]
            I_cur = frame
            if key == EFFECT_TREE_ROOT_ID:
                I_cur = EFFECT_TREE["root"].I
            elif key in EFFECT_TREE["nodes"].keys():
                I_cur = EFFECT_TREE["nodes"][key].I
            GRID_Is[-1].append(I_cur)
        row_width = sum([I_cur.shape[1] for I_cur in GRID_Is[-1]])
        row_height = max([I_cur.shape[0] for I_cur in GRID_Is[-1]])
        OVERALL_IMAGE_SIZE[1] = max(OVERALL_IMAGE_SIZE[1], row_width)
        OVERALL_IMAGE_SIZE[0] += row_height
        ROW_WISE_DATA.append({
            "row_width": row_width,
            "row_height": row_height,
        })
    DISPLAY_GRID["overall"]["grid_size"] = [len(DISPLAY_GRID["grid"]), max([len(g) for g in DISPLAY_GRID["grid"]])]
    DISPLAY_GRID["overall"]["image_size"] = OVERALL_IMAGE_SIZE
    ## Create Output Image
    OUTPUT_IMAGE = np.zeros((OVERALL_IMAGE_SIZE[0], OVERALL_IMAGE_SIZE[1], PIXELDATA_DIMENSIONS), dtype=float)
    ## Fill Output Image
    CUR_POS = [0, 0]
    for i in range(len(GRID_Is)):
        ROW_DATA = ROW_WISE_DATA[i]
        CUR_POS[1] = int((OVERALL_IMAGE_SIZE[1] - ROW_DATA["row_width"]) / 2)
        for j in range(len(GRID_Is[i])):
            CUR_CUR_POS = [CUR_POS[0], CUR_POS[1]]
            CUR_CUR_POS[0] += int((ROW_DATA["row_height"] - GRID_Is[i][j].shape[0]) / 2)
            I_cur = GRID_Is[i][j]
            OUTPUT_IMAGE[
                CUR_CUR_POS[0]:CUR_CUR_POS[0]+I_cur.shape[0], 
                CUR_CUR_POS[1]:CUR_CUR_POS[1]+I_cur.shape[1]
            ] = I_cur
            CUR_POS[1] += I_cur.shape[1]
        CUR_POS[0] += ROW_DATA["row_height"]

    return OUTPUT_IMAGE

def EffectFunc_SingleEffect(frame, EffectFunc=None):
    '''
    Single Effect - Apply
    '''
    # Check
    if EffectFunc is None: return frame
    # Check input image
    if frame.shape[2] < PIXELDATA_DIMENSIONS:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame = np.array(frame, dtype=np.float32) / 255.0
    # Run Effect
    OUTPUT_IMAGE = EffectFunc(frame)
    
    return OUTPUT_IMAGE