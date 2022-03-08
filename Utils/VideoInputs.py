'''
Video Input Modes
'''

# Imports
import cv2
import numpy as np
import requests
import imutils

# Main Classes
class VideoInput:
    def __init__(self, url):
        self.url = url

    def isOpened(self):
        return True

    def release(self):
        pass

    def read(self):
        success = False
        img = None
        try:
            img_resp = requests.get(self.url).content
            img_arr = np.array(bytearray(img_resp), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            # img = imutils.resize(img, width=1000, height=1800)
            success = True
        except:
            pass
        # return success, img
        if img is None: img = np.zeros((480, 640, 3), np.uint8)
        return True, img

# Main Functions
def ReadVideo(path):
    return cv2.VideoCapture(path)

def WebcamVideo():
    return cv2.VideoCapture(0)

def ReadVideo_URL(url):
    return VideoInput(url)

# Driver Code