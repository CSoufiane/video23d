import numpy as np
import yaml
from pathlib import Path
from scripts.extractor import extract_frames
from scripts.aruco_detector import detect_markers
from scripts.colmap_wrapper import run_colmap_reconstruction
from scripts.model_scaler import calculate_scale

def main():
    print("--- MVP 3D Reconstruction Pipeline ---")
    
    VIDEO_INPUT = "data/raw/test_scene.mp4"
    FRAME_OUTPUT = "frames"
    DATA_OUTPUT = "output/aruco_data.json"
    COLMAP_OUTPUT = "output/colmap"
    IMAGES_BIN = "output/colmap/sparse/0/images.bin"
    POINTS_BIN = "output/colmap/sparse/0/points3D.bin"
    FINAL_PLY = "output/scaled_model.ply"

    # Step 1: Extraction
    print("[Step 1] Extracting frames...")
    extract_frames(VIDEO_INPUT, FRAME_OUTPUT, fps=2)

    # Step 2: Detection (US-07)
    print("[Step 2] Detecting ArUco markers...")
    num_detected = detect_markers(FRAME_OUTPUT, DATA_OUTPUT)
    print(f"Markers detected in {num_detected} frames. Data saved to {DATA_OUTPUT}")

    CALIB_PATH = "camera_calib.yaml"
    # Load Calibration (US-06)
    with open(CALIB_PATH, 'r') as f:
        calib = yaml.safe_load(f)
    K = np.array(calib['camera_matrix'])
    D = np.array(calib['distortion_coefficients'])
    
    # Now you can use K and D in your marker detection 
    # to get real-world distances!
    # print("Calibration loaded. Ready for 3D pose estimation.")

    # Step 3: COLMAP Reconstruction (US-08)
    print("[Step 3] Starting COLMAP Structure from Motion...")
    success = run_colmap_reconstruction(FRAME_OUTPUT, COLMAP_OUTPUT)
    
    if success:
        print(f"Reconstruction finished! Files are in {COLMAP_OUTPUT}/sparse/0")
    else:
        print("Reconstruction failed.")

    if Path(IMAGES_BIN).exists():
        print("[Step 4] Scaling model to real-world dimensions...")
        scale = calculate_scale(DATA_OUTPUT, IMAGES_BIN)
        print(f"Final Scale Factor: {scale:.4f} (1 COLMAP unit = {scale:.4f} meters)")
        
        # In a full app, you'd multiply all points3D.bin by this scale
        # For MVP, knowing the scale is the key validation.
    if Path(POINTS_BIN).exists():
        from scripts.ply_exporter import export_scaled_ply
        export_scaled_ply(POINTS_BIN, FINAL_PLY, scale)
        print(f"--- SUCCESS: Open {FINAL_PLY} in MeshLab to see your 3D scene! ---")

if __name__ == "__main__":
    main()
