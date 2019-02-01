import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
	ret, frame = cap.read()
	if ret:
		img = frame.copy()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		cv2.imshow('MadvideoAvant', frame)
		cv2.imshow('MavideoApres', gray)
	else:
		print('video ended')
	if cv2.waitKey(45) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()