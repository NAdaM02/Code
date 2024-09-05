from PIL import Image
import numpy as np
from time import sleep as wait_seconds
import os

vals = {}
imgs = []
for i in range(92):
    img = Image.open(f'./Data/old_OPAS/{i}.png')
    imgs.append(img)
    img_array = np.array(img)
    avg = np.average(img_array)
    #for row in img_array:
    #    print(' '.join(map(str, row)))
    vals[i] = avg

sorted_vals = [v for k, v in sorted(vals.items(), key=lambda item: item[1])]

ratio = 255/sorted_vals[-1]
min_val = min(sorted_vals)
max_val = max(sorted_vals)

normalized_sorted_vals = [(num - min_val) / (max_val - min_val) * 255 for num in sorted_vals]

sorted_vals_indexes = sorted(vals, key=vals.get)
OPAS = tuple(" `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@")
sorted_OPAS = []

for i in range(len(sorted_vals_indexes)):
    sorted_OPAS.append(OPAS[sorted_vals_indexes[i]])

os.system('del new_OPAS')
os.system('mkdir new_OPAS')
for i in range(92):
    imgs[i].save(f'./new_OPAS/{sorted_OPAS.index(OPAS[i])}.png')

print()
print("".join(sorted_OPAS))
print(", ".join(map(str, normalized_sorted_vals)))