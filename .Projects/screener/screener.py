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
import argparse
from colorama import Fore, Style
from scipy.spatial.distance import cdist

DOT = (os.path.dirname(__file__)).replace('\\','/')


def print_separated(val_1, space_between:str, val_2):
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
        output = "\n" + "\n".join((" ".join(row) for row in display_map.array))
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

        
        output_indices = np.zeros((grid_rows, grid_cols), dtype=int)

        reshaped_shapes = np.array(CHARACTER_SHAPES).reshape(len(CHARACTER_SHAPES), -1)

        for i in range(grid_rows):
            for j in range(grid_cols):
                grid = self.array[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3]

                flattened_grid = grid.reshape(-1)

                distances = cdist(flattened_grid[np.newaxis, :], reshaped_shapes, metric='euclidean')

                closest_index = np.argmin(distances)
                output_indices[i, j] = closest_index

        img_map = CharacterMap(width=target_width, height=target_height)

        row_scale = grid_rows / target_height
        col_scale = grid_cols / target_width

        for i in range(target_height):
            for j in range(target_width):
                source_row = int(i * row_scale)
                source_col = int(j * col_scale)
                img_map.array[i, j] = OPAS[output_indices[source_row, source_col]]
        return img_map

    def to_color_shape_map(self, target_width:int= -1, target_height:int= -1, grayed:bool= False):

        self.downscale(target_width * 3, target_height * 3)

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

        color_strings = np.array([f"\033[38;2;{r};{g};{b}m" for r, g, b in color_map.reshape(-1, 3)])
        color_shape_map.array = (color_strings.reshape(target_height, target_width) + chars)

        return color_shape_map
        


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


def get_parsed_inputs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('size', type=str, nargs='?', default='20', help='Size coherent [11,14,19,28,56] or [16x9]')
    
    args = parser.parse_args()

    inp = args.size

    if inp == '':
        width, height = 300, 40
    elif ('x' not in inp) and ('*' not in inp):
        x = int(inp)
        width, height = x*16, x*9
    else:
        width, height = inp.split('x')
        width=int(width); height=int(height)
    
    return width, height


def flashScreen(display_map:CharacterMap, terminal_display:TerminalDisplay, fps:float= 20):
    global OPAS
    o_len = len(OPAS)
    frame_time = o_len/fps
    for char in OPAS:
        display_map.fill(char)
        terminal_display.update(display_map, fps=frame_time)
    for char in reversed(OPAS):
        display_map.fill(char)
        terminal_display.update(display_map, fps=frame_time)


def write_text(text:str= "", char_width:int= None, char_height:int= None, char_row:int= 0, fps:float= 0):
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
            #try:
            display_map.render_char(char_width, char_height, display_map.width - step_index + char_width*char_index, char_row)
            #except:
            #    display_map.fill("!")
        
        terminal_display.update(display_map, fps=fps)
        

def write_szozat(char_width:int= None, char_height:int= None, char_row:int= 0, fps:float= 0):
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
    #for verse in verses: write_text(verse, char_width, char_height, char_row, fps)
    write_text("  /  ".join(verses), char_width, char_height, char_row, fps=fps)


def get_screen_map():
    display_map = CustomImage().be_screenshot().array
    terminal_display.update(display_map)


