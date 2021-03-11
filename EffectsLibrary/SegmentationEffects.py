'''
Segmentation Image Effects Library
'''

# Imports
import os
import cv2
import numpy as np
from skimage import segmentation

import torch
import torch.nn as nn
from EffectsLibrary.ENet_LiteSegmenter.utils import *
from EffectsLibrary.ENet_LiteSegmenter.models.ENet import ENet

Segmenter_Semantic = None
Segmenter_Instance = None
Segmenter_FastSemantic = None

# Main Functions
# Loader Functions
def LoadSemanticSegmenter():
    from pixellib.semantic import semantic_segmentation
    global Segmenter_Semantic
    Segmenter_Semantic = semantic_segmentation()
    Segmenter_Semantic.load_pascalvoc_model("Models/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")

def LoadInstanceSegmenter():
    from pixellib.instance import instance_segmentation
    global Segmenter_Instance
    Segmenter_Instance = instance_segmentation()
    Segmenter_Instance.load_model("Models/mask_rcnn_coco.h5")

def LoadFastSemanticSegmenter():
    global Segmenter_FastSemantic

    model_path = 'Models/ckpt-camvid-enet.pth'
    num_classes = 12
    cuda = torch.device('cuda:0' if torch.cuda.is_available() and True else 'cpu')

    # Check if the pretrained model is available
    if not model_path.endswith('.pth'):
        print('Unknown file passed. Must end with .pth')

    checkpoint = torch.load(model_path, map_location=cuda)
    
    # Assuming the dataset is camvid
    enet = ENet(num_classes)
    enet.load_state_dict(checkpoint['state_dict'])

    Segmenter_FastSemantic = enet

# Direct Video Effects
def VideoEffect_SemanticSegmentation(videoPath, outputPath, overlay=False, fps=20):
    if Segmenter_Semantic is None:
        LoadSemanticSegmenter()
    Segmenter_Semantic.process_video_pascalvoc(videoPath, overlay=overlay, frames_per_second=fps, output_video_name=outputPath)

def VideoEffect_InstanceSegmentation(videoPath, outputPath, show_bboxes=False, fps=20):
    if Segmenter_Instance is None:
        LoadInstanceSegmenter()
    Segmenter_Instance.process_video(videoPath, show_bboxes=show_bboxes, frames_per_second=fps, output_video_name=outputPath)

# Effect Functions
def ImageEffect_SemanticSegmentation(I, overlay=False):
    if Segmenter_Semantic is None:
        LoadSemanticSegmenter()
    segmap, output = Segmenter_Semantic.segmentFrameAsPascalvoc(I, overlay=overlay)
    output = np.array(output)
    return output

def ImageEffect_InstanceSegmentation(I, show_bboxes=False):
    if Segmenter_Instance is None:
        LoadInstanceSegmenter()
    segmap, output = Segmenter_Instance.segmentFrame(I, show_bboxes=show_bboxes)
    output = np.array(output)
    return output

def ImageEffect_FastSemanticSegmentation(I):
    if Segmenter_FastSemantic is None:
        LoadFastSemanticSegmenter()

    h = 512
    w = 512

    tmg_ = cv2.resize(I, (h, w), cv2.INTER_NEAREST)
    tmg = torch.tensor(tmg_).unsqueeze(0).float()
    tmg = tmg.transpose(2, 3).transpose(1, 2)

    with torch.no_grad():
        out1 = Segmenter_FastSemantic(tmg.float()).squeeze(0)

    b_ = out1.data.max(0)[1].cpu().numpy()
    decoded_segmap = decode_segmap(b_)

    output = np.array(b_)

    return output

def ImageEffect_Watershed(I, watershed_line=True):#, bin_threshold=127):
    # I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)# >= bin_threshold
    I_filtered = segmentation.watershed(I, watershed_line=watershed_line)
    I_filtered = np.array(I_filtered*255, dtype=np.uint8)
    return I_filtered

# Driver Code