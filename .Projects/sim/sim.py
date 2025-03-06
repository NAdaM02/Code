import screener
from screener import *
from random import randint, randrange
from itertools import product
from math import ceil, sqrt


def get_relative_neighbours(distance:float = 1):
    max_offset = ceil(distance)
    relative_neighbours = []
    
    for dx, dy in product(range(-max_offset, max_offset + 1), repeat=2):
        if dx == 0 and dy == 0:
            continue
        if sqrt(dx**2 + dy**2) <= distance:
            relative_neighbours.append((dx, dy))
    
    return tuple(relative_neighbours)

def get_real_neighbours(pos, distance:float= 1):
    x, y = pos

    relative_neighbours = get_relative_neighbours(distance)

    neighbours = tuple(map(lambda r: (x+r[0], y+r[1]), relative_neighbours))

    real_neighbours = []
    for neighbour in neighbours:
        if in_range(neighbour):
            real_neighbours.append(neighbour)

    return tuple(real_neighbours)


def random_from(l:tuple):
    return l[randrange(0, len(l))]



def render_dots(dot_char:str= '¤'):
    field_map.fill()

    for x, y in dots:
        field_map[x, y] = dot_char
    
    for r in boulder:
        for pos in r:
            field_map[pos[0], pos[1]] = "@"
    
    return field_map



def in_range(pos):
    return -1 < pos[0] < field_map.width and -1 < pos[1] < field_map.height


def move_in_random_direction():
    global dots
    
    new_dots = dots

    for i, dot_pos in enumerate(dots):

        while True:
            new_x = round( dot_pos[0]+randint(-1, 1) )
            new_y = round( dot_pos[1]+randint(-1, 1) )
            
            if new_x != 0 or new_y != 0:
                break

        if in_range((new_x, new_y)):
            new_dots[i] = [new_x, new_y]
    
    dots = new_dots


def move_away(c_pos:tuple=('x','y'), away_from_pos:tuple=('ox', 'oy'), multiplyer:float=1):
    x, y = c_pos
    ox, oy = away_from_pos

    dev = (
        -1 if ox< x else int(x< ox),
        -1 if oy< y else int(y< oy)
    )

    return (x - dev[0]*multiplyer, y - dev[1]*multiplyer)


def move_away_from_dots(distance:int= 2):
    global dots

    new_dots = dots

    for i, dot_pos in enumerate(dots):
        x, y = dot_pos

        neighbours = get_real_neighbours(dot_pos, distance=distance)

        n_dots = []
        for nx, ny in neighbours:
            if [nx, ny] in dots:
                n_dots.append((nx, ny))

        if 0< len(n_dots):
            nx, ny = random_from(n_dots)
        
            new_pos = move_away((x, y), away_from_pos=(nx, ny))

            if in_range(new_pos):
                if new_pos not in new_dots:
                    new_dots[i] = new_pos
    
    dots = new_dots


def move_down():
    global dots

    new_dots = dots

    for i, dot_pos in enumerate(dots):
        x, y = dot_pos

        if [x, y-1] not in dots and 1< y:
            new_dots[i] = [x, y-1]
    
    dots = new_dots


def move_boulder_down():
    global boulder

    for ri in range(boulder_size[1]):
        for i, b_pos in enumerate(boulder[ri]):
            x, y = b_pos
            if boulder_size[1]< y+ri+1 :
                boulder[ri][i] = [x, y-1]

def move_boulder_right():
    global boulder

    for ri in range(boulder_size[1]):
        for i, b_pos in enumerate(boulder[ri]):
            x, y = b_pos
            if x+boulder_size[0]-i< field_map.width :
                boulder[ri][i] = [x+1, y]


def move_away_from_boulder(distance:int= 2):
    global dots

    new_dots = dots

    for i, dot_pos in enumerate(dots):
        x, y = dot_pos

        bs = []
        for r in boulder:
            for bx, by in r:
                if sqrt((x-bx)**2 + (y-by)**2) <= distance:
                    bs.append((bx, by))

        if 0< len(bs):
            bx, by = random_from(bs)
        
            new_pos = move_away((x, y), away_from_pos=(bx, by), multiplyer=6)

            if in_range(new_pos):
                if new_pos not in new_dots:
                    new_dots[i] = new_pos
    
    dots = new_dots



def calculate_change():

    move_in_random_direction()
    
    move_away_from_boulder()

    move_away_from_dots(1)

    move_down()

    move_boulder_down()




def update_display(fps=7):
    global terminal_display
    terminal_display.update(field_map, fps)



if __name__ == "__main__":
    screener.GLOBAL_last_frame_time = 0
    global terminal_display, field_map, dots

    os.system('cls')
    colorama.init()

    field_map = CharacterMap(100, 80, filler=' ')
    terminal_display = TerminalDisplay(field_map.height)

    boulder_size = (10,10) # width,height

    boulder = [[() for _ in range(boulder_size[0])] for _ in range(boulder_size[1])]

    for j in range(boulder_size[1]):
        for i in range(boulder_size[0]):
            boulder[j][i] = [i+0, j+70]
    
    dots = []
    for i in range(1000):
        while True:
            new_dot_pos = [
                randrange(0, field_map.width),
                randrange(0, field_map.height-70)
                ]
            if new_dot_pos not in dots:
                dots.append(new_dot_pos)
                break

    start = time_in_seconds()

    while time_in_seconds()-start < 6:
        render_dots()
        
        update_display(fps=0)
        #print(f"\n{" ".join(map(str, dots))}")

        calculate_change()
    while True:
        render_dots()
        
        update_display(fps=0)
        #print(f"\n{" ".join(map(str, dots))}")

        move_boulder_right()

        calculate_change()
