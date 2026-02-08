import cv2
import os
from pathlib import Path

def extract_frames(video_path, output_dir, fps=2):
    """
    Extracts frames from a video file at a specific frequency.
    """
    video_path = Path(video_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    container = cv2.VideoCapture(str(video_path))
    if not container.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    video_fps = container.get(cv2.CAP_PROP_FPS)
    # Calculate interval: if video is 30fps and we want 2fps, we take every 15th frame
    interval = max(1, int(video_fps / fps))
    
    count = 0
    saved_count = 0
    
    while True:
        ret, frame = container.read()
        if not ret:
            break
            
        if count % interval == 0:
            frame_name = f"frame_{saved_count:04d}.jpg"
            cv2.imwrite(str(output_path / frame_name), frame)
            saved_count += 1
            
        count += 1

    container.release()
    return saved_count