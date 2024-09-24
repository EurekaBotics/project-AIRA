import cv2
from print_color import print
from ultralytics import YOLO
class CalcPriceYolo:
    def __init__(self) -> None:
        self.model = YOLO("yolov8m.pt")
        self.cap = cv2.VideoCapture(0)

    def _capture_frame(self):
        
        ret, frame = self.cap.read()

        if ret:
            cv2.imwrite("temp_yolo_frame.jpg", frame)
            print("Saved first frame as input.jpg")
        else:
            print("Failed to capture frame")
        self.cap.release()
    
    def perform_object_detection(self,class_path=None):
        self._capture_frame()
        image_path = "temp_yolo_frame.jpg"
        image = cv2.imread(image_path)

        # Perform object detection on the saved image
        results = self.model(image_path)
        class_names = self.model.names  # Same as the printed list of object categories

        # Price dictionary for different items
        item_prices = {
            'bottle': 20,
            'banana': 10,
            'apple': 30,
            'sandwich': 60,
            'hot dog': 100,
            'pizza': 250,
            'donut': 30,
            'orange': 15,
            'broccoli': 40,
            'chair': 500
        }

        # Counter dictionary to store the count of each detected item
        item_counts = {item: 0 for item in item_prices}

        # Iterate through the detected objects in the first result
        for result in results:
            for box in result.boxes:  # result.boxes contains bounding boxes and scores
                class_id = int(box.cls[0])  # Extract the class ID
                class_name = class_names[class_id]  # Look up the class name

                # Check if the detected object is in the item_prices dictionary
                if class_name in item_prices:
                    item_counts[class_name] += 1  # Increment the counter for that item

        # Calculate the total price
        total_price = sum(item_counts[item] * item_prices[item] for item in item_counts)

        # Print the count of each item and the corresponding total price
        for item, count in item_counts.items():
            if count > 0:
                print(f"{item.capitalize()} detected: {count}, Price: {count * item_prices[item]} Rs",color='g')

        print(f"Total price for all items: {total_price} Rs")
        return total_price
        # Visualize the results
        # annotated_image = results[0].plot()

        # # Display the image with bounding boxes and scores
        # cv2.imshow("YOLOv8 Detection - First Frame", annotated_image)

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

if __name__ == '__main__':
    yolo_obj = CalcPriceYolo()
    yolo_obj.perform_object_detection()
