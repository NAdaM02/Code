from time import time as now
from time import sleep as wait
from colorama import init, Style
import os
import numpy as np
import cv2
from PIL import ImageGrab
from sys import stdout
import os
dot = (os.path.dirname(__file__)).replace('\\','/')
import keyboard





filler = ' '

#surround = ''

size_coherent = 15

"""width, height = 24 * size_coherent, 12 * size_coherent
#width, height = 20 * size_coherent, 10 * size_coherent
width, height = 30 * size_coherent, 15 * size_coherent"""

#x = 17
#x = 25
#x = 52

x = 19
#x = 28
#x = 56

width, height = x*16, x*9

move_speed = 1

#width, height = 1920, 1080






Opas10 = tuple(" -~+xrsd#$")
Opas16 = tuple(" .-:~+*rsd#$%&@█")
Opas17 = tuple(" .-:~+*=rsd#$%&@█")
Opas20 = tuple(" .-:~+*=rsdoO#$%&@▓█")
Opas32 = tuple(" .`',-:;il!><xrsahkmodbqwO0#$%@█")
Opas51 = tuple(" .`',-:;il!><xrsahkmoqwzvuyntjf0147235689bpdgq#$%&@█")
Opas64 = tuple(" .`',-~:;_\"^!/|\\(){}[]<>*il?1jtrxzcvunyfLITFJCoaesmkdqbphwO08#$%&@█")
Opas70 = tuple(" .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")
Opas92 = tuple(" `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@")

Opas = Opas92

#thresholds = np.linspace(0, 255, len(Opas) + 1)[1:-1]
thresholds = tuple(map(lambda x: x*255, (0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037)))

clear_display_height_str = str(height + 2)

Map = np.full((height, width), filler, dtype='<U1')

save_i = 0

os.system('cls')
init()

def clearDisplay():
    global clear_display_height_str
    stdout.write("\033[?25l")
    stdout.write("\033[" + clear_display_height_str + "A")
    stdout.write("\033[2K")

def saveDisplay():
    global Map, surround, save_i
    output = "\n" + (surround + " ") * (width + 2) + "\n"
    for row in Map:
        output += surround + " " + " ".join(row) + " " + surround + "\n"
    output += (surround + " ") * (width + 2)

    with open(f'{dot}/DisplayPics/display{save_i}.txt', 'w') as txt:
        txt.write(output)
        txt.close()
        print('\nSaved',save_i)
        save_i += 1

def fillMap(fill=filler):
    Map.fill(fill)

def flashScreen(speed=0.05):
    global Opas
    for char in Opas:
        fillMap(char)
        updateDisplay(speed)
    for char in reversed(Opas):
        fillMap(char)
        updateDisplay(speed)

def grayDownscale(screenshot, target_width, target_height):
    return cv2.resize(screenshot, (target_width, target_height), interpolation=cv2.INTER_AREA)

def monitorToMap():
    global Map, thresholds, width, height

    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    img = grayDownscale(screenshot, width, height)

    indices = np.digitize(img, thresholds)
    Map[:] = np.array(Opas)[indices]

def pressed_shift(event):
    monitorToMap()
    saveDisplay()

if __name__ == "__main__":
    try:
        os.makedirs(f'{dot}/DisplayPics')
    except:
        Exception("Error, directory not empty.")

    keyboard.on_press_key('shift', pressed_shift)
    keyboard.wait('left ctrl')

    
    """char = 'o'
    for i in range(4):
        for x in range(0, width, move_speed):
            #Map[move_height][max(0, x - move_speed)] = filler
            Map[10][x] = char
            updateDisplay(0.01*(i*(1/5)))
        for x in range(width - 1, -1, -move_speed):
            Map[10][min(x + move_speed, width - 1)] = filler
            #Map[move_height][x] = char
            updateDisplay(0.01*(i*(1/5)))
    wait(0.5)
    while True:
        flashScreen(speed=1/len(Opas)/2)"""
    """for i in range(2):
        flashScreen(speed=0.03)"""


print(Style.RESET_ALL)  # Reset terminal formatting
