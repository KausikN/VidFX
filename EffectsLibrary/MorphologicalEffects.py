'''
Morphological Image Effects Library
'''

# Imports
import cv2
import numpy as np
from skimage.morphology import skeletonize, thin

# Main Functions
def ImageEffect_Skeleton(I, method=None, bin_threshold=127):
    I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY) >= bin_threshold
    I_filtered = skeletonize(I, method=method)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_Thin(I, max_iters=None, bin_threshold=127):
    I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY) >= bin_threshold
    I_filtered = thin(I, max_iter=max_iters)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

# Driver Code