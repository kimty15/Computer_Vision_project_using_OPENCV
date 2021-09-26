import cv2
import HandTrackingModule as htm
import numpy as np
import cvzone
startDist = None
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 480)
colorR =(255,0,255)
detector = htm.handDetector(detectionCon=0.8)
cx, cy, w, h = 100, 100, 200, 200

class DragDect():
    def __init__(self, posCenter, size =[200,200]):
        self.posCenter = posCenter
        self.size = size
    def update(self,cursor ):
        cx, cy = self.posCenter
        w, h = self.size
        #if index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor
rectList =[]
for x in range(3):
    rectList.append(DragDect([x * 250 + 150, 150]))
while True:
    success, img = cap.read()
    cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if lmList:
        if startDist is None:
            length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        if length < 40:
            cursor = lmList[8]
            #call the update
            for rect in rectList:
                rect.update(cursor)
    ## Draw solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx - w // 2, cy - h // 2),
    #                   (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    #     cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
    ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)