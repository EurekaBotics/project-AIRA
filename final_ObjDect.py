import cvlib as cv
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch

class objDet:
    def __init__(self):
        self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        
    def detect(self, image_path, threshold=.7):
        image = Image.open(image_path)
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
        out = []
        for object in range(len(results['scores'])):
            if results['scores'][object].item() > threshold:
                out.append((self.model.config.id2label[results['labels'][object].item()], results['boxes'][object]))  
        return out
        
if __name__ == '__main__':
    obj = objDet()
    det = obj.detect('clas1.jpg')
    print("The detections are:\n")
    for i,j in det:
        print(i,j)