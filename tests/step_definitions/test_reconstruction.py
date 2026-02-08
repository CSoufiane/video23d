from pytest_bdd import scenario, given, when, then
from pathlib import Path

@scenario('../../features/reconstruction.feature', 'Generate a sparse 3D point cloud')
def test_sparse_reconstruction():
    pass

@then('a "sparse" directory is created containing ".bin" or ".txt" files')
def check_colmap_output(root_dir):
    sparse_dir = root_dir / "output/colmap/sparse/0"
    # COLMAP creates cameras.bin, images.bin, and points3D.bin
    assert sparse_dir.exists()
    assert any(sparse_dir.glob("*.bin")) or any(sparse_dir.glob("*.txt"))