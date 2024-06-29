import  cv2
import os
import  face_recognition
import pickle

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage


#upload img to database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURl':'https://attendencesystem-dbec0-default-rtdb.firebaseio.com/',
    'storageBucket':'attendencesystem-dbec0.appspot.com'
})

#importing images
imgfolderpath='Images'
imgpathlist=os.listdir(imgfolderpath)
imglist=[]
#print(imgpathlist)
stdid=[]

for path in imgpathlist:
    imglist.append(cv2.imread(os.path.join(imgfolderpath,path)))
    #print(os.path.splitext(path)[0])
    stdid.append(os.path.splitext(path)[0])

#upload image
    fileName=os.path.join(imgfolderpath,path)
    #fileName=f'{imgfolderpath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)

#print(len(imglist))
#print(stdid)


def findencodings(imageslist):
    encodelist=[]
    for img in imageslist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("Encoding Started")
encodelistknown=findencodings(imglist)
encodelistknownwithid=[encodelistknown,stdid]
#print(encodelistknown)
print("Encoding Complete")

#file grnarate
file =open("EncodeFile.p",'wb')
pickle.dump(encodelistknownwithid,file)
file.close()
print("File Saved..")
