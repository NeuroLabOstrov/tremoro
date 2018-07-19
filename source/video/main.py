from typing import Type
import cv2
import numpy as np
import http.client
import base64

addr = '192.168.43.102'
port = 4444
conn = http.client.HTTPConnection("{0}:{1}".format(addr,port))

font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)


while True:


    ret, img = cam.read()
    img = cv2.resize(img,(640,480))
    lowerBound = np.array([40, 33, 33])
    upperBound = np.array([84, 255, 255])
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


    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])#описывающий прямоугольник

        moments = cv2.moments(contours[i])
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        img = cv2.medianBlur(img, 5)
        #  img = cv2.Canny(img, 100, 200)# делает изображение чб с линиями контуров

        if dArea > 500:
            img = cv2.drawContours(img, contours, i, (255, 105, 180), 3)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, str(i + 1), (x, y + h), font, 0.5, (0, 0, 128),2)
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
            
            request_data = base64.b64encode("{0} {1}".format(x,y).encode()).decode()
            conn.request("GET", "/{0}".format(request_data))
            r1 = conn.getresponse()
            data1 = r1.read().decode()
            
            print(i, ' ', x, ' ',y,' ',data1)

        # if lastx > 0 and lasty > 0:
        #     cv2.line(path, (lastx, lasty), (x, y), path_color, 5)
        #     lastx = x
        #     lasty = y

    cv2.imshow("cam", img)
    cv2.imshow("maskClose", maskClose)
    cv2.waitKey(10)
    
conn.close()
