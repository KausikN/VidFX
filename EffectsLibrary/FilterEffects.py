'''
Filter Image Effects Library
'''

# Imports
from .EffectUtils import *

import skimage
import skimage.feature

# Utils Functions
def FilterPostProcess(I, I_filtered, **params):
    I_effect = np.clip(I_filtered, 0.0, 1.0)
    if I_effect.ndim == 2: I_effect = np.dstack((I_effect, I_effect, I_effect))
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Functions
def ImageEffect_GaussianFilter(I, sigma=1.0, **params):
    I_filtered = skimage.filters.gaussian(image=np.array(I[:, :, :3]), sigma=sigma)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_SobelFilter(I, **params):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    I_filtered = skimage.filters.sobel(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_SobelVerticalFilter(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.sobel_v(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_SobelHorizontalFilter(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.sobel_h(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_RobertsFilter(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.roberts(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ScharrFilter(I, **params):
    I_filtered = skimage.filters.scharr(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ScharrVerticalFilter(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.scharr_v(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ScharrHorizontalFilter(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.scharr_h(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_PrewittFilter(I, **params):
    I_filtered = skimage.filters.prewitt(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_MedianFilter(I, **params):
    I_filtered = skimage.filters.median(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_LaplaceFilter(I, ksize=3, **params):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    I_filtered = skimage.filters.laplace(image=np.array(I[:, :, :3]), ksize=ksize)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_FaridEdges(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.farid(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_FaridVerticalEdges(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.farid_v(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_FaridHorizontalEdges(I, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.farid_h(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_CannyEdges(I, sigma=0.0, low_threshold=0.1, high_threshold=0.9, **params):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    edges = skimage.feature.canny(image=np.array(I_rgb), sigma=sigma, low_threshold=low_threshold, high_threshold=high_threshold)
    edges = np.clip(edges, 0.0, 1.0, dtype=float)
    return edges

# Main Vars
EFFECTFUNCS_FILTER = {
    "GaussianFilter": {
        "name": "GaussianFilter",
        "code": "GaussianFilter(sigma=2)",
        "func": ImageEffect_GaussianFilter,
        "params": {
            "sigma": 1.0
        }
    },
    "SobelFilter": {
        "name": "SobelFilter",
        "code": "SobelFilter",
        "func": ImageEffect_SobelFilter,
        "params": {}
    },
    "SobelVerticalFilter": {
        "name": "SobelVerticalFilter",
        "code": "SobelVerticalFilter",
        "func": ImageEffect_SobelVerticalFilter,
        "params": {}
    },
    "SobelHorizontalFilter": {
        "name": "SobelHorizontalFilter",
        "code": "SobelHorizontalFilter",
        "func": ImageEffect_SobelHorizontalFilter,
        "params": {}
    },
    "RobertsFilter": {
        "name": "RobertsFilter",
        "code": "RobertsFilter",
        "func": ImageEffect_RobertsFilter,
        "params": {}
    },
    "ScharrFilter": {
        "name": "ScharrFilter",
        "code": "ScharrFilter",
        "func": ImageEffect_ScharrFilter,
        "params": {}
    },
    "ScharrVerticalFilter": {
        "name": "ScharrVerticalFilter",
        "code": "ScharrVerticalFilter",
        "func": ImageEffect_ScharrVerticalFilter,
        "params": {}
    },
    "ScharrHorizontalFilter": {
        "name": "ScharrHorizontalFilter",
        "code": "ScharrHorizontalFilter",
        "func": ImageEffect_ScharrHorizontalFilter,
        "params": {}
    },
    "PrewittFilter": {
        "name": "PrewittFilter",
        "code": "PrewittFilter",
        "func": ImageEffect_PrewittFilter,
        "params": {}
    },
    "MedianFilter": {
        "name": "MedianFilter",
        "code": "MedianFilter",
        "func": ImageEffect_MedianFilter,
        "params": {}
    },
    "LaplaceFilter": {
        "name": "LaplaceFilter",
        "code": "LaplaceFilter(ksize=3)",
        "func": ImageEffect_LaplaceFilter,
        "params": {
            "ksize": 3
        }
    },
    "FaridEdges": {
        "name": "FaridEdges",
        "code": "FaridEdges",
        "func": ImageEffect_FaridEdges,
        "params": {}
    },
    "FaridVerticalEdges": {
        "name": "FaridVerticalEdges",
        "code": "FaridVerticalEdges",
        "func": ImageEffect_FaridVerticalEdges,
        "params": {}
    },
    "FaridHorizontalEdges": {
        "name": "FaridHorizontalEdges",
        "code": "FaridHorizontalEdges",
        "func": ImageEffect_FaridHorizontalEdges,
        "params": {}
    },
    "CannyEdges": {
        "name": "CannyEdges",
        "code": "CannyEdges(sigma=0.0, low_threshold=0.1, high_threshold=0.9)",
        "func": ImageEffect_CannyEdges,
        "params": {
            "sigma": 0.0,
            "low_threshold": 0.1,
            "high_threshold": 0.9
        }
    }
}