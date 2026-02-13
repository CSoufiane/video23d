import yaml
import numpy as np

def load_camera_params(path):
    """Loads and returns camera matrix and distortion coefficients."""
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    K = np.array(data['camera_matrix'], dtype=np.float32)
    D = np.array(data['distortion_coefficients'], dtype=np.float32)
    return K, D

def validate_calibration_integrity(K, D):
    """Checks if the loaded parameters meet geometric requirements."""
    # K must be 3x3, D must have at least 5 coefficients (k1, k2, p1, p2, k3)
    return K.shape == (3, 3) and len(D.flatten()) >= 5