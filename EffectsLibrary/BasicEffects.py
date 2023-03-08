'''
Basic Image Effects Library
'''

# Imports
from .EffectUtils import *

# Main Vars
INTERPOLATIONS = {
    "nearest": cv2.INTER_NEAREST,
    "linear": cv2.INTER_LINEAR,
    "cubic": cv2.INTER_CUBIC,
    "area": cv2.INTER_AREA
}

# Main Functions
def ImageEffect_None(I):
    return I

def ImageEffect_Binarise(I, threshold=0.5):
    size_RGB = I[:, :, :3].shape
    I_effect = np.zeros(size_RGB, dtype=float) + (I[:, :, :3] >= threshold)*np.ones(size_RGB, dtype=float)

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_GreyScale(I):
    I_effect = np.mean(I[:, :, :3], axis=2)

    I_effect = np.dstack((I_effect, I_effect, I_effect, I[:, :, 3]))
    return I_effect

def ImageEffect_Grey2RGB(I):
    return cv2.cvtColor(I, cv2.COLOR_GRAY2RGBA)

def ImageEffect_RGB2BGR(I):
    return cv2.cvtColor(I, cv2.COLOR_RGBA2BGRA)

def ImageEffect_RedChannel(I):
    return I[:, :, :] * np.array([1, 0, 0, 1])

def ImageEffect_BlueChannel(I):
    return I[:, :, :] * np.array([0, 0, 1, 1])

def ImageEffect_GreenChannel(I):
    return I[:, :, :] * np.array([0, 1, 0, 1])

