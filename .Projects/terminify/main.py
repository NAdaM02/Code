from time import time as epoch_now
from time import perf_counter as precise_time
from time import sleep as wait
from time import sleep as wait_seconds
import time
import os
import numpy as np
import cv2
from PIL.ImageGrab import grab as take_screenshot
from sys import stdout
from PIL import Image
import asyncio
import colorama
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from io import BytesIO
from colorama import Fore
from spotipy.exceptions import SpotifyException
from scipy.spatial.distance import cdist

import sys

import logging
logging.getLogger().setLevel(logging.ERROR)


TIME_CONVERT_LIST = (29030400, 604800, 86400, 3600, 60, 1)
TIME_CHAR_LIST = ('y', 'w', 'd', 'h', 'm', 's')

def secs_to_text(seconds:float) :
    seconds = int(seconds)
    text = ""
    for i in range(6):
        conv = TIME_CONVERT_LIST[i]
        if conv <= seconds:
            un = seconds//conv
            seconds -= un*conv
            text += str(un) + TIME_CHAR_LIST[i] + " "
    text = f'{text}\b'
    return text

def secs_to_units(seconds:float) :
    seconds = int(seconds)
    units = [0 for i in range(6)]
    for i in range(3):
        conv = TIME_CONVERT_LIST[3+i]
        if conv <= seconds:
            un = seconds//conv
            seconds -= un*conv
            s = un%10
            units[i*2+1] = s
            if un != s:
                units[i*2] = (un-s)//10
    return units

DOT = (os.path.dirname(__file__)).replace('\\','/')

OPAS = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")

THRESHOLDS = (19.92, 36.93, 39.75, 39.84, 42.89, 53.66, 54.4, 62.83, 69.53, 74.17, 105.29, 106.47, 108.4, 109.08, 111.08, 116.27, 117.73, 123.66, 125.45, 125.71, 128.68, 130.03, 131.86, 132.5, 135.4, 137.24, 137.5, 142.01, 142.56, 142.75, 143.7, 146.49, 146.71, 147.49, 148.18, 149.43, 149.48, 153.02, 153.36, 155.5, 156.51, 157.07, 157.39, 157.42, 157.54, 157.6, 157.9, 162.86, 163.27, 165.91, 166.07, 167.35, 167.53, 169.5, 170.98, 172.68, 174.85, 181.89, 182.69, 185.28, 185.88, 186.98, 188.07, 188.71, 194.11, 194.94, 195.06, 195.96, 196.18, 196.41, 196.81, 197.21, 197.27, 198.77, 200.79, 203.01, 204.88, 210.01, 212.57, 215.11, 218.92, 219.69, 221.34, 223.96, 232.33, 232.41, 232.83, 233.37, 240.17, 243.34, 255.0)

CHAR_WIDTH_PER_HEIGHT = 117/232

