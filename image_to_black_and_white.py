import numpy as np
from PIL import Image

def convert_to_bw(input_path, output_path, threshold=80):
    threshold /= 100

    # Open the image
    img = Image.open(input_path)
    
    # Convert to grayscale
    img_gray = img.convert('L')
    
    # Convert to numpy array
    img_array = np.array(img_gray)
    
    # Normalize pixel values to range 0-1
    img_normalized = img_array / 255.0
    
    # Apply threshold
    img_bw = (img_normalized > threshold).astype(np.uint8) * 255
    
    # Create new image from array
    output_img = Image.fromarray(img_bw, mode='L')
    
    # Save the result
    output_img.save(output_path.replace('.jpg', f' - {threshold*100}.jpg'))

# Example usage
input_image = "convert_this.jpg"
output_image = "converted_img.jpg"
threshold = int(input('Give threshold [0-100]: '))
convert_to_bw(input_image, output_image, threshold)