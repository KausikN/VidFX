'''
Library for basic video functions
'''

# Imports
import cv2
import numpy as np

# Main Functions
def ReadVideo(path):
    cap = cv2.VideoCapture(path)
    return cap

def WebcamVideo():
    return cv2.VideoCapture(0)

def GetFramesFromVideo(vid=None, path=None, max_frames=-1):
    if vid is None:
        vid = ReadVideo(path)
    
    frames = []
    frameCount = 0

    # Check if camera opened successfully
    if (vid.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(vid.isOpened() and ((frameCount == max_frames) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            frames.append(frame)
            frameCount += 1
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    vid.release()

    return frames

def DisplayVideo(vid=None, path=None, max_frames=-1):
    if vid is None:
        vid = ReadVideo(path)
    
    frameCount = 0

    # Check if camera opened successfully
    if (vid.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(vid.isOpened() and ((frameCount == max_frames) or (max_frames == -1))):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            # Display the resulting frame
            cv2.imshow('Frame' + str(frameCount), frame)
            frameCount += 1
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    vid.release()

    cv2.destroyAllWindows()

# Driver Code
# Params
path = 'TestVids/test.mp4'
# Params

# RunCode
webcam = WebcamVideo()
DisplayVideo(webcam)