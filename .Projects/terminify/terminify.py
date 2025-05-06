# --- Imports ---
from time import perf_counter as precise_time
from time import sleep as wait
from time import sleep as wait_seconds
import os
import numpy as np
import cv2
from sys import stdout
from PIL import Image
import colorama
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from io import BytesIO
from colorama import Fore
from scipy.spatial.distance import cdist
import re, syncedlyrics

import sys

from pynput import keyboard
from pynput.keyboard import Key

from win32gui import GetForegroundWindow, SetForegroundWindow

import psutil






def classes():
    global CharacterMap, TerminalDisplay, CustomImage
    global Selector, Typer
###
###
    class CharacterMap:
        def __init__(self, width:int, height:int, d_list:tuple= None, filler:str= ' ', U1dtype:bool= True): 
            if d_list:
                self.width = len(d_list[0])
                self.height = len(d_list)
                self.array = np.array(d_list, dtype='<U1')
            else:
                self.width = width
                self.height = height
                self.array = np.full(((height, width)), filler, dtype='<U1')
            if not U1dtype:
                self.array = self.array.astype(np.object_)

            self.filler = filler
        
        def __getitem__(self, key):
            x, y = key
            return self.array[self.height-y-1][x]
        
        def __setitem__(self, key, value):
            x, y = key
            self.array[self.height-y-1][x] = value
            
        def fill(self, fill='??'):
            if fill == '??':
                filler = self.filler
            else:
                filler = fill

            self.array[:, :] = filler
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

    class TerminalDisplay:
        def __init__(self, height:int= 512):
            self.height = height

        def to_beginning(self):
            sys.stdout.write(f"\033[{self.height+1}A\033[2K\n")
        
        def clear(self):
            os.system('cls')
        
        def write(self, display_map:CharacterMap):
            output = "\n".join(("".join(row) for row in display_map.array)) + Fore.WHITE
            self.to_beginning()
            stdout.write(output)
            stdout.flush()

        def update(self, display_map:CharacterMap, fps:float= 0):
            global GLOBAL_last_frame_time
            
            if fps == 0:
                self.write(display_map)
            else:
                stay_seconds = int(1000/fps)/1000

                self.write(display_map)

                while (precise_time() - GLOBAL_last_frame_time)< stay_seconds :
                    pass

                GLOBAL_last_frame_time = precise_time()

    class CustomImage:
        def __init__(self, image_array:np.array= ()):
            self.array = np.array(image_array)

        def downscale(self, target_width:int, target_height:int, method=cv2.INTER_LINEAR_EXACT):
            self.array = cv2.resize(self.array, (target_width, target_height), interpolation=method)

            return self

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

            gray_grids = np.mean(grids, axis=4).astype(np.uint8)
            flattened_grids = gray_grids.reshape(grid_rows * grid_cols, -1)

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


    class Selector():
        def __init__(self, field_values:tuple[tuple[int, ...], ...], field_actions:tuple[tuple[any, ...], ...]= None, starting_position:tuple[int, int]=[0, 0]):
            """restricted zones : -1"""
            self.field_values = field_values
            x, y = starting_position
            i, j = len(field_values)-y-1, x
            self.position = [i, j]
            self.last_interaction_time = 0
            self.field_actions = field_actions

        def move(self, direction:tuple[int, int]):
            i, j = self.position
            dx, dy = direction
            di, dj = -dy, dx
            new_i, new_j = i+di, j+dj

            self.last_interaction_time = precise_time()
            
            if 0<= new_i< len(self.field_values) and 0<= new_j< len(self.field_values[0]):

                if self.field_values[new_i][new_j] != -1 and self.field_values[new_i][new_j] != self.field_values[i][j]:
                    self.position = new_i, new_j
                            
                    return self.field_values[new_i][new_j]
            
            return False
        
        def get_val(self):
            i, j = self.position
            return self.field_values[i][j]
        
        def call_action(self):
            t = precise_time()
            i, j = self.position

            self.last_interaction_time = t-3
            return self.field_actions[i][j]()

        def move_up(self):
            self.move((0, 1))

        def move_down(self):
            self.move((0, -1))

        def move_left(self):
            self.move((-1, 0))

        def move_right(self):
            self.move((1, 0))

    class Typer():
        def __init__(self, text:str= "", cursor_position:int= 0, scope:tuple[int, int]= [0, 100]):
            self.text = text
            self.cursor_position = cursor_position
            self.scope = list(scope)
            self.last_interaction_time = 0
        
        def __str__(self):
            return self.text
        
        def __iter__(self):
            yield self.text
            yield self.cursor_position


        def get_in_scope_with_markers(self):
            s = self.text[self.scope[0] : self.scope[1]]
            if 0< self.scope[0]:
                s = '…' + s[1:]
            if self.scope[1]< len(self.text):
                s = s[:-1] + '…'

            return s

        def get(self):
            return self.get_in_scope_with_markers()
        
        def get_with_cursor(self, cursor:str= "_"):
            s = self.get_in_scope_with_markers()
            s = s[: self.cursor_position] + cursor + s[self.cursor_position+1 :]
            return s


        def add_text(self, text:str= ""):
            self.text = self.text[: self.cursor_position] + text + self.text[self.cursor_position :]
            self.move_cursor_right(len(text))

            self.last_interaction_time = precise_time()

        
        def clear(self):
            self.text = ""
            self.cursor_position = 0

            self.last_interaction_time = precise_time()
        

        def backspace(self, amount:int= 1):
            self.text = self.text[: self.cursor_position-amount] + self.text[self.cursor_position :]
            self.move_cursor_left(amount) 

            self.last_interaction_time = precise_time()

        def delete(self, amount:int= 1):
            self.text = self.text[: self.cursor_position] + self.text[self.cursor_position+amount :]

            self.last_interaction_time = precise_time()


        def ctrl_backspace(self):
            there_was_a_char = False
            leading_spaces = 0
            i = self.cursor_position-1
            while -1< i:
                if self.text[i] == ' ':
                    if there_was_a_char:
                        break
                    else:
                        leading_spaces += 1
                else:
                    there_was_a_char = True
                    if 2<= leading_spaces:
                        break
                i -= 1
            
            self.backspace(self.cursor_position - i - 1)

            self.last_interaction_time = precise_time()

        def ctrl_delete(self):
            there_was_a_char = False
            leading_spaces = 0
            i = self.cursor_position

            while i< len(self.text):
                if self.text[i] == ' ':
                    if there_was_a_char:
                        break
                    else:
                        leading_spaces += 1
                else:
                    there_was_a_char = True
                    if 2<= leading_spaces:
                        break
                i += 1
                
            self.delete(i - self.cursor_position)

            self.last_interaction_time = precise_time()


        def move_cursor(self, amount:int= +1):
            new_position = max(0, min(self.cursor_position+amount, len(self.text)))
            
            self.cursor_position = new_position

            if new_position< self.scope[0]:
                d = new_position - self.scope[0]
            elif self.scope[1]<= new_position:
                d = new_position - self.scope[1]

            self.scope[0] += d
            self.scope[1] += d

            self.last_interaction_time = precise_time()


        def move_cursor_left(self, amount:int= 1):
            self.move_cursor(-amount)
        
        def move_cursor_right(self, amount:int= 1):
            self.move_cursor(amount)
        

        def ctrl_move_cursor_left(self):
            there_was_a_char = False
            leading_spaces = 0
            i = self.cursor_position-1
            while -2< i:
                if self.text[i] == ' ':
                    if there_was_a_char:
                        break
                    else:
                        leading_spaces += 1
                else:
                    there_was_a_char = True
                    if 2<= leading_spaces:
                        break
                i -= 1
            
            self.move_cursor_left(self.cursor_position - i - 1)

        def ctrl_move_cursor_right(self):
            there_was_a_char = False
            leading_spaces = 0
            i = self.cursor_position

            while i< len(self.text):
                if self.text[i] == ' ':
                    if there_was_a_char:
                        break
                    else:
                        leading_spaces += 1
                else:
                    there_was_a_char = True
                    if 2<= leading_spaces:
                        break
                i += 1
            
            self.move_cursor_right(i - self.cursor_position)
