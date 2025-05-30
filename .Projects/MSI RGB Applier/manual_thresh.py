import cv2
import numpy as np
from time import sleep as wait
import os
from PIL import ImageGrab
import csv

dot = (os.path.dirname(__file__)).replace('\\','/')

csv_path = f'{dot}/threshes.csv'

with open(csv_path, 'r', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

last_val = 0

def saveThreshold(img_to_detect:str, threshold:float=0.78) :
    global dot, last_val, threshes_df, data
    img_to_detect_path = f'{dot}/Pics/{img_to_detect}.png'

    try:
        template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)
        template_height, template_width = template.shape[:2]

        screenshot = ImageGrab.grab()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        last_val = max_val
    except:
        max_val = ''
        print("Cannot find image path.")
    
    already_had_img = False
    for row in data:
        if row['img'] == img_to_detect:
            already_had_img = True
            row['thresh'] = max_val
            break
    if not already_had_img:
        data.append( {'img': img_to_detect, 'thresh': max_val} )

    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['img','thresh'])
        writer.writeheader()
        writer.writerows(data)

import keyboard

def waitForShift(event):
    global pressed_shift
    if event.event_type == keyboard.KEY_DOWN:
        pressed_shift=True

if __name__ == "__main__" :
    check = ""
    while check != "exit()" :

        check = input('___.png\n-> ')

        if check != "exit()" :
            pressed_shift = False
            keyboard.on_press_key('shift', waitForShift)

            while not pressed_shift: pass

            keyboard.unhook_key('shift')

            saveThreshold(check)

            print(last_val)
