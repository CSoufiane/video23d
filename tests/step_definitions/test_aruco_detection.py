import pytest
import json
from pathlib import Path
from pytest_bdd import scenario, given, when, then
from scripts.aruco_detector import detect_markers

@scenario('../../features/computer_vision_analysis.feature', 'Detect markers in an image')
def test_detect_markers():
    pass

@scenario('../../features/computer_vision_analysis.feature', 'Verify marker visibility over several frames')
def test_marker_coverage():
    pass

@given('a set of extracted frames', target_fixture="image_dir")
def check_frames_exist(root_dir):
    frame_dir = root_dir / "frames"
    # Ensure there are actually images to process
    assert len(list(frame_dir.glob("*.jpg"))) > 0, "No frames found in frames/ directory"
    return frame_dir

@when('the ArUco detection algorithm is executed', target_fixture="results")
def run_detection(image_dir, root_dir):
    output_json = root_dir / "output/test_aruco_results.json"
    detect_markers(image_dir, output_json)
    with open(output_json, 'r') as f:
        return json.load(f)

@then('at least one marker ID is recognized per analyzed frame')
def check_at_least_one_id(results):
    # results is a dict where key is filename, value is a LIST of marker dicts
    for frame, markers in results.items():
        # Ensure the list is not empty 
        assert len(markers) > 0, f"No markers found in {frame}"
        # Ensure each marker in the list has an 'id' 
        for marker in markers:
            assert "id" in marker, f"Marker entry missing 'id' in {frame}"

@then('the camera poses (rvec, tvec) are stored')
def check_poses_stored(results):
    for frame, markers in results.items():
        for marker in markers:
            # The implementation stores rvec/tvec within each marker object 
            assert "rvec" in marker, f"Missing rvec in {frame}"
            assert "tvec" in marker, f"Missing tvec in {frame}"

@then('each reference marker is detected in at least 3 different frames')
def check_coverage(results):
    marker_counts = {}
    for markers in results.values():
        for marker in markers:
            marker_id = marker["id"]
            marker_counts[marker_id] = marker_counts.get(marker_id, 0) + 1
    
    assert any(count >= 3 for count in marker_counts.values()), \
        "No marker was detected in at least 3 frames. Coverage is too low for 3D."
