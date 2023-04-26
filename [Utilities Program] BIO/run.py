# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:09:46 2021

CENTRAL CONTROL 
@author: Erwin

"""

import os
from rich.console import Console
import cowsay

console = Console()

from pyfiglet import Figlet
custom_fig = Figlet(font='chunky')
console.print(custom_fig.renderText('BIO'), style="bold green")
console.print("CENTRAL CONTROL - MY PERSONAL ASSISTANT!")

menus = [
    'Youtube',
    'wiz',
    'Exit'        
]

import youtube_utility as youtube
import wiz_utility as wiz

running = True
while running:
    for i in range(len(menus)):
        console.print("[{}] {}".format(i+1, menus[i]), style="bold")
    
    u = int(input(">>>> "))
    if u == 1:
        link = input("Give a link : ")
        if youtube.download(link):
            print("\nSuccesfully Downloaded!\n")
            print("Saved at Current Directory!\n\n")
        else:
            print("Failed!")
    
    elif u == 2:
        console.print("WiZ Connected Device - CENTRAL CONTROL")
        wiz_menus = [
            'Discovery',
            'Exit'        
        ]
        
        wiz_running = True
        while wiz_running:
            for i in range(len(wiz_menus)):
                console.print("[{}] {}".format(i+1, wiz_menus[i]), style="bold")
            
            w = int(input(">>>> "))
            
            if w == 1:
                brd = input("Enter Broadcast Address : ")
                wiz.discover(brd)
            
            elif w == len(wiz_menus):
                wiz_running = False
        
            
        
    elif u == len(menus):
        cowsay.cow("Seey You, Love You!")
        running = False
        
    else:
        print("Invalid Input - Try Again!")









