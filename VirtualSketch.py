# Import opencv for computer vision stuff
import cv2
import numpy as np

# Import hand Tracking Module
from HandTracker import htm

####################################
camHeight, camWidth = 540, 960
pTime = 0
detector = htm.handDetector(maxHands=1)
drawColor = (255, 255, 255)
brushThickness = 15
xPrevious, yPrevious = 0, 0
imgCanvas = np.zeros((camHeight, camWidth, 3), np.uint8)
smooth = 5
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
        if fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
            # print("Draw")
            cv2.circle(frame, (indFx, indFy), 15, drawColor, cv2.FILLED)

            # check if it is a first frame
            if xPrevious == 0 and yPrevious == 0:
                xPrevious, yPrevious = indFx, indFy

            # # smoothening
            # indFx = xPrevious + (indFx - xPrevious)//smooth
            # indFy = yPrevious + (indFy - yPrevious) // smooth

            # cv2.line(frame, (xPrevious, yPrevious), (indFx, indFy), drawColor, brushThickness)
            cv2.line(imgCanvas, (xPrevious, yPrevious), (indFx, indFy), drawColor, brushThickness)
            # update previous point
            xPrevious, yPrevious = indFx, indFy

        if fingers[1:4] == [1, 1, 1]:
            imgCanvas = np.zeros((camHeight, camWidth, 3), np.uint8)

    # Show image
    cv2.imshow('Webcam', frame)
    cv2.imshow('ImgCanvas', imgCanvas)
    # Checks whether q has been hit and stops the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases the webcam
cap.release()
# Closes the frame
cv2.destroyAllWindows()
