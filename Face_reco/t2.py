import dlib
import cv2
from deepface import DeepFace

# Load a pre-trained face detection model from dlib
detector = dlib.get_frontal_face_detector()

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cam.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use dlib to detect faces (GPU-accelerated)
    faces = detector(gray)

    for rect in faces:
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Rest of the code for emotion analysis remains the same
    result = DeepFace.analyze(frame, enforce_detection=False, actions=["emotion"])
    # ...

    cv2.imshow('img', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
