import cv2
from deepface import DeepFace

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cam= cv2.VideoCapture(0,cv2.CAP_DSHOW)


while True:
    ret, frame =cam.read()
    result = DeepFace.analyze(frame, enforce_detection= False , actions = ["age"])
    # print(result[0]['dominant_emotion'])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,1.1,4)

    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w, y+h), (0,255,0),2)
    
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, result[0]['dominant_emotion'], (50,50),font,3,(0,0,255),2,cv2.LINE_4)
    
    if cv2.waitKey(1) == ord('q'):
        break

    cv2.imshow('img',frame)

cam.release()
cv2.destroyAllWindows()



