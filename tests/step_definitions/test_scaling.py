from pytest_bdd import scenario, given, when, then
import pytest

@scenario('../../features/scaling.feature', 'Calculate and apply scale factor')
def test_model_scaling():
    pass

@given('a successful COLMAP reconstruction')
def check_colmap_res(root_dir):
    path = root_dir / "output/colmap/sparse/0"
    assert path.exists()

@given('a valid "aruco_data.json" with 3D poses')
def check_aruco_json(root_dir):
    path = root_dir / "output/aruco_data.json"
    assert path.exists()

@when('the scaling script is executed', target_fixture="scale")
def execute_scaling(root_dir):
    from scripts.model_scaler import calculate_scale
    return calculate_scale(root_dir / "output/aruco_data.json", None)

@then('a scaling factor is calculated')
def verify_scale(scale):
    assert scale > 0
    print(f"Computed Scale: {scale}")

@then('the final point cloud is saved in meters')
def verify_scaled_output(root_dir):
    # Verify the final PLY exists after scaling
    final_model = root_dir / "output/scaled_model.ply"
    assert final_model.exists(), "The final scaled 3D model was not generated."