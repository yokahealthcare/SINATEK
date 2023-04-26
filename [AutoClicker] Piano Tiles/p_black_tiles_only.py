import pyautogui as gui
import time
import keyboard
import numpy as np
import win32api, win32con
import cv2

"""
COORDINATE
Piano Tiles 2 - ONLINE
Title 1 : (425, 600)
Title 2 : (557, 600)
Title 3 : (680, 600)
Title 4 : (810, 600)

Piano Tiles 2 - Android
Title 1 : (51, 350): (172, 350)
Title 2 
Title 3 : (283, 350)
Title 4 : (407, 350)

"""
y_global = 440
tiles = [51, 172, 283, 407]

def click(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	
while keyboard.is_pressed('q') == False:
	for x in tiles:
		tile_changing = False
		while tile_changing == False:
			color_pixel = gui.pixel(x, y_global)

			if color_pixel[0] < 100:
				click(x, y_global)
			else:
				tile_changing = True
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

			if keyboard.is_pressed('q'):
				exit()