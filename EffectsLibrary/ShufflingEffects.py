'''
Shuffling Image Effects Library
'''

# Imports
from .EffectUtils import *

# Main Functions
def ImageEffect_ShufflePixelsRandom(I):
    I_flat = np.reshape(I, (I.shape[0]*I.shape[1], I.shape[2]))
    I_shuffled_flat = np.copy(I_flat)
    np.random.shuffle(I_shuffled_flat)
    I_shuffled = np.reshape(I_shuffled_flat, (I.shape[0], I.shape[1], I.shape[2]))
    return I_shuffled

# Main Vars
EFFECTFUNCS_SHUFFLING = {
    "ShufflePixelsRandom": {
        "name": "ShufflePixelsRandom",
        "code": "ShufflePixelsRandom",
        "func": ImageEffect_ShufflePixelsRandom,
        "params": {}
    }
}