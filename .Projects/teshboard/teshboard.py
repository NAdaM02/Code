import os
import requests
from datetime import datetime, date, timezone
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import icalendar
from time import sleep as wait
import feedparser
from newspaper import Article

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt_tab')


def classes():
    global CharacterMap, TerminalDisplay, CustomImage
    global Selector, Typer

    import numpy as np
    import cv2
    import os
    from scipy.spatial.distance import cdist
    from sys import stdout
    from time import perf_counter as precise_time
    from colorama import Fore
    global DOT, OPAS, THRESHOLDS, CHARACTER_SHAPES
    DOT = (os.path.dirname(__file__)).replace('\\','/')
    OPAS = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")
    THRESHOLDS = (19.92, 36.93, 39.75, 39.84, 42.89, 53.66, 54.4, 62.83, 69.53, 74.17, 105.29, 106.47, 108.4, 109.08, 111.08, 116.27, 117.73, 123.66, 125.45, 125.71, 128.68, 130.03, 131.86, 132.5, 135.4, 137.24, 137.5, 142.01, 142.56, 142.75, 143.7, 146.49, 146.71, 147.49, 148.18, 149.43, 149.48, 153.02, 153.36, 155.5, 156.51, 157.07, 157.39, 157.42, 157.54, 157.6, 157.9, 162.86, 163.27, 165.91, 166.07, 167.35, 167.53, 169.5, 170.98, 172.68, 174.85, 181.89, 182.69, 185.28, 185.88, 186.98, 188.07, 188.71, 194.11, 194.94, 195.06, 195.96, 196.18, 196.41, 196.81, 197.21, 197.27, 198.77, 200.79, 203.01, 204.88, 210.01, 212.57, 215.11, 218.92, 219.69, 221.34, 223.96, 232.33, 232.41, 232.83, 233.37, 240.17, 243.34, 255.0)
    CHARACTER_SHAPES = (((9.2, 246.45, 0.36), (0.0, 15.92, 1.84), (0.0, 0.0, 0.0)), ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 146.16, 0.0)),((0.0, 0.0, 0.0), (121.82, 161.49, 122.78), (0.0, 0.0, 0.0)),((0.0, 151.87, 0.0), (0.0, 143.26, 0.0), (0.0, 0.0, 0.0)),((0.0, 0.0, 0.0), (0.0, 148.64, 0.0), (0.0, 145.96, 0.0)),((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (118.91, 157.64, 119.83)),((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 314.2, 0.0)),((12.7, 224.55, 13.54), (82.08, 97.76, 83.54), (0.0, 0.0, 0.0)),((0.0, 0.0, 0.0), (243.37, 322.61, 245.28), (0.0, 0.0, 0.0)),((0.0, 0.0, 0.0), (0.0, 148.52, 0.0), (0.0, 314.19, 0.0)),((26.35, 0.0, 0.0), (183.28, 355.89, 212.25), (28.8, 0.0, 0.0)),((0.0, 0.0, 26.04), (205.27, 339.49, 181.82), (0.0, 0.0, 28.37)),((0.0, 56.04, 0.0), (121.94, 434.58, 122.89), (0.0, 58.25, 0.0)),((0.0, 142.66, 0.0), (0.0, 259.75, 0.0), (0.0, 146.03, 0.0)),((0.0, 0.0, 0.0), (213.4, 294.99, 205.79), (149.89, 189.54, 0.0)),((0.0, 0.0, 0.0), (292.51, 176.27, 127.7), (87.63, 177.65, 94.9)),((0.0, 32.66, 0.0), (181.48, 448.31, 183.35), (7.17, 1.02, 7.29)),((0.0, 27.57, 205.16), (8.76, 325.21, 27.76), (174.45, 56.14, 0.0)),((0.0, 0.0, 0.0), (114.68, 388.89, 146.66), (142.24, 180.73, 95.6)),((115.79, 178.18, 99.57), (1.81, 223.96, 111.66), (0.0, 146.75, 0.0)),((0.0, 0.0, 0.0), (200.64, 340.5, 187.72), (97.49, 164.93, 120.92)),((141.99, 0.0, 0.0), (354.36, 0.0, 0.0), (153.27, 161.6, 122.99)),((132.08, 219.56, 133.17), (0.0, 354.87, 0.0), (0.0, 141.04, 0.0)),((0.0, 0.0, 0.0), (271.61, 143.52, 273.5), (9.09, 230.46, 9.73)),((79.32, 230.21, 22.77), (0.0, 157.31, 203.41), (78.39, 228.11, 22.13)),((0.0, 127.84, 164.43), (73.54, 0.0, 354.94), (126.97, 163.48, 101.78)),((175.23, 164.46, 194.53), (85.01, 198.7, 190.97), (0.0, 154.96, 0.0)),((21.78, 229.87, 80.33), (199.77, 160.49, 0.0), (21.13, 227.67, 79.27)),((0.0, 282.01, 0.0), (0.0, 355.97, 0.0), (0.0, 280.77, 0.0)),((146.51, 164.26, 133.25), (359.35, 164.61, 59.0), (141.14, 0.0, 0.0)),((0.0, 146.15, 2.28), (73.62, 406.6, 0.0), (95.34, 216.23, 120.51)),((0.0, 252.76, 69.87), (57.29, 386.48, 0.0), (0.0, 253.06, 68.84)),((81.12, 175.41, 138.92), (378.41, 0.32, 0.0), (85.75, 176.77, 116.29)),((69.11, 253.45, 0.0), (0.0, 385.16, 58.54), (68.13, 254.27, 0.0)),((0.0, 200.11, 129.53), (135.12, 434.79, 101.69), (0.0, 143.14, 0.0)),((96.0, 219.73, 96.76), (0.0, 355.92, 0.0), (94.45, 217.33, 95.2)),((106.64, 172.18, 108.33), (9.62, 195.48, 256.12), (97.52, 166.19, 102.68)),((92.58, 197.85, 0.0), (0.35, 356.42, 0.0), (93.74, 217.35, 103.29)),((38.02, 88.53, 0.0), (216.0, 353.96, 94.49), (14.83, 195.76, 105.72)),((122.97, 184.7, 0.0), (0.0, 358.25, 0.0), (0.0, 188.76, 106.37)),((0.0, 0.0, 0.0), (338.91, 17.49, 324.65), (127.21, 149.57, 196.44)),((32.98, 295.25, 82.78), (49.03, 306.97, 0.0), (32.68, 292.54, 81.89)),((0.0, 0.0, 0.0), (343.76, 165.91, 310.29), (143.55, 0.0, 143.57)),((0.0, 0.0, 0.0), (314.37, 314.31, 251.41), (93.04, 170.07, 77.21)),((0.0, 0.0, 0.0), (304.73, 183.13, 306.3), (99.62, 180.66, 100.99)),((103.5, 171.6, 159.64), (48.24, 301.93, 49.94), (156.44, 169.05, 110.64)),((112.57, 174.22, 83.44), (196.95, 177.83, 256.37), (115.6, 166.08, 121.97)),((147.31, 0.0, 147.42), (93.71, 381.18, 95.15), (0.0, 141.12, 0.0)),((0.0, 0.0, 0.0), (135.04, 396.15, 133.46), (116.57, 84.51, 118.12)),((0.0, 98.22, 50.01), (55.67, 306.91, 143.23), (91.83, 302.23, 91.82)),((0.0, 0.0, 0.0), (273.07, 125.44, 284.62), (144.45, 404.74, 22.51)),((0.0, 0.0, 0.0), (194.09, 337.25, 222.76), (149.58, 140.1, 189.13)),((81.81, 293.91, 34.7), (0.0, 303.85, 51.62), (80.93, 291.21, 34.41)),((118.18, 173.61, 93.31), (8.13, 190.84, 203.74), (152.24, 194.2, 113.1)),((154.63, 164.26, 125.01), (366.98, 164.06, 50.48), (153.27, 161.6, 122.99)),((105.71, 169.41, 99.07), (150.37, 206.65, 162.71), (112.26, 161.5, 116.47)),((0.0, 0.0, 0.0), (308.6, 378.47, 313.41), (141.74, 125.78, 126.02)),((0.0, 0.0, 0.0), (322.79, 152.33, 342.28), (128.18, 147.14, 356.14)),((182.44, 0.0, 0.0), (373.49, 229.74, 249.68), (144.42, 21.11, 154.15)),((154.46, 166.4, 122.55), (366.9, 166.5, 280.66), (140.83, 0.0, 0.0)),((23.41, 172.31, 73.27), (367.11, 170.75, 252.47), (114.58, 168.11, 119.82)),((181.15, 0.0, 0.0), (367.78, 158.5, 310.16), (143.41, 0.0, 143.43)),((107.51, 169.68, 114.2), (254.76, 164.63, 376.95), (67.45, 175.64, 32.23)),((0.0, 0.0, 181.11), (324.52, 154.12, 371.54), (130.12, 152.26, 147.31)),((75.2, 49.24, 127.68), (392.08, 199.3, 372.6), (0.0, 14.04, 126.64)),((144.75, 0.0, 144.76), (250.69, 187.88, 252.93), (7.61, 235.89, 8.32)),((0.0, 0.0, 0.0), (347.85, 156.83, 325.68), (356.24, 151.9, 131.24)),((109.78, 172.04, 110.76), (368.24, 0.0, 368.43), (111.88, 169.2, 112.93)),((93.57, 171.62, 129.89), (376.59, 78.91, 207.66), (100.52, 170.6, 164.61)),((181.18, 0.0, 0.0), (368.5, 158.05, 325.87), (157.32, 160.45, 86.76)),((141.69, 0.0, 142.43), (354.15, 0.0, 354.38), (111.19, 173.1, 110.41)),((5.01, 231.47, 5.43), (250.13, 353.43, 253.17), (140.3, 0.0, 140.31)),((141.81, 0.0, 140.58), (371.32, 265.92, 219.42), (140.65, 4.14, 158.88)),((142.54, 20.09, 142.93), (70.82, 487.91, 72.8), (139.75, 22.52, 140.57)),((141.69, 0.0, 142.67), (374.8, 165.53, 377.36), (140.54, 0.0, 141.51)),((0.0, 0.0, 0.0), (354.73, 349.75, 361.41), (143.43, 123.06, 144.87)),((114.89, 171.66, 115.88), (295.98, 197.49, 297.37), (124.01, 164.45, 124.79)),((162.54, 167.11, 119.27), (374.66, 217.61, 295.9), (140.54, 5.33, 154.13)),((162.47, 174.0, 88.41), (353.62, 0.0, 372.21), (161.19, 170.41, 93.56)),((40.13, 96.11, 105.08), (322.6, 428.49, 326.77), (102.71, 95.09, 41.22)),((105.75, 303.86, 99.35), (150.37, 372.58, 162.73), (112.63, 296.14, 116.84)),((154.46, 170.67, 100.67), (366.9, 173.03, 305.02), (153.26, 163.47, 149.51)),((0.0, 0.0, 0.0), (324.65, 157.1, 347.19), (223.11, 329.87, 284.65)),((93.8, 179.68, 95.14), (366.59, 156.06, 365.96), (95.96, 176.56, 97.18)),((179.7, 105.66, 180.87), (342.96, 300.89, 345.29), (134.8, 0.0, 135.57)),((170.54, 51.81, 142.24), (360.13, 280.92, 359.05), (141.51, 50.96, 170.1)),((141.61, 0.0, 141.61), (337.71, 403.03, 337.82), (147.39, 146.33, 148.77)),((109.78, 172.04, 110.76), (368.32, 0.0, 368.25), (111.99, 347.85, 200.46)),((154.52, 132.67, 0.0), (259.87, 410.84, 270.21), (0.43, 123.8, 162.2)),((85.36, 187.22, 89.1), (315.45, 268.92, 200.51), (157.23, 176.94, 171.74)),((82.65, 165.65, 105.93), (292.41, 372.71, 342.46), (164.06, 263.04, 109.96)),)
    
    global contracted_art_to_array
    def contracted_art_to_array(art, color:str= Fore.WHITE, end_color:str= Fore.WHITE) -> np.array:
        l = []
        for string in art:
            s = list(string)
            if color:
                for i in range(len(s)): s[i] = color + s[i] + end_color
            else:
                s[-1] = s[-1] + end_color
            l.append(s)

        return np.array(l)
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
            
        def fill(self, fill='??') -> np.array:
            if fill == '??':
                filler = self.filler
            else:
                filler = fill

            self.array[:, :] = filler
            return self.array
        
        def get_subarray(self, first_rows:int= None, last_rows:int= None, first_columns:int= None, last_columns:int= None) -> np.array:
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

        def add_map_array(self, position:tuple[int, int]= ('row','col'), added_array:np.array= (), exclude_chars:tuple[str, ...]= ()) -> np.array:
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
        
        def replace(self, replace_what:str= ',', replace_with:str= ' ') -> np.array:
            self.array[self.array == replace_what] = replace_with
            
            return self.array

    class TerminalDisplay:
        def __init__(self, height:int= 512):
            self.height = height

        def to_beginning(self):
            stdout.write(f"\033[{self.height+1}A\033[2K\n")
        
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

        def downscale(self, target_width:int, target_height:int, method=cv2.INTER_LINEAR_EXACT) -> any:
            self.array = cv2.resize(self.array, (target_width, target_height), interpolation=method)

            return self

        def to_color_shape_map(self, target_width:int= -1, target_height:int= -1, downscale_method:int= cv2.INTER_LINEAR_EXACT) -> np.array:

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
        def __init__(self, field_values:tuple[tuple[any, ...], ...], field_actions:tuple[tuple[any, ...], ...]= None, starting_position:tuple[int, int]=[0, 0]):
            """restricted zones : -1"""
            self.field_values = field_values
            x, y = starting_position
            i, j = len(field_values)-y-1, x
            self.position = [i, j]
            self.last_interaction_time = 0
            self.field_actions = field_actions

        def get_position(self) -> tuple[int, int]:
            i, j = self.position
            x, y = len(self.field_values)-i-1, j
            return [x, y]

        def move_to(self, place:tuple[int, int]):
            i, j = self.position
            x, y = place
            new_i, new_j = len(self.field_values)-y-1, x

            self.last_interaction_time = precise_time()
            
            if 0<= new_i< len(self.field_values) and 0<= new_j< len(self.field_values[0]):

                if self.field_values[new_i][new_j] != -1 and self.field_values[new_i][new_j] != self.field_values[i][j]:
                    self.position = new_i, new_j

        def move(self, direction:tuple[int, int]):
            i, j = self.position
            dx, dy = direction
            di, dj = -dy, dx
            new_i, new_j = i+di, j+dj

            self.last_interaction_time = precise_time()
            
            if 0<= new_i< len(self.field_values) and 0<= new_j< len(self.field_values[0]):

                if self.field_values[new_i][new_j] != -1 and self.field_values[new_i][new_j] != self.field_values[i][j]:
                    self.position = new_i, new_j
        
        def get_val(self) -> any:
            i, j = self.position
            return self.field_values[i][j]
        
        def call_action(self) -> any:
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
        
        def get_with_cursor(self, cursor:str= "_") -> str:
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

