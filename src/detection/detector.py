from ultralytics import YOLO
import supervision as sv


class Detector:

    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def detect(self, frame):

        result = self.model(
            frame,
            classes=[2, 3, 5, 7],
            verbose=False
        )[0]

        detections = sv.Detections.from_ultralytics(result)

        return detections