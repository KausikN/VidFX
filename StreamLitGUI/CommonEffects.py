
import cv2
import functools
import numpy as np

from EffectsLibrary import EffectsLibrary

CommonEffects = [
functools.partial(EffectsLibrary.ImageEffect_None)
]