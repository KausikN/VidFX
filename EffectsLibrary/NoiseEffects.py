'''
Noise Image Effects Library
'''

# Imports
import cv2
import numpy as np

# Main Functions
def ImageEffect_GaussianNoise(I, mean=0, SD=1):
    return I + np.random.normal(mean, SD, size=I.shape).astype(int)

def ImageEffect_SpeckleNoise(I):
    noise = np.random.randn(I.shape[0], I.shape[1], I.shape[2]).astype(int)
    I = I + (I*noise)
    return I

def ImageEffect_SaltPepperNoise(I, prob=0.5):
    h, w, c = I.shape
    mask = np.random.choice((0, 1, 2), size=(h, w), p=[1-prob, prob/2., prob/2.])
    I[mask == 1] = 255
    I[mask == 2] = 0
    return I

# Driver Code