def ImageEffect_Invert(I):
    I_effect = 1.0 - I[:, :, :3]

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_MostDominantColor(I):
    I_dom = np.max(I[:, :, :3], axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    I_effect = (I[:, :, :3])*(I_dom == I[:, :, :3])

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_LeastDominantColor(I):
    I_dom = np.min(I[:, :, :3], axis=2)
    I_dom = np.dstack((I_dom, I_dom, I_dom))
    I_effect = (I[:, :, :3])*(I_dom == I[:, :, :3])

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_ScaleValues(I, scaleFactor=[0.0, 0.0, 0.0]):
    scaleFactor = np.array(scaleFactor, dtype=float)
    I_effect = np.multiply(I[:, :, :3], scaleFactor)
    I_effect = np.clip(I_effect, 0.0, 1.0, dtype=float)

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_ClipValues(I, threshold=[0.25, 0.75], replace=[0.25, 0.75]):
    threshold = np.array(threshold, dtype=float)
    replace = np.array(replace, dtype=float)
    I_effect = np.clip(I[:, :, :3], threshold[0], threshold[1], dtype=float)
    lowCheck = (I_effect == threshold[0])
    highCheck = (I_effect == threshold[1])
    I_effect = lowCheck*np.ones(I_effect.shape, dtype=float)*replace[0] + \
        highCheck*np.ones(I_effect.shape, dtype=float)*replace[1] + \
        np.logical_not(np.logical_or(lowCheck, highCheck))*I_effect

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_BinValues(I, bins=[0.0, 0.5, 1.0]):
    bins = np.array(bins, dtype=float)
    binMaps = np.digitize(I[:, :, :3], bins)
    binMaps = np.clip(binMaps, 0, bins.shape[0]-1)
    I_effect = bins[binMaps]

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_Resize(I, size=(480, 640), interpolation="linear"):
    size = tuple(map(int, size))
    I_effect = cv2.resize(I, size, interpolation=INTERPOLATIONS[interpolation])
    return I_effect

def ImageEffect_Mirror(I):
    I_effect = I[:, ::-1]
    return I_effect

def ImageEffect_Translate(I, offset=[0.0, 0.0]):
    offset = np.array(offset, dtype=float)
    M = np.float32([
        [1, 0, offset[0]*I.shape[1]],
        [0, 1, offset[1]*I.shape[0]]
    ])
    I_effect = cv2.warpAffine(I[:, :, :3], M, (I.shape[1], I.shape[0]))

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_Rotate(I, angle=0.0, center=[0.5, 0.5]):
    center = np.array(center, dtype=float)
    angle = float(angle)
    centerPoint = tuple(np.array(I.shape[1::-1]) * center)
    M = cv2.getRotationMatrix2D(centerPoint, angle, 1.0)
    I_effect = cv2.warpAffine(I[:, :, :3], M, (I.shape[1], I.shape[0]))#, flags=cv2.INTER_LINEAR)

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_Scale(I, scale=[1.0, 1.0]):
    scale = np.array(scale, dtype=float)
    M = np.float32([
        [scale[0], 0, 0],
        [0, scale[1], 0]
    ])
    I_effect = cv2.warpAffine(I[:, :, :3], M, (I.shape[1], I.shape[0]))#, flags=cv2.INTER_LINEAR)

    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_GeometricTransform(I, translate=[0, 0], rotate=0.0, scale=[1.0, 1.0]):
    scale = np.array(scale, dtype=float)
    translate = np.array(translate, dtype=float)
    rotate = float(rotate)
    M = np.float32([
        [scale[0] * (np.cos(rotate)), -np.sin(rotate), translate[0]*I.shape[1]],
        [np.sin(rotate), scale[1] * (np.cos(rotate)), translate[1]*I.shape[0]]
    ])
    I_effect = cv2.warpAffine(I[:, :, :3], M, (I.shape[1], I.shape[0]))#, flags=cv2.INTER_LINEAR)
    
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

EFFECTFUNCS_BASIC = {
    "None": {
        "name": "None",
        "code": "None",
        "func": ImageEffect_None,
        "params": {}
    },
    "Binarise": {
        "name": "Binarise",
        "code": "Binarise(threshold=0.5)",
        "func": ImageEffect_Binarise,
        "params": {
            "threshold": 0.5
        }
    },
    "GreyScale": {
        "name": "GreyScale",
        "code": "GreyScale",
        "func": ImageEffect_GreyScale,
        "params": {}
    },
    "RGB2BGR": {
        "name": "RGB2BGR",
        "code": "RGB2BGR",
        "func": ImageEffect_RGB2BGR,
        "params": {}
    },
    "RedChannel": {
        "name": "RedChannel",
        "code": "RedChannel",
        "func": ImageEffect_RedChannel,
        "params": {}
    },
    "BlueChannel": {
        "name": "BlueChannel",
        "code": "BlueChannel",
        "func": ImageEffect_BlueChannel,
        "params": {}
    },
    "GreenChannel": {
        "name": "GreenChannel",
        "code": "GreenChannel",
        "func": ImageEffect_GreenChannel,
        "params": {}
    },
    "Invert": {
        "name": "Invert",
        "code": "Invert",
        "func": ImageEffect_Invert,
        "params": {}
    },
    "MostDominantColor": {
        "name": "MostDominantColor",
        "code": "MostDominantColor",
        "func": ImageEffect_MostDominantColor,
        "params": {}
    },
    "LeastDominantColor": {
        "name": "LeastDominantColor",
        "code": "LeastDominantColor",
        "func": ImageEffect_LeastDominantColor,
        "params": {}
    },
    "ScaleValues": {
        "name": "ScaleValues",
        "code": "ScaleValues(scaleFactor=[1.75, 1.75, 1.75])",
        "func": ImageEffect_ScaleValues,
        "params": {
            "scaleFactor": [1.75, 1.75, 1.75]
        }
    },
    "ClipValues": {
        "name": "ClipValues",
        "code": "ClipValues(threshold=[0.25, 0.75], replace=[0.25, 0.75])",
        "func": ImageEffect_ClipValues,
        "params": {
            "threshold": [0.25, 0.75],
            "replace": [0.25, 0.75]
        }
    },
    "BinValues": {
        "name": "BinValues",
        "code": "BinValues(bins=[0.0, 0.5, 1.0])",
        "func": ImageEffect_BinValues,
        "params": {
            "bins": [0.0, 0.5, 1.0]
        }
    },
    "Resize": {
        "name": "Resize",
        "code": "Resize(size=[640, 480], interpolation='linear')",
        "func": ImageEffect_Resize,
        "params": {
            "size": [640, 480],
            "interpolation": "linear"
        }
    },
    "Mirror": {
        "name": "Mirror",
        "code": "Mirror",
        "func": ImageEffect_Mirror,
        "params": {}
    },
    "Translate": {
        "name": "Translate",
        "code": "Translate(offset=[0.0, 0.0])",
        "func": ImageEffect_Translate,
        "params": {
            "offset": [0.0, 0.0]
        }
    },
    "Rotate": {
        "name": "Rotate",
        "code": "Rotate(angle=0.0, center=[0.5, 0.5])",
        "func": ImageEffect_Rotate,
        "params": {
            "angle": 0.0,
            "center": [0.5, 0.5]
        }
    },
    "Scale": {
        "name": "Scale",
        "code": "Scale(scale=[1.0, 1.0])",
        "func": ImageEffect_Scale,
        "params": {
            "scale": [1.0, 1.0]
        }
    },
    "GeometricTransform": {
        "name": "GeometricTransform",
        "code": "GeometricTransform(translate=[0.0, 0.0], rotate=0.0, scale=[1.0, 1.0])",
        "func": ImageEffect_GeometricTransform,
        "params": {
            "translate": [0.0, 0.0],
            "rotate": 0.0,
            "scale": [1.0, 1.0]
        }
    }
}