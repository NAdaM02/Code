import screener
from screener import *
import numpy as np
from math import ceil
from random import randrange
from functools import reduce
import keyboard


def get_relative_neighbours(distance:float= 1):
        max_offset = ceil(distance)
        dx, dy = np.meshgrid(np.arange(-max_offset, max_offset + 1),
                            np.arange(-max_offset, max_offset + 1))
        mask = (dx**2 + dy**2) <= distance**2
        return np.column_stack((dx[mask], dy[mask]))


def get_possible_neighbours(pos, some_dots:tuple[np.array, ...], distance:float= 1):
    x, y = pos
    relative_neighbours = get_relative_neighbours(distance)
    neighbours = relative_neighbours + np.array([x, y])
    return tuple(map(tuple, neighbours[is_possible(neighbours, some_dots)]))


def in_range(pos):
    pos = np.atleast_2d(pos)
    return np.logical_and.reduce((0<= pos[:, 0], pos[:, 0] < field_map.width,
                                0<= pos[:, 1], pos[:, 1] < field_map.height))

def is_empty(pos, some_dots):
    pos = np.atleast_2d(pos)
    return ~np.any(np.all(pos[:, np.newaxis, :] == np.vstack(some_dots)[np.newaxis, :, :], axis=2), axis=1)

def is_possible(pos, some_dots:tuple[np.array, np.array]):
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
        super().__setattr__('array', np.array(a))
        super().__setattr__('other_dots', [])

    def __getattr__(self, key):
        return self.array[key]

    def __setattr__(self, key, value):
        if key == 'array' or key == 'other_dots':
            super().__setattr__(key, value)
        else:
            self.array[key] = value

    def __iter__(self):
        return iter(self.array)

    def __len__(self):
        return len(self.array)

    def move_in_random_direction(self, amount:int = 1):
        for i, dot in enumerate(self.array):
            possible_neighbours = get_possible_neighbours(dot, [self.array]+self.other_dots, distance=amount)
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

        not_possible = ~is_possible(down_1, [self.array]+self.other_dots)

        down_1[not_possible] = self.array[not_possible]
        
        self.array = down_1
    
    def move_away_from_boulder(self, distance:float= 2):
        new_dots = self.array.copy()

        boulder_center = [boulder[0]+BOULDER_SIZE//2]

        factor = 0
        d = 1
        if frame-last_boulder_move_frame< BOULDER_EFFECT_DECAY:
            factor = BOULDER_EFFECT_AMOUNT
            d = distance

        for i, dot_pos in enumerate(self.array):
            is_inside_square = np.all(np.abs(dot_pos - boulder_center) <= (np.array(BOULDER_SIZE) / 2) + d)
            
            if is_inside_square:
                direction = np.sign(dot_pos - boulder_center)
        
                new_pos = dot_pos + direction * factor
                    
                #if is_possible( new_pos.reshape(1,-1), [self.array]+self.other_dots )[0]:
                if in_range(new_pos.reshape(1,-1)):
                    new_dots[i] = new_pos
        
        
        self.array = new_dots
        


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


def render_dots(dots:tuple[DotGroup, ...], dot_chars:tuple[str, ...], dot_colors:tuple[tuple[int, int, int], ...]):
    global field_map
    
    field_map.fill()
    
    for i in range(len(dots)):
        r, g, b = dot_colors[i]
        for x, y in dots[i]:
            field_map[int(x), int(y)] = f"\033[38;2;{r};{g};{b}m{dot_chars[i]}"
        
    return field_map


def calculate_change():
    global frame
   # move_away_from_dots(1)

    water_particles.other_dots = [boulder]

    water_particles.move_away_from_boulder(BOULDER_EFFECT_DISTANCE)

    water_particles.move_in_random_direction()

    water_particles.move_down()


    air_particles.other_dots = [boulder, water_particles.array]

    air_particles.move_away_from_boulder(BOULDER_EFFECT_DISTANCE)

    air_particles.move_in_random_direction()

    frame += 1


def update_display(fps=0):
    global terminal_display
    #highlight(field_map[0, 0], 0)
    terminal_display.update(field_map, fps)







if __name__ == "__main__":
    screener.GLOBAL_last_frame_time = 0
    global terminal_display, field_map, dots, boulder, frame, last_boulder_move_frame, BOULDER_EFFECT_DECAY, BOULDER_EFFECT_AMOUNT, BOULDER_EFFECT_DISTANCE


    # --- CONSTANTS ---
    BOULDER_EFFECT_DISTANCE = 2
    BOULDER_EFFECT_AMOUNT = 4
    BOULDER_EFFECT_DECAY = 3
    DOT_CHARS = ('¤', '.', '@')
    DOT_COLORS = (
                    (20 , 20 , 255),
                    (255, 255, 255),
                    (20 , 255, 50 ))
    DOT_AMOUNTS = (250, 250)
    BOULDER_SIZE = (8, 8)
    DOTS_AMOUNT = 240
    MAP_SIZE = (50, 40)


    # ~~ Hook keys
    keyboard.on_press_key('a', move_boulder_left)
    keyboard.on_press_key('d', move_boulder_right)
    keyboard.on_press_key('s', move_boulder_down)
    keyboard.on_press_key('w', move_boulder_up)
    
    # ~~ Initialize field_map, terminal_display
    field_map = CharacterMap(MAP_SIZE[0], MAP_SIZE[1], filler=' ', U1dtype=False)
    terminal_display = TerminalDisplay(field_map.height)
    
    # ~~ Create boulder
    BOULDER_SIZE = np.array(BOULDER_SIZE)
    boulder = np.array([[i, j] for i in range(BOULDER_SIZE[0]) for j in range(BOULDER_SIZE[1])])
    
    # ~~ Create dots
    water_particles = DotGroup(np.random.randint([0, 0], [field_map.width, field_map.height], size=(DOT_AMOUNTS[0], 2)))

    air_particles = DotGroup(np.random.randint([0, 0], [field_map.width, field_map.height], size=(DOT_AMOUNTS[1], 2)))

    # ~~ Initialize screen
    os.system('cls')
    colorama.init()

    # ~~ Set global variables
    frame = 0
    last_boulder_move_frame = float('-inf')
    
    while True:
        render_dots((water_particles, air_particles, boulder), DOT_CHARS, DOT_COLORS)
        update_display()
        calculate_change()
