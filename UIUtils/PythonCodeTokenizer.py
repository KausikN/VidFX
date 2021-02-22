'''
Tokenizes any Python Code
'''

# Imports
import re
import json

# Load Config
config = json.load(open('UIUtils/TokenConfig.json', 'rb'))

# Main Functions
# Basic Functions
def ReadPythonCode(path):
    return open(path, 'r').readlines()

def isStringData(val, StringDetectors):
    for sd in StringDetectors:
        if val.startswith(sd) and val.endswith(sd):
            return True
    return False

def StringDataDetector(val, StringDetectors):
    for sd in StringDetectors:
        if val.startswith(sd) and val.endswith(sd):
            return sd
    return None

def isData_DetectorBased(val, Detectors):
    for d in Detectors:
        if d[0] in val and d[1] in val:
            if val.find(d[0]) < (len(val) - val[::-1].find(d[1])):
                return True
    return False

def FindDataDetector(val, Detectors):
    for d in Detectors:
        if d[0] in val and d[1] in val:
            if val.find(d[0]) < (len(val) - val[::-1].find(d[1])):
                return d
    return None

def CheckType(value, TypeFunc):
    try: 
        TypeFunc(value)
        return True
    except ValueError:
        return False

# JSON Code Functions
def LoadCodeDataFromJSON(json_path):
    codeDataJSON = json.load(open(json_path, 'rb'))

    # Assign Window Title
    WindowTitle = codeDataJSON['WindowTitle']

    # Assign Basic Data
    codeData = Code()
    codeData.code_path = codeDataJSON['code_path']
    codeData.code_lines = ReadPythonCode(codeData.code_path)
    # Assign Script Desc, Imports, Driver Code
    codeData.script_desc = codeDataJSON['script_desc']
    codeData.imports = codeDataJSON['imports']
    # Assign Classes
    codeData.classes = []
    for cd in codeDataJSON['classes']:
        c = Class(cd['name'], cd['code'])
        codeData.classes.append(c)
    # Assign Functions
    codeData.functions = []
    for fd in codeDataJSON['functions']:
        f = Function(fd['name'], fd['desc'], fd['parameters'], fd['code'])
        codeData.functions.append(f)
    # Assign Script Parameters
    codeData.script_parameters = []
    for sd in codeDataJSON['script_parameters']:
        s = ScriptParameter(sd['name'], sd['value'])
        codeData.script_parameters.append(s)
    # Assign Driver Code
    codeData.driver_code = codeDataJSON['driver_code']

    return codeData, WindowTitle

def WriteCodeDataToJSON(codeData, json_path, WindowTitle='Generated UI'):
    codeDataJSON = {}

    # Assign Window Title
    codeDataJSON['WindowTitle'] = WindowTitle

    # Assign Basic Data
    codeDataJSON['code_path'] = codeData.code_path
    # Assign Script Desc, Imports, Driver Code
    codeDataJSON['script_desc'] = codeData.script_desc
    codeDataJSON['imports'] = codeData.imports
    # Assign Classes
    codeDataJSON['classes'] = []
    for cd in codeData.classes:
        c = {'name': cd.name, 'code': c.code}
        codeDataJSON['classes'].append(c)
    # Assign Functions
    codeDataJSON['functions'] = []
    for fd in codeData.functions:
        f = {'name': fd.name, 'desc': fd.desc, 'parameters': fd.parameters, 'code': fd.code}
        codeDataJSON['functions'].append(f)
    # Assign Script Parameters
    codeDataJSON['script_parameters'] = []
    for sd in codeDataJSON['script_parameters']:
        s = {'name': sd.name, 'value': sd.valueText}
        codeDataJSON['script_parameters'].append(s)
    # Assign Driver Code
    codeDataJSON['driver_code'] = codeData.driver_code

    json.dump(codeDataJSON, open(json_path, 'wb'))


