'''
Filter Image Effects Library
'''

# Imports
import cv2
import numpy as np
import skimage
import skimage.feature

# Main Functions
def ImageEffect_GaussianFilter(I, sigma=1):
    I_filtered = skimage.filters.gaussian(image=np.array(I/255), sigma=sigma)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_SobelFilter(I):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    I_filtered = skimage.filters.sobel(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_SobelVerticalFilter(I):
    I_filtered = skimage.filters.sobel_v(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_SobelHorizontalFilter(I):
    I_filtered = skimage.filters.sobel_h(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_RobertsFilter(I):
    I_filtered = skimage.filters.roberts(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_ScharrFilter(I):
    I_filtered = skimage.filters.scharr(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_ScharrVerticalFilter(I):
    I_filtered = skimage.filters.scharr_v(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_ScharrHorizontalFilter(I):
    I_filtered = skimage.filters.scharr_h(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_PrewittFilter(I):
    I_filtered = skimage.filters.prewitt(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_MedianFilter(I):
    I_filtered = skimage.filters.median(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_LaplaceFilter(I, ksize=3):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    I_filtered = skimage.filters.laplace(image=np.array(I/255), ksize=ksize)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_FaridEdges(I):
    I_filtered = skimage.filters.farid(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_FaridVerticalEdges(I):
    I_filtered = skimage.filters.farid_v(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_FaridHorizontalEdges(I):
    I_filtered = skimage.filters.farid_h(image=np.array(I/255))
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

def ImageEffect_CannyEdges(I, sigma=0.0, low_threshold=0.1, high_threshold=0.9):
    I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    edges = skimage.feature.canny(image=np.array(I/255), sigma=sigma, low_threshold=low_threshold, high_threshold=high_threshold)
    edges = np.array(edges*255, dtype=np.uint8)
    return edges

# Driver Code