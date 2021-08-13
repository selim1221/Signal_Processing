import numpy as np
import pyautogui
import numpy
import imutils
import cv2
import time
import matplotlib.pyplot as plt


image = cv2.imread("zoom.jpg")

blue, green, red = cv2.split(image)

contours1, hierarchy1 = cv2.findContours(image=blue, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(image_gray, 50, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

image_copy = image.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)


cv2.imshow("resim", image_copy)
cv2.imshow("resim2", thresh)

#kontur farklılıklarından yararlanarak zoom ekranındaki frameleri ayırıyor. 

cv2.waitKey(0)

cv2.destroyWindow()