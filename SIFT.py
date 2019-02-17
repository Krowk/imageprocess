import numpy as np
import cv2
from matplotlib import pyplot as plt
from tkinter.filedialog import askopenfilename


img1 = cv2.imread("oct_output_2_0.png")         # queryImage
img2 = cv2.imread("oct_output_3_0.png") # trainImage

# Initiate SURF detector
sift=cv2.xfeatures2d.SIFT_create()
def match_sift(img1,img2):

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            a=len(good)
    return len(good)/float(len(kp2))

def representant(images: list):
    n = len(images)
    distances = np.zeros(shape=[n, n], dtype=np.float32)
    print("Computing distance Matrix")
    for i in range(n):
        for j in range(i + 1):
            d = 1 - match_sift(images[i], images[j])
            distances[i, j] = d
            distances[j, i] = d
    print("Distances compute complete")
    costs = distances.sum(axis=1)
    return costs.argmin(axis=0, fill_value=10e9)
