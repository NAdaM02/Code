from time import time as now
from time import sleep as wait_seconds
import colorama
import os
import numpy as np
import cv2
from PIL.ImageGrab import grab as take_screenshot
from sys import stdout
from PIL import Image
        


if __name__ == '__main__' :
    os.system('mkdir New_Data')

    for i in range(108):
        img = Image.open(f'./.Projects/screener/Data/Characters/{i}.png')

        img_array = np.array(img)

        mask = img_array == 0
        alpha = np.uint8(np.invert(mask) * 255)
        img_array = np.dstack([img_array, alpha])

        edited_img = Image.fromarray(img_array, mode="LA")
        
        edited_img.save(f'./New_Data/{i}.png')
