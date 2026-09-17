import cv2

from src.detection.detector import Detector


class FrameProcessor:

    def __init__(self):
        self.detector = Detector()

    def process(self, frame):

        detections = self.detector.detect(frame)

        boxes = detections.boxes

        for box in boxes:

            confidence = float(box.conf[0])

            if confidence < 0.50:
                continue

            class_id = int(box.cls[0])

            class_name = self.detector.model.names[class_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            label = f"{class_name} {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        return frame
        