CHARACTER_SHAPES = (
    ((9.2, 246.45, 0.36), (0.0, 15.92, 1.84), (0.0, 0.0, 0.0)),
    ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 146.16, 0.0)),
    ((0.0, 0.0, 0.0), (121.82, 161.49, 122.78), (0.0, 0.0, 0.0)),
    ((0.0, 151.87, 0.0), (0.0, 143.26, 0.0), (0.0, 0.0, 0.0)),
    ((0.0, 0.0, 0.0), (0.0, 148.64, 0.0), (0.0, 145.96, 0.0)),
    ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (118.91, 157.64, 119.83)),
    ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 314.2, 0.0)),
    ((12.7, 224.55, 13.54), (82.08, 97.76, 83.54), (0.0, 0.0, 0.0)),
    ((0.0, 0.0, 0.0), (243.37, 322.61, 245.28), (0.0, 0.0, 0.0)),
    ((0.0, 0.0, 0.0), (0.0, 148.52, 0.0), (0.0, 314.19, 0.0)),
    ((26.35, 0.0, 0.0), (183.28, 355.89, 212.25), (28.8, 0.0, 0.0)),
    ((0.0, 0.0, 26.04), (205.27, 339.49, 181.82), (0.0, 0.0, 28.37)),
    ((0.0, 56.04, 0.0), (121.94, 434.58, 122.89), (0.0, 58.25, 0.0)),
    ((0.0, 142.66, 0.0), (0.0, 259.75, 0.0), (0.0, 146.03, 0.0)),
    ((0.0, 0.0, 0.0), (213.4, 294.99, 205.79), (149.89, 189.54, 0.0)),
    ((0.0, 0.0, 0.0), (292.51, 176.27, 127.7), (87.63, 177.65, 94.9)),
    ((0.0, 32.66, 0.0), (181.48, 448.31, 183.35), (7.17, 1.02, 7.29)),
    ((0.0, 27.57, 205.16), (8.76, 325.21, 27.76), (174.45, 56.14, 0.0)),
    ((0.0, 0.0, 0.0), (114.68, 388.89, 146.66), (142.24, 180.73, 95.6)),
    ((115.79, 178.18, 99.57), (1.81, 223.96, 111.66), (0.0, 146.75, 0.0)),
    ((0.0, 0.0, 0.0), (200.64, 340.5, 187.72), (97.49, 164.93, 120.92)),
    ((141.99, 0.0, 0.0), (354.36, 0.0, 0.0), (153.27, 161.6, 122.99)),
    ((132.08, 219.56, 133.17), (0.0, 354.87, 0.0), (0.0, 141.04, 0.0)),
    ((0.0, 0.0, 0.0), (271.61, 143.52, 273.5), (9.09, 230.46, 9.73)),
    ((79.32, 230.21, 22.77), (0.0, 157.31, 203.41), (78.39, 228.11, 22.13)),
    ((0.0, 127.84, 164.43), (73.54, 0.0, 354.94), (126.97, 163.48, 101.78)),
    ((175.23, 164.46, 194.53), (85.01, 198.7, 190.97), (0.0, 154.96, 0.0)),
    ((21.78, 229.87, 80.33), (199.77, 160.49, 0.0), (21.13, 227.67, 79.27)),
    ((0.0, 282.01, 0.0), (0.0, 355.97, 0.0), (0.0, 280.77, 0.0)),
    ((146.51, 164.26, 133.25), (359.35, 164.61, 59.0), (141.14, 0.0, 0.0)),
    ((0.0, 146.15, 2.28), (73.62, 406.6, 0.0), (95.34, 216.23, 120.51)),
    ((0.0, 252.76, 69.87), (57.29, 386.48, 0.0), (0.0, 253.06, 68.84)),
    ((81.12, 175.41, 138.92), (378.41, 0.32, 0.0), (85.75, 176.77, 116.29)),
    ((69.11, 253.45, 0.0), (0.0, 385.16, 58.54), (68.13, 254.27, 0.0)),
    ((0.0, 200.11, 129.53), (135.12, 434.79, 101.69), (0.0, 143.14, 0.0)),
    ((96.0, 219.73, 96.76), (0.0, 355.92, 0.0), (94.45, 217.33, 95.2)),
    ((106.64, 172.18, 108.33), (9.62, 195.48, 256.12), (97.52, 166.19, 102.68)),
    ((92.58, 197.85, 0.0), (0.35, 356.42, 0.0), (93.74, 217.35, 103.29)),
    ((38.02, 88.53, 0.0), (216.0, 353.96, 94.49), (14.83, 195.76, 105.72)),
    ((122.97, 184.7, 0.0), (0.0, 358.25, 0.0), (0.0, 188.76, 106.37)),
    ((0.0, 0.0, 0.0), (338.91, 17.49, 324.65), (127.21, 149.57, 196.44)),
    ((32.98, 295.25, 82.78), (49.03, 306.97, 0.0), (32.68, 292.54, 81.89)),
    ((0.0, 0.0, 0.0), (343.76, 165.91, 310.29), (143.55, 0.0, 143.57)),
    ((0.0, 0.0, 0.0), (314.37, 314.31, 251.41), (93.04, 170.07, 77.21)),
    ((0.0, 0.0, 0.0), (304.73, 183.13, 306.3), (99.62, 180.66, 100.99)),
    ((103.5, 171.6, 159.64), (48.24, 301.93, 49.94), (156.44, 169.05, 110.64)),
    ((112.57, 174.22, 83.44), (196.95, 177.83, 256.37), (115.6, 166.08, 121.97)),
    ((147.31, 0.0, 147.42), (93.71, 381.18, 95.15), (0.0, 141.12, 0.0)),
    ((0.0, 0.0, 0.0), (135.04, 396.15, 133.46), (116.57, 84.51, 118.12)),
    ((0.0, 98.22, 50.01), (55.67, 306.91, 143.23), (91.83, 302.23, 91.82)),
    ((0.0, 0.0, 0.0), (273.07, 125.44, 284.62), (144.45, 404.74, 22.51)),
    ((0.0, 0.0, 0.0), (194.09, 337.25, 222.76), (149.58, 140.1, 189.13)),
    ((81.81, 293.91, 34.7), (0.0, 303.85, 51.62), (80.93, 291.21, 34.41)),
    ((118.18, 173.61, 93.31), (8.13, 190.84, 203.74), (152.24, 194.2, 113.1)),
    ((154.63, 164.26, 125.01), (366.98, 164.06, 50.48), (153.27, 161.6, 122.99)),
    ((105.71, 169.41, 99.07), (150.37, 206.65, 162.71), (112.26, 161.5, 116.47)),
    ((0.0, 0.0, 0.0), (308.6, 378.47, 313.41), (141.74, 125.78, 126.02)),
    ((0.0, 0.0, 0.0), (322.79, 152.33, 342.28), (128.18, 147.14, 356.14)),
    ((182.44, 0.0, 0.0), (373.49, 229.74, 249.68), (144.42, 21.11, 154.15)),
    ((154.46, 166.4, 122.55), (366.9, 166.5, 280.66), (140.83, 0.0, 0.0)),
    ((23.41, 172.31, 73.27), (367.11, 170.75, 252.47), (114.58, 168.11, 119.82)),
    ((181.15, 0.0, 0.0), (367.78, 158.5, 310.16), (143.41, 0.0, 143.43)),
    ((107.51, 169.68, 114.2), (254.76, 164.63, 376.95), (67.45, 175.64, 32.23)),
    ((0.0, 0.0, 181.11), (324.52, 154.12, 371.54), (130.12, 152.26, 147.31)),
    ((75.2, 49.24, 127.68), (392.08, 199.3, 372.6), (0.0, 14.04, 126.64)),
    ((144.75, 0.0, 144.76), (250.69, 187.88, 252.93), (7.61, 235.89, 8.32)),
    ((0.0, 0.0, 0.0), (347.85, 156.83, 325.68), (356.24, 151.9, 131.24)),
    ((109.78, 172.04, 110.76), (368.24, 0.0, 368.43), (111.88, 169.2, 112.93)),
    ((93.57, 171.62, 129.89), (376.59, 78.91, 207.66), (100.52, 170.6, 164.61)),
    ((181.18, 0.0, 0.0), (368.5, 158.05, 325.87), (157.32, 160.45, 86.76)),
    ((141.69, 0.0, 142.43), (354.15, 0.0, 354.38), (111.19, 173.1, 110.41)),
    ((5.01, 231.47, 5.43), (250.13, 353.43, 253.17), (140.3, 0.0, 140.31)),
    ((141.81, 0.0, 140.58), (371.32, 265.92, 219.42), (140.65, 4.14, 158.88)),
    ((142.54, 20.09, 142.93), (70.82, 487.91, 72.8), (139.75, 22.52, 140.57)),
    ((141.69, 0.0, 142.67), (374.8, 165.53, 377.36), (140.54, 0.0, 141.51)),
    ((0.0, 0.0, 0.0), (354.73, 349.75, 361.41), (143.43, 123.06, 144.87)),
    ((114.89, 171.66, 115.88), (295.98, 197.49, 297.37), (124.01, 164.45, 124.79)),
    ((162.54, 167.11, 119.27), (374.66, 217.61, 295.9), (140.54, 5.33, 154.13)),
    ((162.47, 174.0, 88.41), (353.62, 0.0, 372.21), (161.19, 170.41, 93.56)),
    ((40.13, 96.11, 105.08), (322.6, 428.49, 326.77), (102.71, 95.09, 41.22)),
    ((105.75, 303.86, 99.35), (150.37, 372.58, 162.73), (112.63, 296.14, 116.84)),
    ((154.46, 170.67, 100.67), (366.9, 173.03, 305.02), (153.26, 163.47, 149.51)),
    ((0.0, 0.0, 0.0), (324.65, 157.1, 347.19), (223.11, 329.87, 284.65)),
    ((93.8, 179.68, 95.14), (366.59, 156.06, 365.96), (95.96, 176.56, 97.18)),
    ((179.7, 105.66, 180.87), (342.96, 300.89, 345.29), (134.8, 0.0, 135.57)),
    ((170.54, 51.81, 142.24), (360.13, 280.92, 359.05), (141.51, 50.96, 170.1)),
    ((141.61, 0.0, 141.61), (337.71, 403.03, 337.82), (147.39, 146.33, 148.77)),
    ((109.78, 172.04, 110.76), (368.32, 0.0, 368.25), (111.99, 347.85, 200.46)),
    ((154.52, 132.67, 0.0), (259.87, 410.84, 270.21), (0.43, 123.8, 162.2)),
    ((85.36, 187.22, 89.1), (315.45, 268.92, 200.51), (157.23, 176.94, 171.74)),
    ((82.65, 165.65, 105.93), (292.41, 372.71, 342.46), (164.06, 263.04, 109.96)),
)


