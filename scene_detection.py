import cv2
import numpy as np
import SIFT

# Advanced Scene Detection Parameters
INTENSITY_THRESHOLD = 16  # Pixel intensity threshold (0-255), default 16
MINIMUM_PERCENT = 95  # Min. amount of pixels to be below threshold.
BLOCK_SIZE = 32  # Num. of rows to sum per iteration.

cap = cv2.VideoCapture("lancelot.mp4")


def to_numpy(img):
    return np.asfarray(img) * (1.0 / 255.0)


def from_numpy(mat):
    mat = mat * 255
    return mat.astype(np.uint8, copy=True)


def avg(plan, n):
    res = to_numpy(plan[0])
    for frame in plan[1:]:
        res += to_numpy(frame)
    res = (res - np.min(res)) / (np.max(res) - np.min(res))
    res = from_numpy(res)

    cv2.imwrite('medoid' + str(n) + '.png', plan[np.argmax([SIFT.match_sift(res, frame, 0.9) for frame in plan])])

    cv2.imwrite('avg' + str(n) + '.png', res)


def rep(plan, n):
    best_score = 0
    best_frame = None
    i = np.random.randint(len(plan))
    best = i
    curr_frame = plan[i]
    l = [SIFT.match_sift(curr_frame, frame, 0.9) for frame in plan[max(0, i - 10): i] + plan[i + 1: i + 11]]
    if np.max(l) > best_score:
        best_score = np.max(l)
        best_frame = plan[max(0, i - 10 + np.argmax(l))]
    np.argmax(l)


# Do stuff with cap here.

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(
    "Video Resolution: %d x %d" % (width, height))

# Allow the threshold to be passed as an optional, second argument to the script.
threshold = 16
print(
    "Detecting scenes with threshold = %d" % threshold)
print(
    "Min. pixels under threshold = %d %%" % MINIMUM_PERCENT)
print(
    "Block/row size = %d" % BLOCK_SIZE)
print("")

min_percent = MINIMUM_PERCENT / 100.0
num_rows = BLOCK_SIZE
last_amt = 0  # Number of pixel values above threshold in last frame.
start_time = cv2.getTickCount()  # Used for statistics after loop.

n = 0
l = []
while True:
    # Get next frame from video.
    (rv, im) = cap.read()
    if not rv:  # im is a valid image if and only if rv is true
        break

    l.append(im)

    # Compute # of pixel values and minimum amount to trigger fade.
    num_pixel_vals = float(im.shape[0] * im.shape[1] * im.shape[2])
    min_pixels = int(num_pixel_vals * (1.0 - min_percent))

    # Loop through frame block-by-block, updating current sum.
    frame_amt = 0
    curr_row = 0
    while curr_row < im.shape[0]:
        # Add # of pixel values in current block above the threshold.
        frame_amt += np.sum(
            im[curr_row: curr_row + num_rows, :, :] > threshold)
        if frame_amt > min_pixels:  # We can avoid checking the rest of the
            break  # frame since we crossed the boundary.
        curr_row += num_rows
    # Detect fade in from black.
    if frame_amt >= min_pixels and last_amt < min_pixels:
        print(
            "Detected fade in at %dms (frame %d)." % (
                cap.get(cv2.CAP_PROP_POS_MSEC),
                cap.get(cv2.CAP_PROP_POS_FRAMES)))
        # l.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
        avg(l, n)
        l = []
        n += 1
    # Detect fade out to black.
    elif frame_amt < min_pixels and last_amt >= min_pixels:
        print(
            "Detected fade out at %dms (frame %d)." % (
                cap.get(cv2.CAP_PROP_POS_MSEC),
                cap.get(cv2.CAP_PROP_POS_FRAMES)))
        # l.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
        avg(l, n)
        l = []
        n += 1
    last_amt = frame_amt  # Store current mean to compare in next iteration.
# l.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
avg(l, n)

# Get # of frames in video based on the position of the last frame we read.
frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
# Compute runtime and average framerate
total_runtime = float(cv2.getTickCount() - start_time) / cv2.getTickFrequency()
avg_framerate = float(frame_count) / total_runtime

print(
    "Read %d frames from video in %4.2f seconds (avg. %4.1f FPS)." % (
        frame_count, total_runtime, avg_framerate))

cap.release()
"""
cap = cv2.VideoCapture("lancelot.mp4")
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


n = 0
print(l)
last = None
t= []

def to_numpy(img):
    return np.asfarray(img) * (1.0 / 255.0)


def from_numpy(mat):
    mat = mat * 255
    return mat.astype(np.uint8, copy=True)


while True:
    (rv, im) = cap.read()
    if not rv:  
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == l[n]: 
        if n != 0:
            #last /= frame_count
            last /= np.max(last) - np.min(last)
            last = from_numpy(last)
            cv2.imwrite('test'+str(n)+'.png', last)
        last = to_numpy(im)
        n+=1

        #changement de plan
    #last = cv2.addWeighted(last,0.5 + (n / frame_count) * 2, im, 0.5 - (n / frame_count )*2,0 )
    last += to_numpy(im)

"""