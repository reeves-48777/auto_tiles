import cv2
import time
import mouse
import numpy as np
from mss import mss
from PIL import Image
from functions import *

BBOX = {'top': 50, 'left': 275, 'width': 425, 'height':765}

sct = mss()

last_time = time.time()
fps_list = []
# time.sleep(4)
while(True):
    try: 
        sct_img = sct.grab(BBOX)
        img = np.array(sct_img)
        grayscale = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(grayscale, 1, 100, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            if len(approx) == 4:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
                cv2.putText(img, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 1)
                cv2.putText(img, "Rectangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1, cv2.LINE_AA)
                print(f"X: {cx} Y: {cy}")
                mouse.move(BBOX['left'] + cx, BBOX['top'] + cy)
                mouse.click()
        
        fps = compute_fps((time.time() - last_time))
        if len(fps_list) >= 10:
            fps_list.pop(0)
        fps_list.append(fps)

        # cv2.putText(img, f"FPS: {compute_fps((time.time() - last_time))}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1, cv2.LINE_AA)

        # on affiche la moyenne des fps
        cv2.putText(img, f"AVG_FPS: {compute_average_fps(fps_list)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1, cv2.LINE_AA)
        
        cv2.imshow('Piano Tiles player', img)
        last_time = time.time()

        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break