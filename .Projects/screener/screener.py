from time import time as now_in_seconds
from time import perf_counter as precise_time
from time import sleep as wait_seconds
import colorama
import os
import numpy as np
import cv2
from PIL.ImageGrab import grab as take_screenshot
from sys import stdout
from PIL import Image
from threading import Thread

DOT = (os.path.dirname(__file__)).replace('\\','/')


def print_separated(val_1, space_between, val_2):
    val_1_string = str(val_1)
    val_1_len = len(val_1_string)

    val_2_string = str(val_2)

    stdout.write(val_1_string + space_between[val_1_len : ] + val_2_string)


class CharacterMap:
    def __init__(self, width, height, d_list=None, filler=' '): 
        if d_list:
            self.width = len(d_list[0])
            self.height = len(d_list)
            self.array = np.array(d_list, dtype='<U1')
        else:
            self.width = width
            self.height = height
            self.array = np.full(((self.height, self.width)), filler, dtype='<U1')

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
    
    def get_subarray(self, first_rows:int= None, last_rows:int= None, first_columns: int = None, last_columns: int = None):
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

    def add_map(self, row, col, added_array, exclude_chars:tuple):
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


class TerminalDisplay:
    def __init__(self, height=512):
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
        output = "\n"
        for row in display_map.array:
            output += " ".join(row) + "\n"
        self.to_beginning()
        stdout.write(output)
        stdout.flush()
    
    def update(self, display_map:CharacterMap, stay_seconds:int=None):
        if stay_seconds:
            start_time = precise_time()

            self.write(display_map)

            while precise_time() - start_time < stay_seconds :
                pass
        else:
            self.write(display_map)


class CustomImage:
    def __init__(self, image_array=np.array([]), character=None):
        self.array = image_array
        self.char = character

    def gray(self):
        self.array = cv2.cvtColor(np.array(self.array), cv2.COLOR_RGB2GRAY)
        return self

    def downscale(self, target_width, target_height):
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


class Monitor:
    def __init__(self):
        pass

    def to_map(target_width, target_height):
        img = CustomImage()
        img.be_screenshot()

        img.gray()
        img.downscale(target_width, target_height)

        indices = np.digitize(img.array, THRESHOLDS)
        monitor_display_map = CharacterMap(width=target_width, height=target_height)
        monitor_display_map.array[:] = np.array(OPAS)[indices]
        
        return monitor_display_map




def flashScreen(display_map:CharacterMap, terminal_display:TerminalDisplay, speed = 0.02):
    global OPAS
    for char in OPAS:
        display_map.fill(char)
        terminal_display.update(display_map, stay_seconds=speed)
    for char in reversed(OPAS):
        display_map.fill(char)
        terminal_display.update(display_map, stay_seconds=speed)


def get_terminal_display_size():
    inp = input('input size coherent [11,14,19,28,56] or [16x9]:  ')
    if inp == '':
        width, height = 300, 40
    elif ('x' not in inp) and ('*' not in inp):
        x = int(inp)
        width, height = x*16, x*9
    else:
        width, height = inp.split('x')
        width=int(width); height=int(height)
    
    return width, height

def render_char(char_width, char_height, char_col, char_row, char_map):

    shown = (0-char_width <= char_col <= display_map.width) and (0-char_height <= char_row <= display_map.height)
    if shown:
        display_map.add_map(col=int(char_col), row=int(char_row), added_array=char_map.arra, exclude_chars=(" "))
    
    return shown

def write_text(text="", char_width=None, char_height=None, char_row=0, stay_seconds=0):
    if not char_height:  char_height = char_width//CHAR_WIDTH_PER_HEIGHT
    if not char_width:  char_width = char_height*CHAR_WIDTH_PER_HEIGHT

    char_width = int(char_width);  char_height = int(char_height)

    text_chars_list = tuple(text)
    char_maps = [CHAR_IMAGES[char].to_map(char_width, char_height, grayed=True) for char in text_chars_list]

    text_char_count = len(text)

    render_char_count = display_map.width//char_width + 3
    all_steps_count = display_map.width + char_width*(text_char_count+1)

    for step_index in range(all_steps_count):
        display_map.fill()
        
        render_char_start_index = max(0, int(step_index/char_width) - render_char_count+1)
        render_char_end_index = min(render_char_start_index + render_char_count, text_char_count)

        for char_index in range( render_char_start_index, render_char_end_index ):
            try:
                render_char(char_width, char_height, display_map.width - step_index + char_width*char_index, char_row, char_maps[char_index])
            except:
                display_map.fill("!")
        
        terminal_display.update(display_map, stay_seconds=stay_seconds)
    
    """char_render_threads = []
    for step_index in range(all_steps_count):
        display_map.fill()
        render_char_start_index = max(0, int(step_index/char_width) - render_char_count+1)
        render_char_end_index = min(render_char_start_index + render_char_count, text_char_count)

        for char_index in range( render_char_start_index, render_char_end_index ):
            char_render_thread = Thread(target=render_char, args=(char_width, display_map.width - step_index + char_width*char_index, char_row, char_maps[char_index]))
            char_render_threads.append(char_render_thread)
            char_render_thread.start()
        for running_char_render_thread in char_render_threads:
            running_char_render_thread.join()

        terminal_display.update(display_map, stay_seconds=stay_seconds)"""
        

