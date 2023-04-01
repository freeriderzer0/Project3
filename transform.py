import cv2
import numpy as np


def transform(img, q, w, a, s):
    pts1 = np.float32([q, w, a, s])
    w1 = 432
    h1 = 720
    pts2 = np.float32([[0, 0], [w1, 0], [0, h1], [w1, h1]])
    m = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, m, (w1, h1))
    dsthsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    # blue
    # h_min_b = np.array((87, 7, 76), np.uint8)
    # h_max_b = np.array((141, 144, 250), np.uint8)
    # yellow
    # h_min_y = np.array((17, 113, 165), np.uint8)
    # h_max_y = np.array((255, 255, 255), np.uint8)
    # purple
    # h_min_p = np.array((100, 55, 0), np.uint8)
    # h_max_p = np.array((150, 255, 225), np.uint8)
    # red
    # h_min_r = np.array((0, 130, 160), np.uint8)
    # h_max_r = np.array((30, 255, 255), np.uint8)
    # green 90 81 107
    h_min_g = np.array((80, 50, 50), np.uint8)
    h_max_g = np.array((100, 200, 200), np.uint8)
    # blue big 108 155 156
    h_min_bb = np.array((98, 50, 50), np.uint8)
    h_max_bb = np.array((118, 200, 200), np.uint8)
    dstf = cv2.inRange(dsthsv, h_min_bb, h_max_bb)
    dstb = cv2.inRange(dsthsv, h_min_g, h_max_g)
    f = det(dstf)
    b = det(dstb)
    # if f and b:
        # file = open('position.txt', 'a+')
        # file.write(str((f[0]+b[0])/2) + ', ' + str((f[1]+b[1])/2) + '\n')
        # file.close()
    return dst, f, b


def det(img):
    moments = cv2.moments(img, 1)
    my = moments['m01']
    mx = moments['m10']
    s = moments['m00']
    if s > 50:
        x = int(mx / s)
        y = int(my / s)
        return (x, y)