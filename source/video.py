import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)
while True:



    ret, img = cam.read()
    img=cv2.resize(img,(340,220))
    lowerBound = np.array([21, 89, 49])
    upperBound = np.array([152, 255, 255])
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerBound, upperBound) #'маска для зеленого цвета'
    #cv2.imshow("mask", mask)
    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))

    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    #cv2.imshow("maskOpen", maskOpen)

    maskFinal = maskClose

    _, contours, hierarchy = cv2.findContours(maskFinal, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(img, contours, -1, (255, 105, 180), 3)
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])#описывающий прямоугольник
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, str(i + 1), (x, y + h), font, 0.5, (0, 0, 128),2)
    cv2.imshow("cam", img)
    cv2.imshow("maskClose", maskClose)
    cv2.waitKey(10)

