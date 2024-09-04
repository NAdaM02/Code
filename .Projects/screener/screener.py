from time import time as now
from time import sleep as wait_seconds
import colorama
import os
import numpy as np
import cv2
from PIL.ImageGrab import grab as take_screenshot
from sys import stdout
from PIL import Image



class DisplayMap:
    def __init__(self, width, height, d_list=None, filler=' '): 
        if d_list:
            self.width = len(d_list[0])
            self.height = len(d_list)
            self.val = np.array(d_list, dtype='<U1')
        else:
            self.width = width
            self.height = height
            self.val = np.full(((self.height, self.width)), filler, dtype='<U1')

        self.filler = filler
    
    def get(self):
        return self.val
        
    def fill(self, fill='??'):
        if fill == '??':
            filler = self.filler
        else:
            filler = fill

        self.val = np.full(((self.height, self.width)), filler, dtype='<U1')
        return self.val
    
    def add_map(self, row, col, added_array):
        self.val[row: row + added_array.shape[0], col: col + added_array.shape[1]] = added_array
        return self.val


class TerminalDisplay:
    def __init__(self, height=512):
        self.height = height
        self.clear_height = height+2
        self.clear_height_str = str(height+2)

    def to_beginning(self):
        stdout.write("\033[?25l")
        stdout.write("\033[" + self.clear_height_str + "A")
        stdout.write("\033[2K")
        #stdout.write("\033[2J")
    
    def clear(self):
        os.system('cls')
    
    def write(self, display_map:DisplayMap):
        output = "\n"
        for row in display_map.val:
            output += " ".join(row) + "\n"
        self.to_beginning()
        stdout.write(output)
        stdout.flush()
    
    def update(self, display_map:DisplayMap, stay_seconds=0):
        self.write(display_map)
        if stay_seconds != 0:
            wait_seconds(stay_seconds)


class CustomImage:
    def __init__(self, image_array=np.array([])):
        self.array = image_array

    def gray(self):
        self.array = cv2.cvtColor(np.array(self.array), cv2.COLOR_RGB2GRAY)
        return self

    def downscale(self, target_width, target_height):
        self.array = cv2.resize(self.array, (target_width, target_height), interpolation=cv2.INTER_AREA)
        return self

    def be_screenshot(self):
        self.array = np.array(take_screenshot())
        return self
    
    def save_as_img(self, name:str='image'):
        image = Image.fromarray(self.array)
        return image.save(f'{name}.png')
    
    def save_as_text(self, name:str='text'):
        return np.savetxt(f'{name}.txt', self.array, fmt='%f', delimiter=' | ')
    
    def to_map(self, target_width=-1, target_height=-1, grayed=False, sized=False):
        if not grayed: self.gray()
        if not sized: self.downscale(target_width, target_height)
    
        indices = np.digitize(self.array, THRESHOLDS)
        img_map = DisplayMap(width=target_width, height=target_height)
        img_map.val[:] = np.array(OPAS)[indices]
        
        return img_map

    def get_subarray(self, first_rows:int= None, last_rows:int= None, first_columns: int = None, last_columns: int = None):

        if first_rows is None:
            first_rows = 0
        if last_rows is None:
            last_rows = array.shape[0] - 1
        if first_columns is None:
            first_columns = 0
        if last_columns is None:
            last_columns = array.shape[1] - 1

        if first_rows < 0 or last_rows >= self.array.shape[0] or first_columns < 0 or last_columns >= self.array.shape[1]:
            raise IndexError("Indices are out of bounds.")

        return self.array[first_rows:last_rows+1, first_columns:last_columns+1]


class Monitor:
    def __init__(self):
        pass

    def to_map(target_width, target_height):
        img = CustomImage()
        img.be_screenshot()

        img.gray()
        img.downscale(target_width, target_height)

        indices = np.digitize(img.array, THRESHOLDS)
        monitor_display_map = DisplayMap(width=target_width, height=target_height)
        monitor_display_map.val[:] = np.array(OPAS)[indices]
        
        return monitor_display_map




