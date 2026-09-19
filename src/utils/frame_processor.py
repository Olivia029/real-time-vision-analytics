import cv2

from src.detection.detector import Detector
from src.tracking.tracker import Tracker


class FrameProcessor:

    def __init__(self):
        self.detector = Detector()
        self.tracker = Tracker()

    def process(self, frame):

        detections = self.detector.detect(frame)

        tracked = self.tracker.update(detections)

        for i in range(len(tracked)):

            x1, y1, x2, y2 = tracked.xyxy[i].astype(int)

            class_id = int(tracked.class_id[i])

            confidence = tracked.confidence[i]

            track_id = tracked.tracker_id[i]

            class_name = self.detector.model.names[class_id]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2,
            )

            label = f"ID {track_id} | {class_name}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 0, 0),
                2,
            )

        return frame