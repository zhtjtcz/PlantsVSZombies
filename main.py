'''
Plants VS Zombies

Marvolo

18377221

2020.08.25 -- 2020.09.09
'''

import pygame
import os
from Map import *
import sys
import time
import threading
import psutil
import subprocess
from multiprocessing import Process
from PIL import Image, ImageTk

menu=Menu()
mode=menu.Run()

while 1:
	game=GameControl(mode)
	plantlist=game.Select()
	if (len(plantlist)==0):
		break
	game.Run(plantlist)