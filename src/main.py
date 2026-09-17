from src.utils.frame_processor import FrameProcessor
from src.utils.video_processor import VideoProcessor


def main():
    frame_processor = FrameProcessor()

    processor = VideoProcessor(
        input_path="data/input/traffic.mp4",
        output_path="data/output/processed.mp4",
        frame_processor=frame_processor,
    )

    processor.process()


if __name__ == "__main__":
    main()