def flashScreen(display_map:DisplayMap, terminal_display:TerminalDisplay, speed = 0.02):
    global OPAS
    for char in OPAS:
        display_map.fill(char)
        terminal_display.update(display_map, stay_seconds=speed)
    for char in reversed(OPAS):
        display_map.fill(char)
        terminal_display.update(display_map, stay_seconds=speed)

"""def moveCharacterAcrossDisplay(display_map:DisplayMap, terminal_display, move_height=""):
    if move_height=='' :
        move_height = display_map.height // 2
    move_speed = 1
    char = 'o'
    for i in range(4):
        for x in range(0, width, move_speed):
            display_map.val[move_height][max(0, x - move_speed)] = display_map.filler
            display_map.val[10][x] = char
            (0.01*(i*(1/5)))
        for x in range(width - 1, -1, -move_speed):
            display_map.val[10][min(x + move_speed, width - 1)] = display_map.filler
            #display_map[move_height][x] = char
            terminal_display.update(display_map, stay_seconds=0.01*(i*(1/5)))"""

def get_terminal_display_size():
    inp = input('input size coherent [11,14,19,28,56] or size:  ')
    if ('x' not in inp) and ('*' not in inp):
        x = int(inp) if inp != '' else 19
        width, height = x*16, x*9
    else:
        width, height = inp.split('x').split('*')
        int(height); int(width)
    
    return width, height




#OPAS10 = tuple(" -~+xrsd#$")
#OPAS16 = tuple(" .-:~+*rsd#$%&@█")
#OPAS17 = tuple(" .-:~+*=rsd#$%&@█")
#OPAS20 = tuple(" .-:~+*=rsdoO#$%&@▓█")
#OPAS32 = tuple(" .`',-:;il!><xrsahkmodbqwO0#$%@█")
#OPAS51 = tuple(" .`',-:;il!><xrsahkmoqwzvuyntjf0147235689bpdgq#$%&@█")
#OPAS64 = tuple(" .`',-~:;_\"^!/|\\(){}[]<>*il?1jtrxzcvunyfLITFJCoaesmkdqbphwO08#$%&@█")
#OPAS70 = tuple(" .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")
OPAS92 = tuple(" .`':,_-;^!<+>=/*?|vLclTxY()r1iz{}tnsJjfCuo7FI][e3aVX2yZShk4AUPw5bqK96dEmpHG%O#D80R&gN$BMQW@")

OPAS = OPAS92

