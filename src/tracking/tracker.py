import supervision as sv


class Tracker:
    """ByteTrack multi-object tracker."""

    def __init__(self):
        self.tracker = sv.ByteTrack()

    def update(self, detections):
        return self.tracker.update_with_detections(detections)