###
##
classes()







def globals():
    global globalize_screener_values
    global globalize_time_convert_values
    global globalize_ART_values
    global globalize_spotify_values
    global globalize_key_action_dict
    global globalize_action_selector
    global globalize_mode_values
###
###
    def globalize_screener_values():
        global DOT, OPAS, THRESHOLDS, CHAR_WIDTH_PER_HEIGHT, CHARACTER_SHAPES
        global window_width, window_height, terminal_display, display_map, GLOBAL_last_frame_time

        DOT = (os.path.dirname(__file__)).replace('\\','/')

        OPAS = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")

        THRESHOLDS = (19.92, 36.93, 39.75, 39.84, 42.89, 53.66, 54.4, 62.83, 69.53, 74.17, 105.29, 106.47, 108.4, 109.08, 111.08, 116.27, 117.73, 123.66, 125.45, 125.71, 128.68, 130.03, 131.86, 132.5, 135.4, 137.24, 137.5, 142.01, 142.56, 142.75, 143.7, 146.49, 146.71, 147.49, 148.18, 149.43, 149.48, 153.02, 153.36, 155.5, 156.51, 157.07, 157.39, 157.42, 157.54, 157.6, 157.9, 162.86, 163.27, 165.91, 166.07, 167.35, 167.53, 169.5, 170.98, 172.68, 174.85, 181.89, 182.69, 185.28, 185.88, 186.98, 188.07, 188.71, 194.11, 194.94, 195.06, 195.96, 196.18, 196.41, 196.81, 197.21, 197.27, 198.77, 200.79, 203.01, 204.88, 210.01, 212.57, 215.11, 218.92, 219.69, 221.34, 223.96, 232.33, 232.41, 232.83, 233.37, 240.17, 243.34, 255.0)

        CHAR_WIDTH_PER_HEIGHT = 117/232

        CHARACTER_SHAPES = (((9.2, 246.45, 0.36), (0.0, 15.92, 1.84), (0.0, 0.0, 0.0)), ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 146.16, 0.0)),((0.0, 0.0, 0.0), (121.82, 161.49, 122.78), (0.0, 0.0, 0.0)),((0.0, 151.87, 0.0), (0.0, 143.26, 0.0), (0.0, 0.0, 0.0)),((0.0, 0.0, 0.0), (0.0, 148.64, 0.0), (0.0, 145.96, 0.0)),((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (118.91, 157.64, 119.83)),((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 314.2, 0.0)),((12.7, 224.55, 13.54), (82.08, 97.76, 83.54), (0.0, 0.0, 0.0)),((0.0, 0.0, 0.0), (243.37, 322.61, 245.28), (0.0, 0.0, 0.0)),((0.0, 0.0, 0.0), (0.0, 148.52, 0.0), (0.0, 314.19, 0.0)),((26.35, 0.0, 0.0), (183.28, 355.89, 212.25), (28.8, 0.0, 0.0)),((0.0, 0.0, 26.04), (205.27, 339.49, 181.82), (0.0, 0.0, 28.37)),((0.0, 56.04, 0.0), (121.94, 434.58, 122.89), (0.0, 58.25, 0.0)),((0.0, 142.66, 0.0), (0.0, 259.75, 0.0), (0.0, 146.03, 0.0)),((0.0, 0.0, 0.0), (213.4, 294.99, 205.79), (149.89, 189.54, 0.0)),((0.0, 0.0, 0.0), (292.51, 176.27, 127.7), (87.63, 177.65, 94.9)),((0.0, 32.66, 0.0), (181.48, 448.31, 183.35), (7.17, 1.02, 7.29)),((0.0, 27.57, 205.16), (8.76, 325.21, 27.76), (174.45, 56.14, 0.0)),((0.0, 0.0, 0.0), (114.68, 388.89, 146.66), (142.24, 180.73, 95.6)),((115.79, 178.18, 99.57), (1.81, 223.96, 111.66), (0.0, 146.75, 0.0)),((0.0, 0.0, 0.0), (200.64, 340.5, 187.72), (97.49, 164.93, 120.92)),((141.99, 0.0, 0.0), (354.36, 0.0, 0.0), (153.27, 161.6, 122.99)),((132.08, 219.56, 133.17), (0.0, 354.87, 0.0), (0.0, 141.04, 0.0)),((0.0, 0.0, 0.0), (271.61, 143.52, 273.5), (9.09, 230.46, 9.73)),((79.32, 230.21, 22.77), (0.0, 157.31, 203.41), (78.39, 228.11, 22.13)),((0.0, 127.84, 164.43), (73.54, 0.0, 354.94), (126.97, 163.48, 101.78)),((175.23, 164.46, 194.53), (85.01, 198.7, 190.97), (0.0, 154.96, 0.0)),((21.78, 229.87, 80.33), (199.77, 160.49, 0.0), (21.13, 227.67, 79.27)),((0.0, 282.01, 0.0), (0.0, 355.97, 0.0), (0.0, 280.77, 0.0)),((146.51, 164.26, 133.25), (359.35, 164.61, 59.0), (141.14, 0.0, 0.0)),((0.0, 146.15, 2.28), (73.62, 406.6, 0.0), (95.34, 216.23, 120.51)),((0.0, 252.76, 69.87), (57.29, 386.48, 0.0), (0.0, 253.06, 68.84)),((81.12, 175.41, 138.92), (378.41, 0.32, 0.0), (85.75, 176.77, 116.29)),((69.11, 253.45, 0.0), (0.0, 385.16, 58.54), (68.13, 254.27, 0.0)),((0.0, 200.11, 129.53), (135.12, 434.79, 101.69), (0.0, 143.14, 0.0)),((96.0, 219.73, 96.76), (0.0, 355.92, 0.0), (94.45, 217.33, 95.2)),((106.64, 172.18, 108.33), (9.62, 195.48, 256.12), (97.52, 166.19, 102.68)),((92.58, 197.85, 0.0), (0.35, 356.42, 0.0), (93.74, 217.35, 103.29)),((38.02, 88.53, 0.0), (216.0, 353.96, 94.49), (14.83, 195.76, 105.72)),((122.97, 184.7, 0.0), (0.0, 358.25, 0.0), (0.0, 188.76, 106.37)),((0.0, 0.0, 0.0), (338.91, 17.49, 324.65), (127.21, 149.57, 196.44)),((32.98, 295.25, 82.78), (49.03, 306.97, 0.0), (32.68, 292.54, 81.89)),((0.0, 0.0, 0.0), (343.76, 165.91, 310.29), (143.55, 0.0, 143.57)),((0.0, 0.0, 0.0), (314.37, 314.31, 251.41), (93.04, 170.07, 77.21)),((0.0, 0.0, 0.0), (304.73, 183.13, 306.3), (99.62, 180.66, 100.99)),((103.5, 171.6, 159.64), (48.24, 301.93, 49.94), (156.44, 169.05, 110.64)),((112.57, 174.22, 83.44), (196.95, 177.83, 256.37), (115.6, 166.08, 121.97)),((147.31, 0.0, 147.42), (93.71, 381.18, 95.15), (0.0, 141.12, 0.0)),((0.0, 0.0, 0.0), (135.04, 396.15, 133.46), (116.57, 84.51, 118.12)),((0.0, 98.22, 50.01), (55.67, 306.91, 143.23), (91.83, 302.23, 91.82)),((0.0, 0.0, 0.0), (273.07, 125.44, 284.62), (144.45, 404.74, 22.51)),((0.0, 0.0, 0.0), (194.09, 337.25, 222.76), (149.58, 140.1, 189.13)),((81.81, 293.91, 34.7), (0.0, 303.85, 51.62), (80.93, 291.21, 34.41)),((118.18, 173.61, 93.31), (8.13, 190.84, 203.74), (152.24, 194.2, 113.1)),((154.63, 164.26, 125.01), (366.98, 164.06, 50.48), (153.27, 161.6, 122.99)),((105.71, 169.41, 99.07), (150.37, 206.65, 162.71), (112.26, 161.5, 116.47)),((0.0, 0.0, 0.0), (308.6, 378.47, 313.41), (141.74, 125.78, 126.02)),((0.0, 0.0, 0.0), (322.79, 152.33, 342.28), (128.18, 147.14, 356.14)),((182.44, 0.0, 0.0), (373.49, 229.74, 249.68), (144.42, 21.11, 154.15)),((154.46, 166.4, 122.55), (366.9, 166.5, 280.66), (140.83, 0.0, 0.0)),((23.41, 172.31, 73.27), (367.11, 170.75, 252.47), (114.58, 168.11, 119.82)),((181.15, 0.0, 0.0), (367.78, 158.5, 310.16), (143.41, 0.0, 143.43)),((107.51, 169.68, 114.2), (254.76, 164.63, 376.95), (67.45, 175.64, 32.23)),((0.0, 0.0, 181.11), (324.52, 154.12, 371.54), (130.12, 152.26, 147.31)),((75.2, 49.24, 127.68), (392.08, 199.3, 372.6), (0.0, 14.04, 126.64)),((144.75, 0.0, 144.76), (250.69, 187.88, 252.93), (7.61, 235.89, 8.32)),((0.0, 0.0, 0.0), (347.85, 156.83, 325.68), (356.24, 151.9, 131.24)),((109.78, 172.04, 110.76), (368.24, 0.0, 368.43), (111.88, 169.2, 112.93)),((93.57, 171.62, 129.89), (376.59, 78.91, 207.66), (100.52, 170.6, 164.61)),((181.18, 0.0, 0.0), (368.5, 158.05, 325.87), (157.32, 160.45, 86.76)),((141.69, 0.0, 142.43), (354.15, 0.0, 354.38), (111.19, 173.1, 110.41)),((5.01, 231.47, 5.43), (250.13, 353.43, 253.17), (140.3, 0.0, 140.31)),((141.81, 0.0, 140.58), (371.32, 265.92, 219.42), (140.65, 4.14, 158.88)),((142.54, 20.09, 142.93), (70.82, 487.91, 72.8), (139.75, 22.52, 140.57)),((141.69, 0.0, 142.67), (374.8, 165.53, 377.36), (140.54, 0.0, 141.51)),((0.0, 0.0, 0.0), (354.73, 349.75, 361.41), (143.43, 123.06, 144.87)),((114.89, 171.66, 115.88), (295.98, 197.49, 297.37), (124.01, 164.45, 124.79)),((162.54, 167.11, 119.27), (374.66, 217.61, 295.9), (140.54, 5.33, 154.13)),((162.47, 174.0, 88.41), (353.62, 0.0, 372.21), (161.19, 170.41, 93.56)),((40.13, 96.11, 105.08), (322.6, 428.49, 326.77), (102.71, 95.09, 41.22)),((105.75, 303.86, 99.35), (150.37, 372.58, 162.73), (112.63, 296.14, 116.84)),((154.46, 170.67, 100.67), (366.9, 173.03, 305.02), (153.26, 163.47, 149.51)),((0.0, 0.0, 0.0), (324.65, 157.1, 347.19), (223.11, 329.87, 284.65)),((93.8, 179.68, 95.14), (366.59, 156.06, 365.96), (95.96, 176.56, 97.18)),((179.7, 105.66, 180.87), (342.96, 300.89, 345.29), (134.8, 0.0, 135.57)),((170.54, 51.81, 142.24), (360.13, 280.92, 359.05), (141.51, 50.96, 170.1)),((141.61, 0.0, 141.61), (337.71, 403.03, 337.82), (147.39, 146.33, 148.77)),((109.78, 172.04, 110.76), (368.32, 0.0, 368.25), (111.99, 347.85, 200.46)),((154.52, 132.67, 0.0), (259.87, 410.84, 270.21), (0.43, 123.8, 162.2)),((85.36, 187.22, 89.1), (315.45, 268.92, 200.51), (157.23, 176.94, 171.74)),((82.65, 165.65, 105.93), (292.41, 372.71, 342.46), (164.06, 263.04, 109.96)),)
        

        window_width = 96
        window_height = 36

        terminal_display = TerminalDisplay(window_height+2)

        display_map = CharacterMap(window_width, window_height, filler=' ', U1dtype=False)

        GLOBAL_last_frame_time = 0


    def globalize_time_convert_values():
        global TIME_CONVERT_LIST, TIME_CHAR_LIST

        TIME_CONVERT_LIST = (29030400, 604800, 86400, 3600, 60, 1)
        TIME_CHAR_LIST = ('y', 'w', 'd', 'h', 'm', 's')


    def globalize_ART_values():
        global CONTRACTED_ART_ARRAYS, ART_ARRAYS, ART_COLORS, ART_PLACES
        CONTRACTED_ART_ARRAYS = {
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
            'cover_art' : [". "*30]*30,
            'progress_bar' : [" "*60],
            'next_up' : ["NEXT UP"],
            'next_up_serials' : [f"{i+1}." for i in range(9)],
            'next_up_tracks' : [" "*27]*9,
            'next_up_xs' : ["×"]*9,
            'playing_from' : ["Playing from:"],
            'playlist' : [" "*47],
            'artists' : [" "*60],
            'track_name' : [" "*59],
            '3x3_line' : [" "*29]*3,
            'last_3x3' : [" "*3]*3,
            'hour_dots' : [" "]*4,
            '5x4_second_0' : [" "*5]*4,
            '5x4_second_1' : [" "*5]*4,
            'divider_colon' : ("¤", "¤"),
            '5x4_minute_0' : [" "*5]*4,
            '5x4_minute_1' : [" "*5]*4,
            'lyrics' : [" "*33]*2 + ["."*33] + [" "*33]*2 + ["˙"*33] + [" "*33]*4,
            'search_bar' : [":"*58]*3,
        }
        ART_ARRAYS = CONTRACTED_ART_ARRAYS.copy()

        ART_PLACES = {
                            # row, col [0<=, 0<=]
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
            'hour_dots' : (24, 62),
            '5x4_second_0' : (24, 88),
            '5x4_second_1' : (24, 81),
            'divider_colon' : (25, 79),
            '5x4_minute_0' : (24, 72),
            '5x4_minute_1' : (24, 65),
            'lyrics' : (12, 63),
            'search_bar' : (3, 3),
        }
        
        ART_COLORS = {
            'playing_from' : rgb(170, 170, 170),
            'next_up' : rgb(190, 190, 192),
            'next_up_serials' :  rgb(170, 170, 174),
            'next_up_tracks' : rgb(199, 199, 199),
            'next_up_xs' : rgb(170, 170, 174),
            'artists' : rgb(176, 176, 178),
            'selector' : rgb(157, 214, 245),
            'shuffle' : rgb(25, 196, 88),
            'smart_shuffle' : rgb(25, 196, 88),
            'liked' : rgb(24, 220, 96),
            'divider_colon' : rgb(180, 180, 180),
            '3x3_slash' : rgb(160, 160, 160),
            'search_bar' : rgb(42, 42, 42),
            'search_text' : rgb(255, 255, 255),
            'search_result_text' : rgb(210, 210, 210),
        }
        for i in range(10):
            ART_COLORS.update({f'{i}-5x4' : rgb(180, 180, 180)})
            ART_COLORS.update({f'{i}-3x3' : rgb(150, 150, 150)})

        for key in ART_ARRAYS.keys():
            try:
                _ = ART_COLORS[key]
            except:
                ART_COLORS.update({key : Fore.WHITE})
            ART_ARRAYS[key] = contracted_art_to_array(ART_ARRAYS[key], color=ART_COLORS[key])
        
        def color_search_bar():
            ART_ARRAYS['search_bar'][0][0] = rgb(255, 255, 255) + "."
            ART_ARRAYS['search_bar'][0][-1] = rgb(255, 255, 255) + "."
            ART_ARRAYS['search_bar'][0][1:-1] = rgb(255, 255, 255) + "˙"
            ART_ARRAYS['search_bar'][0][2] = rgb(255, 255, 255) + "˙"
            search_list = list("Search:")
            search_list[0] = rgb(200,200,200) + search_list[0]
            ART_ARRAYS['search_bar'][0][3:10] = np.array(search_list)

            ART_ARRAYS['search_bar'][1][0] = rgb(255, 255, 255) + ":"
            ART_ARRAYS['search_bar'][1][-1] = rgb(255, 255, 255) + ":"
            ART_ARRAYS['search_bar'][1][1] = " "
            ART_ARRAYS['search_bar'][1][-2] = " "

            ART_ARRAYS['search_bar'][2][0] = rgb(255, 255, 255) + "˙"
            ART_ARRAYS['search_bar'][2][-1] = rgb(255, 255, 255) + "˙"
            ART_ARRAYS['search_bar'][2][1:-1] = rgb(255, 255, 255) + "."
        color_search_bar()


    def globalize_spotify_values():
        global sp, current, buffer, current_time, song_length, progress, last_request_time, last_calculated_time, lyrics, playing_status, previous_name, liked_status, time_since_last_sync, album_cover_array, search_result_tracks
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id='67c0740055b9412da3e1e14978c42742',
                client_secret='4116025cf230497699d6feb972d8bfc7',
                redirect_uri='https://example.org/callback',
                scope='user-read-playback-state user-modify-playback-state user-library-read user-library-modify'
            )
        )
        current = None

        buffer = 2#seconds
        
        current_time = 0
        song_length = float('inf')
        progress = 0
        last_request_time = precise_time()-buffer-0.1
        last_calculated_time = 0
        lyrics = ""
        playing_status = False
        previous_name = None
        liked_status = False
        time_since_last_sync = precise_time()-buffer-0.1
        album_cover_array = []
        search_result_tracks = None


    def globalize_key_action_dict():
        global key_action_dict
        key_action_dict = {}


    def globalize_action_selector():
        global action_selector
        action_selector = Selector(
            field_values= [['progress_bar', 'shuffle', 'previous', 'pause', 'next', 'like']],
            field_actions= [[toggle_time_edit_mode, toggle_shuffle, previous_track, pause_resume, next_track, like_unlike_current_song]],
            starting_position= [3, 0],
        )
    

    def globalize_mode_values():
        global time_edit_mode, search_mode, search_typer, listener, ctrl_is_pressed
        time_edit_mode = False
        search_mode = False
        search_typer = Typer(scope=[0, len(ART_ARRAYS['search_bar'][0])-4])

        listener = None
        ctrl_is_pressed = False
