# Mon script OpenCV : Video_processing
# On importe les librairies nécessaires que sont numpy et cv2
import numpy as np
import cv2
kernel = np.ones((5,5),np.uint8)

# On définit une fonction de processing de l'image, passant les couleurs en niveaux de gris
def gray(imgc):
    return cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)

# applique un floue standard à l'image
def blur(imgc):
 return cv2.blur(imgc, (5,5))

# applique un floue gaussian à l'image
def gaussian_blur(imgc):
 return cv2.GaussianBlur(imgc,(5,5), 0)
#applique l'algorithme laplacian à l'image
def laplacian(imgc):
 return cv2.Laplacian(imgc, cv2.CV_8U)

#applique l'algorithme canny à l'image
def canny(imgc):
 return cv2.Canny(imgc, 100, 200)
#applique le global threshold à l'image
def global_threshold(imgc):
 ret, frame = cv2.threshold(imgc, 127, 255, cv2.THRESH_BINARY)
 return frame

#applique le threshold mean adaptatif à l'image
def adaptive_mean_threshold(imgc):
    return cv2.adaptiveThreshold(imgc,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

#applique le threshold gaussian adaptatif à l'image
def adaptive_gaussian_threshold(imgc):
    return cv2.adaptiveThreshold(imgc,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
#applique l'algorithme de sobel à l'image
def sobel(imgc):
    return cv2.Sobel(imgc,cv2.CV_64F,1,0,ksize=5)
#applique le traitement opening à l'image
def opening(imgc):
    return cv2.morphologyEx(adaptive_mean_threshold(imgc), cv2.MORPH_OPEN, kernel)
#applique le traitement gradient à l'image
def gradient(imgc):
    return cv2.morphologyEx(adaptive_mean_threshold(imgc), cv2.MORPH_GRADIENT, kernel)
    # applique le traitement dilation à l'image
def dilation(imgc):
    return cv2.dilate(adaptive_mean_threshold(imgc), kernel, iterations=1)
# applique le traitement erosion à l'image
def erosion(imgc):
    return cv2.erode(adaptive_mean_threshold(imgc), kernel, iterations=1)
    # applique le traitement closing à l'image
def closing(imgc):
    return cv2.morphologyEx(adaptive_mean_threshold(imgc), cv2.MORPH_CLOSE, kernel)



# On définit une variable associée à l'entrée vidéo que l'on veut traiter
cap = cv2.VideoCapture('lancelot.mp4')

while (True):
    # On récupère la prochaine image du flux vidéo ainsi qu'un flag
    ret, frame = cap.read()

    # Si le flag est à True on traite l'image
    if ret == True:

        # On copie l'image afin de pouvoir la traiter sans perdre l'orignal
        img = frame.copy()

        # On applique ici la fonction gray à la copie
        img = gray(img)

        # Ici on affiche en sortie deux vidéos, la première étant notre vidéo d'origine et la deuxième celle modifiée
        cv2.imshow('MavideoAvant', frame)
        cv2.imshow('MavideoApres', img)
    # Si le flag est à False, on sort de la boucle
    else:
        print('video ended')
        break

    # On attend une seconde avant d'afficher la prochaine image et si l'utilisateur presse 'q' on sort de la boucle.
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break
# When everything's done, release the capture
cap.release()
cv2.destroyAllWindows()








