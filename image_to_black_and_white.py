import numpy as np
from PIL import Image

def apply_antialiasing(img, factor=2):
    width, height = img.size
    img = img.resize((width * factor, height * factor), Image.LANCZOS)
    return img.resize((width, height), Image.LANCZOS)

def convert_to_bw(input_path, threshold=80):
    output_path = input_path + f' - {round(threshold)}.jpg'
    input_path = input_path + '.jpg'
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


input_image = input('image to convert name: ')
threshold_input = input('Give threshold [0-100]: ')
while threshold_input != "":

    input_is_correct = False
    while not input_is_correct:
        try:
            threshold = int(threshold_input)
            input_is_correct = True

        except:
            print("\nInput error. Try again.\n")
            threshold_input = input('Give threshold [0-100]: ')


    convert_to_bw(input_image, threshold)

    threshold_input = int(input('Give threshold [0-100]: '))