###
##
globals()







def general_functions():
    global secs_to_text, secs_to_units
    global print_separate, highlight
    global rgb
    global terminal_is_focused
    global contracted_art_to_array, place_art
    global is_spotify_running, ensure_spotify_is_running
    global get_devices, choose_from_devices, get_preferred_device_id
    global call_action_and_update_status
    global on_press_for_selector, on_press_for_typer
    global set_listener_for_selector, set_listener_for_typer
    global set_action_selector_for_key_dict, set_search_typer_for_key_dict, search_tracks_with_typer
    global toggle_time_edit_mode, toggle_search_mode
    global place_search_results
###
###
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


    def rgb(r:int= 0, g:int= 0, b:int= 0):
        return f"\033[38;2;{r};{g};{b}m"


    def terminal_is_focused():
        return GetForegroundWindow() == TERMINAL_WINDOW_ID


    def contracted_art_to_array(art, color=Fore.WHITE, end_color=Fore.WHITE):
        l = []
        for string in art:
            s = list(string)
            if color:
                for i in range(len(s)): s[i] = color + s[i] + end_color
            else:
                s[-1] = s[-1] + end_color
            l.append(s)

        return np.array(l)

    def place_art(art_name):
        row, col = ART_PLACES[art_name]
        display_map.add_map_array((row, col), ART_ARRAYS[art_name])


    def is_spotify_running():
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'spotify' in proc.info['name'].lower():
                return True
        return False

    def ensure_spotify_is_running():
        if not is_spotify_running():
            os.system('powershell -ExecutionPolicy Bypass -Command "Start-Process .\\Spotify.lnk -WindowStyle Hidden"')
            print("Launching spotify...\n")
            while not is_spotify_running(): wait(0.1)
            wait(5)


    def get_devices():
        return sp.devices().get('devices', [])

    def choose_from_devices(devices):
        global selected_device_id

        names = []
        ids = []
        for device in devices:
            if not device.get('is_restricted'):
                names.append(device['name'])
                ids.append(device['id'])
        
        if len(ids) == 1:
            selected_device_id = ids[0]
            print("\nSelected:", names[0])
        else:
            selected_device_id = None
            
            device_selector = Selector(
                field_values=[names],
            )
            global key_action_dict
            _k_a_d = key_action_dict.copy()
            
            def select():
                global selected_device_id
                selected_device_id = ids[device_selector.position[1]]

            key_action_dict = {
                'a' : device_selector.move_left,   Key.left : device_selector.move_left,
                'd' : device_selector.move_right,  Key.right : device_selector.move_right,
                Key.space : select,
                'e' : terminal_display.clear,
            }

            print("Choose a device:\n")
            st = precise_time()
            previous_selected = names[0]
            while not selected_device_id:                    
                text = " "
                dt = precise_time() - st
                for name in names:
                    if name == device_selector.get_val() and dt-int(dt)< 0.5 :
                        text += "#"*len(name) + " "
                        if name != previous_selected:
                            st = precise_time()
                        previous_selected = name
                    else:
                        text += name + " "
                text = text[:-1]
                print(f"\r {text}", end="")
                wait(0.02)
            
            key_action_dict = _k_a_d

            print("\n\nSelected:",device_selector.get_val())

    def get_preferred_device_id():
        devices = get_devices()
        if not devices:
            raise("No available devices found.")

        for device in devices:
            if device.get('is_active') and not device.get('is_restricted'):
                return device['id']
        print("No active devices found.")

        choose_from_devices(devices)
        wait(0.5)
        sp.transfer_playback(selected_device_id)


    def call_action_and_update_status():
        global current
        action_selector.call_action()
        current = sp.current_playback()


    def on_press_for_selector(key):
        if terminal_is_focused():
            try:
                try:
                    c = key.char
                    key_action_dict[c]()
                except:
                    key_action_dict[key]()
            except:
                pass
    
    def on_press_for_typer(key):
        global search_typer, search_result_tracks

        if terminal_is_focused():
            try:
                search_typer.last_interaction_time = precise_time()
                try:
                    key_action_dict[key]()
                except:
                    if key == Key.space:
                        c = " "
                    else:
                        c = key.char
                    
                    search_result_tracks = None
                    search_typer.add_text(c)
            except:
                pass


    def set_listener_for_selector():
        global listener
        try:
            listener.stop()
        except: pass
        listener = keyboard.Listener(on_press=on_press_for_selector)
        listener.start()
        
    def set_listener_for_typer():
        global listener
        def release_ctrl(key):
            global ctrl_is_pressed
            if terminal_is_focused and key==Key.ctrl_l:
                ctrl_is_pressed = False
        try:
            listener.stop()
        except: pass
        listener = keyboard.Listener(on_press=on_press_for_typer, on_release=release_ctrl)
        listener.start()


    def set_action_selector_for_key_dict():
        global key_action_dict
        key_action_dict = {
            'w' : action_selector.move_up,        Key.up : action_selector.move_up,
            's' : action_selector.move_down,      Key.down : action_selector.move_down,
            'a' : action_selector.move_left,      Key.left : action_selector.move_left,
            'd' : action_selector.move_right,     Key.right : action_selector.move_right,
            Key.space : call_action_and_update_status,
            'f' : toggle_search_mode,
            'e' : terminal_display.clear,
        }

    def set_search_typer_for_key_dict():
        global key_action_dict

        def pressed_ctrl():
            global ctrl_is_pressed
            ctrl_is_pressed = True

        def pressed_left():
            if ctrl_is_pressed:
                search_typer.ctrl_move_cursor_left()
            else:
                search_typer.move_cursor_left()

        def pressed_right():
            if ctrl_is_pressed:
                search_typer.ctrl_move_cursor_right()
            else:
                search_typer.move_cursor_right()

        def pressed_backspace():
            if ctrl_is_pressed:
                search_typer.ctrl_backspace()
            else:
                search_typer.backspace()

        def pressed_delete():
            if ctrl_is_pressed:
                search_typer.ctrl_delete()
            else:
                search_typer.delete()

        def pressed_down():
            pass
        
        def pressed_up():
            pass

        def pressed_tab():
            pass

        global search_tracks_with_typer
        def search_tracks_with_typer():
            search_tracks(search_typer.text)

        key_action_dict = {
            Key.ctrl_l : pressed_ctrl,
            Key.left : pressed_left,
            Key.right : pressed_right,
            Key.backspace : pressed_backspace,
            Key.delete : pressed_delete,
            Key.enter : search_tracks_with_typer,
            Key.esc : toggle_search_mode,
            Key.down : pressed_down,
            Key.up : pressed_up,
            Key.tab : pressed_tab,
        }


    def toggle_time_edit_mode():
        global time_edit_mode, key_action_dict, _k_a_d
        time_edit_mode = not time_edit_mode
        if time_edit_mode:
            _k_a_d = key_action_dict.copy()
            key_action_dict.update({
                'a' : adjust_time_left,  Key.left : adjust_time_left,
                'd' : adjust_time_right,  Key.right : adjust_time_right,
            })
        else:
            key_action_dict = _k_a_d

        return time_edit_mode

    def toggle_search_mode():
        global search_mode, key_action_dict, _k_a_d, search_typer, search_result_tracks

        search_mode = not search_mode
        

        if search_mode:
            set_listener_for_typer()
            
            _k_a_d = key_action_dict.copy()
            set_search_typer_for_key_dict()

            #search_typer.last_interaction_time = precise_time()
        else:
            set_listener_for_selector()

            key_action_dict = _k_a_d

            search_result_tracks = None
            
        return search_mode


    def place_search_results():
        amount = len(search_result_tracks)
        for row in range(amount):
            if search_result_tracks[row][0]:
                i,j = ART_PLACES['search_bar']
                display_map.add_map_array((i+3+row, j), np.array([ART_ARRAYS['search_bar'][1]]))
                l = len(ART_ARRAYS['search_bar'][0])-4
                track_text = search_result_tracks[row][0]
                if l< len(track_text):
                    track_text = track_text[:l-1] + '…'
                display_map.add_map_array((i+3+row, j+2), contracted_art_to_array([track_text], ART_COLORS['search_result_text']))

        display_map.add_map_array((i+3+amount, j), np.array([ART_ARRAYS['search_bar'][2]]))
