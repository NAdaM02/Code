from PIL import Image
import numpy as np
from PIL.ImageGrab import grab as take_screenshot
from time import sleep as wait
import os
import subprocess

def get_char_image(char, terminal_roi, background_color):
    os.system('cls')
    print(char)
    wait(0.1)
    try:
        img = take_screenshot()
        cropped_img = img.crop(terminal_roi)  # Crop to terminal ROI
        cropped_img_np = np.array(cropped_img)

        # Find character (pixels NOT the background color)
        char_mask = np.all(cropped_img_np != background_color, axis=2).astype(np.uint8) * 255

        # Find bounding box
        rows = np.any(char_mask, axis=1)
        cols = np.any(char_mask, axis=0)
        if not np.any(rows) or not np.any(cols):
            return Image.new('RGB', (10, 10), color='black')  # No character found

        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        return cropped_img.crop((xmin, ymin, xmax + 1, ymax + 1))

    except Exception as e:
        print(f"Error capturing/processing '{char}': {e}")
        return Image.new('RGB', (10, 10), color='black')

def get_terminal_roi(background_color):
    os.system('cls')
    print('█')  # Print a solid block
    wait(0.5)
    img = np.array(take_screenshot())

    # Find the solid block (pixels that ARE the background color)
    mask = np.all(img == background_color, axis=2).astype(np.uint8) * 255

    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows) or not np.any(cols):
        raise Exception("Could not find terminal ROI. Check background color.")
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    return xmin, ymin, xmax + 1, ymax + 1

characters = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
background_color = np.array([220, 223, 228])

# --- Get Terminal ROI ---
try:
    terminal_roi = get_terminal_roi(background_color)
    print(f"Terminal ROI: {terminal_roi}")
except Exception as e:
    print(f"Error during initial setup: {e}")
    exit()

# --- Capture and Process Characters ---
imgs = []
for char in characters:
    imgs.append(get_char_image(char, terminal_roi, background_color))

# --- Save Images ---
save_dir = "PICS"
if os.path.exists(save_dir):
    i = 1
    while os.path.exists(f'{save_dir}{i}'):
        i += 1
    save_dir += str(i)
os.makedirs(save_dir)

for i, img in enumerate(imgs):
    try:
        img.save(f'./{save_dir}/{i}.png')
    except Exception as e:
        print(f"Error saving image {i}: {e}")

print(f"Images saved to: {save_dir}")