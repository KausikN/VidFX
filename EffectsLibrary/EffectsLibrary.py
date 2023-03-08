'''
Image Effects Library
'''

# Imports
from .BasicEffects import *
from .CombinationEffects import *
from .TimeEffects import *
from .FrameEffects import *
from .NoiseEffects import *
from .FilterEffects import *
from .SegmentationEffects import *
from .MorphologicalEffects import *
from .TerrainGenEffects import *
from .PlotEffects import *
from .TransparencyEffects import *
from .ShufflingEffects import *
from .QRBarEffects import *

from .EffectUtils import *

# Load Effect Modules
EFFECT_MODULES_FUNCS = {
    "basic": EFFECTFUNCS_BASIC,
    "combination": EFFECTFUNCS_COMBINATION,
    "time": EFFECTFUNCS_TIME,
    "frame": EFFECTFUNCS_FRAME,
    "noise": EFFECTFUNCS_NOISE,
    "filter": EFFECTFUNCS_FILTER,
    "segmentation": EFFECTFUNCS_SEGMENTATION,
    "morphological": EFFECTFUNCS_MORPHOLOGICAL,
    "terraingen": EFFECTFUNCS_TERRAINGEN,
    "plot": EFFECTFUNCS_PLOT,
    "transparency": EFFECTFUNCS_TRANSPARENCY,
    "shuffling": EFFECTFUNCS_SHUFFLING,
    "qrbar": EFFECTFUNCS_QRBAR
}
AVAILABLE_EFFECTS = {}
for k in EFFECT_MODULES_FUNCS.keys(): AVAILABLE_EFFECTS.update(EFFECT_MODULES_FUNCS[k])