# ─────────────────────────────────────────────────────────────────────────────
#                             LOAD ENVIRONMENT
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()
OPENWEATHER_KEY    = os.getenv('OPENWEATHER_KEY')
NEWSAPI_KEY        = os.getenv('NEWSAPI_KEY')
CALENDAR_ICS_URL   = os.getenv('CALENDAR_ICS_URL')
SPOTIFY_CLIENT_ID     = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# ─────────────────────────────────────────────────────────────────────────────
#                              DATA FETCHERS
# ─────────────────────────────────────────────────────────────────────────────
def get_weather(city:str= 'Budapest'):
    r = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={'q': city, 'units': 'metric', 'appid': OPENWEATHER_KEY}
    ).json()
    desc = r['weather'][0]['description'].title()
    temp = round(r['main']['temp'])
    return f"{desc}, {temp}°C"


def get_headlines(count:int= 3):
    d = feedparser.parse('https://telex.hu/rss')
    if d.bozo:
        return []
    return [(e.title, e.link) for e in d.entries[:count]]

def fetch_full_text(url: str) -> str:
    art = Article(url, language='hu')
    art.download()
    art.parse()
    return art.text  # plain text of the article

def summarize(text: str) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=1)
    return " ".join(str(s) for s in summary)

def get_calendar_events() -> list:
    now = datetime.now(timezone.utc)
    events = []
    cal = icalendar.Calendar.from_ical(requests.get(CALENDAR_ICS_URL).content)
    for comp in cal.walk():
        if comp.name!='VEVENT': continue
        start = comp.get('dtstart').dt

        if isinstance(start, date) and not isinstance(start, datetime):
            start = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
        elif isinstance(start, datetime) and start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if start>now and len(events)<3:
            events.append((start, str(comp.get('summary'))))

    events.sort(key=lambda x: x[0])
    return [f"{dt.astimezone().strftime('%d %b %H:%M')} {title}" for dt, title in events]