def print_separate(val_1:any, space_between:str, val_2:any):
    val_1_string = str(val_1)
    val_1_len = len(val_1_string)

    val_2_string = str(val_2)

    stdout.write(val_1_string + space_between[val_1_len : ] + val_2_string)

def highlight(var:any, for_seconds:float= 10):
    os.system('cls')
    print()
    print(var)
    print()
    wait_seconds(for_seconds)


class CharacterMap:
    def __init__(self, width:int, height:int, d_list:tuple= None, filler:str= ' ', U1dtype:bool= True): 
        if d_list:
            self.width = len(d_list[0])
            self.height = len(d_list)
            if U1dtype:
                self.array = np.array(d_list, dtype='<U1')
            else:
                self.array = np.array(d_list, dtype=np.object_)
        else:
            self.width = width
            self.height = height
            if U1dtype:
                self.array = np.full(((height, width)), filler, dtype='<U1')
            else:
                self.array = np.full(((height, width)), filler, dtype=np.object_)

        self.filler = filler
    
    def get(self):
        return self.array
        
    def fill(self, fill='??'):
        if fill == '??':
            filler = self.filler
        else:
            filler = fill

        self.array = np.full(((self.height, self.width)), filler, dtype='<U1')
        return self.array
    
    def get_subarray(self, first_rows:int= None, last_rows:int= None, first_columns:int= None, last_columns:int= None):
        if first_rows is None:
            first_rows = 0
        if last_rows is None:
            last_rows = self.array.shape[0] - 1
        if first_columns is None:
            first_columns = 0
        if last_columns is None:
            last_columns = self.array.shape[1] - 1

        if first_rows < 0 or last_rows >= self.array.shape[0] or first_columns < 0 or last_columns >= self.array.shape[1]:
            raise IndexError("Indices are out of bounds.")

        return self.array[first_rows:last_rows+1, first_columns:last_columns+1]

    def add_map_array(self, position:tuple= ('row','col'), added_array:np.array= (), exclude_chars:tuple= ()):
        height, width = self.array.shape
        added_height, added_width = added_array.shape
        row, col = position

        start_row, end_row = max(0, row), min(height, row + added_height)
        start_col, end_col = max(0, col), min(width, col + added_width)

        local_start_row, local_end_row = max(0, -row), min(added_height, height - row)
        local_start_col, local_end_col = max(0, -col), min(added_width, width - col)

        target_region = self.array[start_row:end_row, start_col:end_col]
        source_region = added_array[local_start_row:local_end_row, local_start_col:local_end_col]

        if self.array.dtype != np.object_:
            self.array = self.array.astype(np.object_)

        if exclude_chars:
            for i in range(target_region.shape[0]):
                for j in range(target_region.shape[1]):
                    if source_region[i, j] not in exclude_chars:
                        target_region[i, j] = source_region[i, j]
        else:
            self.array[start_row:end_row, start_col:end_col] = source_region

        return self.array
    
    def replace(self, replace_what:str= ',', replace_with:str= ' '):
        self.array[self.array == replace_what] = replace_with
        
        return self.array

    def render_char(self, char_width:int, char_height:int, char_col:int, char_row:int):
        shown = (0-char_width <= char_col <= self.width) and (0-char_height <= char_row <= self.height)
        if shown:
            self.add_map_array((char_col, char_row), self.array, exclude_chars=(" "))
        
        return shown


