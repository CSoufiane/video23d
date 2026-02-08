import yaml
import numpy as np

def generate_standard_calibration(width, height, output_path="camera_calib.yaml"):
    """
    Generates a heuristic camera matrix and zero distortion.
    Focal length is estimated at ~width of the frame.
    """
    # Heuristic: f = width (standard for many phone lenses)
    f = width 
    cx = width / 2
    cy = height / 2

    # Camera Matrix K
    # [fx  0 cx]
    # [ 0 fy cy]
    # [ 0  0  1]
    camera_matrix = [
        [float(f), 0.0, float(cx)],
        [0.0, float(f), float(cy)],
        [0.0, 0.0, 1.0]
    ]

    # Standard distortion (assuming a modern phone with low distortion)
    dist_coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]

    data = {
        "image_width": width,
        "image_height": height,
        "camera_matrix": camera_matrix,
        "distortion_coefficients": dist_coeffs
    }

    with open(output_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    
    return data

if __name__ == "__main__":
    # Standard 1080p example
    generate_standard_calibration(1920, 1080)
    print("Generated standard camera_calib.yaml")