# Code Class
class Code:
    def __init__(self, path=None):
        if path is not None:
            self.code_path = path
            self.tokenize()
        else:
            self.code_path = None
            self.code_lines = None
            self.script_desc, self.imports, self.classes, self.functions, self.script_parameters, self.driver_code = '', [], [], [], [], ''

    def tokenize(self):
        # Read the code lines
        self.code_lines = ReadPythonCode(self.code_path)
        # Tokenize and get all the required parts of the code
        self.script_desc, self.imports, self.classes, self.functions, self.script_parameters, self.driver_code = PythonCode_Tokenize(self.code_lines)

# Function Class
class Function:
    def __init__(self, name, desc, parameters, code):
        self.name = name
        self.desc = desc
        self.parameters = parameters
        self.code = code

# Classes Class
class Class:
    def __init__(self, name, code):
        self.name = name
        self.code = code

# Script Parameters
class ScriptParameter:
    def __init__(self, name, value):
        self.name = name
        self.valueText = value
        self.value = value
        self.value_prefix = ''
        self.value_suffix = ''
        self.type = None
        self.ui_mode = None
        self.otherData = {}
        self.findType(value)
    def getCodeText(self):
        if self.value is None:
            return self.name + " = " + "None"
        elif type(self.value) == list:
            data = []
            for i in range(len(self.otherData['ListData'])):
                ref_index = i
                if i >= len(self.value):
                    ref_index = 0
                self.value[ref_index].value = self.otherData['ListData'][i]
                data.append(self.value[ref_index].getValueText())
            return self.name + " = " + self.value_prefix + ','.join(data) + self.value_suffix
        else:
            return self.name + " = " + self.value_prefix + str(self.value) + self.value_suffix
    def getValueText(self):
        if self.value is None:
            return "None"
        elif type(self.value) == list:
            data = []
            for i in range(len(self.otherData['ListData'])):
                ref_index = i
                if i >= len(self.value):
                    ref_index = 0
                self.value[ref_index].value = self.otherData['ListData'][i]
                data.append(self.value[ref_index].getCodeText())
            return self.value_prefix + ','.join(data) + self.value_suffix
        else:
            return self.value_prefix + str(self.value) + self.value_suffix
    def findType(self, value):
        # No Type - Put as it is
        NoType = False
        self.otherData['multiple_lines_string'] = False
        # String MultiLine Preprocess
        if value.strip().endswith(config['String_MultiLine_Declare']):
            self.otherData['multiple_lines_string'] = True
            value = value.strip().rstrip(config['String_MultiLine_Declare'])

        if config['NoType_Declare'] in value:
            self.value = value.replace(config['NoType_Declare'], '').strip()
            self.type = str
            NoType = True
            return
        # Specified Type
        SpecifiedType = True
        if config['SpecificType_Declare'] in value:
            ValueData = re.findall('^(.*)' + config['SpecificType_Declare'], value)[-1].strip()
            SpecTypeData = re.findall(config['SpecificType_Declare'] + '(.*)', value)[-1].strip().split(' ')
            # Dropdown Type
            if SpecTypeData[0] == config['SpecificTypes']['Dropdown']:
                self.ui_mode = config['SpecificTypes']['Dropdown']
                choices = ' '.join(SpecTypeData[1:]).split(',')
                sp_temp = ScriptParameter('temp', choices[0])
                choices[0] = sp_temp.value
                self.type = sp_temp.type
                self.value = list(map(self.type, choices))
            # File Select Type
            elif SpecTypeData[0] == config['SpecificTypes']['FileSelect']:
                self.ui_mode = config['SpecificTypes']['FileSelect']
                self.value = ValueData[1:-1]
                self.type = type(self.value)
                self.value_prefix = ValueData[0]
                self.value_suffix = ValueData[-1]
                # Check for accepted extensions
                if len(SpecTypeData) > 1:
                    # Check for existing extension packs
                    exts = None
                    if (SpecTypeData[1].strip() + "_Extensions") in config.keys():
                        exts = config[SpecTypeData[1].strip() + "_Extensions"]
                    else:
                        exts = SpecTypeData[1].split(',')
                    self.otherData['ext'] = exts
            # Dir Select Type
            elif SpecTypeData[0] == config['SpecificTypes']['DirectorySelect']:
                self.ui_mode = config['SpecificTypes']['DirectorySelect']
                self.value = ValueData[1:-1]
                self.type = type(self.value)
                self.value_prefix = ValueData[0]
                self.value_suffix = ValueData[-1]
            else: # Empty Specification - IGNORE
                SpecifiedType = False
        else:
            SpecifiedType = False

        if not SpecifiedType:
            # None Type
            if value == 'None':
                self.value = None
                self.type = type(None)
            # Bool Type
            elif value in ['True', 'False']:
                self.value = value == 'True'
                self.type = type(self.value)
            # String Type
            elif isStringData(value, config['String_Detect']):
                detectedDetector = StringDataDetector(value, config['String_Detect'])
                self.value = value[len(detectedDetector):-len(detectedDetector)]
                self.type = type(self.value)
                self.value_prefix = value[0]
                self.value_suffix = value[-1]
                
            # Array Type
            elif isData_DetectorBased(value, config['Array_Detect']):
                self.otherData['sizeRange'] = [0, 5]

                SizeCheck = False
                for ad in config['Array_Detect']:
                    if config['ArrayType_SizeRestrict_Declare'] in value.split(ad[1])[-1] and ad[1] in value:
                        SizeCheck = True
                        print(value)
                        print(re.findall(config['ArrayType_SizeRestrict_Declare'] + '(.*)', value.split(ad[1])[-1])[-1])
                        sizeRange = re.findall(config['ArrayType_SizeRestrict_Declare'] + '(.*)', value.split(ad[1])[-1])[-1].strip().split('$')
                        self.otherData['sizeRange'] = [int(sizeRange[0].strip()), int(sizeRange[1].strip())]
                        value = re.findall('^(.*)' + config['ArrayType_SizeRestrict_Declare'], value)[0].strip()
                        break

                detectedDetector = FindDataDetector(value, config['Array_Detect'])
                self.value = value[len(detectedDetector[0]):-len(detectedDetector[1])]
                if self.value == '':
                    self.value = []
                else:
                    datalist = self.value.split(',')
                    self.value = []
                    for i in range(len(datalist)):
                        self.value.append(ScriptParameter(str(i), datalist[i].strip()))
                self.type = config['ArrayType_Declare']
                self.value_prefix = value[0]
                self.value_suffix = value[-1]
                self.ui_mode = config['ArrayType_Declare']
            # Other Types
            else:
                Types = [int, float]

                TypeFound = False
                for ty in Types:
                    if CheckType(value, ty):
                        self.value = ty(value)
                        self.type = type(self.value)
                        TypeFound = True
                        break
                        
                if not TypeFound and not NoType:
                    # If no available type consider as no type
                    self.value = value
                    self.type = str
                
            



