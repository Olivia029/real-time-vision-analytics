import time


class PerformanceMonitor:
    """Measure the processing performance of the application."""

    def __init__(self):
        self.start_time = None
        self.frame_count = 0

    def start(self):
        self.start_time = time.perf_counter()

    def update(self):
        self.frame_count += 1

    def get_elapsed_time(self) -> float:
        if self.start_time is None:
            return 0.0

        return time.perf_counter() - self.start_time

    def get_fps(self) -> float:
        elapsed_time = self.get_elapsed_time()

        if elapsed_time <= 0:
            return 0.0

        return self.frame_count / elapsed_time