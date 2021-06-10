'''
Shuffling Image Effects Library
'''

# Imports
import cv2
import numpy as np

# Main Functions
def ImageEffect_RandomShufflePixels(I):
    I_flat = np.reshape(I, (I.shape[0]*I.shape[1], I.shape[2]))
    I_shuffled_flat = I_flat
    np.random.shuffle(I_shuffled_flat)
    I_shuffled = np.reshape(I_shuffled_flat, (I.shape[0], I.shape[1], I.shape[2]))
    return I_shuffled

# Driver Code