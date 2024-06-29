import os
import pickle
import numpy as np
import cv2
import cvzone

import face_recognition

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage
from datetime import datetime


#get data from database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURl':'https://attendencesystem-dbec0-default-rtdb.firebaseio.com/',
    'storageBucket':'attendencesystem-dbec0.appspot.com'
})
bucket=storage.bucket()
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)





#load encoding file
print("Loading encode file")
file=open('EncodeFile.p','rb')
encodelistknownwithid=pickle.load(file)
encodelistknown,stdid=encodelistknownwithid
file.close()
#print(stdid)
print("Loaded encode file ")


#database
counter=0
id=-1
studentimage=[]


while True:
    success,img=cap.read()
#resize
    imgsmall=cv2.resize(img,(0,0),None,0.25,0.25)
    imgsmall=cv2.cvtColor(imgsmall,cv2.COLOR_BGR2RGB)

    #current frmae encoding
    facecurfrmae=face_recognition.face_locations(imgsmall)
    encodecurframe=face_recognition.face_encodings(imgsmall,facecurfrmae)




    if facecurfrmae:

        # compare
        for encodeface, faceloc in zip(encodecurframe, facecurfrmae):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)

            # print("Matches",matches)
            # print("dis",facedis)
            # check comapare
            matchindex = np.argmin(facedis)
            # print("Match Index",matchindex)

            if matches[matchindex]:
                # print("Known Face Detecvted")
                # matched id detection
                # print(stdid[matchindex])
                # bounding box
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                img = cvzone.cornerRect(img, bbox, rt=0)

                # after detecting
                id = stdid[matchindex]
                print(id)
                if counter == 0:
                    cvzone.putTextRect(img,"Loading",(275,400))
                    cv2.imshow("Face Recogntion",img)
                    cv2.waitKey(1)
                    counter = 1

        if counter != 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # get image
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                studentimage = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update Attendence Data
                datetimeobject = datetime.strptime(studentInfo['Last_Attendence_Time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondElapsed = (datetime.now() - datetimeobject).total_seconds()
                print(secondElapsed)
 # duration second for next time
                if secondElapsed > 2:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['Total_Attendence'] += 1
                    ref.child('Total_Attendence').set(studentInfo['Total_Attendence'])
                    ref.child('Last_Attendence_Time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                if counter <= 10:

                    counter += 1

                if counter >= 20:
                    counter = 0
                    studentInfo = []
                    studentimage = []


    else:
        counter=0

    #cv2.imshow("Webcam",img)
    cv2.imshow("Face Recogntion",img)
    cv2.waitKey(1)