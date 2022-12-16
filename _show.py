# This script simply displays the image captured by the webcam.
#
# Last edit: 14 Nov, 2022 
# By: Jonah Boe
#

import cv2  
from PIL import Image  
img = cv2.imread("images/portrait.jpg", 1)
img2 = Image.fromarray(img, 'RGB')
cv2.imshow("Image", img)
img2.show()
