import numpy as np
from PIL import Image

def apply_antialiasing(img, factor=2):
    width, height = img.size
    img = img.resize((width * factor, height * factor), Image.LANCZOS)
    return img.resize((width, height), Image.LANCZOS)

def convert_near_white_to_white(input_path, threshold=80):
    output_path = input_path.replace('.jpg', f' - {round(threshold)}.jpg')
    threshold = 1 - threshold/100
    img = Image.open(input_path)
    
    #img = apply_antialiasing(img)
    
    img_array = np.array(img)
    
    mask = (img_array[:, :, 0] / 255.0 > threshold) & \
           (img_array[:, :, 1] / 255.0 > threshold) & \
           (img_array[:, :, 2] / 255.0 > threshold)
    
    img_modified = img_array.copy()
    img_modified[mask] = 255
    output_img = Image.fromarray(img_modified.astype(np.uint8))
    
    output_img.save(output_path)
    print(f"Modified image saved as {output_path}")

input_image = input('Image to modify path: ')
threshold = int(input('Give threshold [0-100]: '))
convert_near_white_to_white(input_image, threshold)