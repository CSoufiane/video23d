import pytest
import cv2
import shutil
from pathlib import Path
from pytest_bdd import scenario, given, when, then
from scripts.extractor import extract_frames

@scenario('../../features/data_preparation.feature', 'Extract usable frames from a video')
def test_extract_frames_logic():
    pass

@given('a valid input video file "input.mp4"', target_fixture="video_file")
def video_file(tmp_path):
    # This creates a dummy video for testing if you don't have one
    path = tmp_path / "input.mp4"
    # (In a real scenario, you'd use a small 1sec sample video)
    return path 

@given('the FPS parameter is set to 2 frames per second', target_fixture="fps_param")
def fps_param():
    return 2

@when('the extraction script is executed')
def run_extraction(video_file, fps_param, tmp_path):
    # We use tmp_path to keep tests clean
    extract_frames("data/raw/test_scene.mp4", tmp_path / "frames", fps=fps_param)

@then('a frames directory is created')
def check_dir(tmp_path):
    assert (tmp_path / "frames").is_dir()

@then('the images are named sequentially (e.g., frame_0001.jpg)')
def check_naming(tmp_path):
    frames = sorted(list((tmp_path / "frames").glob("*.jpg")))
    assert "frame_0000.jpg" in frames[0].name

@then('every extracted image is readable by the OpenCV library')
def check_readability(tmp_path):
    for img_path in (tmp_path / "frames").glob("*.jpg"):
        img = cv2.imread(str(img_path))
        assert img is not None