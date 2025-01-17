from time import time as epoch_now
from time import perf_counter as precise_time
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

DOT = (os.path.dirname(__file__)).replace('\\','/')

OPAS = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")

THRESHOLDS = (19.92, 36.93, 39.75, 39.84, 42.89, 53.66, 54.4, 62.83, 69.53, 74.17, 105.29, 106.47, 108.4, 109.08, 111.08, 116.27, 117.73, 123.66, 125.45, 125.71, 128.68, 130.03, 131.86, 132.5, 135.4, 137.24, 137.5, 142.01, 142.56, 142.75, 143.7, 146.49, 146.71, 147.49, 148.18, 149.43, 149.48, 153.02, 153.36, 155.5, 156.51, 157.07, 157.39, 157.42, 157.54, 157.6, 157.9, 162.86, 163.27, 165.91, 166.07, 167.35, 167.53, 169.5, 170.98, 172.68, 174.85, 181.89, 182.69, 185.28, 185.88, 186.98, 188.07, 188.71, 194.11, 194.94, 195.06, 195.96, 196.18, 196.41, 196.81, 197.21, 197.27, 198.77, 200.79, 203.01, 204.88, 210.01, 212.57, 215.11, 218.92, 219.69, 221.34, 223.96, 232.33, 232.41, 232.83, 233.37, 240.17, 243.34, 255.0)

CHAR_WIDTH_PER_HEIGHT = 78/155


def print_separate(val_1, space_between:str, val_2):
    val_1_string = str(val_1)
    val_1_len = len(val_1_string)

    val_2_string = str(val_2)

    stdout.write(val_1_string + space_between[val_1_len : ] + val_2_string)


class CharacterMap:
    def __init__(self, width:int, height:int, d_list:tuple=None, filler:str=' '): 
        if d_list:
            self.width = len(d_list[0])
            self.height = len(d_list)
            self.array = np.array(d_list, dtype='<U1')
        else:
            self.width = width
            self.height = height
            self.array = np.full(((height, width)), filler, dtype='<U1')

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

    def add_map_array(self, row:int, col:int, added_array:np.array, exclude_chars:tuple=()):
        height, width = self.array.shape
        added_height, added_width = added_array.shape

        start_row = max(0, row); end_row = min(height, row + added_height); start_col = max(0, col); end_col = min(width, col + added_width)
        local_start_row = max(0, -row); local_end_row = min(added_height, height - row); local_start_col = max(0, -col); local_end_col = min(added_width, width - col)

        mask = ~np.isin(added_array[local_start_row:local_end_row, local_start_col:local_end_col], exclude_chars)

        self.array[start_row:end_row, start_col:end_col][mask] = added_array[local_start_row:local_end_row, local_start_col:local_end_col][mask]
        
        return self.array
    
    def replace(self, replace_what=',', replace_with=' '):
        self.array[self.array == replace_what] = replace_with
        
        return self.array

    def render_char(self, char_width:int, char_height:int, char_col:int, char_row:int):
        shown = (0-char_width <= char_col <= self.array.width) and (0-char_height <= char_row <= self.array.height)
        if shown:
            self.array.add_map_array(col=int(char_col), row=int(char_row), added_array=self.array, exclude_chars=(" "))
        
        return shown


class TerminalDisplay:
    def __init__(self, height:int=512):
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
        output = "\n" + "\n".join(("".join(row) for row in display_map.array))
        self.to_beginning()
        stdout.write(output)
        stdout.flush()

    def update(self, display_map:CharacterMap, fps:float=0):

        start_time = precise_time()
        if fps == 0:
            self.write(display_map)
        else:
            stay_seconds = int(10000/fps)/10000

            self.write(display_map)

            while precise_time() - start_time < stay_seconds :
                pass


class CustomImage:
    def __init__(self, image_array=np.array([]), character:str=None):
        self.array = image_array
        self.char = character

    def gray(self):
        self.array = cv2.cvtColor(np.array(self.array), cv2.COLOR_RGB2GRAY)
        return self

    def downscale(self, target_width:int, target_height:int):
        if target_width == 1 and target_height == 1:
            self.array = np.array(np.array(self.char))
        else:
            self.array = cv2.resize(self.array, (target_width, target_height), interpolation=cv2.INTER_AREA)
        return self

    def be_screenshot(self):
        self.array = np.array(take_screenshot())
        return self
    
    def save_as_img(self, name:str='image'):
        image = Image.fromarray(self.array)
        return image.save(f'{name}.png')
    
    def save_as_text(self, name:str='text'):
        return np.savetxt(f'{name}.txt', self.array, fmt='%f', delimiter=' ')
    
    def to_map(self, target_width=-1, target_height=-1, grayed=False, sized=False):
        if not grayed: self.gray()
        if not sized: self.downscale(target_width, target_height)

        indices = np.digitize(self.array, THRESHOLDS)
        img_map = CharacterMap(width=target_width, height=target_height)
        img_map.array[:] = np.array(OPAS)[indices]
        
        return img_map


ART_DICT = {
    '0' : (".o.", "| |", "'0'"),
    '1' : (".~1", "  |", "  |"),
    '2' : ("˛=,", " ,I", "2__"),
    '3' : ("˙´\\", " ~3", ".˛/"),
    '4' : ("/  ", "4+*", " | "),
    '5' : ("_~~", "5o.", "--/"),
    '6' : ("˛o.", "6*.", "˙o˙"),
    '7' : ("\"\"7", " / ", "*  "),
    '8' : (",o,", ",8,", "˙o˙"),
    '9' : (".o,", "´~9", " / "),
    'previous' : (" .-", "<:|", " ˙-"),
    'pause' :    ("¤ ¤", "O O", "¤ ¤"),
    'resume' :   ("¤. ", "O]>", "¤˙ "),
    'next' :     ("-. ", "|:>", "-˙ "),
    'no_shuffle' :    (".¸ ˛.", "  =  ", "˙´ `˙"),
    'shuffle' :       ("~¸ ˛>", "  ¤  ", "~´ `>"),
    'smart_shuffle' : ("@¸ ˛>", "  ¤  ", "~´ `>"),
    'like' :  (",-.-,", "', ,'", "  `  "),
    'liked' : (",=_=,", "\\"+"%"+"X%/", " ˇ÷ˇ ")
}
for key in ART_DICT.keys():
    m = tuple(tuple(string) for string in ART_DICT[key])
    ART_DICT[key] = np.array(m)



"""import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id='67c0740055b9412da3e1e14978c42742',
        client_secret='4116025cf230497699d6feb972d8bfc7',
        redirect_uri='http://localhost'
    )
)"""


def song_view():
    display_map.fill()

    display_map.add_map_array(31, 65, ART_DICT['smart_shuffle'])

    display_map.add_map_array(31, 72, ART_DICT['previous'])
    display_map.add_map_array(31, 77, ART_DICT['pause'])
    display_map.add_map_array(31, 82, ART_DICT['next'])

    display_map.add_map_array(31, 87, ART_DICT['liked'])

    terminal_display.update(display_map)

    """wait_seconds(2)
    display_map.add_map_array(31, 65, ART_DICT['no_shuffle'])
    terminal_display.update(display_map)

    wait_seconds(2)
    display_map.add_map_array(31, 65, ART_DICT['shuffle'])
    terminal_display.update(display_map)"""



if __name__ == "__main__":

    colorama.init() # Initialize terminal formatting

    window_width = 96
    window_height = 36

    os.system('cls')

    terminal_display = TerminalDisplay(window_height)

    display_map = CharacterMap(window_width, window_height, filler=' ')

    song_view()

    print(colorama.Style.RESET_ALL)
