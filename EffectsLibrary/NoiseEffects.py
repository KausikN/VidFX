'''
Noise Image Effects Library
'''

# Imports
import cv2
import numpy as np

# Main Functions
def ImageEffect_GaussianNoise(I, mean=0.0, SD=0.25):
    I_effect = I[:, :, :3] + np.random.normal(mean, SD, size=I[:, :, :3].shape).astype(float)
    I_effect = np.clip(I_effect, 0.0, 1.0)

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_SpeckleNoise(I):
    noise = np.random.randn(I.shape[0], I.shape[1], 3).astype(float)
    I_effect = I[:, :, :3] + (I[:, :, :3]*noise)
    I_effect = np.clip(I_effect, 0.0, 1.0)

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_SaltPepperNoise(I, prob=0.5):
    h, w, c = I.shape
    mask = np.random.choice((0, 1, 2), size=(h, w), p=[1-prob, prob/2., prob/2.])
    I_effect = I[:, :, :3]
    I_effect[mask == 1] = 1.0
    I_effect[mask == 2] = 0.0
    
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Vars
EFFECTFUNCS_NOISE = [
    {
        "name": "GaussianNoise",
        "code": "GaussianNoise(mean=0.2, SD=0.1)",
        "func": ImageEffect_GaussianNoise,
        "params": [
            {
                "name": "mean",
                "default": 0.2,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.05
            },
            {
                "name": "SD",
                "default": 0.1,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.05
            }
        ]
    },
    {
        "name": "SpeckleNoise",
        "code": "SpeckleNoise",
        "func": ImageEffect_SpeckleNoise,
        "params": []
    },
    {
        "name": "SaltPepperNoise",
        "code": "SaltPepperNoise(prob=0.5)",
        "func": ImageEffect_SaltPepperNoise,
        "params": [
            {
                "name": "prob",
                "default": 0.5,
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "step": 0.1
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_NOISE)

# Driver Code