import cv2
import numpy as np

if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow("result")
cv2.namedWindow("settings")

cap = cv2.VideoCapture(0)

cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(11, 50)
cap.set(10, 50)
cap.set(15, -3)
cap.set(17, 5000)
crange = [0, 0, 0, 0, 0, 0]
flag = True
while True:
    flag, img = cap.read()
    if flag:
        img = cv2.resize(img, (1280, 720))
        pts1 = np.float32([[584, 303], [967, 307], [254, 607], [1254, 676]])
        w1 = 432
        h1 = 720
        pts2 = np.float32([[0, 0], [w1, 0], [0, h1], [w1, h1]])
        m = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, m, (w1, h1))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')
        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        cv2.imshow('result', thresh)

        ch = cv2.waitKey(5)
        if ch == 27:
            break

cap.release()
cv2.destroyAllWindows()