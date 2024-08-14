from PIL import Image
import cv2
import cv
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
import pyautogui

import pyautogui
from pynput.mouse import Listener
def NewBox():
    global box
    clicks = []
    def is_clicked(x, y, button, pressed):
        if pressed:
            clicks.append(pyautogui.position())
            return False # to stop the thread after click
    for i in range(3):
        with Listener(on_click=is_clicked) as listener:
            listener.join()
    box = (clicks[0][0], clicks[0][1], clicks[1][0]-clicks[0][0], clicks[2][1]-clicks[0][1])

box = (454, 138, 27, 13)
config = '-psm'+str(5)
NewBox()
width = box[2]
height = box[3]

#print(f'{box}\n')


def get_text(image):
    return pytesseract.image_to_string(image)
x = pyautogui.screenshot('x.png',region=(box))
img1 = Image.open('x.png')

y = pyautogui.screenshot('y.png',region=(box[0]+66,box[1],box[2],box[3]))
img2 = Image.open('y.png')


dict = {}
shape = -1
img1_map = []
img = Image.new('RGB', img1.size, "white")
blacks = 0
for i in img1.getdata():
    if i[0] > 240 or i[1] > 240 and i[2] > 240:
        img1_map.append([(255,255,255),' '])
    else:
        img1_map.append([(0,0,0),' '])
for i in range(len(img1_map)):
    if img1_map[i][0] == (0,0,0):
        blacks += 1
        if (blacks == 1):
            img1_map[i][1] = '0'
            shape += 1
            dict.update({str(shape): 0})
            dict[str(shape)] += 1
        else:
            try:
                if img1_map[i - width][0] == (0,0,0):
                    img1_map[i][1] = img1_map[i - width][1]
                    dict[img1_map[i][1]] += 1

                elif img1_map[i - 1][0] == (0,0,0):
                    img1_map[i][1] = img1_map[i - 1][1]
                    dict[(img1_map[i][1])] += 1

                elif img1_map[i - width - 1][0] == (0,0,0):
                    img1_map[i][1] = img1_map[i - width - 1][1]
                    dict[(img1_map[i][1])] += 1

                elif img1_map[i - width + 1][0] == (0,0,0):
                    img1_map[i][1] = img1_map[i - width + 1][1]
                    dict[(img1_map[i][1])] += 1

                else:
                    shape += 1
                    img1_map[i][1] = str(shape)
                    dict.update({str(shape): 0})
                    dict[str(shape)] += 1

            except:
                shape += 1
                dict.update({str(shape):0})
                dict[str(shape)] += 1
def Key(key):
    return dict[key]

for i in range(height):
    for j in range(width):
        print(img1_map[i*width+j][1], end=' ')
    print('')

for i in range(len(dict.items())):
    if(dict[str(i)] == 16):
        what = str(i)
        break
what = 0

for i in range(len(img1_map)):
    if(img1_map[i][1] == what):
        img1_map[i] = (255,255,255)
    else:
        img1_map[i] = img1_map[i][0]

img.putdata(img1_map)
img.save('img1_processed.png')


dict = {}
shape = -1
img2_map = []
img = Image.new('RGB', img2.size, "white")
blacks = 0
for i in img2.getdata():
    if i[0] > 240 or i[1] > 240 and i[2] > 240:
        img2_map.append([(255,255,255),' '])
    else:
        img2_map.append([(0,0,0),' '])
for i in range(len(img2_map)):
    if img2_map[i][0] == (0,0,0):
        blacks += 1
        if (blacks == 1):
            img2_map[i][1] = '0'
            shape += 1
            dict.update({str(shape): 0})
            dict[str(shape)] += 1
        else:
            try:
                if img2_map[i - width][0] == (0,0,0):
                    img2_map[i][1] = img2_map[i - width][1]
                    dict[img2_map[i][1]] += 1

                elif img2_map[i - 1][0] == (0,0,0):
                    img2_map[i][1] = img2_map[i - 1][1]
                    dict[(img2_map[i][1])] += 1
                else:
                    shape += 1
                    img2_map[i][1] = str(shape)
                    dict.update({str(shape): 0})
                    dict[str(shape)] += 1

            except:
                shape += 1
                dict.update({str(shape):0})
                dict[str(shape)] += 1
def Key(key):
    return dict[key]

for i in range(height):
    for j in range(width):
        print(img2_map[i*width+j][1], end=' ')
    print('')

for i in range(len(dict.items())):
    if(dict[str(i)] == 16):
        what = str(i)
        break


for i in range(len(img2_map)):
    if(img2_map[i][1] == what):
        #img2_map[i] = (255,255,255)
        img2_map[i] = (0, 0, 0)
    else:
        img2_map[i] = img2_map[i][0]

img.putdata(img2_map)
img.save('img2_processed.png')

img1 = Image.open('img1_processed.png')
img2 = Image.open('img2_processed.png')

config = '-psm'+str(6)
    
x = pytesseract.image_to_string(img1, config=config)
print(x)
y = pytesseract.image_to_string(img2, config=config)
print(y)

"""import cv2
import numpy as np

def ReadImage1():
    # opencv loads the image in BGR, convert it to RGB
    img1 = cv2.cvtColor(cv2.imread('img1.png'), cv2.COLOR_BGR2RGB)

    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(img1, lower_white, upper_white)  # could also use threshold
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # "erase" the small white points in the resulting mask
    mask = cv2.bitwise_not(mask)  # invert mask

    # load background (could be an image too)
    bk = np.full(img1.shape, 255, dtype=np.uint8)  # white bk

    # get masked foreground
    fg_masked = cv2.bitwise_and(img1, img1, mask=mask)

    # get masked background, mask must be inverted
    mask = cv2.bitwise_not(mask)
    bk_masked = cv2.bitwise_and(bk, bk, mask=mask)

    # combine masked foreground and masked background
    final = cv2.bitwise_or(fg_masked, bk_masked)
    mask = cv2.bitwise_not(mask)  # revert mask to original

    # resize the image
    img1 = cv2.resize(mask,(0,0),fx=3,fy=3)
    cv2.imwrite('ocr.png', img1)

    text = pytesseract.image_to_string(cv2.imread('ocr.png'), lang='eng')

    return text
def ReadImage2():
    # opencv loads the image in BGR, convert it to RGB
    img2 = cv2.cvtColor(cv2.imread('img2.png'), cv2.COLOR_BGR2RGB)

    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(img2, lower_white, upper_white)  # could also use threshold
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # "erase" the small white points in the resulting mask
    mask = cv2.bitwise_not(mask)  # invert mask

    # load background (could be an image too)
    bk = np.full(img2.shape, 255, dtype=np.uint8)  # white bk

    # get masked foreground
    fg_masked = cv2.bitwise_and(img2, img2, mask=mask)

    # get masked background, mask must be inverted
    mask = cv2.bitwise_not(mask)
    bk_masked = cv2.bitwise_and(bk, bk, mask=mask)

    # combine masked foreground and masked background
    final = cv2.bitwise_or(fg_masked, bk_masked)
    mask = cv2.bitwise_not(mask)  # revert mask to original

    # resize the image
    img2 = cv2.resize(mask,(0,0),fx=3,fy=3)
    cv2.imwrite('ocr.png', img2)

    text = pytesseract.image_to_string(cv2.imread('ocr.png'), lang='eng')

    return text

print(ReadImage1())
#print(ReadImage2())"""
