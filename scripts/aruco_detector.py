import cv2
import cv2.aruco as aruco
import json
import numpy as np
import yaml
from pathlib import Path

def detect_markers(image_dir, output_json, calib_path="camera_calib.yaml", marker_size=0.05):
    """
    Detects ArUco markers and estimates their 3D pose (rvec, tvec).
    :param marker_size: The real-world side length of the marker in meters (e.g., 0.05 for 5cm).
    """
    # 1. Load Calibration Data
    with open(calib_path, 'r') as f:
        calib = yaml.safe_load(f)
    
    matrix_coefficients = np.array(calib['camera_matrix'])
    distortion_coefficients = np.array(calib['distortion_coefficients'])

    # 2. Setup Detector
    # Ensure this matches the dictionary you used (you mentioned 7x7)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_7X7_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    # Define the 3D coordinates of the marker corners in its own coordinate system
    # This is required for solvePnP to map 2D -> 3D
    obj_points = np.array([
        [-marker_size / 2,  marker_size / 2, 0],
        [ marker_size / 2,  marker_size / 2, 0],
        [ marker_size / 2, -marker_size / 2, 0],
        [-marker_size / 2, -marker_size / 2, 0]
    ], dtype=np.float32)

    image_path = Path(image_dir)
    results = {}

    for img_file in sorted(image_path.glob("*.jpg")):
        frame = cv2.imread(str(img_file))
        if frame is None: continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is not None:
            frame_results = []
            for i in range(len(ids)):
                # Estimate pose for each marker found
                # solvePnP returns:
                # rvec: Rotation vector (orientation)
                # tvec: Translation vector (position in x, y, z)
                success, rvec, tvec = cv2.solvePnP(
                    obj_points, corners[i], 
                    matrix_coefficients, distortion_coefficients
                )

                if success:
                    frame_results.append({
                        "id": int(ids[i][0]),
                        "rvec": rvec.flatten().tolist(),
                        "tvec": tvec.flatten().tolist(),
                        "corners": corners[i].tolist()
                    })
            
            if frame_results:
                results[img_file.name] = frame_results

    # 3. Save to JSON
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=4)
    
    return len(results)