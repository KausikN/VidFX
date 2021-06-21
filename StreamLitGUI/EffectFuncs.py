
import cv2
import functools
import numpy as np

from EffectsLibrary import EffectsLibrary

EffectFuncs = [
[
functools.partial(EffectsLibrary.ImageEffect_Resize, size=(1, 2))
]]