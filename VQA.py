import os
import google.generativeai as genai
import cv2

# genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# if ret:
#     # Save the image if a frame was successfully captured
#     cv2.imwrite('captured_image.jpg', frame)
# cap.release()

# myfile = genai.upload_file("captured_image.jpg")
# print(f"{myfile=}")

# model = genai.GenerativeModel("gemini-1.5-flash")
# result = model.generate_content(
#     [myfile, "\n\n", "what am i holding"]
# )
# print(f"{result.text=}")


class GeminiVisionModel:
    def __init__(self) -> None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.cap = cv2.VideoCapture(0)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def take_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Save the image if a frame was successfully captured
            cv2.imwrite("captured_image.jpg", frame)
        self.cap.release()

    def perform_vqa(self, question, image_path="captured_image.jpg"):
        self.take_image()
        myfile = genai.upload_file(image_path)
        result = self.model.generate_content([myfile, "\n\n", question])
        return result.text


if __name__ == "__main__":
    from VQA import GeminiVisionModel

    vqa = GeminiVisionModel()
    print(vqa.perform_vqa("what can you see in this image?"))
