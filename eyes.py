import cv2
import mediapipe as mp

# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# while True:

#     ret, frame = cam.read()

#     if cv2.waitKey(1) == ord("q"):
#         break
    
#     cv2.imshow("feed", frame)

# cv2.destroyAllWindows()
# cam.release()
    


cx = 0

def eyes():
    global cx
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    mp_face = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils

    x = 0
    y = 0
    cx = 0
    cy = 0
    while True:
        ret,frame = cam.read()
        h,w,c = frame.shape
        # print(h,w, c)
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        if cam.isOpened():
            with mp_face.FaceDetection(model_selection = 0) as face:

                results = face.process(img)

                if results.detections:
                    for detection in results.detections:
                        #mp_draw.draw_detection(frame,detection)
                        detections = results.detections
                        loc = detections[0].location_data
                        bbox = loc.relative_bounding_box
                        x,y,iw,ih = bbox.xmin*w,bbox.ymin*h,bbox.width,bbox.height
                        cv2.rectangle(frame,(int(x),int(y)),(int(x+iw*w),int(y+h*ih)),(0,255,0),2)
                        cv2.circle(frame,(int((2*x+w*iw)/2),int((2*y+h*ih)/2)),5,(0,255,0),4)
                        cx,cy = int((2*x+w*iw)/2),int((2*y+h*ih)/2)
            

            
        
        cv2.imshow("image",frame)

        

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()

if __name__ == "__main__":
    eyes()