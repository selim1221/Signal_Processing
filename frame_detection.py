import numpy as np
import pyautogui
import numpy
import imutils
import cv2
import time
import matplotlib.pyplot as plt

BLACK_PIXEL_THRESHOLD = 100

image = cv2.imread("zoom2.png")
blue, green, red = cv2.split(image)
x_indexes = []  # this will hold the indexes of vertical black lines,
# since black lines are bold there may be consecutive black lines, take only one of them.
x_indexes_duplicates_removed = []  # this will hold the indexes of vertical black lines
y_indexes = []  # this will hold the indexes of horizontal black lines,
# since black lines are bold there may be consecutive black lines, take only one of them.
y_indexes_duplicates_removed = []  # this will hold the indexes of horizontal black lines
frame_indexes = []  # this will hold the corner points of each frame,
# e.g: [[x_str1,x_end1,y_str1,y_end1], [x_str1,x_end1,y_str1,y_end1],..]

# TODO: a further improvement: instead of calculating these in each screenshot,
#  we can keep track the number of participants from meeting settings
#  and recalculate these when there is a change in there.

## find horizontal black line locations
for i in range(len(blue) * 8 // 10):  # TODO: do not start from the beginning, cut first 5% to eliminate window header
    is_current_black = True
    for j in range(len(blue[i])):
        if not (blue[i + len(blue) * 1 // 10][j] < BLACK_PIXEL_THRESHOLD
                and red[i + len(blue) * 1 // 10][j] < BLACK_PIXEL_THRESHOLD
                and green[i + len(blue) * 1 // 10][j] < BLACK_PIXEL_THRESHOLD):
            is_current_black = False
            break
    if is_current_black:
        y_indexes.append(i + len(blue) * 1 // 10)

## find vertical black line locations
for j in range(len(blue[0])):
    is_current_black = True
    for i in range(y_indexes[-1] - y_indexes[0]):
        # because top of the picture is not black but window information,
        # also there are meeting settings in the bottom of the window. I dont want to consider them
        if not (blue[i + y_indexes[0]][j] < BLACK_PIXEL_THRESHOLD and
                red[i + y_indexes[0]][j] < BLACK_PIXEL_THRESHOLD
                and green[i + y_indexes[0]][j] < BLACK_PIXEL_THRESHOLD):
            is_current_black = False
            break
    if is_current_black:
        x_indexes.append(j)

print(y_indexes)
print(x_indexes)

for i in range(len(x_indexes) - 1):
    if not x_indexes[i + 1] - x_indexes[i] == 1:
        x_indexes_duplicates_removed.append(x_indexes[i])
x_indexes_duplicates_removed.append(x_indexes[-1])

for i in range(len(y_indexes) - 1):
    if not y_indexes[i + 1] - y_indexes[i] == 1:
        y_indexes_duplicates_removed.append(y_indexes[i])
y_indexes_duplicates_removed.append(y_indexes[-1])

print(y_indexes_duplicates_removed)
print(x_indexes_duplicates_removed)

for i in range(len(x_indexes_duplicates_removed) - 1):
    for j in range(len(y_indexes_duplicates_removed) - 1):
        frame_indexes.append(
            [x_indexes_duplicates_removed[i], x_indexes_duplicates_removed[i + 1]
                , y_indexes_duplicates_removed[j], y_indexes_duplicates_removed[j + 1]])

print(frame_indexes)
for i, indexes in enumerate(frame_indexes):
    cv2.imwrite("./frames/frame{}.png".format(i), image[indexes[2]: indexes[3], indexes[0]: indexes[1]])
# 2 ve 14 numaralar sıkıntılı, onları elemek lazım, bir de en alttakilerin altında ekstra siyah şeritler var. çözülür zor değil
cv2.imshow("resim", cv2.merge([blue, green, red]))
cv2.waitKey(0)
cv2.destroyWindow()

"""

contours1, hierarchy1 = cv2.findContours(image=blue, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(image_gray, 50, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

image_copy = image.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)


#cv2.imshow("resim", image_copy)
#cv2.imshow("resim2", thresh)

#kontur farklılıklarından yararlanarak zoom ekranındaki frameleri ayırıyor. 

#cv2.waitKey(0)

cv2.destroyWindow()
"""
