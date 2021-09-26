import os

import cv2

path ='Fingers'
mylist = os.listdir(path)
for image in mylist:
    img = cv2.imread(f'{path}/{image}')
    img = cv2.resize(img, (150, 150))
    img = cv2.imwrite(f'{path}/{image}', img)