###
##
general_functions()






def spotify_status_functions():
    global get_shuffle_status, update_shuffle_status
    global get_playing_status, update_playing_status
    global get_liked_status, update_liked_status
    global get_song_length, update_song_length
    global get_time, update_time
    global update_progress_bar
    global get_next_up_tracks, update_next_up_tracks
    global get_album_cover_url, download_image, get_album_cover_array, update_album_cover
    global get_lyrics, get_current_lyrics_part, update_lyrics
    global get_current_playlist_name, update_playlist_name
    global get_current_track_name, update_track_name
    global get_current_artists, update_artists
    global update_selector, update_search_bar
###
###
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


    def get_playing_status():
        if current:
            return current['is_playing']

    def update_playing_status():
        if current:
            playing_status = get_playing_status()
            place_art('pause' if playing_status else 'resume')
            
            return playing_status


    def get_liked_status():
        if current:
            track_id = current['item']['id']
            liked = sp.current_user_saved_tracks_contains([track_id])[0]
            
            return liked

    def update_liked_status(status):
        if current:
            place_art('liked' if status else 'like')


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

            display_map.add_map_array((row, col), contracted_art_to_array(['  /', ' / ', '/  '], ART_COLORS['3x3_slash']))

    def update_progress_bar(progress):
        progress = round(progress*60)
        progress_bar_string = "¤"*(progress-1) + "@" + "-"*(60-progress)
        progress_bar = list(progress_bar_string)
        progress_bar[0] = Fore.WHITE + progress_bar[0]
        if progress == 0:
            progress_bar[0] = f'{Fore.WHITE}@{rgb(100, 100, 100)}'
            progress_bar = progress_bar[:-1]
        elif progress != len(progress_bar):
            progress_bar[progress] = f"{rgb(100, 100, 100)}-"

        display_map.add_map_array(ART_PLACES['progress_bar'], np.array([progress_bar], dtype=np.object_))


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

            display_map.add_map_array(ART_PLACES['next_up_tracks'], contracted_art_to_array(next_up_tracks, ART_COLORS['next_up_tracks']))


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

    def get_album_cover_array():
        album_cover_url = get_album_cover_url() # 'https://i.scdn.co/image/ab67616d0000b27351c02a77d09dfcd53c8676d0' # 
        downloaded_image = download_image(album_cover_url)

        #for tw, th in ((30,30),(90,90)): Image.fromarray(downloaded_image.downscale(tw,th).array).save(f"album_cover-{tw}x{th}.png")

        album_cover_array = downloaded_image.to_color_shape_map(60,30).array

        return album_cover_array

    def update_album_cover(album_cover_array):
        if current:
            display_map.add_map_array(ART_PLACES['cover_art'], album_cover_array)



    def get_lyrics():
        def parse_lrc(lrc_content):
            timestamp_pattern = re.compile(r'\[(\d+):(\d+(?:\.\d+)?)\]')
            lyrics = []
            if not lrc_content:
                return " "
            for line in lrc_content.splitlines():
                timestamps = timestamp_pattern.findall(line)
                if timestamps:
                    lyric_text = timestamp_pattern.sub('', line).strip()
                    for minute, second in timestamps:
                        timestamp = int(minute) * 60 + float(second)
                        lyrics.append((timestamp, lyric_text))
            lyrics.sort(key=lambda x: x[0])
            return lyrics
        
        if current:
            lyrics = syncedlyrics.search(f"{get_current_track_name()} - {get_current_artists()}", synced_only=True)
            return parse_lrc(lyrics)
        else:
            return " "

    def get_current_lyrics_part(lyrics, current_time, previous_lines_count, next_lines_count):
        current_index = -1

        for i, (timestamp, line) in enumerate(lyrics):
            if current_time < timestamp:
                current_index = i - 1
                break
            current_index = i

        if not lyrics:
            current_index = -1

        start_index = max(0, current_index - previous_lines_count)
        end_index = min(len(lyrics), current_index + next_lines_count + 1)

        current_lyrics_part = lyrics[start_index:end_index]

        padding_needed_previous = previous_lines_count - (current_index - start_index)
        if padding_needed_previous > 0:
            padding_previous = [(-1, " ") for _ in range(padding_needed_previous)]
            current_lyrics_part = padding_previous + current_lyrics_part

        padding_needed_next = next_lines_count - (end_index - (current_index + 1))
        if padding_needed_next > 0:
            padding_next = [(-1, " ") for _ in range(padding_needed_next)]
            current_lyrics_part = current_lyrics_part + padding_next

        current_text = [text for _, text in current_lyrics_part]
        return current_text

    def update_lyrics(lyrics, current_time, previous_lines_count=2, next_lines_count=4):
        place_art('lyrics')

        if lyrics and lyrics[0] and 1< len(lyrics[0]):
            def get_two_rows(text, give_empty=True):
                if len(text)<= 33:
                    if not give_empty:
                        return [text]
                    else:
                        return [text, " "]

                first_row = " "
                second_row = " "
                for i in range(33, 0, -1):
                    if text[i] == ' ':
                        first_row = text[:i]
                        second_row = text[i+1:i+34]
                        if i+34< len(text):
                            for j in range(i+33, i+1, -1):
                                if text[j] == ' ':
                                    second_row = second_row[:(j-i-1)] + '…'
                                    break
                        break
                
                return [first_row, second_row]

            current_part = get_current_lyrics_part(lyrics, current_time, previous_lines_count, next_lines_count)
            text_rows = []

            is_multiple_rows = [33< len(text) for text in current_part]
            if is_multiple_rows[1]:
                text_rows += get_two_rows(current_part[1])
            elif is_multiple_rows[0]:
                text_rows += [get_two_rows(current_part[0])[1]] + [current_part[1]]
            else:
                text_rows += [current_part[0], current_part[1]]
            
            text_rows += get_two_rows(current_part[2])

            for i in range(3, len(current_part)):
                text_rows += get_two_rows(current_part[i], give_empty=False)
                if 7<= len(text_rows):
                    if len(text_rows) != 8:
                        text_rows += [get_two_rows(current_part[i+1])[0]]
                    break

            y, x = ART_PLACES['lyrics']
            for i, text_row in enumerate(text_rows):
                if i+1 == 3 or i +1 == 4:
                    color = rgb(200, 200, 200)
                else:
                    color = rgb(150, 150, 150)
                
                chars = list(text_row)
                if chars == [ ]: chars = ["♪"]
                chars[0] = color + chars[0]
                display_map.add_map_array((y, x), np.array([chars], dtype=np.object_))
                y += 1
                if i+1 == 2 or i+1 == 4:
                    y += 1
            

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
            return "Spotify's selection"

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

        display_map.add_map_array(ART_PLACES['track_name'], contracted_art_to_array([track_name], ART_COLORS['track_name']))
        
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

        display_map.add_map_array(ART_PLACES['artists'], contracted_art_to_array([artists], ART_COLORS['artists']))

        return artists
                

    def update_selector():
        if current:
            place_art('previous'); place_art('next')

            dt = precise_time() - action_selector.last_interaction_time
            if dt>5:
                if time_edit_mode: toggle_time_edit_mode()
            elif dt< 5 or time_edit_mode:
                if dt-int(dt)< 0.5 :
                    selected = action_selector.get_val()
                    i, j = ART_PLACES[selected]
                    if selected == "progress_bar":
                        j = j + max(0, round(progress*60)-1)
                        size = (1, 1)
                    elif selected == 'shuffle' or selected == 'like':
                        size = (5, 5)
                    else:
                        size = (3, 3)

                    display_map.add_map_array((i, j), contracted_art_to_array([f'#'*size[0]]*size[1], ART_COLORS['selector']))

    def update_search_bar():
        if current:
            if search_mode:
                place_art('search_bar')
                i, j = ART_PLACES['search_bar']
                dt = precise_time() - search_typer.last_interaction_time

                if dt-int(dt)< 0.5:
                    text = search_typer.get_with_cursor()
                else:
                    text = search_typer.get()
                
                display_map.add_map_array((i+1, j+2), contracted_art_to_array([text], ART_COLORS['search_text']))

                if 0.2< dt and (not search_result_tracks) and search_typer.text:
                    search_tracks_with_typer()
            
            if search_result_tracks:
                place_search_results()
