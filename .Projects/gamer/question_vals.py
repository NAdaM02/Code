from PIL import ImageGrab
import pygetwindow as gw
import cv2
import os
import numpy as np
import pyautogui
from time import sleep as wait

dot = (os.path.dirname(__file__)).replace('\\','/')

with open( f'{dot}/Data/question_vals.txt', 'r') as question_vals_file:
    question_vals = list(map(float,question_vals_file.read().split(' | ')))

window = gw.getWindowsWithTitle("Firefox")[0]
window_rect = (window.left, window.top, window.right, window.bottom)

def saveQuestionVal(num):
    global window
    i = int(num)-1
    pyautogui.click(x=window.right-1, y=window.bottom-1)
    wait(0.1)
    pyautogui.moveTo(x=window.right+1, y=window.bottom+1)
    wait(0.1)
    screenshot = ImageGrab.grab(window_rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    val = np.average(screenshot)
    question_vals[i] = val
    print(val)

    with open( f'{dot}/Data/question_vals.txt', 'w') as question_vals_file:
        question_vals_file.write(' | '.join(list(map(str,question_vals))))
    print(" ".join(list(map(lambda x: "1" if x > 0 else "0" , question_vals))))

if __name__ == "__main__" :
    check = ""
    while check != "exit" :

        check = input('q_.png\n-> ')

        if check != "exit" :
            saveQuestionVal(check)
        