import cv2
import numpy as np
from Libraries.Camera import CameraObject

def nothing(x):
    pass

cap = CameraObject(0, WaitReady=False, ScreenCapture=False, Receive=False)

# Create a window
cv2.namedWindow('image')
# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0
Array = np.zeros([480, 640, 3], np.uint8)
Array[:, :] = (80, 0, 0)
Array2 = np.zeros([480, 640, 3], np.uint8)
Array2[:, :] = (0, 0, 50)

mon = {'left': 0, 'top': 0, 'width': 960, 'height': 480}

old_mask = None
while True:
    frame = cap.read(mon)
    frame = cv2.resize(frame, (960, 480))
    if not frame.any() or cv2.waitKey(10) & 0xFF == ord('q'):
        break
    # frame = cv2.add(frame, Array)#renk ekle
    # frame=cv2.subtract(frame,Array2)#renk çıkar
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')
    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')


    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    #mask = cv2.GaussianBlur(mask, (25, 25), 0)
    if old_mask is not None:
        result_frame = cv2.bitwise_or(mask, old_mask)
    else :
        result_frame = mask


    old_mask = mask
    result = cv2.bitwise_and(frame, frame, mask=result_frame)

    # Print if there is a change in HSV value
    if (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
            hMin, sMin, vMin, hMax, sMax, vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display result image
    cv2.imshow('image', result)

cap.release()
cv2.destroyAllWindows()