class TerminalDisplay:
    def __init__(self, height:int= 512):
        self.height = height
        self.clear_height = height+2
        self.clear_height_str = str(height+2)

    def to_beginning(self):
        stdout.write("\033[?25l")
        stdout.write("\033[" + self.clear_height_str + "A")
        stdout.write("\033[2K")
    
    def clear(self):
        os.system('cls')
    
    def write(self, display_map:CharacterMap):
        output = "\n" + "\n".join((" ".join(row) for row in display_map.array)) + Fore.WHITE
        self.to_beginning()
        stdout.write(output)
        stdout.flush()

    def update(self, display_map:CharacterMap, fps:float= 0):
        global GLOBAL_last_frame_time
        
        if fps == 0:
            self.write(display_map)
        else:
            stay_seconds = int(10000/fps)/10000

            self.write(display_map)

            while (precise_time() - GLOBAL_last_frame_time)< stay_seconds :
                pass

            GLOBAL_last_frame_time = precise_time()


class CustomImage:
    def __init__(self, image_array:np.array= ()):
        self.array = np.array(image_array)

    def gray(self):
        lookup_table = np.array([(i / 255.0) ** 1.5 * 255 for i in range(256)], dtype=np.uint8)
        self.array = cv2.LUT(cv2.cvtColor(self.array, cv2.COLOR_RGB2GRAY), lookup_table)

        return self.array

    def downscale(self, target_width:int, target_height:int, method=cv2.INTER_LINEAR_EXACT):
        self.array = cv2.resize(self.array, (target_width, target_height), interpolation=method)

        return self

    def be_screenshot(self):
        self.array = np.array(take_screenshot())
        return self
    
    def save_as_img(self, name:str= 'image'):
        image = Image.fromarray(self.array)
        return image.save(f'{name}.png')
    
    def save_as_text(self, name:str= 'text'):
        return np.savetxt(f'{name}.txt', self.array, fmt='%f', delimiter=' ')
    
    def to_map(self, target_width:int= -1, target_height:int= -1, grayed:bool= False, sized:bool= False):
        if not grayed: self.gray()
        if not sized: self.downscale(target_width, target_height)

        indices = np.digitize(self.array, THRESHOLDS)
        img_map = CharacterMap(target_width, target_height)
        img_map.array[:] = np.array(OPAS)[indices]
        
        return img_map
    
    def to_color_map(self, target_width:int= -1, target_height:int= -1):
        self.downscale(target_width, target_height)

        color_map = CharacterMap(target_width, target_height, U1dtype=False)

        for y in range(target_height):
            for x in range(target_width):
                r, g, b = self.array[y, x].astype(np.int32)

                luminance = 0.299 * r + 0.587 * g + 0.114 * b  

                char_index = np.digitize(luminance, THRESHOLDS, right=True)
                char_index = max(0, min(char_index, len(OPAS) - 1))
                char = OPAS[char_index]

                color_map.array[y, x] = f"\033[38;2;{r};{g};{b}m{char}"

        return color_map

    def to_shape_map(self, target_width:int= -1, target_height:int= -1, grayed:bool= False):
        if not grayed: self.gray()
        
        self.downscale(target_width * 3, target_height * 3)
        
        height, width = self.array.shape
        grid_rows = height // 3
        grid_cols = width // 3
        
        reshaped_shapes = np.array(CHARACTER_SHAPES).reshape(len(CHARACTER_SHAPES), -1)
        
        grids = np.lib.stride_tricks.as_strided(
            self.array,
            shape=(grid_rows, grid_cols, 3, 3),
            strides=(self.array.strides[0] * 3, self.array.strides[1] * 3, *self.array.strides)
        )
        
        flattened_grids = grids.reshape(grid_rows * grid_cols, -1)
        distances = cdist(flattened_grids, reshaped_shapes, metric='euclidean')
        output_indices = np.argmin(distances, axis=1).reshape(grid_rows, grid_cols)
        
        img_map = CharacterMap(width=target_width, height=target_height)
        
        row_indices = (np.arange(target_height) * (grid_rows / target_height)).astype(int)
        col_indices = (np.arange(target_width) * (grid_cols / target_width)).astype(int)
        
        indices_map = output_indices[row_indices[:, None], col_indices]
        img_map.array = np.array(OPAS)[indices_map]
        
        return img_map

    def to_color_shape_map(self, target_width:int= -1, target_height:int= -1, downscale_method:int= cv2.INTER_LINEAR_EXACT):

        self.downscale(target_width * 3, target_height * 3, downscale_method)

        height, width, _ = self.array.shape
        grid_rows = height // 3
        grid_cols = width // 3

        reshaped_shapes = np.array(CHARACTER_SHAPES).reshape(len(CHARACTER_SHAPES), -1)

        grids = np.lib.stride_tricks.as_strided(
            self.array,
            shape=(grid_rows, grid_cols, 3, 3, 3),
            strides=(self.array.strides[0] * 3, self.array.strides[1] * 3, *self.array.strides)
        )

        grid_colors = np.mean(grids, axis=(2, 3)).astype(np.uint8)

        gray_grids = np.mean(grids, axis=4).astype(np.uint8)  # Get grayscale version
        flattened_grids = gray_grids.reshape(grid_rows * grid_cols, -1) # Flatten grayscale

        distances = cdist(flattened_grids, reshaped_shapes, metric='euclidean')
        output_indices = np.argmin(distances, axis=1).reshape(grid_rows, grid_cols)

        color_shape_map = CharacterMap(width=target_width, height=target_height)

        row_indices = (np.arange(target_height) * (grid_rows / target_height)).astype(int)
        col_indices = (np.arange(target_width) * (grid_cols / target_width)).astype(int)

        indices_map = output_indices[row_indices[:, None], col_indices]
        color_map = grid_colors[row_indices[:, None], col_indices]

        chars = np.array(OPAS)[indices_map]
        color_strings = np.array([f"\033[38;2;{r};{g};{b}m" for r, g, b in color_map.reshape(-1, 3) ])
        color_shape_map.array = (color_strings.reshape(target_height, target_width) + chars)

        return color_shape_map






sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id='67c0740055b9412da3e1e14978c42742',
        client_secret='4116025cf230497699d6feb972d8bfc7',
        redirect_uri='http://localhost:8080',
        scope='user-read-playback-state user-modify-playback-state user-library-read user-library-modify'
    )
)

def safe_spotify_request(call, *args, **kwargs):
    for i in range(5):
        try:
            return call(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:  # Rate limit error
                retry_after = int(e.headers.get("Retry-After", 5))  # Get wait time
                time.sleep(retry_after)
            else:
                return





ART_ARRAYS = {  # Thanks to Guih48 for the 5x4 number art!
    '0-3x3' : (".o.", "| |", "'0'"),
    '1-3x3' : (".~1", "  |", "  |"),
    '2-3x3' : ("˛=,", " ,I", "2__"),
    '3-3x3' : ("˙`\\", " *3", ".˛/"),
    '4-3x3' : ("/  ", "4+*", " | "),
    '5-3x3' : ("_~~", "5o.", "--/"),
    '6-3x3' : ("˛o.", "6*.", "˙o˙"),
    '7-3x3' : ("\"\"7", " / ", "*  "),
    '8-3x3' : (",o,", ",8,", "˙o˙"),
    '9-3x3' : (".o,", "´~9", " / "),

    #'0-5x4' :  (" /¯\\ ", "|   |", "|   |", " \\_/ "),  #["  ╷ ", "╶─┤ ", "  │ ", "  │ ", "  │ "],
    #'1-5x4' :  ("  |  ", " /|  ", "  |  ", "  |  "),    #["╭──╮", "╵  │", "╭──╯", "│   ", "└──┘"],
    #'2-5x4' :  (" /¯\\ ", "   / ", "  /  ", " /___"),   #["╭──╮", "╵  │", " ╶─┤", "╷  │", "╰──╯"],
    #'3-5x4' :  (" /¯\\ ", "   / ", "  -< ", " \\_/ "),  #["╭   ", "│ ╷ ", "└─┼╴", "  │ ", "  │ "],
    #'4-5x4' :  ("   | ", "  /| ", " /¯|_", "   | "),    #["┌──╴", "│   ", "└──╮", "   │", "╰──╯"],
    #'5-5x4' :  (" /¯¯ ", "|__  ", "   \\ ", " \\_/ "),  #["╭──╮", "│  ╵", "├──╮", "│  │", "╰──╯"],
    #'6-5x4' :  (" /¯¯ ", "|__  ", "|  \\ ", " \\_/ "),  #["┌──┐", "╵  │", "  ╭╯", "  │ ", "  │ "],
    #'7-5x4' :  ("¯¯/¯ ", "  /  ", " /   ", "/    "),    #["╭──╮", "│  │", "├──┤", "│  │", "╰──╯"],
    #'8-5x4' :  (" /¯\\ ", "|_ _|", "|   |", " \\_/ "),  #["╭──╮", "│  │", "╰──┤", "╷  │", "╰──╯"],
    #'9-5x4' :  (" /¯\\ ", "|   |", " \\__|", "  ¯/ "),  #["╭──╮", "│ /│", "│  │", "│/ │", "╰──╯"],

    '0-5x4' :  
    (",:-:,",
     ";   ;",
     ";   ;",
     "':_:'"),

    '1-5x4' :  
    ("  ,1 ", 
     " / | ", 
     "   | ", 
     "   | "),

    '2-5x4' :  
    (" .-~,", 
     "    '", 
     "  ,˝ ", 
     " /___"),

    '3-5x4' :  
    (" ,~, ", 
     "   / ", 
     "  ˝\\ ", 
     " \\_/ "),

    '4-5x4' :  
    ("  /  ", 
     " / , ", 
     "/__4_", 
     "   | "),

    '5-5x4' :  
    (" ,---", 
     " \\__ ", 
     "    \\", 
     " \\__/"),

    '6-5x4' :  
    (" ,~- ", 
     "í    ", 
     "|¨˝\\ ", 
     "'__/ "),

    '7-5x4' :  
    (" --~;", 
     "   / ", 
     "  /  ", 
     " /   "),
    
    '8-5x4' :  
    (" /~\\ ", 
     " \\_/ ", 
     " / \\ ", 
     " \\_/ "),

    '9-5x4' :  
    (" ,--,", 
     " {  |", 
     "  '*}", 
     " ._/ "),

    'previous' : (" .-", "<:|", " ˙-"),
    'pause' :    ("¤ ¤", "O O", "¤ ¤"),
    'resume' :   ("¤. ", "O]>", "¤˙ "),
    'next' :     ("-. ", "|:>", "-˙ "),
    'no_shuffle' :    (".¸ ˛.", "  =  ", "˙´ `˙"),
    'shuffle' :       ("~¸ ˛>", "  ¤  ", "~´ `>"),
    'smart_shuffle' : ("@¸ ˛>", "  ¤  ", "~´ `>"),
    'like' :  (",-.-,", "', ,'", "  `  "),
    'liked' : (",=_=,", "\\"+"%"+"X%/", " ˇ÷ˇ "),
    'cover_art' : [". "*30 for _ in range(30)],
    'progress_bar' : [" "*60,],
    'next_up' : ["NEXT UP",],
    'next_up_serials' : [f"{i+1}." for i in range(9)],
    'next_up_tracks' : [" "*27 for _ in range(9)],
    'next_up_xs' : ["×" for _ in range(9)],
    'playing_from' : ["Playing from:"],
    'playlist' : [" "*47],
    'artists' : [" "*60],
    'track_name' : [" "*59],
    '3x3_line' : [" "*29 for _ in range(3)],
    'last_3x3' : [" "*3 for _ in range(3)],
    'hour_dots' : [" " for _ in range(4)],
    '5x4_second_0' : [" "*5 for _ in range(4)],
    '5x4_second_1' : [" "*5 for _ in range(4)],
    '5x4_minute_0' : [" "*5 for _ in range(4)],
    '5x4_minute_1' : [" "*5 for _ in range(4)],
    'divider_colon' : ("¤", "¤"),

}


def contracted_art_to_array(art):
    return np.array([tuple(string) for string in art])

for key in ART_ARRAYS.keys():
    ART_ARRAYS[key] = contracted_art_to_array(ART_ARRAYS[key])

ART_PLACES = {
    'no_shuffle'     : (33, 66),
    'shuffle'        : (33, 66),
    'smart_shuffle'  : (33, 66),
    'previous'      : (33, 73),
    'pause'          : (33, 78),
    'resume'         : (33, 78),
    'next'          : (33, 83),
    'like'           : (33, 88),
    'liked'          : (33, 88),
    'cover_art' : (2, 2),
    'progress_bar' : (32, 2),
    'next_up'         : (1,63),
    'next_up_serials' : (2, 63),
    'next_up_tracks'  : (2, 66),
    'next_up_xs'      : (2, 95),
    'playing_from' : (0, 1),
    'playlist' : (0, 15),
    'artists'  : (33, 2),
    'track_name' : (34, 3),
    '3x3_line' : (29, 64),
    'last_3x3' : (29, 90),
    'hour_dots' : (24, 63),
    '5x4_second_0' : (24, 88),
    '5x4_second_1' : (24, 81),
    '5x4_minute_0' : (24, 73),
    '5x4_minute_1' : (24, 66),
    'divider_colon' : (25, 79),
}



def place_art(art_name):
    row, col = ART_PLACES[art_name]
    display_map.add_map_array((row, col), ART_ARRAYS[art_name])




current = None


def get_shuffle_status():
    if current:
        if current['smart_shuffle']:
            return 'smart_shuffle'

        elif current['shuffle_state']:
            return 'shuffle'
        
        else:
            return 'no_shuffle'

def update_shuffle_status():
    if current:
        shuffle_status = get_shuffle_status()
        place_art(shuffle_status)

        return shuffle_status

def cycle_shuffle():
    if current:
        current_shuffle_status = get_shuffle_status()

        if current_shuffle_status == 'no_shuffle':
            sp.shuffle(True)

        elif current_shuffle_status == 'shuffle':
            sp.shuffle(True, smart_shuffle=True)

        else:
            sp.shuffle(False)


def get_playing_status():
    if current:
        return current['is_playing']

def stop_resume():
    if current:
        if current['is_playing']:
            sp.pause_playback()
        else:
            sp.start_playback()


def previous_track():
    sp.previous_track()

def next_track():
    sp.next_track()


def get_liked_status():
    if current:
        track_id = current['item']['id']
        liked = sp.current_user_saved_tracks_contains([track_id])[0]
        
        return liked

def update_liked_status():
    if current:
        liked_status = get_liked_status()
        place_art('liked' if liked_status else 'like')
        
        return liked_status

def like_unlike_current_song():
    if current:
        track_id = current['item']['id']
        liked = get_liked_status()
        if liked:
            sp.current_user_saved_tracks_delete([track_id])
        else:
            sp.current_user_saved_tracks_add([track_id])


def get_song_length():
    if current and current['item']['duration_ms']:
        song_length = current['item']['duration_ms'] / 1000
        return song_length
    else:
        return float('inf')

def update_song_length(secs):
    for u in ('second', 'minute'):
        for i in range(2):
            place_art(f'5x4_{u}_{i}')
    place_art('hour_dots')

    if 0<= secs:
        units = secs_to_units(secs)

        second_0_art = ART_ARRAYS[f'{units[5]}-5x4']
        second_1_art = ART_ARRAYS[f'{units[4]}-5x4']
        display_map.add_map_array(ART_PLACES['5x4_second_0'], second_0_art)
        display_map.add_map_array(ART_PLACES['5x4_second_1'], second_1_art)

        h1, h0, m1, m0 = (0< units[i] for i in range(4))
        if h1 or h0:
            dot_count = min(4, units[1]+units[0])
            hour_dots = contracted_art_to_array(["@" for _ in range(dot_count)] + ["˙" for _ in range(4-dot_count)])
            minute_0_art = ART_ARRAYS[f'{units[3]}-5x4']
            minute_1_art = ART_ARRAYS[f'{units[2]}-5x4']
            display_map.add_map_array(ART_PLACES['hour_dots'], hour_dots)
            display_map.add_map_array(ART_PLACES['5x4_minute_0'], minute_0_art)
            display_map.add_map_array(ART_PLACES['5x4_minute_1'], minute_1_art)
        if m0:
            minute_0_art = ART_ARRAYS[f'{units[3]}-5x4']
            if m1:
                minute_1_art = ART_ARRAYS[f'{units[2]}-5x4']
                display_map.add_map_array(ART_PLACES['5x4_minute_1'], minute_1_art)
            display_map.add_map_array(ART_PLACES['5x4_minute_0'], minute_0_art)

        terminal_display.update(display_map)


def get_time():
    if current and current['progress_ms']:
        current_time = current['progress_ms'] / 1000
        return current_time
    else:
        return 0

def update_time(secs):
    place_art('3x3_line')

    if 0<= secs:
        units = secs_to_units(secs)

        for x in range(6):
            if units[x] != 0:
                break
        count = 6-x
    
        row, col = ART_PLACES['last_3x3']
        for i in range(0, count, 2):
            if i == count-1:
                num1 = units[5-i]
                display_map.add_map_array((row, col), ART_ARRAYS[f'{num1}-3x3'])
                col -= 3
            else:
                num1 = units[5-i]
                num2 = units[4-i]
                display_map.add_map_array((row, col), ART_ARRAYS[f'{num1}-3x3'])
                col -= 3
                display_map.add_map_array((row, col), ART_ARRAYS[f'{num2}-3x3'])
                if i != count-2:
                    col -= 2
                    display_map.add_map_array((row+2, col), np.array([['¤']]))
                col -= 4
        display_map.add_map_array((row, col), np.array([
                                                    [' ', ' ', '/'],
                                                    [' ', '/', ' '],
                                                    ['/', ' ', ' ']
                                                ]) )
        
        terminal_display.update(display_map)


def add_progress_bar(progress):
    progress = round(progress*60)
    progress_bar_string = "¤"*(progress-1) + "@" + "-"*(60-progress)

    display_map.add_map_array(ART_PLACES['progress_bar'], np.array([tuple(progress_bar_string)]))


def get_next_up_tracks():
    if current:
        queue = sp.queue()
        next_up_tracks = []
        for track in queue['queue']:
            next_up_tracks.append( (track['name'], ', '.join(artist['name'] for artist in track['artists'])) )

        return next_up_tracks

def update_next_up_tracks():
    next_up_tracks = get_next_up_tracks()
    if next_up_tracks:
        next_9_tracks = get_next_up_tracks()[:9]

        next_up_tracks = []

        track_length_limit = len(ART_ARRAYS['next_up_tracks'][0])
        for track in next_9_tracks:
            track_name, artists = track
            artists_len = len(artists)
            track_name_len = len(track_name)

            if track_name_len + artists_len + 3 <= track_length_limit:
                track_text = track_name + ' - ' + artists

            elif artists_len+9 < track_length_limit:
                track_text = track_name[ :(track_length_limit-artists_len-4)].rstrip() + '…' + ' - ' + artists

            elif track_name_len+9 < track_length_limit:
                track_text = track_name + ' - ' + artists[ :(track_length_limit-track_name_len-4)] + '…'

            else:
                track_text = track_name[:(track_length_limit//2-1)].rstrip() + '… - ' + artists[ :(track_length_limit-5-(track_length_limit//2-1) + 1*(track_name[track_length_limit//2-2]==' ')) ] + '…'
            
            leftover = track_length_limit-len(track_text)
            if 0< leftover: track_text += " "*leftover

            next_up_tracks.append(track_text)

        place_art('next_up_tracks')

        next_up_tracks = np.array([tuple(string) for string in next_up_tracks])

        display_map.add_map_array(ART_PLACES['next_up_tracks'], next_up_tracks)


def get_album_cover_url():
    if current:
        return current['item']['album']['images'][0]['url']

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        return CustomImage(np.array(image))
    except:
        return CustomImage(ART_ARRAYS['cover_art'])

def update_album_cover():
    if current:
        album_cover_url = get_album_cover_url() # 'https://i.scdn.co/image/ab67616d0000b27351c02a77d09dfcd53c8676d0' # 
        downloaded_image = download_image(album_cover_url)

        for tw, th in ((30,30),(90,90)): Image.fromarray(downloaded_image.downscale(tw,th).array).save(f"album_cover-{tw}x{th}.png")

        album_cover = downloaded_image.to_color_shape_map(60,30)

        display_map.add_map_array(ART_PLACES['cover_art'], album_cover.array)
        

def get_current_playlist_name():
    if current and current['context']:
        context_type = current['context']['type']
        if context_type == 'playlist':
            playlist_uri = current['context']['uri']
            playlist_id = playlist_uri.split(':')[-1]
            playlist = sp.playlist(playlist_id)
            return playlist['name']

        elif context_type == 'collection':
            return "Liked Songs"

        elif context_type == 'album':
            return current['item']['album']['name']

        elif context_type == 'artist':
            return current['item']['artists'][0]['name']
    else:
        return " "

def update_playlist_name():
    playlist_name = get_current_playlist_name()[ :len(ART_ARRAYS['playlist'][0])]
    place_art('playlist')

    display_map.add_map_array(ART_PLACES['playlist'], np.array([tuple(playlist_name)]))

    return playlist_name


def get_current_track_name():
    if current:
        return current['item']['name']
    else:
        return " "

def update_track_name():
    track_name = get_current_track_name()[ :len(ART_ARRAYS['track_name'][0])]
    place_art('track_name')

    display_map.add_map_array(ART_PLACES['track_name'], np.array([tuple(track_name)]))
    
    return track_name


def get_current_artists():
    if current:
        artists = []
        for artist in current['item']['artists']:
            artists.append(artist['name'])
        return ", ".join(artists)
    else:
        return " "

def update_artists():
    artists = get_current_artists()[ :len(ART_ARRAYS['artists'][0])]
    place_art('artists')

    display_map.add_map_array(ART_PLACES['artists'], np.array([tuple(artists)]))

    return artists
            


def update_playing_status():
    if current:
        playing_status = get_playing_status()
        place_art('pause' if playing_status else 'resume')
        
        return playing_status


def song_view():
    global current
    display_map.fill()

    arts = (
        'playing_from', 'playlist',
        'cover_art',
        'progress_bar',
        'artists', 'track_name',
        'next_up', 'next_up_serials', 'next_up_tracks', 'next_up_xs',
        'hour_dots', '5x4_minute_1', '5x4_minute_0', 'divider_colon', '5x4_second_1', '5x4_second_0',
        'no_shuffle', 'previous', 'resume', 'next', 'like',
    )
    for art in arts: place_art(art)



    buffer = 0.5#seconds
    last_request_time = 0
    current_time = 0
    last_calculated_time = 0
    song_length = float('inf')

    previous_name = None
    previous_playing_status = False


    while True:
        try:
            if buffer< precise_time() - last_request_time:
                
                current = safe_spotify_request(sp.current_playback)

                if current:
                    playing_status = update_playing_status()

                    update_playlist_name()

                    if current['item'] and previous_name != current['item']['name']:
                        update_album_cover()
                        update_next_up_tracks()
                        song_length = get_song_length()
                        update_song_length(song_length)
                        update_track_name()
                        update_artists()

                    update_shuffle_status()
                    update_liked_status()

                    current_time = get_time()
                    update_time(current_time)

                    add_progress_bar(current_time/song_length)

                    previous_name = current['item']['name']
                    previous_playing_status = playing_status

                else:
                    previous_name = None
            else:
                current_time = last_calculated_time + precise_time() - last_request_time
                update_time(current_time)
            
            terminal_display.update(display_map)
        
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass





if __name__ == "__main__":
    global GLOBAL_last_frame_time, bottom_text
    bottom_text = ""
    GLOBAL_last_frame_time = 0

    colorama.init(autoreset=True) # Initialize terminal formatting

    window_width = 96
    window_height = 36

    os.system('cls')

    terminal_display = TerminalDisplay(window_height)

    display_map = CharacterMap(window_width, window_height, filler=' ', U1dtype=False)

    song_view()

    print(colorama.Style.RESET_ALL) # End terminal formatting
