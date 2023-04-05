"""
VidFX - Lite
"""

# Imports
import os
import cv2
import json
import functools
import argparse
import numpy as np

from VidFX import *

# Main Functions
def VidFX_Lite_ArgumentParse():
    '''
    VidFX - Lite - Parse Command Line Arguments
    '''
    # Create Argument Parser
    parser = argparse.ArgumentParser(description="VidFX - Lite")
    ## Add Arguments
    parser.add_argument(
        "-i", "--input", 
        help="Input Video Source (Leave empty for webcam)", 
        type=str, default=""
    )
    parser.add_argument(
        "-e", "--effect_json", 
        help="Effect Tree JSON File", 
        type=str, default="StreamLitGUI/CacheData/EffectTreeCache.json"
    )
    parser.add_argument(
        "-d", "--display_json", 
        help="Display Grid JSON File", 
        type=str, default="StreamLitGUI/CacheData/DisplayGridCache.json"
    )
    # Parse Arguments
    args = parser.parse_args()
    # Form Arguments
    ARGUMENTS = {
        "source": args.input if os.path.exists(args.input) else "",
        "effect_tree": EffectTreeCache_Dict2Tree(json.load(open(args.effect_json, "r")))["EFFECT_TREE"],
        "display_grid": dict(json.load(open(args.display_json, "r")))
    }
    print(ARGUMENTS)

    return ARGUMENTS

def UI_DisplayEffectVideo(vid, EffectFunc, max_frames=-1):
    '''
    UI - Display Effect Video
    '''
    # Check if camera opened successfully
    if not vid.isOpened():
        print("Error opening video stream or file")
        return
    # Read until video is completed
    FRAME_COUNT = 0
    while(vid.isOpened() and ((not (FRAME_COUNT == max_frames)) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Apply Effect if needed
            if EffectFunc is not None: frame = EffectFunc(frame)
            # Display the resulting frame
            cv2.imshow("Effect", frame)
            FRAME_COUNT += 1
            # Press Q on keyboard to exit
            if (cv2.waitKey(1) & 0xFF == ord("q")): break
        # Break the loop
        else: 
            break
    # When everything done, release the video capture object
    vid.release()
    # Closes all the frames
    cv2.destroyAllWindows()

# RunCode
if __name__ == "__main__":
    # Parse Arguments
    ARGUMENTS = VidFX_Lite_ArgumentParse()
    # Set Arguments
    EFFECT_TREE = ARGUMENTS["effect_tree"]
    DISPLAY_GRID = ARGUMENTS["display_grid"]
    # Load Video
    if ARGUMENTS["source"] == "":
        VIDEO = INPUTREADERS_VIDEO["Webcam"]()
    else:
        VIDEO = INPUTREADERS_VIDEO["Upload Video File"](ARGUMENTS["source"])
    # Set Effect Function
    EffectFunc = functools.partial(EffectFunc_TreeApply, EFFECT_TREE=EFFECT_TREE, DISPLAY_GRID=DISPLAY_GRID)
    # Run
    UI_DisplayEffectVideo(VIDEO, EffectFunc, max_frames=-1)