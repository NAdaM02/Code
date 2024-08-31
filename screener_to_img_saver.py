from time import time as now
from time import sleep as wait_seconds
import colorama
import os
import numpy as np
import cv2
from PIL.ImageGrab import grab as take_screenshot
from sys import stdout
from PIL import Image


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
        self.array = np.array(take_screenshot(bbox=(320,39,398,194)))
        return self
    
    def save_as_img(self, name:str='image'):
        image = Image.fromarray(self.array)
        return image.save(f'./Data/{name}.png')
    
    def save_as_text(self, name:str='text'):
        return np.savetxt(f'./Data/{name}.txt', self.array, fmt='%f', delimiter=' | ')


if __name__ == '__main__' :
    os.system('mkdir Data')


    char_list = tuple(" `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@")

    for i in range(len(char_list)):
        os.system('cls')
        print(f"██ █{char_list[i]}")
        wait_seconds(0.1)

        img = Custom_Image()

        img.be_screenshot()

        img.gray()

        img.save_as_img(f"image{i}")
        img.save_as_text(f"text{i}")
