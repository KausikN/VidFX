'''
Segmentation Image Effects Library
'''

# Imports
from .EffectUtils import *

from skimage import segmentation

# Main Vars
ModelsDir = "ModelFiles/"

Segmenter_Semantic = None
Segmenter_Instance = None
Segmenter_FastSemantic = None

# Main Functions
# Loader Functions
def LoadSemanticSegmenter():
    from pixellib.semantic import semantic_segmentation
    global Segmenter_Semantic
    Segmenter_Semantic = semantic_segmentation()
    Segmenter_Semantic.load_pascalvoc_model(ModelsDir + "deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")

def LoadInstanceSegmenter():
    from pixellib.instance import instance_segmentation
    global Segmenter_Instance
    Segmenter_Instance = instance_segmentation()
    Segmenter_Instance.load_model(ModelsDir + "mask_rcnn_coco.h5")

# Direct Video Effects
def VideoEffect_SemanticSegmentation(videoPath, outputPath, overlay=False, fps=20, **params):
    if Segmenter_Semantic is None:
        LoadSemanticSegmenter()
    Segmenter_Semantic.process_video_pascalvoc(videoPath, overlay=overlay, frames_per_second=fps, output_video_name=outputPath)

def VideoEffect_InstanceSegmentation(videoPath, outputPath, show_bboxes=False, fps=20, **params):
    if Segmenter_Instance is None:
        LoadInstanceSegmenter()
    Segmenter_Instance.process_video(videoPath, show_bboxes=show_bboxes, frames_per_second=fps, output_video_name=outputPath)

# Effect Functions
def ImageEffect_SemanticSegmentation(I, overlay=False, **params):
    if Segmenter_Semantic is None:
        LoadSemanticSegmenter()
    segmap, output = Segmenter_Semantic.segmentFrameAsPascalvoc(I[:, :, :3], overlay=overlay)
    I_effect = np.array(output)
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_InstanceSegmentation(I, show_bboxes=False, **params):
    if Segmenter_Instance is None:
        LoadInstanceSegmenter()
    segmap, output = Segmenter_Instance.segmentFrame(I[:, :, :3], show_bboxes=show_bboxes)
    I_effect = np.array(output)
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_Watershed(I, watershed_line=True, **params):#, bin_threshold=127):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)# >= bin_threshold
    I_filtered = segmentation.watershed(I[:, :, :3], watershed_line=watershed_line)
    
    I_effect = np.clip(I_filtered, 0.0, 1.0, dtype=float)
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Vars
EFFECTFUNCS_SEGMENTATION = {
    "SemanticSegmentation": {
        "name": "SemanticSegmentation",
        "code": "SemanticSegmentation(overlay=True)",
        "func": ImageEffect_SemanticSegmentation,
        "params": {
            "overlay": True
        }
    },
    "InstanceSegmentation": {
        "name": "InstanceSegmentation",
        "code": "InstanceSegmentation(show_bboxes=True)",
        "func": ImageEffect_InstanceSegmentation,
        "params": {
            "show_bboxes": True
        }
    },
    "Watershed": {
        "name": "Watershed",
        "code": "Watershed(watershed_line=True)",
        "func": ImageEffect_Watershed,
        "params": {
            "watershed_line": True
        }
    }
}