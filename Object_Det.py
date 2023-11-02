import time
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch

t1 = time.time()
image = Image.open("C:\\Users\\ROHIT FRANCIS\\OneDrive\\Desktop\\ALL Here\\AIRA\\AIRA 3.0\\Cow.jpg")

model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

# t1 = time.time()
inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

logits = outputs.logits
bboxes = outputs.pred_boxes

target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
        f"Detected {model.config.id2label[label.item()]} with confidence "
        f"{round(score.item(), 3)} at location {box}"
    )
t2 = time.time()
print(t2-t1)