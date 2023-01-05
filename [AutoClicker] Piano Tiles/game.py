import cv2
import numpy as np
import pyautogui as gui
from PIL import Image, ImageGrab

# VIDEO
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

"""
# CAPTURE THE SCREEN AND CONVERT TO OPENCV FORMAT (--BGR)
im = ImageGrab.grab(bbox = (0, 49, 463, 872)).convert("RGB")
im = np.array(im) 
# Convert RGB to BGR 
im = im[:, :, ::-1].copy()
"""

BLUE = (255, 0, 0)

while True:
    _, frame = vid.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape
    
    for y in range(height):
        for x in range(width):
            if hsv_frame[y, x][2] <= 5:
                print(hsv_frame[y, x])
                print("Coordinate : ({}, {})".format(x, y))
                #cv2.circle(frame, (x, y), 2, BLUE, 1)
            
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

vid.release()
cv2.destroyAllWindows()

"""
print("Shape : {}".format(im.shape))
cv2.imshow("im", im)
cv2.waitKey(0)
"""
 