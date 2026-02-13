import pytest
from pytest_bdd import scenario, given, when, then, parsers
from scripts.calibration_generator import compute_calibration
from pathlib import Path

@scenario('../../features/camera_calibration_computation.feature', 'Compute camera matrix and distortion coefficients')
def test_compute_calibration():
    pass

@given(parsers.parse('a directory "{image_dir}" containing checkerboard images'), target_fixture="img_dir")
def check_images(image_dir):
    path = Path(image_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path

@given(parsers.parse('the checkerboard dimensions are {width:d}x{height:d}'), target_fixture="dims")
def set_dims(width, height):
    return (width, height)

@when('the calibration script is executed', target_fixture="error")
def run_calibration(img_dir, dims):
    # This assumes images exist in data/calibration for the test to pass
    return compute_calibration(img_dir, grid_size=dims)

@then('the re-projection error is calculated')
def check_error(error):
    assert error >= 0

@then(parsers.parse('the file "{filename}" is generated in the root directory'))
def check_file_gen(filename):
    assert Path(filename).exists()

@then(parsers.parse('the file contains "{key1}" and "{key2}"'))
def check_yaml_content(key1, key2):
    import yaml
    with open("camera_calib.yaml", "r") as f:
        data = yaml.safe_load(f)
    assert key1 in data
    assert key2 in data