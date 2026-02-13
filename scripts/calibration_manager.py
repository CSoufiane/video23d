import numpy as np
import yaml
from pathlib import Path

class CalibrationManager:
    def __init__(self, calib_path: str):
        self.path = Path(calib_path)
        self.K = None
        self.D = None
        self.reprojection_error = 0.0

    def load_calibration(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Calibration file {self.path} not found.")
        
        with open(self.path, 'r') as f:
            data = yaml.safe_load(f)
        
        self.K = np.array(data['camera_matrix'], dtype=np.float32)
        self.D = np.array(data['distortion_coefficients'], dtype=np.float32)
        self.reprojection_error = data.get('reprojection_error', 0.0)
        
        return self.K, self.D

    def validate_geometry(self):
        # Basic sanity check for a standard pinhole model
        return self.K.shape == (3, 3) and len(self.D.flatten()) >= 5