'''
Morphological Image Effects Library
'''

# Imports
import cv2
import numpy as np
from skimage import morphology, segmentation

# Utils Functions
def FilterPostProcess(I, I_filtered):
    I_effect = np.clip(I_filtered, 0.0, 1.0)
    if I_effect.ndim == 2:
        I_effect = np.dstack((I_effect, I_effect, I_effect))
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Functions
def ImageEffect_Skeleton(I, method=None, bin_threshold=127):
    I_bin = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY) >= bin_threshold
    I_filtered = morphology.skeletonize(I_bin, method=method)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_Thin(I, max_iters=None, bin_threshold=127):
    I_bin = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY) >= bin_threshold
    I_filtered = morphology.thin(I_bin, max_iter=max_iters)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_Dilate(I):
    I_filtered = morphology.dilation(I[:, :, :3])
    return FilterPostProcess(I, I_filtered)

def ImageEffect_RemoveSmallObjects(I, min_size=64):
    I_filtered = morphology.remove_small_objects(I[:, :, :3], min_size=min_size)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_Erode(I):
    I_filtered = morphology.erosion(I[:, :, :3])
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ConvexHull(I, obj=False):
    if obj:
        I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
        I_filtered = morphology.convex_hull_object(I_rgb)
    else:
        I_filtered = morphology.convex_hull_image(I[:, :, :3])
    return FilterPostProcess(I, I_filtered)

# Main Vars
EFFECTFUNCS_MORPHOLOGICAL = [
    {
        "name": "Skeleton",
        "code": "Skeleton(method=None, bin_threshold=0.5)",
        "func": ImageEffect_Skeleton,
        "params": [
            {
                "name": "method",
                "default": None,
                "type": "str"
            },
            {
                "name": "bin_threshold",
                "default": 0.5,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.1
            }
        ]
    },
    {
        "name": "Thin",
        "code": "Thin(max_iters=None, bin_threshold=0.5)",
        "func": ImageEffect_Thin,
        "params": [
            {
                "name": "max_iters",
                "default": 1,
                "type": "int",
                "min": 1,
                "max": 5,
                "step": 1
            },
            {
                "name": "bin_threshold",
                "default": 0.5,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.1
            }
        ]
    },
    {
        "name": "Dilate",
        "code": "Dilate",
        "func": ImageEffect_Dilate,
        "params": []
    },
    {
        "name": "RemoveSmallObjects",
        "code": "RemoveSmallObjects(min_size=64)",
        "func": ImageEffect_RemoveSmallObjects,
        "params": [
            {
                "name": "min_size",
                "default": 64,
                "type": "int",
                "min": 0,
                "max": 1024,
                "step": 32
            }
        ]
    },
    {
        "name": "Erode",
        "code": "Erode",
        "func": ImageEffect_Erode,
        "params": []
    },
    {
        "name": "ConvexHull",
        "code": "ConvexHull(obj=False)",
        "func": ImageEffect_ConvexHull,
        "params": [
            {
                "name": "obj",
                "default": False,
                "type": "bool"
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_MORPHOLOGICAL)

# Driver Code