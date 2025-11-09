from ultralytics import YOLO
import cv2
from tracker import Tracker
from util import (
    draw_counter,
    draw_label,
    trigger_line,
    update_counter
)

model = YOLO(r"C:\Users\lukad\vehicle-counter-capstone-project\models\yolov8s-300epoch.pt")
tracker = Tracker()

# Kelas kendaraan yang akan dilacak
vehicle_classes = [0, 1, 2, 3]  # (bus, car, motorbike, truck)

# Garis pemicu
line_point1 = (125, 480)  
line_point2 = (738, 705)  
offset = 15  

# Inisialisasi penghitung kendaraan
counter = {"bus": 0, "car": 0, "motorbike": 0, "truck": 0}

results = model.predict(source=r"C:\Users\lukad\vehicle-counter-capstone-project-1\Untitled.mp4", stream=True)

for result in results:
    frame = result.orig_img

    bounding_boxes = []
    tracked_boxes_input = []  

    for box in result.boxes:
        class_id = int(box.cls)  
        if class_id in vehicle_classes:
            x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
            w, h = x2 - x1, y2 - y1

            bounding_boxes.append([x1, y1, w, h, class_id])  
            tracked_boxes_input.append([x1, y1, w, h])  

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{result.names[class_id]} {box.conf.item():.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    tracked_boxes = tracker.update(tracked_boxes_input)

    for tracked_box in tracked_boxes:
        x, y, w, h, object_id = tracked_box
        center_y = y + h // 2  

        for bbox in bounding_boxes:
            if bbox[:4] == [x, y, w, h]:
                class_id = bbox[4]
                break

        if trigger_line(line_point1[1], line_point2[1], offset, [center_y]):
            update_counter(class_id, counter)


        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, f"ID: {object_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.line(frame, line_point1, line_point2, (255, 0, 0), 2)

    draw_counter(frame, counter)

    cv2.imshow("Vehicle Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()