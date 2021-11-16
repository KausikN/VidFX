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
    # Convert to grayscale
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    # Decode
    decoded_data = decode(I_gray)
    # Add boxes to image
    for obj in decoded_data:
        x, y, w, h = obj.rect
        points = np.array(obj.polygon, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        # Draw Thick Lines of Black
        cv2.polylines(I, [points], True, box_padding_color, box_padding_thickness)
        # Draw Thin Lines
        cv2.polylines(I, [points], True, box_color, box_thickness)
        # Get Data
        data = str(obj.data.decode('utf-8'))
        codeType = obj.type
        displayText = text_formatting.format(codeType=codeType, data=data)
        # Add Text to Image
        cv2.putText(I, displayText, (x, y), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, text_thickness)

    return I

# Driver Code