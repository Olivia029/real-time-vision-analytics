from collections import defaultdict
import math


class SpeedEstimator:
    """Estimate vehicle speed from tracked trajectories."""

    PIXELS_TO_METERS = 0.08 

    def __init__(self):
        self.history = defaultdict(list)

    def update(self, track_id, center_x, center_y, fps):

        if track_id is None:
            return 0.0

        self.history[track_id].append((center_x, center_y))

        if len(self.history[track_id]) > 10:
            self.history[track_id].pop(0)

        points = self.history[track_id]

        if len(points) < 2:
            return 0.0

        x1, y1 = points[0]
        x2, y2 = points[-1]

        distance_pixels = math.hypot(x2 - x1, y2 - y1)

        distance_meters = distance_pixels * self.PIXELS_TO_METERS

        time_seconds = (len(points) - 1) / fps

        if time_seconds == 0:
            return 0.0

        speed_ms = distance_meters / time_seconds

        return speed_ms * 3.6