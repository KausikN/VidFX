'''
UI File for VidFX
'''

# Imports
from UIUtils import Py2UI

# Main Functions
def UICommonEffectsCodeParser(data):
    # INPUT FORMAT
    # <EffectFuncName>(<Param1Name>=<Param1Value>, <Param2Name>=<Param2Value>, ...)
    # OUTPUT FORMAT
    # functools.partial(<EffectFuncName>, <Param1Name>=<Param1Value>, <Param2Name>=<Param2Value>, ...)

    data = data.split('\n')

    parsedData = []
    for line in data:
        line = line.strip()
        if line in ['', '[', ']', ',']:
            continue
        else:
            funcname = "EffectsLibrary.ImageEffect_" + line.split('(')[0].strip()
            paramText = '('.join(line.split('(')[1:]).rstrip(',')
            if paramText.endswith(')'):
                paramText = paramText[:-1]
            if not paramText.strip() == "":
                paramText = ", " + paramText
            parsedData.append('functools.partial(' + funcname + paramText + ')')
    
    parsedData = "[\n" + ',\n'.join(parsedData) + "\n]"

    return parsedData

def UIMultiEffectsCodeParser(data):
    # GAP BETWEEN EFFECTS is a line with only ',' in it

    data = data.split('\n')

    parsedData = []
    parsedCurEffectData = []
    for line in data:
        line = line.strip()
        if line in ['[', ']']:
            continue
        elif line in ['', ',']:
            if len(parsedCurEffectData) > 0:
                parsedCurEffectData = UICommonEffectsCodeParser('\n'.join(parsedCurEffectData))
                parsedData.append(parsedCurEffectData)
                parsedCurEffectData = []
        else:
            parsedCurEffectData.append(line)
    
    parsedData = "[\n" + ',\n'.join(parsedData) + "]"

    return parsedData

# Driver Code
# Params
jsonPath = 'UIUtils/VidFXUI.json'

specialCodeProcessing = {"CommonEffects": UICommonEffectsCodeParser, "EffectFuncs": UIMultiEffectsCodeParser}
# Params

# RunCode
Py2UI.JSON2UI(jsonPath, specialCodeProcessing)