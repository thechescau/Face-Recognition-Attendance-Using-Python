import cv2
import face_recognition
import os

def load_and_encode(path='Images'):
    images = []
    classNames = []
    myList = os.listdir(path)

    for cl in myList:
        if cl.lower().endswith(('.png', '.jpg', '.jpeg')):
            curImg = cv2.imread(f'{path}/{cl}')

            if curImg is not None:
                images.append(curImg)
                classNames.append(os.path.splitext(cl)[0])

    print(f'Encoding {len(images)} faces...')
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList, classNames