def get_spotify_status() -> str:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri='http://localhost:8888/callback',
            scope='user-read-playback-state'
        ))
        cur = sp.current_playback()
        if cur and cur.get('item'):
            t = cur['item']
            return f"♪ {t['name']} - {t['artists'][0]['name']}"
        return "♪ Paused"
    except:
        return "No songs playing"

# ─────────────────────────────────────────────────────────────────────────────
#                             RENDER DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def draw_dashboard():
    W, H = 200, 36
    display_map = CharacterMap(W, H, filler=' ')
    display_map.fill()

    # Header
    now = datetime.now().strftime('%H:%M:%S %d-%b-%Y')
    header = f"{now} | {get_weather()}"
    for i, ch in enumerate(header):
        display_map[i, H-2] = ch

    # Events
    evs = get_calendar_events()
    for i, line in enumerate(["Events:"] + evs):
        display_map.add_map_array((4+i, 0), contracted_art_to_array([line]))

    # News
    news = get_headlines(3)
    for idx, (title, url) in enumerate(news):
        display_map.add_map_array((10+3*idx, 0), contracted_art_to_array([title]))
        full_text = fetch_full_text(url)
        summary = summarize(full_text)
        #terminal_display.clear()
        #print(full_text)
        #print()
        #print(summary)
        #wait(10)
        display_map.add_map_array((10+3*idx+1, 0), contracted_art_to_array([summary]))
        display_map.add_map_array((10+3*idx+2, 0), contracted_art_to_array([summary[W:]]))

    # Spotify
    sp = get_spotify_status()
    for i, ch in enumerate(sp):
        display_map[i, 1] = ch

    return display_map

# ─────────────────────────────────────────────────────────────────────────────
#                                MAIN LOOP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    global terminal_display
    terminal_display = TerminalDisplay(38)
    
    terminal_display.clear()
    while True:
        terminal_display.update(draw_dashboard())
        wait(60)

if __name__ == "__main__":
    main()
