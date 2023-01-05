import pyautogui as gui
import time
import keyboard
import numpy as np
import win32api, win32con
import cv2

"""
Piano Tiles 2 - ONLINE

Title 1 : (425, 600)
Title 2 : (557, 600)
Title 3 : (680, 600)
Title 4 : (810, 600)

"""
y_global = 350
x_title1 = 51
x_title2 = 172
x_title3 = 283
x_title4 = 407
def click(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	time.sleep(0.01)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while keyboard.is_pressed('q') == False:

	if gui.pixel(x_title1, y_global)[0] == 0:
		click(x_title1, y_global)
	if gui.pixel(x_title2, y_global)[0] == 0:
		click(x_title2, y_global)
	if gui.pixel(x_title3, y_global)[0] == 0:
		click(x_title3, y_global)
	if gui.pixel(x_title4, y_global)[0] == 0:
		click(x_title4, y_global)