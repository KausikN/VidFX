'''
UI File for VidFX
'''

# Imports
from UIUtils import Py2UI
import VidFX

# Main Vars
funcKeyVals = {}

# Main Functions

# Driver Code
# Params
jsonPath = 'UIUtils/VidFXUI.json'

specialCodeProcessing = {"CommonEffects": VidFX.UICommonEffectsCodeParser, "EffectFuncs": VidFX.UIMultiEffectsCodeParser}
# Params

# RunCode
Py2UI.JSON2UI(jsonPath, specialCodeProcessing)