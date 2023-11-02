import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import pandas as pd


class objDet:
    def __init__(self, model="yolov3-tiny", confidence=0.5):
        self.model = model
        self.confidence = confidence

    def detect(self,image, return_bbox=False):
        bbox, label, conf = cv.detect_common_objects(image, confidence=self.confidence, model=self.model)

        if return_bbox:
            return bbox, label, conf
        else:
            return label, conf
        

if __name__ == "__main__":
    
    detector = objDet()
    img = cv2.imread("D:\\F!L(5\\common_obj.jpg")
    label, conf = detector.detect(img)
    print(label, conf)

    cv2.imshow('image', img)
    cv2.waitKey(0)
