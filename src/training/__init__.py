import cv2
from ultralytics import YOLO


def main() -> None:
    model = YOLO("models/best.pt")

    video_capture = cv2.VideoCapture(1)
    if not video_capture.isOpened():
        raise IOError("Couldn't open webcam or video")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        results = model(frame, stream=True)
        for result in results:
            boxes = result.boxes
            if boxes:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = f"{model.names[cls]} {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("YOLO Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
