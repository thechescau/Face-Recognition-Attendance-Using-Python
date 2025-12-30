import cv2
import numpy as np
import face_recognition
import os

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)

print(f'Found images: {myList}')

for cl in myList:
    if not cl.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    fullPath = f'{path}/{cl}'
    curImg = cv2.imread(fullPath)
        
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    else: 
        print(f"Warning: Could not read image {cl}")

if not images:
    print("Error: No valid images found in the 'Images' folder!")
    exit()

print(f'Attendance list: {classNames}')

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print('Encoding started...please wait.')
encodeListKnown = findEncodings(images)
print('Encoding Complete! System is ready.')


import datetime

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            markAttendance(name)
    
    cv2.imshow('Face Recognition Attendance System', img)

    #Press 'q' to stop

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.releaase()
cv2.destroyAllWindows()