#THRESHOLDS = np.linspace(0, 255, len(OPAS) + 1)[1:-1]
#THRESHOLDS = tuple(map(lambda x: x*255, (0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037)))
#THRESHOLDS = (44.0, 48.40330851943755, 52.163937138130684, 52.78817204301075, 52.807361455748556, 53.4818858560794, 55.86236559139785, 56.02564102564103, 57.89057071960298, 59.37105045492142, 60.396195202646815, 67.27766749379653, 67.53870967741935, 67.9641852770885, 68.11364764267991, 68.55690653432589, 69.70496277915633, 70.02605459057072, 71.33738626964434, 71.7347394540943, 71.79131513647643, 72.44747725392887, 72.74582299421009, 73.15004135649296, 73.29330024813896, 73.93399503722084, 74.34069478908188, 74.3974358974359, 75.39520264681555, 75.51621174524401, 75.55930521091811, 75.76923076923077, 76.38428453267163, 76.4332506203474, 76.60636889991729, 76.7590570719603, 77.03556658395368, 77.04557485525227, 77.82952853598015, 77.9029776674938, 78.37717121588089, 78.6010752688172, 78.72406947890819, 78.79495450785774, 78.80124069478909, 78.82721257237387, 78.84127377998345, 78.90727874276261, 80.00363937138131, 80.09553349875931, 80.67750206782465, 80.71439205955335, 80.99735318444996, 81.03598014888337, 81.4712158808933, 81.79842845326716, 82.17502067824648, 82.65566583953681, 84.21182795698925, 84.38726220016542, 84.96087675765095, 85.0923076923077, 85.33655913978495, 85.57791563275434, 85.71819685690653, 86.91166253101737, 87.09652605459057, 87.12191894127378, 87.32158808933002, 87.37138130686517, 87.42133995037221, 87.51000827129859, 87.59900744416873, 87.61025641025641, 87.9428453267163, 88.38916459884202, 88.88047973531845, 89.29404466501241, 90.42787427626138, 90.99478908188586, 91.55533498759306, 92.39751861042184, 92.567576509512, 92.93225806451613, 93.51149710504549, 95.36294458229942, 95.38072787427626, 95.47237386269644, 95.59131513647642, 97.09578163771712, 97.795947063689, 100.37386269644334)
THRESHOLDS = (19.91780620928458, 36.928531603967365, 39.752178825048425, 39.838979693644006, 42.89010505311343, 53.65790245906449, 54.39645812547686, 62.832230471271785, 69.5289923117554, 74.16610423146898, 105.2935691648571, 106.47436029109686, 108.3989450671988, 109.07501907388935, 111.0800443101121, 116.27313075884739, 117.72554874112332, 123.65719085627094, 125.4545674628793, 125.71048036856624, 128.67854627618993, 130.0280752978461, 131.8565056634779, 132.5045190445449, 135.4026204589471, 137.2422750748283, 137.49893626386523, 142.01220728916016, 142.55957655965727, 142.75450437232232, 143.70407594342396, 146.48619343858206, 146.7076853101708, 147.49076383590585, 148.18142936792066, 149.4321849873819, 149.47745613005455, 153.02357092552379, 153.3558087329069, 155.5007629555725, 156.51356446974586, 157.06991314044254, 157.39055255590122, 157.41898732319973, 157.53646780914377, 157.60007189389046, 157.8986369505253, 162.85788485239746, 163.27355625330128, 165.90601707846704, 166.07288426550852, 167.35282293561832, 167.52754709783437, 169.496280591584, 170.97638505780859, 172.67985210399672, 174.8539893773109, 181.89309085040205, 182.68664534303656, 185.2813178590293, 185.875828980574, 186.9806693467927, 188.07241475438698, 188.70695903515465, 194.10544926345443, 194.9416559070368, 195.05651740125595, 195.95969540465987, 196.1849286929984, 196.41091026468695, 196.81199014026643, 197.21456658254593, 197.26544985034334, 198.76987352544165, 200.7887420036387, 203.01114355302542, 204.88185192793006, 210.0105860085686, 212.57495304888786, 215.1105111802336, 218.9200217148894, 219.68925699865017, 221.3388476436411, 223.9589617935325, 232.33374904630554, 232.41418950642645, 232.8287384823053, 233.36675421092787, 240.17201713715596, 243.3391264158695, 255.0)

CHAR_LIST = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/ ")

CHAR_IMAGES = {CHAR_LIST[i] : CustomImage( np.array(Image.open(f'./Data/Characters/{i}.png')) ) for i in range(len(CHAR_LIST))}

CHAR_IMAGE_RATIO = 78/155

if __name__ == "__main__":

    os.system('cls')

    display_width, display_height = get_terminal_display_size()

    display_map = DisplayMap(display_width, display_height, filler=",")

    terminal_display = TerminalDisplay(display_height)

    monitor = Monitor



    colorama.init() # Initialize terminal formatting

    terminal_display.update(display_map)

    wait_seconds(1)

    char_width = int(display_width//10)
    char_height = int(char_width//CHAR_IMAGE_RATIO)

    char_top_left_display_row = 4*display_height//10
    char_top_left_display_col = 4*display_width//10

    for i in range(len(CHAR_LIST)):
        display_map.fill()

        char_map = CHAR_IMAGES[CHAR_LIST[i]].to_map(char_width, char_height, grayed=True)

        display_map.add_map(col=char_top_left_display_col+i, row=char_top_left_display_row-i, added_array=char_map.val)

        terminal_display.update(display_map)

        wait_seconds(0.5)

    #terminal_display.clear()


    print(colorama.Style.RESET_ALL)  # Reset terminal formatting
