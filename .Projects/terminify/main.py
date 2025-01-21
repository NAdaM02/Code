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
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from io import BytesIO


TIME_CONVERT_LIST = (29030400, 604800, 86400, 3600, 60, 1)
TIME_CHAR_LIST = ('y', 'w', 'd', 'h', 'm', 's')

def secs_to_text(seconds:float) :
    seconds = int(seconds)
    text = ""
    for i in range(len(TIME_CONVERT_LIST)):
        conv = TIME_CONVERT_LIST[i]
        if conv <= seconds:
            un = seconds//conv
            seconds -= un*conv
            text += str(un) + TIME_CHAR_LIST[i] + " "
    text = f'{text}\b'
    return text

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
    def __init__(self, image_array=np.array([])):
        self.array = image_array

    def gray(self):
        self.array = cv2.cvtColor(np.array(self.array), cv2.COLOR_RGB2GRAY)
        return self

    def downscale(self, target_width:int, target_height:int):
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





sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id='67c0740055b9412da3e1e14978c42742',
        client_secret='4116025cf230497699d6feb972d8bfc7',
        redirect_uri='http://localhost:8080',
        scope='user-read-playback-state user-modify-playback-state user-library-read user-library-modify'
    )
)




ART_MAPS = {
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
    'liked' : (",=_=,", "\\"+"%"+"X%/", " ˇ÷ˇ "),
    'cover_art' : [". "*30 for _ in range(30)],
    'progress_bar' : [" "*60,],
    'next_up' : ["NEXT UP",],
    'playing_from' : ["Playing from:"],
    'playlist' : [" "],
}
for key in ART_MAPS.keys():
    m = np.array([tuple(string) for string in ART_MAPS[key]])
    ART_MAPS[key] = m

ART_PLACES = {
    'previous' : (31, 72),
    'pause' :    (31, 77),
    'resume' :   (31, 77),
    'next' :     (31, 82),
    'no_shuffle' :    (31, 65),
    'shuffle' :       (31, 65),
    'smart_shuffle' : (31, 65),
    'like' :  (31, 87),
    'liked' : (31, 87),
    'cover_art' : (2,2),
    'progress_bar' : (31,2),
    'next_up' : (1,63),
    'playing_from' : (0,1), 
    'playlist' : (0, 15),
}



def place_art(art_name):
    row, col = ART_PLACES[art_name]
    display_map.add_map_array(row, col, ART_MAPS[art_name])

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        custom_image = CustomImage(np.array(image))
        return custom_image
    except:
        return CustomImage(ART_MAPS['cover_art'])

def pad_with_spaces(array):
    rows, cols = array.shape
    
    result = np.empty((rows, cols * 2 - 1), dtype=array.dtype)
    
    result[:, ::2] = array
    result[:, 1::2] = ' ' 
    
    return result

def update_album_cover(cover_map):
    row, col = ART_PLACES['cover_art']
    display_map.add_map_array(row, col, cover_map.array)





current = None


def get_shuffle_status():
    if current:
        return current['shuffle_state']

def toggle_shuffle():
    if current:
        shuffle_state = not current['shuffle_state']
        sp.shuffle(state=shuffle_state)


def get_playing_status():
    if current:
        return current['is_playing']

def stop_resume():
    if current:
        if current['is_playing']:
            sp.pause_playback()
            return 'Paused'
        else:
            sp.start_playback()
            return 'Resumed'


def next_track():
    sp.next_track()
    return 'Next track'


def previous_track():
    sp.previous_track()
    return 'Previous track'


def get_liked_status():
    if current:
        track_id = current['item']['id']
        liked = sp.current_user_saved_tracks_contains([track_id])[0]
        return liked

def like_unlike_current_song():
    if current:
        track_id = current['item']['id']
        liked = get_liked_status()
        if liked:
            sp.current_user_saved_tracks_delete([track_id])
            return 'Unliked'
        else:
            sp.current_user_saved_tracks_add([track_id])
            return 'Liked'


def get_song_length():
    if current:
        song_length = round(current['item']['duration_ms'] / 1000)
        return song_length

def get_time():
    if current:
        current_time = round(current['progress_ms'] / 1000)
        return current_time

def add_progress_bar(progress):
    progress = round(progress*60)
    progress_bar_string = "¤"*(progress-1) + "@" + "-"*(60-progress)

    row, col = ART_PLACES['progress_bar']

    display_map.add_map_array(row, col, np.array([tuple(progress_bar_string)]))

def get_next_queued_songs():
    if current and 'queue' in current:
        return [track['name'] for track in current['queue']]


def get_album_cover_url():
    if current:
        return current['item']['album']['images'][0]['url']

def update_current_album_cover():
    if current:
        album_cover_url = get_album_cover_url()
        album_cover = download_image(album_cover_url).to_map(60,30)
        update_album_cover(album_cover)


def get_current_playlist_name():
    if current and current['context'] and current['context']['type'] == 'playlist':
        playlist_uri = current['context']['uri']
        playlist_id = playlist_uri.split(':')[-1]
        playlist = sp.playlist(playlist_id)
        return playlist['name']
    else:
        return " "

def update_current_playlist_name():
    if current:
        playlist_name = get_current_playlist_name()
        row, col = ART_PLACES['playlist']
        display_map.add_map_array(row, col, np.array([tuple(playlist_name)]))



def update_shuffle_status():
    if current:
        place_art('shuffle' if get_shuffle_status() else 'no_shuffle')

def update_playing_status():
    if current:
        place_art('pause' if get_playing_status() else 'resume')

def update_liked_status():
    if current:
        place_art('liked' if get_liked_status() else 'like')
    


def song_view():
    global current
    display_map.fill()

    arts = (
        'playing_from', 'playlist',
        'cover_art',
        'progress_bar',
        'next_up',
        'no_shuffle', 'previous', 'resume', 'next', 'liked',
    )
    for art in arts: place_art(art)

    #result = sp.search(q='sigma', limit=1, type='track')

    #track_cover_url = result['tracks']['items'][0]['album']['images'][0]['url']

    #terminal_display.update(display_map)
    #print()
    #print(track_cover_url)
    
    stop_resume()

    while True:
        current = sp.current_playback()

        update_current_album_cover()
        update_current_playlist_name()
        update_liked_status()
        update_playing_status()
        update_shuffle_status()

        song_length = get_song_length()
        current_time = get_time()

        if current: add_progress_bar(current_time/song_length)

        terminal_display.update(display_map)



if __name__ == "__main__":

    colorama.init() # Initialize terminal formatting

    window_width = 96
    window_height = 36

    os.system('cls')

    terminal_display = TerminalDisplay(window_height)

    display_map = CharacterMap(window_width, window_height, filler=' ')

    song_view()

    print(colorama.Style.RESET_ALL) # End terminal formatting
