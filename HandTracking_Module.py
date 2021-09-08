import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self,mode=False,maxhands=2,detectconf=0.5,trackconf=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detectconf=detectconf
        self.trackconf=trackconf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.detectconf,self.trackconf)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw=True):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo=0,draw=True):
        lm_list=[]
        if self.results.multi_hand_landmarks:
            my_hand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(my_hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id,cx,cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return lm_list


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector=HandDetector()
    while True:
        success, img = cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist)!=0:
            print(lmlist[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__=="__main__":
    main()
