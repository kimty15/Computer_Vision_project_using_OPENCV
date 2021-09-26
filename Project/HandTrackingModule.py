import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        h, w, c = img.shape
        allHands = []

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py = int(lm.x * w), int(lm.y * h)
                    xList.append(px)
                    yList.append(py)
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (0, 0, 255), 2)
        return img
    # def findHands(self, img, draw=True, flipType=True):
    #     """
    #     Finds hands in a BGR image.
    #     :param img: Image to find the hands in.
    #     :param draw: Flag to draw the output on the image.
    #     :return: Image with or without drawings
    #     """
    #     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     self.results = self.hands.process(imgRGB)
    #     allHands = []
    #     h, w, c = img.shape
    #     if self.results.multi_hand_landmarks:
    #         for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
    #             myHand = {}
    #             ## lmList
    #             mylmList = []
    #             xList = []
    #             yList = []
    #             for id, lm in enumerate(handLms.landmark):
    #                 px, py = int(lm.x * w), int(lm.y * h)
    #                 mylmList.append([px, py])
    #                 xList.append(px)
    #                 yList.append(py)
    #
    #             ## bbox
    #             xmin, xmax = min(xList), max(xList)
    #             ymin, ymax = min(yList), max(yList)
    #             boxW, boxH = xmax - xmin, ymax - ymin
    #             bbox = xmin, ymin, boxW, boxH
    #             cx, cy = bbox[0] + (bbox[2] // 2), \
    #                      bbox[1] + (bbox[3] // 2)
    #
    #             myHand["lmList"] = mylmList
    #             myHand["bbox"] = bbox
    #             myHand["center"] = (cx, cy)
    #
    #             if flipType:
    #                 if handType.classification[0].label == "Right":
    #                     myHand["type"] = "Left"
    #                 else:
    #                     myHand["type"] = "Right"
    #             else:
    #                 myHand["type"] = handType.classification[0].label
    #             allHands.append(myHand)
    #
    #             ## draw
    #             if draw:
    #                 self.mpDraw.draw_landmarks(img, handLms,
    #                                            self.mpHands.HAND_CONNECTIONS)
    #                 cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
    #                               (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
    #                               (255, 0, 255), 2)
    #                 cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
    #                             2, (255, 0, 255), 2)
    #     if draw:
    #         return allHands, img
    #     else:
    #         return allHands

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

    def findDistance(self, p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()