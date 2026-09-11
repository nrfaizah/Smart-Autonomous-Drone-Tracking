import cv2
from djitellopy import Tello
import numpy as np

# Connect to Tello
tello = Tello()
tello.connect()
tello.streamon()

# Load pre-trained model for person detection
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]


# Define function to get person bounding boxes
def detect_person(frame):
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # 0 is the class ID for 'person' in YOLO
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    person_boxes = []
    for i in range(len(boxes)):
        if i in indexes:
            person_boxes.append(boxes[i])
    return person_boxes


# Function to follow the person
def follow_person():
    while True:
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (640, 480))
        person_boxes = detect_person(frame)

        for box in person_boxes:
            x, y, w, h = box
            cx = x + w // 2
            cy = y + h // 2

            # Simple proportional controller for following
            if cx < 200:
                tello.move_left(20)
            elif cx > 440:
                tello.move_right(20)

            if cy < 160:
                tello.move_up(20)
            elif cy > 320:
                tello.move_down(20)

        # Display the frame
        for box in person_boxes:
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Tello Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Land and release resources
    tello.land()
    cv2.destroyAllWindows()


# Start following the person
tello.takeoff()
follow_person()