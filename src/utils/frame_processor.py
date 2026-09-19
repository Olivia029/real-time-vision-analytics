import cv2

from src.analytics.speed_estimator import SpeedEstimator
from src.analytics.vehicle_counter import VehicleCounter
from src.detection.detector import Detector
from src.tracking.tracker import Tracker


class FrameProcessor:
    """Run detection, tracking and traffic analytics on each frame."""

    def __init__(self):
        self.detector = Detector()
        self.tracker = Tracker()
        self.counter = VehicleCounter(line_y=1300)
        self.speed_estimator = SpeedEstimator()

    def process(self, frame):

        # 1. Detect vehicles
        detections = self.detector.detect(frame)

        # 2. Assign persistent IDs
        tracked = self.tracker.update(detections)

        # 3. Process every tracked vehicle
        for i in range(len(tracked)):

            x1, y1, x2, y2 = tracked.xyxy[i].astype(int)

            class_id = int(tracked.class_id[i])
            class_name = self.detector.model.names[class_id]

            track_id = tracked.tracker_id[i]

            if track_id is None:
                continue

            track_id = int(track_id)

            # Bounding-box centre
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Update vehicle counter
            self.counter.update(
                track_id=track_id,
                center_y=center_y,
            )

            # Estimate speed
            speed = self.speed_estimator.update(
                track_id=track_id,
                center_x=center_x,
                center_y=center_y,
                fps=60,
            )

            # Draw trajectory
            history = self.speed_estimator.history[track_id]

            for j in range(1, len(history)):
                cv2.line(
                    frame,
                    history[j - 1],
                    history[j],
                    (0, 255, 255),
                    2,
                )

            # Draw centre point
            cv2.circle(
                frame,
                (center_x, center_y),
                4,
                (0, 255, 255),
                -1,
            )

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2,
            )

            # Label
            label = f"ID {track_id} | {class_name} | {speed:.0f} km/h"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 0, 0),
                2,
            )

        # 4. Draw counting line
        cv2.line(
            frame,
            (0, self.counter.line_y),
            (frame.shape[1], self.counter.line_y),
            (0, 0, 255),
            2,
        )

        # 5. Dashboard
        _, width = frame.shape[:2]

        cv2.putText(
            frame,
            f"IN : {self.counter.in_count}",
            (width - 180, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"OUT: {self.counter.out_count}",
            (width - 180, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

        return frame