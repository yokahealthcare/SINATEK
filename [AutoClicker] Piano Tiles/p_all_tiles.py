import cv2
import numpy as np
import pyautogui as gui
from PIL import Image, ImageGrab

BLUE = (255, 0, 0)

print("Program Started!")

for i in range(1000):
    # CAPTURE THE SCREEN AND CONVERT TO OPENCV FORMAT (--BGR)
    im = ImageGrab.grab(bbox = (5, 60, 450, 650)).convert("RGB")
    im = np.array(im) 
    # Convert RGB to BGR 
    im = im[:, :, ::-1].copy()

    frame = im
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape
    
    black_color_founded = False
    for y in range(height):
        y = height - 1 - y
        for x in range(width):
            x = width - 1 - x
            hue = hsv_frame[y, x][0]
            saturation = hsv_frame[y, x][1]
            value = hsv_frame[y, x][2]

            if hue == 0 and saturation == 0 and value == 0:
                #print(hsv_frame[y, x])
                print("Coordinate : (Y: {}, X: {})".format(y, x))
                
                #gui.moveTo(x, y, 0.01)
                gui.click(x=x, y=y)
                
                black_color_founded = True
                break
        if black_color_founded:
            break


    key = cv2.waitKey(1)
    #break
    if key == 27:
        break

"""
print("Shape : {}".format(im.shape))
cv2.imshow("im", im)
cv2.waitKey(0)
"""
cv2.imshow("hsv_frame", hsv_frame)
cv2.waitKey(0)