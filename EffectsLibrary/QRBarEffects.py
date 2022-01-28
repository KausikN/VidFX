'''
QRCode and BarCode Image Effects Library
'''

# Imports
import cv2
import numpy as np

from pyzbar.pyzbar import decode

# Main Functions
def ImageEffect_QRCode(I, 
    box_padding_color=(0, 0, 0), box_padding_thickness=1,
    box_color=(0, 0, 255), box_thickness=3,
    text_color=(0, 255, 0), text_scale=0.8, text_thickness=1,
    text_formatting="[{codeType}]: {data}"):
    # Fix Params
    box_padding_color = (int(box_padding_color[0]), int(box_padding_color[1]), int(box_padding_color[2]))
    box_color = (int(box_color[0]), int(box_color[1]), int(box_color[2]))
    text_color = (int(text_color[0]), int(text_color[1]), int(text_color[2]))
    box_thickness = max(1, int(box_thickness))
    box_padding_thickness = max(1, int(box_thickness + 2*box_padding_thickness))
    text_thickness = max(1, int(text_thickness))

    I_effect = np.array(I[:, :, :3] * 255, dtype=np.uint8)

    # Convert to grayscale
    I_gray = cv2.cvtColor(I, cv2.COLOR_RGBA2GRAY)
    # Decode
    decoded_data = decode(I_gray)
    # Add boxes to image
    for obj in decoded_data:
        x, y, w, h = obj.rect
        points = np.array(obj.polygon, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        # Draw Thick Lines of Black
        cv2.polylines(I_effect, [points], True, box_padding_color, box_padding_thickness)
        # Draw Thin Lines
        cv2.polylines(I_effect, [points], True, box_color, box_thickness)
        # Get Data
        data = str(obj.data.decode('utf-8'))
        codeType = obj.type
        displayText = text_formatting.format(codeType=codeType, data=data)
        # Add Text to Image
        cv2.putText(I_effect, displayText, (x, y), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, text_thickness)

    return I_effect

# Main Vars
EFFECTFUNCS_QRBAR = [
    {
        "name": "QRCode",
        "code": "QRCode(box_padding_color=(0, 0, 0), box_padding_thickness=1, box_color=(0, 0, 255), box_thickness=3, text_color=(0, 255, 0), text_scale=0.8, text_thickness=1, text_formatting=\"[{codeType}]: {data}\")",
        "func": ImageEffect_QRCode,
        "params": [
            {
                "name": "box_padding_color",
                "default": [0, 0, 0],
                "type": "list:int"
            },
            {
                "name": "box_padding_thickness",
                "default": 1,
                "type": "int",
                "min": 0,
                "max": 10,
                "step": 1
            },
            {
                "name": "box_color",
                "default": [0, 0, 255],
                "type": "list:int"
            },
            {
                "name": "box_thickness",
                "default": 3,
                "type": "int",
                "min": 0,
                "max": 10,
                "step": 1
            },
            {
                "name": "text_color",
                "default": [0, 255, 0],
                "type": "list:int"
            },
            {
                "name": "text_scale",
                "default": 0.8,
                "type": "float",
                "min": 0.1,
                "max": 1.0,
                "step": 0.1
            },
            {
                "name": "text_thickness",
                "default": 1,
                "type": "int",
                "min": 0,
                "max": 10,
                "step": 1
            },
            {
                "name": "text_formatting",
                "default": "[{codeType}]: {data}",
                "type": "str"
            }
        ]
    }
]
AVAILABLE_EFFECTS.extend(EFFECTFUNCS_QRBAR)

# Driver Code