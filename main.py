from ultralytics import YOLO
import cv2

# Load model
model = YOLO("yolov8n.pt")

# Open video
cap = cv2.VideoCapture("traffic.mp4")
print("Video opened:", cap.isOpened())

# Vehicle classes (COCO dataset IDs)
vehicle_classes = [2, 3, 5, 7]  # car, motorbike, bus, truck
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls in vehicle_classes:
                count += 1

        frame = r.plot()

    # Traffic level
    if count < 10:
        level = "Low Traffic"
    elif count < 30:
        level = "Medium Traffic"
    else:
        level = "High Traffic"

    # Signal timing
    if count < 10:
        signal = "Green: 20s"
    elif count < 30:
        signal = "Green: 40s"
    else:
        signal = "Green: 60s"

    # Display text
    cv2.putText(frame, f"Vehicles: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, level, (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(frame, signal, (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Traffic Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()