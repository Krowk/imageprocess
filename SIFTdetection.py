import cv2
import numpy as np

cap = cv2.VideoCapture('lancelot.mp4')
ret, frame = cap.read()

while(cap.isOpened()):
    prev_frame=frame[:]
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #detect key feature points
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)

        #some magic with prev_frame

        #draw key points detected
        img=cv2.drawKeypoints(gray,kp,gray, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("grayframe",img)
    else:
        print('Could not read frame')

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()