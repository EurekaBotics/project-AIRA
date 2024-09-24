import cv2
from ultralytics import YOLO

# Load the YOLOv8x model (Extra-large model)
model = YOLO("yolov8m.pt")

# Open the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

# Capture only the first frame
ret, frame = cap.read()

if ret:
    # Save the first frame as input.jpg
    cv2.imwrite("input.jpg", frame)
    print("Saved first frame as input.jpg")
else:
    print("Failed to capture frame")

# Release the webcam
cap.release()

# Load the saved image
image_path = "input.jpg"
image = cv2.imread(image_path)

# Perform object detection on the saved image
results = model(image_path)
class_names = model.names  # Same as the printed list of object categories

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
        print(f"{item.capitalize()} detected: {count}, Price: {count * item_prices[item]} Rs")

print(f"Total price for all items: {total_price} Rs")
# Visualize the results
annotated_image = results[0].plot()

# Display the image with bounding boxes and scores
cv2.imshow("YOLOv8 Detection - First Frame", annotated_image)

# Wait for a key press to close the window
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()
