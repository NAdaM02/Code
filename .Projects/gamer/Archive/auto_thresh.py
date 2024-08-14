import cv2
import numpy as np
from time import sleep as wait
import random
import os
from PIL import ImageGrab
import csv
from main import question_num


dot = (os.path.dirname(__file__)).replace('\\','/')

file_path = f'{dot}/Data/threshes.csv'

with open(file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]


while input() == '':
    print('Start')
    
    for i in range( len(data) ):
        if data[i]['img'] != '' and data[i]['img'] != '.' and data[i]['img'] != '..' and data[i]['img'] != '...' and data[i]['img'][0] == 'q':
            try:
                img_to_detect_path = f'{dot}/Pics/{data[i]["img"]}.png'

                template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)

                screenshot = ImageGrab.grab()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                changed = False
                if data[i]['thresh'] == '' or max_val > float(data[i]['thresh']):
                    data[i]['thresh'] = max_val

                    img_to_detect_path = f'{dot}/Pics/{data[i+question_num]["img"]}.png'

                    template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)

                    screenshot = ImageGrab.grab()
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

                    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    data[i+question_num+1]['thresh'] = max_val

                    changed = True
            except:
                print("Err")
            print(data[i]["img"],':',(int(max_val*100)/100), "<-", data[i+question_num]["thresh"]) if changed else print(data[i]["img"],':',max_val)
        
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['img','thresh'])
        writer.writeheader()
        writer.writerows(data)

    print('Done\n')