def make_axis(mark_counts:tuple= (5,5), marking_spaces:tuple= (3,3)) -> CharacterMap:
    mark_count = {'x':mark_counts[0], 'y':mark_counts[1]}
    marking_space = {'x':marking_spaces[0], 'y':marking_spaces[1]}

    width = (marking_space['x']+1)*(mark_count['x']-1) + 5
    height =  (marking_space['y']+1)*(mark_count['y']-1) + 5

    axis_map = CharacterMap(width, height)
    
    char = ''

    for i in range(width):
        if i == width-1 :
            char = '>' # 🡢
            axis_map.array[height//2+1][-1] = 'x'
        elif (i-2) % (marking_space['x']+1) == 0:
            char = '+' # ✛
        else:
            char = '-' # ─
        axis_map.array[height//2][i] = char
    
    y_axis_col = (mark_count['x']//2)*(marking_space['x']+1)+2
    for i in range(height):
        if i == 0 :
            char = '^' # 🡡
            axis_map.array[0][y_axis_col-1] = 'y'
        elif (i-2) % (marking_space['y']+1) == 0:
            char = '+' # ✛
        else:
            char = '|' # 〡
        axis_map.array[i][y_axis_col] = char
    
    return axis_map

def get_graph_marks(funct, width:int, height:int, x_range:tuple= (0., 0.), y_range:tuple= (0., 0.), marker:str= "×") -> CharacterMap:
    if x_range[0] == x_range[1]:
        x_range = (-5, 5)
    
    if y_range[0] == y_range[1]:
        y_range = (-5, 5)
    
    x_range_len = x_range[1] - x_range[0]
    y_range_len = y_range[1] - y_range[0]
    
    marks_map = CharacterMap(width, height)
    
    x_values = np.linspace(x_range[0], x_range[1], width)
    
    deviation = 0
    for col in range(width):
        x = x_values[col]
        
        try:
            y_val = funct(x)
            
            scaled_y = round(((y_val - y_range[0]) / y_range_len) * (height - 1))
            
            graph_y = height - 1 - scaled_y
            
            if 0 <= graph_y < height:
                marks_map.array[graph_y][col] = marker
        
        except Exception:
            pass
    
    return marks_map

def make_graph(funct, width:int, height:int, x_range:tuple= (0.,0.), y_range:tuple= (0.,0.), mark_counts:tuple= (0,0), marker:str="×") -> CharacterMap:
    if mark_counts == (0,0):
        mark_counts = (5, 5)
    
    marking_spaces = ((width-5)//mark_counts[0]-1, (height-5)//mark_counts[1]-1)
    
    axis_map = make_axis(mark_counts, marking_spaces)
    
    marks_map = get_graph_marks(funct, axis_map.width-4, axis_map.height-4, x_range, y_range, marker)
    
    graph_map = axis_map
    graph_map.add_map_array(2, 2, marks_map.array, (' '))
    
    return graph_map



OPAS = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")

THRESHOLDS = (19.92, 36.93, 39.75, 39.84, 42.89, 53.66, 54.4, 62.83, 69.53, 74.17, 105.29, 106.47, 108.4, 109.08, 111.08, 116.27, 117.73, 123.66, 125.45, 125.71, 128.68, 130.03, 131.86, 132.5, 135.4, 137.24, 137.5, 142.01, 142.56, 142.75, 143.7, 146.49, 146.71, 147.49, 148.18, 149.43, 149.48, 153.02, 153.36, 155.5, 156.51, 157.07, 157.39, 157.42, 157.54, 157.6, 157.9, 162.86, 163.27, 165.91, 166.07, 167.35, 167.53, 169.5, 170.98, 172.68, 174.85, 181.89, 182.69, 185.28, 185.88, 186.98, 188.07, 188.71, 194.11, 194.94, 195.06, 195.96, 196.18, 196.41, 196.81, 197.21, 197.27, 198.77, 200.79, 203.01, 204.88, 210.01, 212.57, 215.11, 218.92, 219.69, 221.34, 223.96, 232.33, 232.41, 232.83, 233.37, 240.17, 243.34, 255.0)
THRESHOLDS = np.array(THRESHOLDS)

CHAR_LIST = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/ áéíóöőúüűÁÉÍÓÖŐÚÜŰ")
 
CHAR_COUNT = len(CHAR_LIST)

CHAR_IMAGES = {CHAR_LIST[i] : CustomImage( np.array(Image.open(f'{DOT}/Data/Characters/{i}.png')) ) for i in range(CHAR_COUNT)}

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


"""if __name__ == "__main__":

    colorama.init() # Initialize terminal formatting


    os.system('cls')

    #start_display_width, start_display_height = get_terminal_display_size()
    #display_map = CharacterMap(start_display_width, start_display_height, filler=" ")
    #terminal_display = TerminalDisplay(start_display_height)
    #monitor = Monitor()
    #terminal_display.update(display_map)

    #char_width, char_height = 20, 30
    #char_row = (display_map.height-char_height)//2

    #write_text('911 was an inside job...', char_width, char_height, char_row, 0.001*20/4)
    
    #write_szozat(char_width, char_height, char_row, 0.001)

    
    #graph_map = make_graph(lambda x: np.sin(x), width=121, height=30, x_range=(-10, 10), y_range=(-1, 1), mark_counts=(11, 3), marker="×")

    #graph_map = make_graph(lambda x: x**2, width=80, height=40, x_range=(-5, 5), y_range=(0, 25))

    #graph_map = make_graph(lambda x: x**2, 100, 100)


    graph_map = make_graph(lambda x: -7/4*x+5/4, 120, 120)

    terminal_display = TerminalDisplay(graph_map.height)

    terminal_display.update(graph_map)


    print(colorama.Style.RESET_ALL)  # Reset terminal formatting"""

if __name__ == "__main__":

    os.system('cls')

    width, height = get_parsed_inputs()

    display_map = CharacterMap(width, height)

    terminal_display = TerminalDisplay(height)



    colorama.init() # Initialize terminal formatting

    #write_text("A mexikóiak részt vettek a Bakel és tuba közt forgatásában", 20, None, 2, 5)

    while True:
        monitor_image = CustomImage().be_screenshot()
        display_map = monitor_image.to_color_shape_map(width, height)
        terminal_display.update(display_map, 60)
    terminal_display.clear()
        

    print(colorama.Style.RESET_ALL)  # Reset terminal formatting