def write_szozat(char_width=None, char_height=None, char_row=0, stay_seconds=0):
    verses = [
        'Hazádnak rendületlenűl  Légy híve, oh magyar;  Bölcsőd az s majdan sírod is,  Mely ápol s eltakar.',
        'A nagy világon e kivűl  Nincsen számodra hely;  Áldjon vagy verjen sors keze;  Itt élned, halnod kell.',
        'Ez a föld, melyen annyiszor Apáid vére folyt; Ez, melyhez minden szent nevet Egy ezredév csatolt.',
        'Itt küzdtenek honért a hős  Árpádnak hadai;  Itt törtek össze rabigát  Hunyadnak karjai.',
        'Szabadság! itten hordozák  Véres zászlóidat,  S elhulltanak legjobbjaink  A hosszu harc alatt.',
        'És annyi balszerencse közt,  Oly sok viszály után,  Megfogyva bár, de törve nem,  Él nemzet e hazán.',
        'S népek hazája, nagy világ!  Hozzád bátran kiált:  ^Egy ezredévi szenvedés  Kér éltet vagy halált!^',
        'Az nem lehet hogy annyi szív  Hiában onta vért,  S keservben annyi hű kebel  Szakadt meg a honért.',
        'Az nem lehet, hogy ész, erő,  És oly szent akarat  Hiába sorvadozzanak  Egy átoksúly alatt.',
        'Még jőni kell, még jőni fog  Egy jobb kor, mely után  Buzgó imádság epedez  Százezrek ajakán.',
        'Vagy jőni fog, ha jőni kell,  A nagyszerű halál,  Hol a temetkezés fölött  Egy ország vérben áll.',
        'S a sírt, hol nemzet sűlyed el,  Népek veszik körűl,  S az ember millióinak  Szemében gyászköny űl.',
        'Légy híve rendületlenűl  Hazádnak, oh magyar:  Ez éltetőd, s ha elbukál,  Hantjával ez takar.',
        'A nagy világon e kivűl  Nincsen számodra hely;  Áldjon vagy verjen sors keze:  Itt élned, halnod kell.',
    ]
    #for verse in verses: write_text(verse, char_width, char_height, char_row, stay_seconds)
    write_text("  /  ".join(verses), char_width, char_height, char_row, stay_seconds=stay_seconds)

def get_screen_map():
    display_map = CustomImage().be_screenshot().array
    terminal_display.update(display_map)

