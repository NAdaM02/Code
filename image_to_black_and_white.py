import numpy as np
from PIL import Image
import argparse

def apply_antialiasing(img, factor=2):
    width, height = img.size
    img = img.resize((width * factor, height * factor), Image.LANCZOS)
    return img.resize((width, height), Image.LANCZOS)

def convert_to_bw(input_path, threshold=80):
    output_path = input_path.replace(".jpg","").replace(".png","") + f' - {round(threshold)}.png'
    threshold = 1 - threshold/100
    img = Image.open(input_path)
    
    #img = apply_antialiasing(img)
    
    img_gray = img.convert('L')
    img_array = np.array(img_gray)

    img_normalized = img_array / 255.0

    img_bw = (img_normalized > threshold).astype(np.uint8) * 255
    output_img = Image.fromarray(img_bw, mode='L')
    
    output_img.save(output_path)

    print(f"Converted image saved as {output_path}")


def get_parsed_inputs():
    parser = argparse.ArgumentParser()
    
    for i in range(1,2+1): parser.add_argument(f'p{i}', type=str, nargs='?', default='')
    
    args = parser.parse_args()

    p1, p2 = args.p1, args.p2

    if '.png' or '.jpg' in p1:
        if p2 != "":
            return p1, p2
        else:
            return p1, None
    else:
        return None, None


input_image, threshold_input = get_parsed_inputs()

if not input_image:
    input_image = input('image to convert name: ')

if not threshold_input:
    threshold_input = input('Give threshold [0-100]: ')

while threshold_input != "":

    input_is_correct = False
    while not input_is_correct:
        try:
            input_is_correct = True
            if threshold_input == 'a':
                for threshold in range(0, 101, 5):
                    convert_to_bw(input_image, threshold)
            else:
                threshold = int(threshold_input)

        except:
            print("\nInput error. Try again.\n")
            threshold_input = input('Give threshold [0-100]: ')


    convert_to_bw(input_image, threshold)

    threshold_input = input('Give threshold [0-100]: ')
