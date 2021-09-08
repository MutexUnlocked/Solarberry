import numpy as np
import cv2
from cv2 import cv

# Load image as string from file/database
fd = open('foo.jpg')
img_str = fd.read()
fd.close()

# CV2
nparr = np.fromstring(img_str, np.uint8)
img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1

# CV
img_ipl = cv.CreateImageHeader((img_np.shape[1], img_np.shape[0]), cv.IPL_DEPTH_8U, 3)
cv.SetData(img_ipl, img_np.tostring(), img_np.dtype.itemsize * 3 * img_np.shape[1])

# check types
print type(img_str)
print type(img_np)
print type(img_ipl)
