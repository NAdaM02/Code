from time import time as now
from time import sleep as wait_seconds
import colorama
import os
import numpy as np
import cv2
from PIL.ImageGrab import grab as take_screenshot
from sys import stdout
from PIL import Image



class DisplayMap:
    def __init__(self, width, height, d_list=None, filler=' '): 
        if d_list:
            self.width = len(ls[0])
            self.height = len(ls)
            self.val = np.array(d_list, dtype='<U1')
        else:
            self.width = width
            self.height = height
            self.val = np.full(((self.height, self.width)), filler, dtype='<U1')

        self.filler = filler
        
    def fill(self, fill='??'):
        if fill == '??':
            filler = self.filler
        else:
            filler = fill

        self.val = np.full(((self.height, self.width)), filler, dtype='<U1')
        return self.val


class TerminalDisplay:
    def __init__(self, height=512):
        self.height = height
        self.clear_height = height+2
        self.clear_height_str = str(height+2)

    def to_beginning(self):
        stdout.write("\033[?25l")
        stdout.write("\033[" + self.clear_height_str + "A")
        stdout.write("\033[2K")
        #stdout.write("\033[2J")
    
    def clear(self):
        os.system('cls')
    
    def write(self, display_map:DisplayMap):
        output = "\n"
        for row in display_map.val:
            output += " ".join(row) + "\n"
        self.to_beginning()
        stdout.write(output)
        stdout.flush()
    
    def update(self, display_map:DisplayMap, stay_seconds=0):
        self.write(display_map)
        if stay_seconds != 0:
            wait_seconds(stay_seconds)


class Custom_Image:
    def __init__(self, image_array=np.array([])):
        self.array = image_array

    def gray(self):
        self.array = cv2.cvtColor(np.array(self.array), cv2.COLOR_RGB2GRAY)
        return self

    def downscale(self, target_width, target_height):
        self.array = cv2.resize(self.array, (target_width, target_height), interpolation=cv2.INTER_AREA)
        return self

    def be_screenshot(self):
        self.array = np.array(take_screenshot())
        return self
    
    def save_as_img(self, name:str='image'):
        image = Image.fromarray(self.array)
        return image.save(f'{name}.png')
    
    def save_as_text(self, name:str='text'):
        return np.savetxt(f'{name}.txt', self.array, fmt='%f', delimiter=' | ')


class Monitor:
    def __init__(self):
        pass

    def to_map(target_width, target_height):
        img = Custom_Image(screenshot)
        img.be_screenshot()

        img.gray()
        img.downscale(target_width, target_height)

        indices = np.digitize(img.array, THRESHOLDS)
        monitor_display_map = DisplayMap(width=target_width, height=target_height)
        monitor_display_map.val[:] = np.array(OPAS)[indices]
        
        return monitor_display_map








def flashScreen(display_map:DisplayMap, terminal_display:TerminalDisplay, speed = 0.02):
    global OPAS
    for char in OPAS:
        display_map.fill(char)
        terminal_display.update(display_map, stay_seconds=speed)
    for char in reversed(OPAS):
        display_map.fill(char)
        terminal_display.update(display_map, stay_seconds=speed)

def moveCharacterAcrossDisplay(display_map:DisplayMap, terminal_display, move_height=""):
    if move_height=='' :
        move_height = display_map.height // 2
    move_speed = 1
    char = 'o'
    for i in range(4):
        for x in range(0, width, move_speed):
            display_map.val[move_height][max(0, x - move_speed)] = display_map.filler
            display_map.val[10][x] = char
            (0.01*(i*(1/5)))
        for x in range(width - 1, -1, -move_speed):
            display_map.val[10][min(x + move_speed, width - 1)] = display_map.filler
            #display_map[move_height][x] = char
            terminal_display.update(display_map, stay_seconds=0.01*(i*(1/5)))


def get_terminal_display_size():
    inp = input('input size coherent [11,14,19,28,56] or size:  ')
    if ('x' not in inp) and ('*' not in inp):
        x = int(inp) if inp != '' else 19
        width, height = x*16, x*9
    else:
        width, height = inp.split('x').split('*')
        int(height); int(width)
    
    return height, width



if False:
    OPAS10 = tuple(" -~+xrsd#$")
    OPAS16 = tuple(" .-:~+*rsd#$%&@█")
    OPAS17 = tuple(" .-:~+*=rsd#$%&@█")
    OPAS20 = tuple(" .-:~+*=rsdoO#$%&@▓█")
    OPAS32 = tuple(" .`',-:;il!><xrsahkmodbqwO0#$%@█")
    OPAS51 = tuple(" .`',-:;il!><xrsahkmoqwzvuyntjf0147235689bpdgq#$%&@█")
    OPAS64 = tuple(" .`',-~:;_\"^!/|\\(){}[]<>*il?1jtrxzcvunyfLITFJCoaesmkdqbphwO08#$%&@█")
    OPAS70 = tuple(" .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")

OPAS92 = tuple(" `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@")

OPAS = OPAS92

#THRESHOLDS = np.linspace(0, 255, len(OPAS) + 1)[1:-1]
THRESHOLDS = tuple(map(lambda x: x*255, (0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037)))



if __name__ == "__main__":

    os.system('cls')

    height, width = get_terminal_display_size()

    display_map = DisplayMap(width, height)

    terminal_display = TerminalDisplay(height)

    monitor = Monitor



    colorama.init() # Initialize terminal formatting


    while True:
        display_map = monitor.to_map(width, height)
        terminal_display.update(display_map)

    terminal_display.clear()

    print(colorama.Style.RESET_ALL)  # Reset terminal formatting
