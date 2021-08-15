import numpy as np
import pyautogui
import numpy
import imutils
import cv2
import time

sayi = 0

while sayi < 10:

    image = pyautogui.screenshot("resim {}.png".format(sayi))
    time.sleep(0.3)
    sayi += 1

#0.3 saniye aralıklarla 10 adet ekran görüntüsü alıyor.

