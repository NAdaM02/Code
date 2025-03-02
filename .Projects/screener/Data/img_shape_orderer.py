from PIL import Image
import numpy as np
import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("open_dir", nargs="?", default="Characters")
args = parser.parse_args()

sorting_key = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

def calculate_brightness_grid(img):
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    third_height = height // 3
    third_width = width // 3

    brightness_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for i in range(3):
        for j in range(3):
            start_row = i * third_height
            end_row = (i + 1) * third_height
            start_col = j * third_width
            end_col = (j + 1) * third_width

            if i == 2:
                end_row = height
            if j == 2:
                end_col = width

            # Extract the section from the image array
            section = img_array[start_row:end_row, start_col:end_col]
            
            #Calculate section area
            section_area = (end_row-start_row)*(end_col-start_col)

            if len(section.shape) == 3:  # Color image (height, width, channels)
                brightness_sum = np.sum(section)
                brightness_grid[i][j] = brightness_sum / section_area
            else:  # Grayscale image (height, width)
                brightness_sum = np.sum(section)
                brightness_grid[i][j] = brightness_sum / section_area
                
    return brightness_grid


vals = {}
imgs = []
for i in range(len(sorting_key)):
    img = Image.open(f'{args.open_dir}/{i}.png')
    imgs.append(img)
    brightness_grid = calculate_brightness_grid(img)
    vals[i] = brightness_grid


grid_sums = [sum(sum(row) for row in grid) for grid in vals.values()]
min_val = min(grid_sums)
max_val = max(grid_sums)
if min_val == max_val:
    normalized_grid_sums = [0.0] * len(grid_sums)
else:
    normalized_grid_sums = [(num - min_val) / (max_val - min_val) * 255 for num in grid_sums]

save_dir = "ORDERED"
d = subprocess.check_output("dir", shell=True, text=True)
if save_dir in d:
    i = 1
    while f'{save_dir}{i}' in d:
        i += 1
    save_dir += str(i)
os.makedirs(save_dir, exist_ok=True)
    
for i in range(len(sorting_key)):
    imgs[i].save(f'./{save_dir}/{i}.png')

print()
print("".join(sorting_key))
print(", ".join(map(lambda x: str(round(x,2)), normalized_grid_sums))) 
for i in range(len(vals)):
    formatted_grid = tuple(tuple(float(round(val, 2)) for val in row) for row in vals[i])  # Round *here*
    print(f'{formatted_grid},')