###
##
spotify_status_functions()




def spotify_interact_functions():
    global toggle_shuffle
    global pause_resume
    global previous_track, next_track
    global like_unlike_current_song
    global adjust_time, adjust_time_left, adjust_time_right
    global search_tracks
###
###
    def toggle_shuffle():
        if current:
            current_shuffle_status = get_shuffle_status()

            if current_shuffle_status == 'no_shuffle':
                sp.shuffle(True)
            else:
                sp.shuffle(False)
            
            update_shuffle_status()


    def pause_resume():
        if 10< time_since_last_sync:
            sp.transfer_playback(DEVICE_ID)
            terminal_display.clear()
        elif current:
            if current['is_playing']:
                sp.pause_playback()
            else:
                sp.start_playback()

            update_playing_status()


    def previous_track():
        try:
            sp.previous_track()
        except:
            pass
    def next_track():
        sp.next_track()


    def like_unlike_current_song():
        global liked_status

        if current:
            track_id = current['item']['id']
            liked = get_liked_status()
            if liked:
                sp.current_user_saved_tracks_delete([track_id])
            else:
                sp.current_user_saved_tracks_add([track_id])

            liked_status = not liked_status


    def adjust_time(dir=+1, change=15):
        global current_time, progress
        if current:
            new_time = max(0, min((current_time + dir*change), get_song_length()-0.1))
            current_time = new_time
            progress = new_time / song_length
            sp.seek_track(int(new_time*1000), DEVICE_ID)

    def adjust_time_left():
        adjust_time(-1)
        action_selector.last_interaction_time = precise_time()

    def adjust_time_right():
        adjust_time(+1)
        action_selector.last_interaction_time = precise_time()


    def search_tracks(query:str, limit=5):
        global search_result_tracks

        if query:
            results = sp.search(q=query, type='track', limit=limit)['tracks']['items']
            search_result_tracks = [(f"{track['name']} - {', '.join(artist['name'] for artist in track['artists'])}",track['uri']) for track in results]
            return search_result_tracks
        else:
            return None
        #sp.start_playback(uris=[track_uri])
