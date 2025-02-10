from PIL import Image
import numpy as np
from PIL.ImageGrab import grab as take_screenshot
from time import sleep as wait_seconds
import os
import subprocess

import numpy as np
from PIL import Image
import os

def find_solid_color_rectangle(image: np.ndarray, color: np.ndarray, min_height=20, min_width=3, tolerance=20):
    h_img, w_img, _ = image.shape
    visited = np.zeros((h_img, w_img), dtype=bool)

    def color_within_tolerance(c1, c2, tolerance):
        return np.all(np.abs(c1 - c2) <= tolerance)

    for y in range(h_img):
        for x in range(w_img):
            if visited[y, x] or not color_within_tolerance(image[y, x], color, tolerance):
                continue

            y_end = y
            while y_end < h_img and color_within_tolerance(image[y_end, x], color, tolerance):
                y_end += 1

            x_end = x
            while x_end < w_img and np.all([color_within_tolerance(image[y:y_end, x_end, c], color[c], tolerance) for c in range(3)]):
                x_end += 1

            visited[y:y_end, x:x_end] = True

            if (y_end - y) >= min_height and (x_end - x) >= min_width:
                return (x, y, x_end, y_end)

    return None

characters = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

os.system('cls')
print('█')
img = np.array(take_screenshot())
section = find_solid_color_rectangle(img, (220, 223, 228), tolerance=20)  # Added tolerance parameter
if section:
    square = img[section[1]:section[3], section[0]:section[2]]
    Image.fromarray(square).save('asd.png')


print(section)
wait_seconds(100)


imgs = []
for i in range(len(characters)):
    img = take_screenshot()
    imgs.append(img)

save_dir = "PICS"
d = subprocess.check_output("dir", shell=True, text=True)
if save_dir in d:
    i = 1
    while f'{save_dir}{i}' in d:
        i += 1
    save_dir += str(i)
os.system(f'mkdir {save_dir}')
    
for i in range(len(characters)):
    imgs[i].save(f'./{save_dir}/{i}.png')
