#Takes the pictures for the training

import numpy as np
import os
import cv2

face_cascade = cv2.CascadeClassifier('/home/edov84/Documentos/TEC/Semestre1_2020/Taller_Sistemas_Embebidos/Proyecto3/Entrenador/haarcascade_frontalface_alt.xml')

cap = cv2.VideoCapture(0)
path = "/home/edov84/Documentos/TEC/Semestre1_2020/Taller_Sistemas_Embebidos/Proyecto3/Entrenador/"# path were u want store the data set
id = input('Digite su nombre entre comillas: ')

try:
    # Create target Directory
    os.mkdir(path+str(id))
    print("Directory " , path+str(id),  " Created ") 
except FileExistsError:
    print("Directory " , path+str(id) ,  " already exists")

sampleN=0;

while 1:

    ret, img = cap.read()
    frame = img.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        sampleN=sampleN+1

        cv2.imwrite(path+str(id)+ "/" +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.waitKey(1)

    if sampleN > 100:

        break

cap.release()
cv2.destroyAllWindows()
