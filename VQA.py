import torch
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering


class VQA():

    def __init__(self)->None:
        self.model = BlipForQuestionAnswering.from_pretrained("ybelkada/blip-vqa-base", torch_dtype=torch.float16).to("cuda")
        self.processor = BlipProcessor.from_pretrained("ybelkada/blip-vqa-base")        
        
        # self.model = BlipForQuestionAnswering.from_pretrained("D:\F!L(5\Cache\huggingface\hub\models--ybelkada--blip-vqa-base", torch_dtype=torch.float16).to("cuda")
        # self.processor = BlipProcessor.from_pretrained("D:\F!L(5\Cache\huggingface\hub\models--ybelkada--blip-vqa-base")

    def __call__(self, image, question):
 
        inputs = self.processor(image, question, return_tensors="pt").to("cuda", torch.float16)
        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)
    
    


if __name__ == '__main__':

    model = VQA()
    raw_image = Image.open("D:\\F!L(5\\common_obj.jpg")

    question = "describe the picture?"
    out = model(raw_image, question)
    print(out)

# processor = BlipProcessor.from_pretrained("ybelkada/blip-vqa-base")
# model = BlipForQuestionAnswering.from_pretrained("ybelkada/blip-vqa-base", torch_dtype=torch.float16).to("cuda")

# raw_image = Image.open("D:\\F!L(5\\common_obj.jpg")

# question = "describe the picture?"
# inputs = processor(raw_image, question, return_tensors="pt").to("cuda", torch.float16)

# out = model.generate(**inputs)
# print(processor.decode(out[0], skip_special_tokens=True))