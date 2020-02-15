import numpy as np
import cv2
import pickle
import pickle as pkl
import datetime
import MySQLdb
from uuid import uuid4

def face_recognizer():
    face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")
    labels={}
    detected_faces = [];
    with open("labels.pkl","rb") as f:
        og_labels=pickle.load(f)
        labels={v:k for k,v in og_labels.items()}
    cap=cv2.VideoCapture(0)
    i=0
    while cv2.waitKey(1)<0:
        i =i+1
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
        for x,y,w,h in faces:
            roi_gray=gray[y:y+h,x:x+w]
            roi_color=frame[y:y+h,x:x+w]
            id_,conf=recognizer.predict(roi_gray)
            if conf>=45:
                detected_faces.append(labels[id_])
                print(labels[id_])
                font=cv2.FONT_HERSHEY_SIMPLEX
                name=labels[id_]
                color=(0,255,0)
                stroke=2
                cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
            else:
                print("=================")
                eventid = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
                my_item = cv2.imwrite("unknown/{}.jpg".format(eventid), roi_color)

            # my_item=cv2.imwrite("alton2.jpg",roi_gray)
            color=(255,0,0)
            stroke=2
            cv2.rectangle(frame,(x,y),(x+w,y+h),color,stroke)
        cv2.imshow('frame',frame)
        if i==500:
        # if cv2.waitKey(0):
            break
    cap.release()
    cv2.destroyAllWindows()
    db = MySQLdb.connect("localhost","root","","attendance")
    cursor=db.cursor()
    now = datetime.datetime.now()
    date  = now.strftime("%Y-%m-%d")
    time = now.strftime('%I:%M %p')
    print("outside")
    for i in set(detected_faces):
        print("inside")
        sql = "Insert into attendanceapp_attendence (student_id_id,date,time,status) values({},'{}','{}',{})".format(i,date,time,1)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("Sucessfully added "+i)
face_recognizer()

