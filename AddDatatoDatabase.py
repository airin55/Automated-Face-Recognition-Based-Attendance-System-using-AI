
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURl':'https://attendencesystem-dbec0-default-rtdb.firebaseio.com/'
})


ref=db.reference('Students')


#add data
data={
    "05":
        {
            "Name":"Airin Jahan Akhi",
            "Dept": "ICE 9th",
            "Total_Attendence":1,
            "Last_Attendence_Time":"2023-03-30 11:56:43"
        },
    "16":
        {
            "Name": "Lubna Khanam",
            "Dept": "ICE 9th",
            "Total_Attendence": 1,
            "Last_Attendence_Time": "2023-03-30 11:56:43"
        },
    "07":
        {
            "Name": "Zannat Keya",
            "Dept": "ICE 9th",
            "Total_Attendence": 1,
            "Last_Attendence_Time": "2023-03-30 11:56:43"
        },



}

#send data
for key,value in data.items():
    ref.child(key).set(value)