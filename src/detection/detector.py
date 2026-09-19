from ultralytics import YOLO


class Detector:
    """YOLO object detector."""

    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def detect(self, frame):
        results = self.model(
            frame,
            classes=[2, 3, 5, 7],   # car, motorcycle, bus, truck
            verbose=False
        )
        return results[0]