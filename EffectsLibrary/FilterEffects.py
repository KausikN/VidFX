'''
Filter Image Effects Library
'''

# Imports
import cv2
import numpy as np
import skimage
import skimage.feature

# Utils Functions
def FilterPostProcess(I, I_filtered):
    I_effect = np.clip(I_filtered, 0.0, 1.0)
    if I_effect.ndim == 2:
        I_effect = np.dstack((I_effect, I_effect, I_effect))
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Functions
def ImageEffect_GaussianFilter(I, sigma=1):
    I_filtered = skimage.filters.gaussian(image=np.array(I[:, :, :3]), sigma=sigma)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_SobelFilter(I):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    I_filtered = skimage.filters.sobel(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_SobelVerticalFilter(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.sobel_v(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_SobelHorizontalFilter(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.sobel_h(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_RobertsFilter(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.roberts(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ScharrFilter(I):
    I_filtered = skimage.filters.scharr(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ScharrVerticalFilter(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.scharr_v(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_ScharrHorizontalFilter(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.scharr_h(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_PrewittFilter(I):
    I_filtered = skimage.filters.prewitt(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_MedianFilter(I):
    I_filtered = skimage.filters.median(image=np.array(I[:, :, :3]))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_LaplaceFilter(I, ksize=3):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    I_filtered = skimage.filters.laplace(image=np.array(I[:, :, :3]), ksize=ksize)
    return FilterPostProcess(I, I_filtered)

def ImageEffect_FaridEdges(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.farid(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_FaridVerticalEdges(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.farid_v(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_FaridHorizontalEdges(I):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    I_filtered = skimage.filters.farid_h(image=np.array(I_rgb))
    return FilterPostProcess(I, I_filtered)

def ImageEffect_CannyEdges(I, sigma=0.0, low_threshold=0.1, high_threshold=0.9):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    edges = skimage.feature.canny(image=np.array(I_rgb), sigma=sigma, low_threshold=low_threshold, high_threshold=high_threshold)
    edges = np.clip(edges, 0.0, 1.0, dtype=float)
    return edges

# Main Vars
EFFECTFUNCS_FILTER = [
    {
        "name": "GaussianFilter",
        "code": "GaussianFilter(sigma=2)",
        "func": ImageEffect_GaussianFilter,
        "params": [
            {
                "name": "sigma",
                "default": 2,
                "type": "int",
                "min": 0,
                "max": 5,
                "step": 1
            }
        ]
    },
    {
        "name": "SobelFilter",
        "code": "SobelFilter",
        "func": ImageEffect_SobelFilter,
        "params": []
    },
    {
        "name": "SobelVerticalFilter",
        "code": "SobelVerticalFilter",
        "func": ImageEffect_SobelVerticalFilter,
        "params": []
    },
    {
        "name": "SobelHorizontalFilter",
        "code": "SobelHorizontalFilter",
        "func": ImageEffect_SobelHorizontalFilter,
        "params": []
    },
    {
        "name": "RobertsFilter",
        "code": "RobertsFilter",
        "func": ImageEffect_RobertsFilter,
        "params": []
    },
    {
        "name": "ScharrFilter",
        "code": "ScharrFilter",
        "func": ImageEffect_ScharrFilter,
        "params": []
    },
    {
        "name": "ScharrVerticalFilter",
        "code": "ScharrVerticalFilter",
        "func": ImageEffect_ScharrVerticalFilter,
        "params": []
    },
    {
        "name": "ScharrHorizontalFilter",
        "code": "ScharrHorizontalFilter",
        "func": ImageEffect_ScharrHorizontalFilter,
        "params": []
    },
    {
        "name": "PrewittFilter",
        "code": "PrewittFilter",
        "func": ImageEffect_PrewittFilter,
        "params": []
    },
    {
        "name": "MedianFilter",
        "code": "MedianFilter",
        "func": ImageEffect_MedianFilter,
        "params": []
    },
    {
        "name": "LaplaceFilter",
        "code": "LaplaceFilter(ksize=3)",
        "func": ImageEffect_LaplaceFilter,
        "params": [
            {
                "name": "ksize",
                "default": 3,
                "type": "int",
                "min": 0,
                "max": 5,
                "step": 1
            }
        ]
    },
    {
        "name": "FaridEdges",
        "code": "FaridEdges",
        "func": ImageEffect_FaridEdges,
        "params": []
    },
    {
        "name": "FaridVerticalEdges",
        "code": "FaridVerticalEdges",
        "func": ImageEffect_FaridVerticalEdges,
        "params": []
    },
    {
        "name": "FaridHorizontalEdges",
        "code": "FaridHorizontalEdges",
        "func": ImageEffect_FaridHorizontalEdges,
        "params": []
    },
    {
        "name": "CannyEdges",
        "code": "CannyEdges(sigma=0.0, low_threshold=0.1, high_threshold=0.9)",
        "func": ImageEffect_CannyEdges,
        "params": [
            {
                "name": "sigma",
                "default": 0.0,
                "type": "float",
                "min": 0.0,
                "max": 3.0,
                "step": 0.1
            },
            {
                "name": "low_threshold",
                "default": 0.1,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.1
            },
            {
                "name": "high_threshold",
                "default": 0.9,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.1
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_FILTER)

# Driver Code