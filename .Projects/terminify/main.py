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
from colorama import Fore, Style
from spotipy.exceptions import SpotifyException

import logging
logging.getLogger().setLevel(logging.ERROR)


TIME_CONVERT_LIST = (29030400, 604800, 86400, 3600, 60, 1)
TIME_CHAR_LIST = ('y', 'w', 'd', 'h', 'm', 's')
COLORS = [
    Fore.BLACK, Fore.BLUE, Fore.CYAN, Fore.GREEN,
    Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

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

CHAR_WIDTH_PER_HEIGHT = 78/155


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

        # Ensure dtype is object to preserve ANSI escape codes
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
        shown = (0-char_width <= char_col <= self.array.width) and (0-char_height <= char_row <= self.array.height)
        if shown:
            self.array.add_map_array((int(char_col), int(char_row)), self.array, exclude_chars=(" "))
        
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

    def update(self, display_map:CharacterMap, fps:float= 0):

        start_time = precise_time()
        if fps == 0:
            self.write(display_map)
        else:
            stay_seconds = int(10000/fps)/10000

            self.write(display_map)

            while precise_time() - start_time < stay_seconds :
                pass


class CustomImage:
    def __init__(self, image_array:np.array= ()):
        self.array = np.array(image_array)

    def gray(self):
        gray = cv2.cvtColor(self.array, cv2.COLOR_RGB2GRAY)
        gamma = 1.5  # Adjust gamma for higher contrast
        enhanced_gray = np.power(gray / 255.0, gamma) * 255.0
        enhanced_gray = np.clip(enhanced_gray, 0, 255).astype(np.uint8)
        """image = self.array
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)"""
        self.array = enhanced_gray

        #self.array = cv2.cvtColor(self.array, cv2.COLOR_RGB2GRAY)
        return self.array

    def downscale(self, target_width:int, target_height:int):
        self.array = cv2.resize(self.array, (target_width, target_height), interpolation=cv2.INTER_AREA)
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
        img_map = CharacterMap(width=target_width, height=target_height)
        img_map.array[:] = np.array(OPAS)[indices]
        
        return img_map
    
    def to_colorized_map(self, target_width:int= -1, target_height:int= -1):
        self.downscale(target_width, target_height)

        colorized_map = CharacterMap(width=target_width, height=target_height, U1dtype=False)

        for y in range(target_height):
            for x in range(target_width):
                r, g, b = self.array[y, x].astype(np.int32)

                luminance = 0.299 * r + 0.587 * g + 0.114 * b  

                char_index = np.digitize(luminance, THRESHOLDS, right=True)
                char_index = max(0, min(char_index, len(OPAS) - 1))
                ascii_char = OPAS[char_index]

                total = max(r + g + b, 1)
                r_ratio, g_ratio, b_ratio = r / total, g / total, b / total  

                if luminance > 200:
                    color = Fore.WHITE
                elif luminance > 150:
                    if r_ratio > 0.5:
                        color = Fore.LIGHTRED_EX
                    elif g_ratio > 0.5:
                        color = Fore.LIGHTGREEN_EX
                    elif b_ratio > 0.5:
                        color = Fore.LIGHTBLUE_EX
                    else:
                        color = Fore.LIGHTWHITE_EX
                elif luminance > 100:
                    if r_ratio > 0.5 and g_ratio > 0.4:
                        color = Fore.LIGHTYELLOW_EX
                    elif g_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.LIGHTCYAN_EX
                    elif r_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.LIGHTMAGENTA_EX
                    elif r_ratio > 0.5:
                        color = Fore.RED
                    elif g_ratio > 0.5:
                        color = Fore.GREEN
                    elif b_ratio > 0.5:
                        color = Fore.BLUE
                    else:
                        color = Fore.LIGHTBLACK_EX
                elif luminance > 50:
                    if r_ratio > 0.5 and g_ratio > 0.4:
                        color = Fore.YELLOW
                    elif g_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.CYAN
                    elif r_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.MAGENTA
                    elif r_ratio > 0.5:
                        color = Fore.RED
                    elif g_ratio > 0.5:
                        color = Fore.GREEN
                    elif b_ratio > 0.5:
                        color = Fore.BLUE
                    else:
                        color = Fore.BLACK
                else:
                    color = Fore.BLACK

                colorized_map.array[y, x] = color + ascii_char + Fore.WHITE

        return colorized_map
    
    def to_colorized_map(self, target_width:int= -1, target_height:int= -1):
        self.downscale(target_width, target_height)

        colorized_map = CharacterMap(width=target_width, height=target_height, U1dtype=False)

        for y in range(target_height):
            for x in range(target_width):
                r, g, b = self.array[y, x].astype(np.int32)

                luminance = 0.299 * r + 0.587 * g + 0.114 * b  

                char_index = np.digitize(luminance, THRESHOLDS, right=True)
                char_index = max(0, min(char_index, len(OPAS) - 1))
                ascii_char = OPAS[char_index]

                total = max(r + g + b, 1)
                r_ratio, g_ratio, b_ratio = r / total, g / total, b / total  

                if luminance > 200:
                    color = Fore.WHITE
                elif luminance > 150:
                    if r_ratio > 0.5:
                        color = Fore.LIGHTRED_EX
                    elif g_ratio > 0.5:
                        color = Fore.LIGHTGREEN_EX
                    elif b_ratio > 0.5:
                        color = Fore.LIGHTBLUE_EX
                    else:
                        color = Fore.LIGHTWHITE_EX
                elif luminance > 100:
                    if r_ratio > 0.5 and g_ratio > 0.4:
                        color = Fore.LIGHTYELLOW_EX
                    elif g_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.LIGHTCYAN_EX
                    elif r_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.LIGHTMAGENTA_EX
                    elif r_ratio > 0.5:
                        color = Fore.RED
                    elif g_ratio > 0.5:
                        color = Fore.GREEN
                    elif b_ratio > 0.5:
                        color = Fore.BLUE
                    else:
                        color = Fore.LIGHTBLACK_EX
                elif luminance > 50:
                    if r_ratio > 0.5 and g_ratio > 0.4:
                        color = Fore.YELLOW
                    elif g_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.CYAN
                    elif r_ratio > 0.5 and b_ratio > 0.4:
                        color = Fore.MAGENTA
                    elif r_ratio > 0.5:
                        color = Fore.RED
                    elif g_ratio > 0.5:
                        color = Fore.GREEN
                    elif b_ratio > 0.5:
                        color = Fore.BLUE
                    else:
                        color = Fore.BLACK
                else:
                    color = Fore.BLACK

                colorized_map.array[y, x] = color + ascii_char + Fore.WHITE

        return colorized_map







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
    '3-3x3' : ("˙´\\", " *3", ".˛/"),
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
    (",---,",
     "|   |",
     "|   |",
     "'___'"),

    '1-5x4' :  
    ("  /| ", 
     " / | ", 
     "   | ", 
     "   | "),

    '2-5x4' :  
    (" .-~,", 
     "   / ", 
     "  /  ", 
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
    (" ,--*", 
     " \\__ ", 
     "    \\", 
     " \\__/"),

    '6-5x4' :  
    (" ,~- ", 
     "í    ", 
     "|¨˝\\ ", 
     "'__/ "),

    '7-5x4' :  
    (" ---7", 
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
     " |  |", 
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
        custom_image = CustomImage(np.array(image))
        return custom_image
    except:
        return CustomImage(ART_ARRAYS['cover_art'])

def update_album_cover():
    if current:
        """img = download_image('https://i.scdn.co/image/ab67616d0000b27351c02a77d09dfcd53c8676d0')
        album_cover = img.to_colorized_map(60,30)"""
        album_cover_url = get_album_cover_url()
        album_cover = download_image(album_cover_url).to_colorized_map(60,30)        

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



    buffer = 0.13#seconds
    last_request_time = 0
    current_time = 0
    last_calculated_time = 0
    song_length = float('inf')

    previous_name = None
    previous_playing_status = False


    while True:
        #try:
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
        
        #except KeyboardInterrupt:
        #    return 0
        #except:
        #    pass





if __name__ == "__main__":

    colorama.init(autoreset=True) # Initialize terminal formatting

    window_width = 96
    window_height = 36

    os.system('cls')

    terminal_display = TerminalDisplay(window_height)

    display_map = CharacterMap(window_width, window_height, filler=' ', U1dtype=False)

    song_view()

    """album_cover_url = 'https://i.scdn.co/image/ab67616d0000b27351c02a77d09dfcd53c8676d0'

    img = download_image(album_cover_url)
    album_cover = img.to_colorized_map(60,30)
    display_map.add_map_array(ART_PLACES['cover_art'], album_cover.array)

    terminal_display.update(display_map)"""

    print(colorama.Style.RESET_ALL) # End terminal formatting
