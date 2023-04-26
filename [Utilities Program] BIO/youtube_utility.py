# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 11:17:09 2022

YOUTUBE - CENTRAL CONTROL
@author: Erwin
"""

from pytube import YouTube

def download(link):
    
    yt = YouTube(link)
    
    # Title of video
    print("Title: \n {} \n".format(yt.title))
    
    # Number of views of video
    print("Number of views : \n {} \n".format(yt.views))
    
    # Length of the video
    print("Length of video : \n {} seconds \n".format(yt.length))
    
    # Rating
    print("Ratings : \n {} \n".format(yt.rating))
    
    # Video Stream
    print("Video Stream : \n ")
    
    index = 0
    videos = yt.streams.filter(progressive=True, file_extension='mp4')
    for i in videos:
        print("{} - {}".format(index, i))
        index += 1
        
    # Audio Stream
    print("\nAudio Stream : \n ")
    
    index = 0
    audios = yt.streams.filter(only_audio=True, file_extension='mp4')
    for i in audios:
        print("{} - {}".format(index, i))
        index += 1
    
    print("Example. V0 (video index 0), A1 (audio index 1)\n")
    u = input("\nWhich One?: ")
    
    if u[0] == 'V':
        videos[int(u[1])].download()
        return 1
    elif u[0] == 'A':
        audios[int(u[1])].download()
        return 1
    else:
        print("\nInvalid Command!\n")
        return 0