def make_axis(mark_counts=(5,3), marking_spaces=(2,2)):
    mark_count = {'x':mark_counts[0], 'y':mark_counts[1]}
    marking_space = {'x':marking_spaces[0], 'y':marking_spaces[1]}

    width = (marking_space['x']+1)*(mark_count['x']-1) + 5
    height =  (marking_space['y']+1)*(mark_count['y']-1) + 5

    axis_map = CharacterMap(width=width, height=height)
    
    char = ''

    for i in range(width):
        if i == width-1 :
            char = '🡢'
            axis_map.array[height//2+1][-1] = 'x'
        elif (i-2) % (marking_space['x']+1) == 0:
            char = '✛'
        else:
            char = '─'
        axis_map.array[height//2][i] = char
    
    y_axis_col = (mark_count['x']//2)*(marking_space['x']+1)+2
    for i in range(height):
        if i == 0 :
            char = '🡡'
            axis_map.array[0][y_axis_col-1] = 'y'
        elif (i-2) % (marking_space['y']+1) == 0:
            char = '✛'
        else:
            char = '〡'
        axis_map.array[i][y_axis_col] = char
    
    return axis_map


def graph(f, test_range=(-2,2), step=0.5) -> CharacterMap:
    can_graph_range = test_range[0] < test_range[1]

    mark_count = (test_range[1]-test_range[0]) / step
    make_axis()
    
    if not can_graph_range:
        raise Exception("Range error.")
    else:
        make_axis()



OPAS = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")

#THRESHOLDS = (19.91780620928458, 36.928531603967365, 39.752178825048425, 39.838979693644006, 42.89010505311343, 53.65790245906449, 54.39645812547686, 62.832230471271785, 69.5289923117554, 74.16610423146898, 105.2935691648571, 106.47436029109686, 108.3989450671988, 109.07501907388935, 111.0800443101121, 116.27313075884739, 117.72554874112332, 123.65719085627094, 125.4545674628793, 125.71048036856624, 128.67854627618993, 130.0280752978461, 131.8565056634779, 132.5045190445449, 135.4026204589471, 137.2422750748283, 137.49893626386523, 142.01220728916016, 142.55957655965727, 142.75450437232232, 143.70407594342396, 146.48619343858206, 146.7076853101708, 147.49076383590585, 148.18142936792066, 149.4321849873819, 149.47745613005455, 153.02357092552379, 153.3558087329069, 155.5007629555725, 156.51356446974586, 157.06991314044254, 157.39055255590122, 157.41898732319973, 157.53646780914377, 157.60007189389046, 157.8986369505253, 162.85788485239746, 163.27355625330128, 165.90601707846704, 166.07288426550852, 167.35282293561832, 167.52754709783437, 169.496280591584, 170.97638505780859, 172.67985210399672, 174.8539893773109, 181.89309085040205, 182.68664534303656, 185.2813178590293, 185.875828980574, 186.9806693467927, 188.07241475438698, 188.70695903515465, 194.10544926345443, 194.9416559070368, 195.05651740125595, 195.95969540465987, 196.1849286929984, 196.41091026468695, 196.81199014026643, 197.21456658254593, 197.26544985034334, 198.76987352544165, 200.7887420036387, 203.01114355302542, 204.88185192793006, 210.0105860085686, 212.57495304888786, 215.1105111802336, 218.9200217148894, 219.68925699865017, 221.3388476436411, 223.9589617935325, 232.33374904630554, 232.41418950642645, 232.8287384823053, 233.36675421092787, 240.17201713715596, 243.3391264158695, 255.0)
THRESHOLDS = (19.92, 36.93, 39.75, 39.84, 42.89, 53.66, 54.4, 62.83, 69.53, 74.17, 105.29, 106.47, 108.4, 109.08, 111.08, 116.27, 117.73, 123.66, 125.45, 125.71, 128.68, 130.03, 131.86, 132.5, 135.4, 137.24, 137.5, 142.01, 142.56, 142.75, 143.7, 146.49, 146.71, 147.49, 148.18, 149.43, 149.48, 153.02, 153.36, 155.5, 156.51, 157.07, 157.39, 157.42, 157.54, 157.6, 157.9, 162.86, 163.27, 165.91, 166.07, 167.35, 167.53, 169.5, 170.98, 172.68, 174.85, 181.89, 182.69, 185.28, 185.88, 186.98, 188.07, 188.71, 194.11, 194.94, 195.06, 195.96, 196.18, 196.41, 196.81, 197.21, 197.27, 198.77, 200.79, 203.01, 204.88, 210.01, 212.57, 215.11, 218.92, 219.69, 221.34, 223.96, 232.33, 232.41, 232.83, 233.37, 240.17, 243.34, 255.0)


CHAR_LIST = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/ áéíóöőúüűÁÉÍÓÖŐÚÜŰ")
 
CHAR_COUNT = len(CHAR_LIST)

CHAR_IMAGES = {CHAR_LIST[i] : CustomImage( np.array(Image.open(f'{DOT}/Data/Characters/{i}.png')), CHAR_LIST[i] ) for i in range(CHAR_COUNT)}


CHAR_WIDTH_PER_HEIGHT = 78/155


if __name__ == "__main__":

    os.system('cls')

    start_display_width, start_display_height = get_terminal_display_size()

    display_map = CharacterMap(start_display_width, start_display_height, filler=" ")

    terminal_display = TerminalDisplay(start_display_height)

    monitor = Monitor


    colorama.init() # Initialize terminal formatting



    terminal_display.update(display_map)
    
    char_width, char_height = 20, 30

    char_row = (display_map.height-char_height)//2
    
    #+write_text('911 was an inside job...', char_width, char_height, char_row, 0.001*20/4)
    #write_szozat(char_width, char_height, char_row, 0.001)
    
    display_map = make_axis()

    terminal_display.update(display_map)

    """display_map.fill(' ')
    terminal_display.update(display_map)"""


    print(colorama.Style.RESET_ALL)  # Reset terminal formatting
