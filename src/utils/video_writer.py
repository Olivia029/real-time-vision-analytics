import subprocess
from pathlib import Path


class VideoWriter:
    """Write processed frames to a temporary video and encode the final output."""

    def __init__(
        self,
        temporary_path: str,
        output_path: str,
        fps: float,
        width: int,
        height: int,
    ):
        self.temporary_path = Path(temporary_path)
        self.output_path = Path(output_path)
        self.fps = fps
        self.width = width
        self.height = height

        self.writer = None

    def open(self):
        import cv2

        self.temporary_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self.writer = cv2.VideoWriter(
            str(self.temporary_path),
            fourcc,
            self.fps,
            (self.width, self.height),
        )

        if not self.writer.isOpened():
            raise RuntimeError(
                f"Could not open video writer for {self.temporary_path}"
            )

    def write(self, frame):
        if self.writer is None:
            raise RuntimeError("VideoWriter is not open.")

        self.writer.write(frame)

    def close(self):
        if self.writer is not None:
            self.writer.release()
            self.writer = None

    def encode(self):
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(self.temporary_path),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(self.output_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg encoding failed:\n"
                f"{result.stderr}"
            )

        self.temporary_path.unlink(missing_ok=True)