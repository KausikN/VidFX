'''
Morphological Image Effects Library
'''

# Imports
from .EffectUtils import *

from skimage import morphology, segmentation

# Utils Functions
def FilterPostProcess(I, I_filtered, **params):
    I_effect = np.clip(I_filtered, 0.0, 1.0)
    if I_effect.ndim == 2:
        I_effect = np.dstack((I_effect, I_effect, I_effect))
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Functions
def ImageEffect_Skeleton(I, method=None, bin_threshold=0.5, **params):
    I_bin = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY) >= (bin_threshold*255)
    I_filtered = morphology.skeletonize(I_bin, method=method)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_Thin(I, max_iters=None, bin_threshold=0.5, **params):
    I_bin = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY) >= (bin_threshold*255)
    I_filtered = morphology.thin(I_bin, max_iter=max_iters)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_Dilate(I, **params):
    I_filtered = morphology.dilation(I[:, :, :3])
    return FilterPostProcess(I, I_filtered)

def ImageEffect_RemoveSmallObjects(I, min_size=64, **params):
    I_filtered = morphology.remove_small_objects(I[:, :, :3], min_size=min_size)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_Erode(I, **params):
    I_filtered = morphology.erosion(I[:, :, :3])
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ConvexHull(I, obj=False, **params):
    if obj:
        I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
        I_filtered = morphology.convex_hull_object(I_rgb)
    else:
        I_filtered = morphology.convex_hull_image(I[:, :, :3])
    return FilterPostProcess(I, I_filtered)

# Main Vars
EFFECTFUNCS_MORPHOLOGICAL = {
    "Skeleton": {
        "name": "Skeleton",
        "code": "Skeleton(method=None, bin_threshold=0.5)",
        "func": ImageEffect_Skeleton,
        "params": {
            "method": None,
            "bin_threshold": 0.5
        }
    },
    "Thin": {
        "name": "Thin",
        "code": "Thin(max_iters=None, bin_threshold=0.5)",
        "func": ImageEffect_Thin,
        "params": {
            "max_iters": None,
            "bin_threshold": 0.5
        }
    },
    "Dilate": {
        "name": "Dilate",
        "code": "Dilate",
        "func": ImageEffect_Dilate,
        "params": {}
    },
    "RemoveSmallObjects": {
        "name": "RemoveSmallObjects",
        "code": "RemoveSmallObjects(min_size=64)",
        "func": ImageEffect_RemoveSmallObjects,
        "params": {
            "min_size": 64
        }
    },
    "Erode": {
        "name": "Erode",
        "code": "Erode",
        "func": ImageEffect_Erode,
        "params": {}
    },
    "ConvexHull": {
        "name": "ConvexHull",
        "code": "ConvexHull(obj=False)",
        "func": ImageEffect_ConvexHull,
        "params": {
            "obj": False
        }
    }
}