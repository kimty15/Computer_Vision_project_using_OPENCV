import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVolume = volRange[0]
maxVolume = volRange[1]
vol = 0
volBar = 300
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][0], lmList[4][1]
        x2, y2 = lmList[8][0], lmList[8][1]
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1,y1), 10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255 ), 3)
        cv2.circle(img,(cx,cy),10, (255,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        # print(length)
        #Hand range 50->300, convert volume range -65->0
        vol = np.interp(length,[13,215],[minVolume,maxVolume])
        volBar = np.interp(length,[13,215],[300,100])
        volPer = np.interp(length,[13,215],[0,100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (50,100), (80,300),(0,255,0),3)
    cv2.rectangle(img,(50, int(volBar)),(80,300),(0,255,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 350), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}', (40,50), cv2.FONT_HERSHEY_SIMPLEX,
                1,(255,0,0),2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)