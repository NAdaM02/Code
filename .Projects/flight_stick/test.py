"""import cv
import cv2

img = cv2.imread("x.png")
cImg = img.copy()
img = cv2.blur(img, (5, 5))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

scale = 1
delta = 0
ddepth = cv.CV_16S

grad_x = cv.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
grad_y = cv.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

abs_grad_x = cv.convertScaleAbs(grad_x)
abs_grad_y = cv.convertScaleAbs(grad_y)

grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

ret, thresh = cv2.threshold(grad, 10, 255, cv2.THRESH_BINARY_INV)

c, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

areas = [cv2.contourArea(c1) for c1 in c]
maxAreaIndex = areas.index(max(areas))

cv2.drawContours(cImg, c, maxAreaIndex, (255, 0, 0), -1)

cImg.show()"""

my_dictionary = {"song": "Estranged", "artist": "Guns N' Roses"}
print(my_dictionary["song"])
my_dictionary["song"] = "Paradise City"
print(my_dictionary["song"])
