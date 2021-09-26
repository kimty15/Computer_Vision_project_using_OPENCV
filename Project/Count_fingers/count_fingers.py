import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = "Fingers"
mylist = os.listdir(folderPath)
print(mylist)
overlaylist = []
for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    image = cv2.resize(image, (200,200))
    overlaylist.append(image)
print(len(overlaylist))
# for id in range(0,6):
#     w, h, c = overlaylist[id].shape
#     print(w, ' ', h, ' ', c)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipsId = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)
    if len(lmList) != 0:
        fingers =[]
        #THUMB
        if lmList[tipsId[0]][1] > lmList[tipsId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #The rest
        for id in range(1, 5):
            if lmList[tipsId[id]][2] < lmList[tipsId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        total_finger = fingers.count(1)
        print(total_finger)
        h, w, c = overlaylist[total_finger-1].shape
        img[0:h, 0:w] = overlaylist[total_finger-1]
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(total_finger), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (500,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)