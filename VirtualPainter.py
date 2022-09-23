# Import opencv for computer vision stuff
import cv2
#Import Time
import time

#Import hand Tracking Module
from Hand_Tracking_Module import handTrackingModule as htm


pTime = 0
detector = htm.handDetector(maxHands = 2)

# Connect to webcam
cap = cv2.VideoCapture(0)
# Loop through every frame until we close our webcam
while cap.isOpened():
    # Find  Hand
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList, bbox = detector.findPosition(frame)

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 245, 0), 3)

    # Show image
    cv2.imshow('Webcam', frame)

    # Checks whether q has been hit and stops the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases the webcam
cap.release()
# Closes the frame
cv2.destroyAllWindows()

