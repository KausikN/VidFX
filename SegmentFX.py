'''
Segmentation based Effects in video and images
'''

# Imports
import functools

from EffectsLibrary import EffectsLibrary

# Main Functions


# Driver Code
# Params
videoPath = 'TestVids/Test_Car.mp4' #TYPE: FILE

fps = 20

SegmentFunc = functools.partial(EffectsLibrary.VideoEffect_InstanceSegmentation, show_bboxes=True)

savePath = 'TestVids/CarVidSeg_Video.wmv'
# Params

# RunCode
SegmentFunc = functools.partial(SegmentFunc, fps=fps)
SegmentFunc(videoPath, savePath)