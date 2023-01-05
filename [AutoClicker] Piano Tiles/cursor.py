import os
import time
import pyautogui as gui

while True:
	pos = gui.position()
	os.system("cls")
	print("X : {}".format(pos[0]))
	print("Y : {}".format(pos[1]))
	time.sleep(0.1)