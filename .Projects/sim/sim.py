import screener
from screener import *
import numpy as np
from math import ceil
from random import randrange
from functools import reduce


def get_relative_neighbours(distance:float= 1):
        max_offset = ceil(distance)
        dx, dy = np.meshgrid(np.arange(-max_offset, max_offset + 1),
                            np.arange(-max_offset, max_offset + 1))
        mask = (dx**2 + dy**2) <= distance**2
        return np.column_stack((dx[mask], dy[mask]))


def get_possible_neighbours(pos, some_dots, distance:float= 1):
    x, y = pos
    relative_neighbours = get_relative_neighbours(distance)
    neighbours = relative_neighbours + np.array([x, y])
    return tuple(map(tuple, neighbours[is_possible(neighbours, some_dots)]))


def in_range(pos):
    pos = np.atleast_2d(pos)
    return np.logical_and.reduce((0<= pos[:, 0], pos[:, 0] < field_map.width,
                                0<= pos[:, 1], pos[:, 1] < field_map.height))

def is_empty(pos, some_dots=(np.array(), np.array())):
    pos = np.atleast_2d(pos)
    dots = reduce(np.union1d, some_dots)
    return ~np.any(np.all(pos[:, np.newaxis, :] == dots[np.newaxis, :, :], axis=2), axis=1)

def is_possible(pos, some_dots):
    pos = np.atleast_2d(pos)
    valid_mask = in_range(pos)
    result = np.zeros(len(pos), dtype=bool)
    result[valid_mask] = is_empty(pos[valid_mask], some_dots)
    return result

def random_from(l: tuple):
    return l[randrange(len(l))]


def move_away(c_pos, away_from_pos, multiplier:int= 1):
    direction = np.sign(c_pos - away_from_pos)
    return c_pos + direction * multiplier



class DotGroup():
    def __init__(self, a=np.array([])):
        self.array = np.array(a)

    def __getattr__(self, key):
        return self.array[key]

    def __setattr__(self, key, value):
        self.array[key] = value

    def move_in_random_direction(self, amount:int = 1):
        for i, dot in enumerate(self.array):
            possible_neighbours = get_possible_neighbours(dot, distance=amount)
            if possible_neighbours:
                self.array[i] = random_from(possible_neighbours)


    def move_away_from_dots(self, distance:float= 2):
        new_dots = self.array.copy()
        
        for i, dot_pos in enumerate(self.array):
            neighbours = get_possible_neighbours(tuple(dot_pos), distance=distance)
            if neighbours:
                nx, ny = random_from(neighbours)
                new_pos = move_away(dot_pos, np.array([nx, ny]))
                if in_range(new_pos.reshape(1, -1))[0]:
                    new_dots[i] = new_pos
        
        self.array = new_dots


    def move_down(self):
        down_1 = self.array.copy()
        down_1[:, 1] -= 1

        not_possible = ~is_possible(down_1)

        down_1[not_possible] = self.array[not_possible]
        
        self.array = down_1
        


    def move_boulder(d:np.array= ['x', 'y']):
        global boulder, last_boulder_move_frame

        last_boulder_move_frame = frame
        
        new_boulder = boulder + np.array(d)
        if np.all(in_range(new_boulder)):
            boulder[:] = new_boulder


    def move_boulder_left(event):
        move_boulder([-1,  0 ])

    def move_boulder_right(event):
        move_boulder([ 1,  0 ])

    def move_boulder_down(event):
        move_boulder([ 0, -1 ])

    def move_boulder_up(event):
        move_boulder([ 0,  1 ])




    def move_away_from_boulder(distance:float= 2):
        global dots

        dots_array = np.array(dots)
        new_dots = dots_array.copy()

        boulder_center = [boulder[0]+BOULDER_SIZE//2]

        factor = 1
        d = 1
        if frame-last_boulder_move_frame< BOULDER_EFFECT_DECAY:
            factor = BOULDER_EFFECT_AMOUNT
            d = distance

        for i, dot_pos in enumerate(dots_array):
            is_inside_square = np.all(np.abs(dot_pos - boulder_center) <= (np.array(BOULDER_SIZE) / 2) + d)
            
            if is_inside_square:
                direction = np.sign(dot_pos - boulder_center)
        
                new_pos = dot_pos + direction * factor
                    
                if is_possible(new_pos.reshape(1,-1))[0]:
                    new_dots[i] = new_pos
        
        
        dots = new_dots


    def render_dots(dot_char:str= '¤', boulder_char:str= '*'):
        global field_map
        
        field_map.fill()
        
        for x, y in dots:
            field_map[int(x), int(y)] = dot_char
        
        for x, y in boulder:
            field_map[int(x), int(y)] = boulder_char
        
        return field_map


def calculate_change():
    global frame
   # move_away_from_dots(1)

    move_away_from_boulder(BOULDER_EFFECT_DISTANCE)

    move_in_random_direction()

    frame += 1


def update_display(fps=0):
    global terminal_display
    terminal_display.update(field_map, fps)




import keyboard



if __name__ == "__main__":
    screener.GLOBAL_last_frame_time = 0
    global terminal_display, field_map, dots, boulder, frame, last_boulder_move_frame, BOULDER_EFFECT_DECAY, BOULDER_EFFECT_AMOUNT, BOULDER_EFFECT_DISTANCE


    # --- CONSTANTS ---
    BOULDER_EFFECT_DISTANCE = 2
    BOULDER_EFFECT_AMOUNT = 4
    BOULDER_EFFECT_DECAY = 3
    DOT_CHAR = '¤'
    BOULDER_CHAR = '@'
    BOULDER_SIZE = (8, 8)
    DOTS_AMOUNT = 240
    MAP_SIZE = (50, 40)


    # ~~ Hook keys
    keyboard.on_press_key('a', move_boulder_left)
    keyboard.on_press_key('d', move_boulder_right)
    keyboard.on_press_key('s', move_boulder_down)
    keyboard.on_press_key('w', move_boulder_up)
    
    # ~~ Initialize field_map, terminal_display
    field_map = CharacterMap(MAP_SIZE[0], MAP_SIZE[1], filler=' ')
    terminal_display = TerminalDisplay(field_map.height)
    
    # ~~ Create boulder
    BOULDER_SIZE = np.array(BOULDER_SIZE)
    boulder = np.array([[i, j] for i in range(BOULDER_SIZE[0]) for j in range(BOULDER_SIZE[1])])
    
    # ~~ Create dots
    dots = np.random.randint([0, 0], [field_map.width, field_map.height], size=(DOTS_AMOUNT, 2))
    
    # ~~ Initialize screen
    os.system('cls')
    colorama.init()

    # ~~ Set global variables
    start = time_in_seconds()
    frame = 0
    last_boulder_move_frame = float('-inf')
    
    while True:
        render_dots(DOT_CHAR, BOULDER_CHAR)
        update_display()
        calculate_change()
