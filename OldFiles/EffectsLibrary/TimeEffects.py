'''
Time based Image Effects Library
'''

# Imports
import os
import cv2
import numpy as np

# Main Vars
savedFrames = {}
delayInitCounts = {}

# Main Functions
# Effect Functions
def ImageEffect_FrameDelay(I, delay=12, funcKey='FrameDelay_0'):
    global delayInitCounts
    global savedFrames

    if delay < 1:
        return I

    output = None
    if not funcKey in delayInitCounts.keys():
        delayInitCounts[funcKey] = [1, delay]
        savedFrames[funcKey] = [np.copy(I)]
        output = np.zeros(I.shape, dtype=np.uint8)
    elif delayInitCounts[funcKey][0] < delay:
        delayInitCounts[funcKey][0] += 1
        savedFrames[funcKey].append(np.copy(I))
        output = np.zeros(I.shape, dtype=np.uint8)
    elif delayInitCounts[funcKey][0] == delay:
        delayInitCounts[funcKey][0] += 1
        output = savedFrames[funcKey][0]
        savedFrames[funcKey].pop(0)
        savedFrames[funcKey].append(np.copy(I))
    else:
        output = savedFrames[funcKey][0]
        savedFrames[funcKey].pop(0)
        savedFrames[funcKey].append(np.copy(I))

    return output

# Driver Code