import cv2
import mediapipe as mp
import time

cap= cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
pTime=0
cTime=0
while True:
    success,img=cap.read()
    img_RGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(img_RGB)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id,lm in enumerate(hand_landmarks.landmark):

                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if id==4:
                    cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)

            mpDraw.draw_landmarks(img,hand_landmarks,mpHands.HAND_CONNECTIONS)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)


    cv2.imshow("Image",img)
    cv2.waitKey(1)
