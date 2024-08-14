import cv2
import numpy as np
from time import sleep as wait
import random
import os
from PIL import ImageGrab
import csv
from main import question_num
import pygetwindow as gw
import keyboard

window = gw.getWindowsWithTitle("Firefox")[0]
window_rect = (window.left, window.top, window.right, window.bottom)
window_center = ( (window.left + window.right)/2, (window.top + window.bottom)/2 )

dot = (os.path.dirname(__file__)).replace('\\','/')

csv_path = f'{dot}/Data/threshes.csv'

with open(csv_path, 'r', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

done = []

finished = False

def pressed_enter(event):
    global finished
    if event.event_type == keyboard.KEY_DOWN:
        finished = True

def Thresh(event):
    if event.event_type == keyboard.KEY_DOWN:
        print('Start')
        max_v, max_i = 0, 0
        for i in range( len(data) ):
            if data[i]['img'] != '' and data[i]['img'] != '.' and data[i]['img'] != '..' and data[i]['img'] != '...' and data[i]['img'][0] == 'q':
                try:
                    img_to_detect_path = f'{dot}/Pics/{data[i]["img"]}.png'

                    template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)

                    screenshot = ImageGrab.grab(window_rect)
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

                    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                    if max_val > max_v:
                        max_v = max_val
                        max_i = i
                except:
                    print("Err  ",end="")
            
                print(data[i]["img"],':',round(max_val,2))

        changed = False

        if data[max_i]['thresh'] == '' or max_v > float(data[max_i]['thresh']):
            data[max_i]['thresh'] = max_v

            img_to_detect_path = f'{dot}/Pics/{data[max_i+question_num+1]["img"]}.png'

            template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)

            screenshot = ImageGrab.grab(window_rect)
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            data[max_i+question_num+1]['thresh'] = max_val

            changed = True
        
        print()
        print(data[max_i]["img"],':',round(max_v,3), "<-", data[max_i+question_num+1]["img"], round(data[max_i+question_num+1]["thresh"],2)) if changed else print(data[max_i]["img"],':',max_v, 'x')

        if max_i not in done :
            done.append(max_i)
        if len(done) == question_num:
            print("\nProbably finished")

        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['img','thresh'])
            writer.writeheader()
            writer.writerows(data)

        print('Done\n')


keyboard.on_press_key('shift', Thresh)
keyboard.on_press_key('enter', pressed_enter)

while not finished:
    wait(0.5)

print("\n\nDone")
