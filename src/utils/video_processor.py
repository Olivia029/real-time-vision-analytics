import cv2
from pathlib import Path

from src.utils.frame_processor import FrameProcessor
from src.utils.video_writer import VideoWriter


class VideoProcessor:
    """Read a video, process each frame and save the result."""

    def __init__(
        self,
        input_path: str,
        output_path: str,
        frame_processor: FrameProcessor,
    ):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.frame_processor = frame_processor

    def process(self):
        cap = cv2.VideoCapture(str(self.input_path))

        if not cap.isOpened():
            raise FileNotFoundError(
                f"Cannot open {self.input_path}"
            )

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        temporary_path = self.output_path.with_name(
            f"{self.output_path.stem}_temp.mp4"
        )

        writer = VideoWriter(
            temporary_path=str(temporary_path),
            output_path=str(self.output_path),
            fps=fps,
            width=width,
            height=height,
        )

        writer.open()

        frame_number = 0

        try:
            while True:
                success, frame = cap.read()

                if not success:
                    break

                frame_number += 1

                frame = self.frame_processor.process(frame)

                cv2.putText(
                    frame,
                    f"Frame: {frame_number}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    frame,
                    f"FPS: {fps:.1f}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 0),
                    2,
                )

                writer.write(frame)

        finally:
            cap.release()
            writer.close()

        writer.encode()

        print(f"Processed {frame_number} frames.")
        print(f"Saved to {self.output_path}")