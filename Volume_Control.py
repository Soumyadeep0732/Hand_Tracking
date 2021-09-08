import cv2
import time
import numpy as np
import HandTracking_Module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap=cv2.VideoCapture(0)
wcam,hcam=640,480
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector=htm.HandDetector(detectconf=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange=volume.GetVolumeRange()
minvol=volrange[0]
maxvol=volrange[1]
vol=0
volBar=400
volPer=0
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        lx,ly=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,255,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),2)
        cv2.circle(img, (lx, ly), 10, (255, 255, 0), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)

        vol=np.interp(int(length),[50,220],[minvol,maxvol])
        volBar = np.interp(int(length), [50, 220], [400, 150])
        volPer= np.interp(int(length), [50, 220], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        if length<50:
            cv2.circle(img, (lx, ly), 10, (0, 255, 0), cv2.FILLED)


    cv2.rectangle(img,(50,150),(85,400),(0,255,255),2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 255),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 250, 250), 2)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("Img", img)
    cv2.waitKey(1)