###
##
spotify_interact_functions()





def main_loop():
    global sp, current, current_time, song_length, progress, liked_status, time_since_last_sync, album_cover_array, DEVICE_ID

    last_request_time, last_calculated_time, lyrics, playing_status, previous_name = (precise_time()-buffer-0.1, 0, "", False, "")


    display_map.fill()

    arts_to_place = (
        'playing_from', 'playlist',
        'cover_art',
        'progress_bar',
        'artists', 'track_name',
        'next_up', 'next_up_serials', 'next_up_tracks', 'next_up_xs',
        'hour_dots', '5x4_minute_1', '5x4_minute_0', 'divider_colon', '5x4_second_1', '5x4_second_0',
        'no_shuffle', 'previous', 'resume', 'next', 'like',
        'lyrics',
    )
    for art in arts_to_place: place_art(art)


    while True:
        try:
            if buffer< precise_time() - last_request_time:
                current = sp.current_playback()

                if current:
                    current_time = get_time()
                    last_calculated_time = current_time

                    last_request_time = precise_time()

                    update_playlist_name()
                    
                    if current['item']:
                        if previous_name != current['item']['name']:
                            album_cover_array = get_album_cover_array()
                            update_next_up_tracks()
                            song_length = get_song_length()
                            update_song_length(song_length)
                            lyrics = get_lyrics()
                            update_track_name()
                            update_artists()
                            liked_status = get_liked_status()

                        previous_name = current['item']['name']
                else:
                    previous_name = None
                
            else:
                if playing_status and current_time< song_length:
                    current_time = last_calculated_time + precise_time()-last_request_time

            update_time(current_time)
            
            progress = current_time/song_length
            update_progress_bar(progress)
            
            update_lyrics(lyrics, current_time)
            
            update_shuffle_status()
            playing_status = update_playing_status()

            update_liked_status(liked_status)

            update_selector()

            update_album_cover(album_cover_array)

            update_search_bar()

            terminal_display.update(display_map, 12)

            time_since_last_sync = round(precise_time() - last_request_time,1)
            sys.stdout.write(f'\n{rgb(55, 55, 55)}Last Sync:{rgb(30, 40, 40)} {time_since_last_sync} ')

            if 10< time_since_last_sync:
                sys.stdout.write(f'{rgb(120, 55, 55)}+')
                ensure_spotify_is_running()
                DEVICE_ID = get_preferred_device_id()
                if not playing_status:
                    sp.pause_playback()

        except Exception as e:
            sys.stdout.write(f'{rgb(120, 55, 55)}|Error| {e}')
            sys.stdout.flush()





