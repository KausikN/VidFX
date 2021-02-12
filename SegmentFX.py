'''
Segmentation based Effects in video and images
'''

# Imports
import functools

from Utils import EffectsLibrary

# Main Functions


# Driver Code
# Params
videoPath = 'TestVids/Test_Animation.wmv' #TYPE: FILE

fps = 20

SegmentFunc = functools.partial(EffectsLibrary.VideoEffect_SemanticSegmentation, overlay=False)

savePath = 'TestVids/Test_Effect.wmv'
# Params

# RunCode
SegmentFunc = functools.partial(SegmentFunc, fps=fps)
SegmentFunc(videoPath, savePath)