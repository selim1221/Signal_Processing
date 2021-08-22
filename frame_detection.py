import PIL.Image
import numpy as np
import pyautogui
import numpy
import imutils
import cv2
import time
import matplotlib.pyplot as plt
from datetime import datetime

# TODO: write function for each operation.
time.sleep(2)
LOWER_RESOLUTION = True
BLACK_PIXEL_THRESHOLD = 65
start = datetime.now()
while True:
    image = pyautogui.screenshot()
    image = np.array(image)

    if LOWER_RESOLUTION:
        image = cv2.resize(image, (720, 480), interpolation=cv2.INTER_AREA)

    blue, green, red = cv2.split(image)
    x_indexes = []  # this will hold the indexes of vertical black lines,
    x_indexes_of_last_row = []  # this will hold the indexes of vertical black lines of last row,
    # since black lines are bold there may be consecutive black lines, take only one of them.
    x_indexes_duplicates_removed = []  # this will hold the indexes of vertical black lines
    x_indexes_last_row_duplicates_removed = []  # this will hold the indexes of vertical black lines
    y_indexes = []  # this will hold the indexes of horizontal black lines,
    # since black lines are bold there may be consecutive black lines, take only one of them.
    y_indexes_duplicates_removed = []  # this will hold the indexes of horizontal black lines
    frame_rows = []  # this will hold the corner points of each frame,
    # e.g: [[x_str1,x_end1,y_str1,y_end1], [x_str1,x_end1,y_str1,y_end1],..]
    frame_indexes = []
    # TODO: a further improvement: instead of calculating these in each screenshot,
    #  we can keep track the number of participants from meeting settings
    #  and recalculate these when there is a change in there.
    print((datetime.now() - start).total_seconds())

    #################################################
    ## find horizontal black line indexes
    for i in range(len(blue) * 1 // 20,
                   len(blue) * 19 // 20):  # do not start from the beginning, cut first and last 5% to eliminate window header
        is_current_black = True
        for j in range(len(blue[i])):
            if not (blue[i][j] < BLACK_PIXEL_THRESHOLD
                    and red[i][j] < BLACK_PIXEL_THRESHOLD
                    and green[i][j] < BLACK_PIXEL_THRESHOLD):
                is_current_black = False
                break
        if is_current_black:
            y_indexes.append(i)
    #################################################

    #################################################
    ### remove duplicates from horizantal indexes
    for i in range(len(y_indexes) - 1):
        if y_indexes[i + 1] - y_indexes[i] > 50:
            y_indexes_duplicates_removed.append(y_indexes[i])
            last = y_indexes[i + 1]
    y_indexes_duplicates_removed.append(last)
    #################################################

    print((datetime.now() - start).total_seconds())

    # row pictures
    for j in range(len(y_indexes_duplicates_removed) - 1):
        frame_rows.append([0, len(blue[1]), y_indexes_duplicates_removed[j], y_indexes_duplicates_removed[j + 1]])
    #################################################
    for i, indexes in enumerate(frame_rows):
        cv2.imwrite("./frames/framexx{}.png".format(i), image[indexes[2]: indexes[3], indexes[0]: indexes[1]])

    #################################################

    #################################################
    print(y_indexes)
    print(x_indexes_duplicates_removed)
    print(x_indexes_last_row_duplicates_removed)
    print(y_indexes_duplicates_removed)
    print(frame_rows)
    print(frame_indexes)
    ### find vertical black line indexes except last row
    for i in range(frame_rows[0][0], frame_rows[0][1]):
        is_current_black = True
        for j in range(frame_rows[0][2], frame_rows[0][3]):
            if not (blue[j][i] < BLACK_PIXEL_THRESHOLD
                    and red[j][i] < BLACK_PIXEL_THRESHOLD
                    and green[j][i] < BLACK_PIXEL_THRESHOLD):
                is_current_black = False
                break
        if is_current_black:
            x_indexes.append(i)
    #################################################

    ### TODO: check whether we seperated successfully
    ################################################
    # how: maybe check difference of successive numbers (lengths) if something vary, there might be a mistake
    ################################################

    #################################################
    ### remove duplicates from vertical indexes
    last = ""
    for i in range(len(x_indexes) - 1):
        if x_indexes[i + 1] - x_indexes[i] > 50:
            first = x_indexes[i]
            if last != "":
                x_indexes_duplicates_removed.append((first + last) // 2)
            else:
                x_indexes_duplicates_removed.append(first)
            last = x_indexes[i + 1]
    x_indexes_duplicates_removed.append(last)
    #################################################

    #################################################
    ### find vertical black line indexes of last row
    for i in range(frame_rows[-1][0], frame_rows[-1][1]):
        is_current_black = True
        for j in range(frame_rows[-1][2], frame_rows[-1][3]):
            if not (blue[j][i] < BLACK_PIXEL_THRESHOLD
                    and red[j][i] < BLACK_PIXEL_THRESHOLD
                    and green[j][i] < BLACK_PIXEL_THRESHOLD):
                is_current_black = False
                break
        if is_current_black:
            x_indexes_of_last_row.append(i)
    #################################################

    #################################################
    ### remove duplicates from vertical indexes of last row
    last = ""
    for i in range(len(x_indexes_of_last_row) - 1):
        if x_indexes_of_last_row[i + 1] - x_indexes_of_last_row[i] > 50:
            first = x_indexes_of_last_row[i]
            if last != "":
                x_indexes_last_row_duplicates_removed.append((first + last) // 2)
            else:
                x_indexes_last_row_duplicates_removed.append(first)
            last = x_indexes_of_last_row[i + 1]
    x_indexes_last_row_duplicates_removed.append(last)
    #################################################

    #################################################
    ### construct frames except final row
    for row in frame_rows[:-1]:
        for i in range(len(x_indexes_duplicates_removed) - 1):
            frame_indexes.append([x_indexes_duplicates_removed[i], x_indexes_duplicates_removed[i + 1], row[2], row[3]])
    #################################################

    #################################################
    ### construct frames of final row
    for i in range(len(x_indexes_last_row_duplicates_removed) - 1):
        frame_indexes.append(
            [x_indexes_last_row_duplicates_removed[i], x_indexes_last_row_duplicates_removed[i + 1], frame_rows[-1][2],
             frame_rows[-1][3]])
    #################################################

    #################################################
    print(frame_indexes)
    print((datetime.now() - start).total_seconds())
    for i, indexes in enumerate(frame_indexes):
        cv2.imwrite("./frames/frame{}.png".format(i), image[indexes[2]: indexes[3], indexes[0]: indexes[1]])
    #################################################
