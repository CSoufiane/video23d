import pytest
import yaml
import numpy as np
from pathlib import Path
from pytest_bdd import scenario, given, when, then

@scenario('../../features/computer_vision_analysis.feature', 'Load a valid camera calibration')
def test_load_calibration():
    pass

@given('a camera calibration file "camera_calib.yaml"', target_fixture="calib_file")
def check_calib_exists(root_dir):
    path = root_dir / "camera_calib.yaml"
    if not path.exists():
        # Auto-generate if missing for 1080p
        from scripts.calibration_generator import generate_standard_calibration
        generate_standard_calibration(1920, 1080, output_path=path)
    return path

@when('the pipeline starts', target_fixture="calib_data")
def load_calib(calib_file):
    with open(calib_file, 'r') as f:
        return yaml.safe_load(f)

@then('the camera matrix K is successfully loaded')
def check_k_matrix(calib_data):
    K = np.array(calib_data['camera_matrix'])
    assert K.shape == (3, 3)
    assert K[2, 2] == 1.0

@then('the distortion coefficients D are available')
def check_dist_coeffs(calib_data):
    D = np.array(calib_data['distortion_coefficients'])
    assert len(D) >= 5

@then('no projection errors are raised during a test on a target image')
def check_projection_test(calib_data):
    # Test logic: project a 3D point (0,0,0) to 2D
    import cv2
    K = np.array(calib_data['camera_matrix'])
    D = np.array(calib_data['distortion_coefficients'])
    rvec = np.zeros((3, 1))
    tvec = np.array([0, 0, 1.0]) # 1 meter in front of camera
    obj_pts = np.array([[0, 0, 0]], dtype=np.float32)
    
    img_pts, _ = cv2.projectPoints(obj_pts, rvec, tvec, K, D)
    assert img_pts is not None