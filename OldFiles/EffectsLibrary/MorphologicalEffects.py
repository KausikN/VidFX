'''
Morphological Image Effects Library
'''

# Imports
import cv2
import numpy as np
from skimage import morphology, segmentation

# Main Functions
def ImageEffect_Skeleton(I, method=None, bin_threshold=127):
    I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY) >= bin_threshold
    I_filtered = morphology.skeletonize(I, method=method)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_Thin(I, max_iters=None, bin_threshold=127):
    I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY) >= bin_threshold
    I_filtered = morphology.thin(I, max_iter=max_iters)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_Dilate(I):
    I_filtered = morphology.dilation(I)
    return I_filtered

def ImageEffect_RemoveSmallObjects(I, min_size=64):
    I_filtered = morphology.remove_small_objects(I, min_size=min_size)
    return I_filtered

def ImageEffect_Erode(I):
    I_filtered = morphology.erosion(I)
    return I_filtered

def ImageEffect_ConvexHull(I, obj=False):
    if obj:
        I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
        I_filtered = morphology.convex_hull_object(I)
    else:
        I_filtered = morphology.convex_hull_image(I)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

# Driver Code