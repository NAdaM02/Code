import pyautogui
import cv2
import csv
import numpy as np
from time import sleep as wait
import sys
import os
import screeninfo
from PIL import ImageGrab
import subprocess

Monitors = screeninfo.get_monitors()
selected_monitor = Monitors[0]


dot = (os.path.dirname(__file__)).replace('\\','/')


with open(f'{dot}/threshes.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    threshes = {}
    for row in reader:
        if row['img'] != '' and row['img'] != '.' and row['img'] != '...':
            try:
                threshes = threshes | {row['img']:float(row['thresh'])}
            except:
                threshes = threshes | {row['img']:0.0}


def findImageOnScreen(img_to_detect:str, threshold:float='', screen_index:int=0, memory:bool=False) :
    global last_val, selected_monitor

    img_to_detect_path = f'{dot}/Pics/{img_to_detect}.png'
    if threshold == '':
        threshold = threshes[img_to_detect]

    template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)
    template_height, template_width = template.shape[:2]

    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if memory == True:
        last_val = max_val
    if max_val >= threshold-0.001:
        center_x = max_loc[0] + selected_monitor.x + template_width // 2
        center_y = max_loc[1] + selected_monitor.y + template_height // 2
        return (center_x, center_y)
    else:
        return None


def findAndClick(name):
    item = findImageOnScreen(name)
    while not item:
        dropdown = findImageOnScreen(name)
    
    pyautogui.click(item)
    wait(0.3)

    print(f'{name} <')



if __name__ == "__main__" :
    subprocess.Popen(r'.\\msi_center.lnk', shell=True)

    while not findImageOnScreen('lines'): pass

    wait(0.5)

    print("Opened")

    findAndClick('dropdown')
    findAndClick('1')
    findAndClick('apply')
    print()

    while not findImageOnScreen('lines'): pass
    wait(0.2)

    findAndClick('dropdown')
    findAndClick('2')
    findAndClick('apply')
    print()

    while not findImageOnScreen('lines'): pass
    wait(0.2)

    findAndClick('exit')
