# Import opencv for computer vision stuff
import cv2
import numpy as np

# Import math Library
import math


# Import hand Tracking Module
from HandTracker import htm

####################################
camHeight, camWidth = 540, 960
pTime = 0
detector = htm.handDetector(maxHands=1)
drawColor = (141, 43, 193)
brushThickness = 5
xPrevious, yPrevious = 0, 0
imgCanvas = np.zeros((camHeight, camWidth, 3), np.uint8)
smooth = 2
rectIniWid, rectIniHei = int(camWidth * 0.1), int(camHeight * 0.1)
rectEndWid, rectEndHei = int(camWidth * 0.9), int(camHeight * 0.4)
####################################

########## CONSTANTS ###############
MIN_DISTANCE_THRESHOLD = 1
####################################

# Connect to webcam
cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeight)
# Loop through every frame until we close our webcam
while cap.isOpened():
    # Find  Hand
    ret, frame = cap.read()

    # Flip img
    frame = cv2.flip(frame, 1)

    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) != 0:
        # tip of index finger
        indFx, indFy = lmList[8][1:]

        # tip of mid finger
        midFx, midFy = lmList[12][1:]

        # fingers up detection
        fingers = detector.fingerUp()

        # Pause Mode
        if fingers[1] and fingers[2]:
            xPrevious, yPrevious = 0, 0

        # Draw Mode
        if fingers[1] and not fingers[2] and not fingers[3] and not fingers[4] and rectIniWid < indFx < rectEndWid \
                and rectIniHei < indFy < rectEndHei:

            # print("Draw")
            cv2.circle(frame, (indFx, indFy), 10, drawColor, cv2.FILLED)

            # check if it is a first frame
            if xPrevious == 0 and yPrevious == 0:
                xPrevious, yPrevious = indFx, indFy

            # # smoothening
            indFx = xPrevious + (indFx - xPrevious)//smooth
            indFy = yPrevious + (indFy - yPrevious) // smooth

            # cv2.line(frame, (xPrevious, yPrevious), (indFx, indFy), drawColor, brushThickness)
            # Calculate Euclidean distance
            distance = int((math.dist((xPrevious, yPrevious), (indFx, indFy))))
            nippleThickness = brushThickness // distance if distance > 0 else brushThickness
            nippleThickness = nippleThickness if nippleThickness > 0 else MIN_DISTANCE_THRESHOLD
            cv2.line(imgCanvas, (xPrevious, yPrevious), (indFx, indFy), drawColor, nippleThickness)
            # update previous point
            xPrevious, yPrevious = indFx, indFy

        if fingers[1:4] == [1, 1, 1]:
            imgCanvas = np.zeros((camHeight, camWidth, 3), np.uint8)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, imgCanvas)

    frame = cv2.rectangle(frame, (rectIniWid, rectIniHei), (rectEndWid, rectEndHei), (0, 78, 0), 2)

    # Show image
    cv2.imshow('Webcam', frame)
    #cv2.imshow('ImgCanvas', imgCanvas)

    # Checks whether q has been hit and stops the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases the webcam
cap.release()
# Closes the frame
cv2.destroyAllWindows()