# ///==================== Main thread ====================\\\
                                                            #
if __name__ == "__main__":                                  #
    # ~~ Guess terminal as currently focused window         #
    TERMINAL_WINDOW_ID = GetForegroundWindow()              #
                                                            #
    # ~~ Initialize colorama, Clear output, Hide cursor     #
    colorama.init()                                         #
    os.system('cls')                                        #
    stdout.write("\033[?25l")                               #
                                                            #
    # ~~ Ensure Spotify                                     #
    ensure_spotify_is_running()                             #
    # ~~ Focus back on terminal window                      #
    SetForegroundWindow(TERMINAL_WINDOW_ID)                 #
                                                            #
    # ~~ Set globals                                        #
    globalize_screener_values()                             #
    globalize_time_convert_values()                         #
    globalize_ART_values()                                  #
    globalize_spotify_values()                              #
    globalize_key_action_dict()                             #
    globalize_action_selector()                             #
    globalize_mode_values()                                 #
                                                            #
    # ~~ Start listener                                     #
    set_listener_for_selector()                             #
                                                            #
    # ~~ Choose device                                      #
    DEVICE_ID = get_preferred_device_id()                   #
                                                            #
    # ~~ Use action_selector                                #
    set_action_selector_for_key_dict()                      #
                                                            #
    # ~~ Enter main loop                                    #
    main_loop()                                             #
                                                            #
# \\\================== Main thread end ==================///
                                                             