import cv2
import numpy as np
import yaml
from pathlib import Path

def compute_calibration(image_dir, grid_size=(9, 6), square_size=0.025):
    """
    Computes camera intrinsics and saves to camera_calib.yaml.
    square_size is the size of a square side in meters.
    """
    # Prepare object points (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
    objp = np.zeros((grid_size[0] * grid_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:grid_size[0], 0:grid_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = list(Path(image_dir).glob('*.jpg'))
    if not images:
        raise FileNotFoundError(f"No images found in {image_dir}")

    for fname in images:
        img = cv2.imread(str(fname))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, grid_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

    # Perform calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    data = {
        "camera_matrix": mtx.tolist(),
        "distortion_coefficients": dist.tolist()[0],
        "reprojection_error": float(ret)
    }

    with open("camera_calib.yaml", "w") as f:
        yaml.dump(data, f)
    
    return ret

def generate_standard_calibration(width, height, output_path):
    """Generates a generic 1080p calibration if no images are available."""
    f = max(width, height) * 0.8 # Rough estimate for wide angle
    data = {
        "camera_matrix": [[f, 0, width/2], [0, f, height/2], [0, 0, 1]],
        "distortion_coefficients": [0.0, 0.0, 0.0, 0.0, 0.0],
        "reprojection_error": 0.0
    }
    with open(output_path, 'w') as f:
        yaml.dump(data, f)