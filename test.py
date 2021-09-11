import numpy as np
import cv2

img = cv2.imread("darkRoom.jpeg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(img_hsv)
bright_pixel = np.mean(v)
print(bright_pixel)