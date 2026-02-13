import pytest
import numpy as np
import cv2
from pathlib import Path
from pytest_bdd import scenario, given, when, then, parsers
from scripts.calibration_utils import load_camera_params, validate_calibration_integrity

# Linking to the specific scenario in your feature file 
@scenario('../../features/computer_vision_analysis.feature', 'Load a valid camera calibration')
def test_load_calibration():
    """This function remains empty as pytest-bdd handles execution."""
    pass

@given(parsers.parse('a camera calibration file "{filename}"'), target_fixture="calib_path")
def check_calib_exists(root_dir, filename):
    """Ensures the file exists or generates a default for the MVP."""
    path = Path(root_dir) / filename
    if not path.exists():
        # Fallback: create a dummy calibration for testing if file is missing
        from scripts.calibration_generator import generate_standard_calibration
        generate_standard_calibration(1920, 1080, output_path=path)
    return path

@when('the pipeline starts', target_fixture="calib_results")
def load_calib(calib_path):
    """Uses the business logic to load parameters."""
    K, D = load_camera_params(calib_path)
    return {"K": K, "D": D}

@then('the camera matrix K is successfully loaded')
def check_k_matrix(calib_results):
    """Validates the intrinsic matrix K."""
    K = calib_results["K"]
    assert K.shape == (3, 3)
    assert K[2, 2] == 1.0  # Homogeneous coordinate normalization

@then('the distortion coefficients D are available')
def check_dist_coeffs(calib_results):
    """Validates the distortion vector D."""
    D = calib_results["D"]
    assert len(D.flatten()) >= 5  # Standard OpenCV distortion model

@then('no projection errors are raised during a test on a target image')
def check_projection_test(calib_results):
    """
    Validates geometric consistency by projecting a 3D point 
    onto the 2D image plane.
    """
    K, D = calib_results["K"], calib_results["D"]
    
    # Setup test geometry: point 1 meter directly in front of camera
    obj_pts = np.array([[0, 0, 1.0]], dtype=np.float32)
    rvec = np.zeros((3, 1), dtype=np.float32)
    tvec = np.zeros((3, 1), dtype=np.float32)
    
    img_pts, _ = cv2.projectPoints(obj_pts, rvec, tvec, K, D)
    
    # Assert successful projection
    assert img_pts is not None
    assert img_pts.shape == (1, 1, 2)