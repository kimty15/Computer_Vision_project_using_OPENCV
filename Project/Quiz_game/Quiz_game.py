import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
pathcsv = "Question.csv"

class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None
    def update(self, cursor, bboxs):
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1< cursor[0]< x2  and y1 <cursor[1]< y2:
                self.userAns = x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)
with open(pathcsv, newline='\n') as f:
    reader = csv.reader(f)
    Alldata = list(reader)[1:]
#print((data))
qNo =0
qTotal = len(Alldata)
mcqList =[]
for q in Alldata:
    mcqList.append(MCQ(q))
detector = HandDetector(detectionCon=0.8)
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands , img = detector.findHands(img, flipType=False)
    if qNo<qTotal:
        mcq = mcqList[qNo]
        img, bbox = cvzone.putTextRect(img, mcq.question,[100,100], 2,2,offset=25, border=3)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=25, border=3)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=25, border=3)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=25, border=3)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=25, border=3)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info, img = detector.findDistance(lmList[8],lmList[12],img)
            if length <50 :
                mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
                print(mcq.userAns)
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo+=1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score +=1
        score = round((score/qTotal)*100,2)
        img,_ = cvzone.putTextRect(img, "Quiz completed",[250,300],2,2,offset=30, border=5)
        img,_ = cvzone.putTextRect(img,f'Your score: {score}%',[700,300],2,2,offset=30,border=5)


    #Draw progress bar
    barValue = 150 +(950//qTotal)*qNo
    cv2.rectangle(img, (150,600),(barValue,650),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100,650),(255,0,255),3)
    img,_ = cvzone.putTextRect(img, f'{round((qNo/qTotal)*100)}%',[1135,650],2,2,offset=16)
    cv2.imshow("Image",img)
    cv2.waitKey(1)