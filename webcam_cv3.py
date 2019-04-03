import cv2
import sys
import logging as log
import datetime as dt
import os
from time import sleep
import time
from subprocess import Popen, PIPE
import tensorflow




text = 'Face..!!'
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0
strt_time= time.time()
x=0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)




    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for f in faces:
        x,y,w,h=[ v for v in f ]
        x=x-20
        w=w+50
        h=h+50
        y=y-20

        cv2.rectangle(frame,(x,y),(x+w+10, y+h+10),(0,0,0),2)
        cv2.putText(frame, text,(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.4,(0,0,255))

    	#Save the first face frame


    if(time.time() - strt_time) > 3:
        ti=int(round(time.time(),0))
        path="/home/rahul//tf_rahul/"+(str(ti))+".jpg"



        sub_face = gray[y:y+h, x:x+w]

        cv2.imwrite(path,sub_face)

        process = Popen(["python3", "/home/rahul/tf_rahul/classify.py",path], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        try:
            if(output[0]=='r'):
            	text="Rahul"
            elif(output[0]=='n') :
            	text="Nishita"
            elif(output[0]=='f') :
                text = "Female"
            else:
            	text= "Male"
        except:
            pass


        strt_time= time.time()

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
