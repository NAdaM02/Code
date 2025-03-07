import screener
from screener import *
import numpy as np
from itertools import product
from math import ceil, sqrt
from random import randrange

def get_relative_neighbours(distance:float= 1):
    max_offset = ceil(distance)
    dx, dy = np.meshgrid(np.arange(-max_offset, max_offset + 1),
                         np.arange(-max_offset, max_offset + 1))
    mask = (dx**2 + dy**2) <= distance**2
    return np.column_stack((dx[mask], dy[mask]))


def get_real_neighbours(pos, distance:float= 1):
    x, y = pos
    relative_neighbours = get_relative_neighbours(distance)
    neighbours = relative_neighbours + np.array([x, y])
    return tuple(map(tuple, neighbours[in_range(neighbours)]))


def in_range(pos):
    pos = np.atleast_2d(pos)  # Ensure input is always 2D
    return np.logical_and.reduce((0<= pos[:, 0], pos[:, 0] < field_map.width,
                                  0<= pos[:, 1], pos[:, 1] < field_map.height))
def is_empty(pos):
    pos = np.atleast_2d(pos)  # Ensure input is always 2D
    return ~np.any(np.all(pos[:, np.newaxis, :] == dots[np.newaxis, :, :], axis=2), axis=1)


def random_from(l: tuple):
    return l[randrange(0, len(l))]


def move_in_random_direction():
    global dots
    offsets = np.random.randint(-1, 2, size=dots.shape)
    new_dots = dots + offsets
    out_of_bounds_mask = ~in_range(new_dots)
    new_dots[out_of_bounds_mask] = dots[out_of_bounds_mask]  # Prevent moving out of bounds
    dots = new_dots


def move_away(c_pos, away_from_pos, multiplier:float= 1):
    direction = np.sign(c_pos - away_from_pos)
    return c_pos + direction * multiplier


def move_away_from_dots(distance:float= 2):
    global dots
    dots_array = np.array(dots)
    new_dots = dots_array.copy()
    
    for i, dot_pos in enumerate(dots_array):
        neighbours = get_real_neighbours(tuple(dot_pos), distance=distance)
        if neighbours:
            nx, ny = random_from(neighbours)
            new_pos = move_away(dot_pos, np.array([nx, ny]))
            if in_range(new_pos.reshape(1, -1))[0]:
                new_dots[i] = new_pos
    dots = new_dots


def move_down():
    global dots
    new_dots = dots.copy()
    new_dots[:, 1] -= 1
    out_of_bounds_mask = ~in_range(new_dots)
    new_dots[out_of_bounds_mask] = dots[out_of_bounds_mask]  # Prevent moving out of bounds
    not_empty_mask = ~is_empty(new_dots)
    new_dots[not_empty_mask] = dots[not_empty_mask]
    dots = new_dots


def move_boulder_down():
    global boulder
    new_boulder = boulder + np.array([0, -1])
    if np.all(in_range(new_boulder)):
        boulder[:] = new_boulder  # Move only if the entire boulder stays in bounds


def move_boulder_right():
    global boulder
    new_boulder = boulder + np.array([1, 0])
    if np.all(in_range(new_boulder)):
        boulder[:] = new_boulder  # Move only if the entire boulder stays in bounds

def move_boulder_left():
    global boulder
    new_boulder = boulder + np.array([-1, 0])
    if np.all(in_range(new_boulder)):
        boulder[:] = new_boulder  # Move only if the entire boulder stays in bounds


def move_away_from_boulder(distance:float= 2):
    global dots
    dots_array = np.array(dots)
    distances = np.linalg.norm(dots_array[:, None] - boulder, axis=2)
    close_mask = np.any(distances <= distance, axis=1)
    
    for i in np.where(close_mask)[0]:
        bx, by = boulder[np.argmin(distances[i])]
        new_pos = move_away(dots_array[i], np.array([bx, by]), multiplier=6)
        if in_range(new_pos.reshape(1, -1))[0]:
            dots_array[i] = new_pos
    dots = dots_array


def render_dots(dot_char:str= '¤'):
    global field_map
    
    field_map.fill()
    
    dots_in_bounds = dots[in_range(dots)]
    boulder_in_bounds = boulder[in_range(boulder)]
    
    for x, y in dots_in_bounds:
        field_map[int(x), int(y)] = dot_char
    
    for x, y in boulder_in_bounds:
        field_map[int(x), int(y)] = "@"
    
    return field_map


def calculate_change():
    move_down()
    move_in_random_direction()
    move_boulder_down()
    move_away_from_dots(1)
    move_away_from_boulder()


def update_display(fps=7):
    global terminal_display
    terminal_display.update(field_map, fps)

if __name__ == "__main__":
    screener.GLOBAL_last_frame_time = 0
    global terminal_display, field_map, dots, boulder
    
    field_map = CharacterMap(60, 30, filler='.')
    terminal_display = TerminalDisplay(field_map.height)
    boulder_size = (10, 10)
    
    boulder = np.array([[i, j + 20] for i in range(boulder_size[0]) for j in range(boulder_size[1])])
    dots = np.random.randint([0, 0], [field_map.width, field_map.height], size=(600, 2))
    
    os.system('cls')
    colorama.init()
    start = time_in_seconds()
    
    while time_in_seconds() - start < 6:
        render_dots()
        update_display(fps=0)
        calculate_change()
    
    while True:
        start = time_in_seconds()
        while time_in_seconds() - start < 10:
            render_dots()
            update_display(fps=0)

            move_boulder_right()
            calculate_change()
        
        start = time_in_seconds()
        while time_in_seconds() - start < 10:
            render_dots()
            update_display(fps=0)

            move_boulder_left()
            calculate_change()