# Following Rules should be followed in Code
# 1. Script Description MUST be given at start in ''' or """
# 2. Code must be separated in 3 parts:
#       -   Imports after line # Imports
#       -   Functions after line # Main Functions
#       -   Driver Code after line # Driver Code
def PythonCode_Tokenize(code_lines, verbose=False):
    # Preprocess
    # Remove all empty lines
    code_lines_preprocessed = []
    for l in code_lines:
        if not l.strip() == '':
            code_lines_preprocessed.append(l)
    code_lines = code_lines_preprocessed

    if verbose:
        print("Initial Code:\n", code_lines)

    curIndex = 0
    # Get the Script Description
    ScriptDesc, remaining_code_lines = GetScriptDesc(code_lines)
    code_lines = remaining_code_lines
    if verbose:
        print("Script Desc:\n", ScriptDesc)
        # print("Code after Script Desc:\n", code_lines)

    # Get the Imports
    Imports, remaining_code_lines = GetImports(code_lines)
    code_lines = remaining_code_lines
    if verbose:
        print("Imports:\n", Imports)
        # print("Code after Imports:\n", code_lines)  

    # Get Functions
    Functions, Classes, remaining_code_lines = GetClassesFunctions(code_lines)
    code_lines = remaining_code_lines
    if verbose:
        print("Functions:\n")
        for f in Functions:
            print(f.name, "\n", f.parameters, "\n", f.code)
        # print("Code after Functions Code:\n", code_lines)

    # Get ScriptParameters
    ScriptParameters, remaining_code_lines = GetScriptParameters(code_lines)
    code_lines = remaining_code_lines
    if verbose:
        print("ScriptParameters:\n")
        for sp in ScriptParameters:
            print(sp.name, "\n", sp.value, "\n", sp.type)
        # print("Code after ScriptParameters:\n", code_lines)
    
    # Get Driver Code
    DriverCode = code_lines
    if verbose:
        print("Driver Code:\n")
        for c in DriverCode:
            print(c)

    return ScriptDesc, Imports, Classes, Functions, ScriptParameters, DriverCode
            
