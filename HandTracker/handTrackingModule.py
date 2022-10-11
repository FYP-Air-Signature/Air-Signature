
'''------------------Creating Hand trackig Package----------------------------'''
import cv2 
import mediapipe as np
import time
import math



'''-------------------------------Creation  of Hand_Detection Class---------------------------------'''
'''
               Methods inside Hand Detection Class

               1.findHands() :-   Detect No of Hands Inside The Frame

               2.FindPosition() :-  Find location Of Hands Points

               3. FingerUp() :-  Count Number Of Finger Up 

               4. Distance() :- Find Distance Between Two Points Of Finger's
         
'''


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon


        self.npHands=np.solutions.hands
        self.hands=self.npHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.npDraw=np.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]
        

    
    def findHands(self,img,draw=True):

        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                   self.npDraw.draw_landmarks(img,handLMS,self.npHands.HAND_CONNECTIONS)
      
        return img 


    def findPosition(self,img,handNo=0,draw=True):

        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                h,w,c=img.shape
                cx, cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                self.lmlist.append([id,cx,cy])
               
                if draw:
                     cv2.circle(img,(cx,cy),7,(255,0,255),cv2.FILLED)

        return self.lmlist

    def fingerUp(self):
        finger=[]
        #Thumb
        if self.lmlist[self.tipIds[0]] [1] < self.lmlist[self.tipIds[0]-1][1]:
            finger.append(0)
        else:
            finger.append(1)

        # 4 finger

        for id in range(1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
                finger.append(1)
            else:
                finger.append(0)
        return finger
        

    def Distance(self,img,Top_1,Top_2,draw=True):
        x1,y1=self.lmlist[Top_1][1:]
        x2,y2=self.lmlist[Top_2][1:]

        cx,cy=(x1+x2)//2 , (y1+y2)//2

        length=math.hypot(x1-x2,y1-y2)

        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.circle(img,(cx,cy),7,(0,0,255),cv2.FILLED)
        
        return length


'''--------------------------Main Function-----------------------------------'''

def main():
    
    pTime=0
    cTime=0

    cap=cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        success,img=cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)


        
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,170),2)

        cv2.imshow("output",img)
        if(cv2.waitKey(1)==27):
            break



if __name__=="__main__":
    main()