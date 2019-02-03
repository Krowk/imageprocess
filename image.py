import cv2
import numpy as np

cap = cv2.VideoCapture("lancelot.mp4")
kernel = np.ones((5,5),np.uint8)
for i in range(2650):
    cap.read()
while True:
    ret, frame = cap.read()
    if ret:
        img = frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),8)
        median = cv2.medianBlur(gray,5)

        sobelx64f = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
        abs_sobel64f = np.absolute(sobelx64f)
        sobel_8u = np.uint8(abs_sobel64f)
        th1 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
        th2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)   
        th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
        opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
        gradient = cv2.morphologyEx(th2, cv2.MORPH_GRADIENT, kernel)
        dilation = cv2.dilate(th2, kernel, iterations=1)
        erosion = cv2.erode(th2, kernel, iterations=1)
        closing = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)
        edges = cv2.Canny(erosion,100,200)
        laplacian = cv2.Laplacian(erosion,cv2.CV_8U)
        sobelx8u = cv2.Sobel(dilation, cv2.CV_8U, 1, 0, ksize=5)



        cv2.imshow('MadvideoAvant', dilation)
        cv2.imshow('MavideoApres', sobelx8u)
    else:
        print('video ended')
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()