def GetScriptDesc(code_lines):
    remaining_code_lines = []

    ScriptDesc = ''
    DescSeparators = config['Desc_Detect']
    
    DescFound = False
    SepFound = False
    UsedSep = None
    for i in range(len(code_lines)):
        if DescFound:
            remaining_code_lines.append(code_lines[i])
            continue
        l = code_lines[i].strip()
        if not SepFound:
            for sep in DescSeparators:
                if l.startswith(sep):
                    UsedSep = sep
                    SepFound = True
                    if len(l) > len(UsedSep):
                        ScriptDesc = l[len(UsedSep):]
                        # print("Added1:", l[len(UsedSep):])
                        if l.endswith(UsedSep):
                            if len(ScriptDesc) > len(UsedSep):
                                ScriptDesc = ScriptDesc[:-len(UsedSep)]
                                # print("Replaced Same Line:", ScriptDesc[:-len(UsedSep)])
                            SepFound = False
                            DescFound = True
                        else:
                            ScriptDesc = ScriptDesc + "\n"
                            # print("Added:", "\\n")
                    break
            if SepFound:
                continue
        if SepFound:
            if l.endswith(UsedSep):
                if len(l) > len(UsedSep):
                    ScriptDesc = ScriptDesc + l[:-len(UsedSep)]
                    # print("Added2:", l[:-len(UsedSep)])
                SepFound = False
                DescFound = True
            else:
                ScriptDesc = ScriptDesc + l + "\n"
                # print("Added3:", l)

    if not DescFound:
        ScriptDesc = ''
        remaining_code_lines = code_lines

    ScriptDesc = ScriptDesc.strip('\n')

    return ScriptDesc, remaining_code_lines

def GetImports(code_lines):
    remaining_code_lines = []

    Imports = []
    ImportDetectors = config['Import_Detect']

    lastImport_Index = -1
    for i in range(len(code_lines)):
        for imd in ImportDetectors:
            if re.search(imd, code_lines[i]) is not None:
                Imports.append(code_lines[i].strip('\n'))
                lastImport_Index = i
                break

    if lastImport_Index == -1:
        remaining_code_lines = code_lines
    elif lastImport_Index < len(code_lines)-1:
        remaining_code_lines = code_lines[lastImport_Index+1:]

    return Imports, remaining_code_lines

