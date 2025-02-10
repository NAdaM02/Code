from PIL import Image
import numpy as np
from time import sleep as wait_seconds
import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("open_dir", nargs="?", default="Characters")
args = parser.parse_args()

sorting_key = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

vals = {}
imgs = []
for i in range(len(sorting_key)):
    img = Image.open(f'{args.open_dir}/{i}.png')
    imgs.append(img)
    img_array = np.array(img)
    avg = np.average(img_array)
    vals[i] = avg

sorted_vals = [v for k, v in sorted(vals.items(), key=lambda item: item[1])]

ratio = 255/sorted_vals[-1]
min_val = min(sorted_vals)
max_val = max(sorted_vals)

normalized_sorted_vals = [(num - min_val) / (max_val - min_val) * 255 for num in sorted_vals]
sorted_vals_indexes = sorted(vals, key=vals.get)
sorting_key = tuple(sorting_key)
sorted_characters = []

for i in range(len(sorted_vals_indexes)):
    sorted_characters.append(sorting_key[sorted_vals_indexes[i]])

save_dir = "ORDERED"
d = subprocess.check_output("dir", shell=True, text=True)
if save_dir in d:
    i = 1
    while f'{save_dir}{i}' in d:
        i += 1
    save_dir += str(i)
os.system(f'mkdir {save_dir}')
    
for i in range(len(sorting_key)):
    imgs[i].save(f'./{save_dir}/{sorted_characters.index(sorting_key[i])}.png')

print()
print("".join(sorted_characters))
print(", ".join(map(str, normalized_sorted_vals)))