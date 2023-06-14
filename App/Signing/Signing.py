# Import opencv for computer vision stuff
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
# Import hand Tracking Module
from App.Signing.HandTracker import htm


class AirSigning:

    def __init__(self, defaultCam=0):
        ####################################
        self.primaryCam = defaultCam
        self.camHeight, self.camWidth = 540, 960
        self.detector = htm.handDetector(maxHands=1)
        self.drawColor = (141, 43, 193)
        self.brushThickness = 5

        self.smooth = 3
        ####################################

        ########## CONSTANTS ###############
        self.cntSign = 1
        ####################################

    def drawSign(self, filePath, loop=False):
        # Connect to webcam
        cap = cv2.VideoCapture(self.primaryCam)
        # cap.set(3, self.camWidth)
        # cap.set(4, self.camHeight)
        self.camWidth = int(cap.get(3))
        self.camHeight = int(cap.get(4))
        # Loop through every frame until we close our webcam

        # Sign Area rectangle
        rectIniWid, rectIniHei = int(self.camWidth * 0.1), int(self.camHeight * 0.1)
        rectEndWid, rectEndHei = int(self.camWidth * 0.9), int(self.camHeight * 0.4)
        xPrevious, yPrevious = 0, 0
        imgCanvas = np.zeros((self.camHeight, self.camWidth, 3), np.uint8)

        while cap.isOpened():
            # Find  Hand
            ret, frame = cap.read()

            # Flip img
            frame = cv2.flip(frame, 1)

            frame = self.detector.findHands(frame)
            lmList = self.detector.findPosition(frame, draw=False)

            if len(lmList) != 0:
                # tip of index finger
                indFx, indFy = lmList[8][1:]

                # fingers up detectionq
                fingers = self.detector.fingerUp()

                # Pause Mode
                if fingers[1] and fingers[2]:
                    xPrevious, yPrevious = 0, 0

                # Draw Mode
                if fingers[1] and not fingers[2] and not fingers[3] and not fingers[
                    4] and rectIniWid < indFx < rectEndWid \
                        and rectIniHei < indFy < rectEndHei:

                    # print("Draw")
                    cv2.circle(frame, (indFx, indFy), 10, self.drawColor, cv2.FILLED)

                    # check if it is a first frame
                    if xPrevious == 0 and yPrevious == 0:
                        xPrevious, yPrevious = indFx, indFy

                    # # smoothening
                    indFx = xPrevious + (indFx - xPrevious) // self.smooth
                    indFy = yPrevious + (indFy - yPrevious) // self.smooth

                    cv2.line(imgCanvas, (xPrevious, yPrevious), (indFx, indFy), self.drawColor, self.brushThickness)
                    # update previous point
                    xPrevious, yPrevious = indFx, indFy

                if fingers[1:4] == [1, 1, 1]:
                    imgCanvas = np.zeros((self.camHeight, self.camWidth, 3), np.uint8)

            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            frame = cv2.bitwise_and(frame, imgInv)
            frame = cv2.bitwise_or(frame, imgCanvas)

            frame = cv2.rectangle(frame, (rectIniWid, rectIniHei), (rectEndWid, rectEndHei), (0, 78, 0), 2)
            # put text
            # Choose the font style and scale
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8

            # Set the position and color for the text
            position = (self.camWidth // 2, self.camHeight - 30)  # Top-left corner coordinates
            color = (0, 0, 0)  # White color

            # Put the text on the image
            cv2.putText(frame, "After draw press 'Q' to continue - >", position, font, font_scale, color, 2,
                        cv2.LINE_AA)

            # Show image
            cv2.imshow('Webcam', frame)
            # cv2.imshow('ImgCanvas', imgCanvas)

            if not loop:
                # Checks whether q has been hit and stops the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    pngOfSign = self.removeBlackBackground(imgCanvas)
                    # save the image as a PNG file in the specified path
                    cv2.imwrite(filePath + "\\tempSign.png", pngOfSign[rectIniHei:rectEndHei, rectIniWid:rectEndWid])
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    pngOfSign = self.removeBlackBackground(imgCanvas)
                    # save the image as a PNG file in the specified path
                    cv2.imwrite(filePath + f"\\tempSign{self.cntSign}.png", pngOfSign[rectIniHei:rectEndHei, rectIniWid:rectEndWid])
                    self.cntSign+=1
                    break

        # Releases the webcam
        cap.release()
        # Closes the frame
        cv2.destroyAllWindows()

        return filePath + "\\tempSign.png"

    def removeBlackBackground(self, imgCanvas):
        # convert the image to grayscale
        gray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

        # threshold the image to create a mask
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

        # invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # apply the mask to the image
        img_masked = cv2.bitwise_and(imgCanvas, imgCanvas, mask=mask)

        # add an alpha channel to the image
        alpha = np.ones(imgCanvas.shape[:2], dtype=np.uint8) * 255
        alpha[mask_inv == 255] = 0
        return cv2.merge((img_masked, alpha))


if __name__ == "__main__":
    signComponent = AirSigning()
    signComponent.drawSign("")