def GetClassesFunctions(code_lines):
    remaining_code_lines = []

    Functions = []
    Classes = []
    ClassStart = config['Class_Start']
    ClassEnd = config['Class_End']
    FunctionStart = config['Function_Start']
    FunctionEnd = config['Function_End']

    FunctionStarted = False
    ClassStarted = False
    curFunction = None
    curClass = None
    for i in range(len(code_lines)):
        if ClassStarted:
            if code_lines[i].strip().startswith(ClassEnd):
                ClassStarted = False
                Classes.append(curClass)
                curClass = None
                if i < len(code_lines)-1:
                    remaining_code_lines = code_lines[i+1:]
                continue
            else:
                curClass.code.append(code_lines[i].strip('\n'))
        elif re.search(ClassStart, code_lines[i]) is not None:
            ClassStarted = True
            name = re.findall(config['Class_Name_Detect'], code_lines[i])[0].strip('\n')
            curClass = Class(name, [])
            continue
        if FunctionStarted:
            if code_lines[i].strip().startswith(FunctionEnd):
                FunctionStarted = False
                Functions.append(curFunction)
                curFunction = None
                if i < len(code_lines)-1:
                    remaining_code_lines = code_lines[i+1:]
                continue
            else:
                curFunction.code.append(code_lines[i].strip('\n'))
        elif re.search(FunctionStart, code_lines[i]) is not None:
            FunctionStarted = True
            name = re.findall(config['Function_Name_Detect'], code_lines[i])[0].strip('\n')
            parameters = re.findall(config['Function_Parameters_Detect'], code_lines[i])[0].replace(' ', '').strip('\n').split(',')
            curFunction = Function(name, '', parameters, [])
            continue

    if len(Functions) == 0 and len(Classes) == 0:
        remaining_code_lines = code_lines

    return Functions, Classes, remaining_code_lines

def GetScriptParameters(code_lines):
    remaining_code_lines = []

    ScriptParameters = []
    ParamsStart = config['ScriptParams_Start']
    ParamsEnd = config['ScriptParams_End']

    ParamsStarted = False
    curParams = []
    for i in range(len(code_lines)):
        print(code_lines[i])
        if ParamsStarted:
            if code_lines[i].strip().startswith(ParamsEnd):
                ParamsStarted = False
                ScriptParameters.extend(curParams)
                curParams = []
                continue
            else:
                name = re.findall(config['ScriptParams_Name_Detect'], code_lines[i])[0].strip().strip('\n')
                value = re.findall(config['ScriptParams_Value_Detect'], code_lines[i])[0].strip().strip('\n')
                param = ScriptParameter(name, value)
                curParams.append(param)
        elif code_lines[i].strip().startswith(ParamsStart):
            ParamsStarted = True
            continue
        else:
            remaining_code_lines.append(code_lines[i].strip('\n'))

    return ScriptParameters, remaining_code_lines

# Reconstruction Functions
def ReconstructCodeText(code_data):
    code_text = []

    # Reconstruct Script Desc
    code_text.append(config['Desc_Detect'][0])
    code_text.append(code_data.script_desc)
    code_text.append(config['Desc_Detect'][0])

    code_text.append("")

    # Reconstruct Imports
    code_text.append("# Imports")
    for imp in code_data.imports:
        code_text.append(imp)
    
    code_text.append("")

    # Reconstruct Main Functions
    code_text.append("# Main Functions")
    for c in code_data.classes:
        code_text.append("class " + c.name + ":")
        code_text.extend(c.code)
    for f in code_data.functions:
        code_text.append("def " + f.name + "(" + ', '.join(f.parameters) + "):")
        code_text.extend(f.code)

    code_text.append("")

    # Reconstruct Script Parameters
    code_text.append("# Driver Code")
    code_text.append("# Params")
    for sp in code_data.script_parameters:
        code_text.append(sp.getCodeText())

    code_text.append("")

    # Reconstruct Driver Code
    code_text.extend(code_data.driver_code)

    return '\n'.join(code_text)

"""
# Driver Code
# Params
mainPath = 'TestCodes/'
fileName = 'Test.py'

ReconstructedCode_savePath = 'Test_RE.py'

# Parse Original Code
PyCode = Code(mainPath + fileName)

# Change Data
changeParamName = 'IntVal'
replaceVal = 2
for i in range(len(PyCode.script_parameters)):
    if PyCode.script_parameters[i].name == changeParamName:
        PyCode.script_parameters[i].value = replaceVal

# Reconstruct Code
code_RE = ReconstructCodeText(PyCode)
open(mainPath + ReconstructedCode_savePath, 'w').write(code_RE)
"""