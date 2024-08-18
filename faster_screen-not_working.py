from time import time as now
from time import sleep as wait
from colorama import init, Style
import os
import numpy as np
import cv2
from PIL import ImageGrab
from sys import stdout
import cupy as cp






filler = ' '

#surround = ''

#x = 17
#x = 25
#x = 52

#x = 19
#x = 28
#x = 56

#width, height = x*16, x*9

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

OPAS = Opas92

#THRESHOLDS = np.linspace(0, 255, len(OPAS) + 1)[1:-1]
THRESHOLDS = tuple(map(lambda x: x*255, (0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037)))


OPAS_CP = cp.array(list(map(ord, OPAS)))
THRESHOLDS_GPU = cp.asarray(THRESHOLDS)



def clear_display():
    global height
    stdout.write("\033[?25l")
    stdout.write("\033[" + clear_display_height_str + "A")
    stdout.write("\033[2K")

"""def print_display():
    global Map, surround
    output = "\n" + (surround + " ") * (width + 2) + "\n"
    for row in Map:
        output += surround + " " + " ".join(row) + " " + surround + "\n"
    output += (surround + " ") * (width + 2)
    clear_display()
    stdout.write(output)
    stdout.flush()"""
def print_display():
    global Map, surround
    output = "\n"
    for row in Map:
        output += " ".join(row) + "\n"
    clear_display()
    stdout.write(output)
    stdout.flush()

def update_display(stay=0):
    print_display()
    if stay != 0:
        wait(stay)

def fill_map(fill=filler):
    Map.fill(fill)

def flash_screen(speed=0.05):
    global OPAS
    for char in OPAS:
        fill_map(char)
        update_display(speed)
    for char in reversed(OPAS):
        fill_map(char)
        update_display(speed)

def gray_downscale(screenshot, target_width, target_height):
    screenshot_cp = cp.asarray(screenshot)
    screenshot_resized_cp = cp.empty((target_height, target_width), dtype=cp.uint8)
    
    screenshot_gray = cp.dot(screenshot_cp[...,:3], cp.array([0.2989, 0.5870, 0.1140]))
    screenshot_resized_cp = cp.resize(screenshot_gray, (target_height, target_width))
    
    screenshot_resized = cp.asnumpy(screenshot_resized_cp)
    
    return screenshot_resized

def monitor_to_map():
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    img = gray_downscale(screenshot, width, height)

    img_gpu = cp.asarray(img)

    indices = cp.digitize(img_gpu, THRESHOLDS_GPU)
    result_gpu = OPAS_CP[indices]

    return result_gpu.get()

if __name__ == "__main__":

    os.system('cls')
    inp = input('input size coherent [11,14,19,28,56]:  ')
    x = int(inp) if inp != '' else 19
    width, height = x*16, x*9

    Map = np.full((height, width), filler, dtype='<U1')
    clear_display_height_str = str(height + 2)

    os.system('cls')
    init()
    while True:
        monitor_to_map()
        update_display()
    
    """char = 'o'
    for i in range(4):
        for x in range(0, width, move_speed):
            #Map[move_height][max(0, x - move_speed)] = filler
            Map[10][x] = char
            update_display(0.01*(i*(1/5)))
        for x in range(width - 1, -1, -move_speed):
            Map[10][min(x + move_speed, width - 1)] = filler
            #Map[move_height][x] = char
            update_display(0.01*(i*(1/5)))
    wait(0.5)
    while True:
        flash_screen(speed=1/len(OPAS)/2)"""
    """for i in range(2):
        flash_screen(speed=0.03)"""


print(Style.RESET_ALL)  # Reset terminal formatting

