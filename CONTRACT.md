# Technical Pipeline Contract (Video23D)

This contract defines the data schemas and file interfaces required for the 3D reconstruction pipeline to ensure consistency between the implementation and the BDD test suite.

## 1. Camera Calibration
* [cite_start]**Module**: `scripts/calibration_generator.py` [cite: 1, 15]
* [cite_start]**Output File**: `camera_calib.yaml` [cite: 1, 2]
* [cite_start]**Data Schema**: Must contain `camera_matrix` (3x3) and `distortion_coefficients` (1x5)[cite: 2, 3].

## 2. Frame Extraction
* [cite_start]**Module**: `scripts/extractor.py` [cite: 1, 15]
* [cite_start]**Output Folder**: `frames/` [cite: 1, 6]
* [cite_start]**Constraint**: Images must be named sequentially (e.g., `frame_0001.jpg`) and be readable by OpenCV[cite: 6, 7].

## 3. ArUco Marker Detection
* [cite_start]**Module**: `scripts/aruco_detector.py` [cite: 1, 15]
* [cite_start]**Output File**: `output/aruco_data.json` [cite: 1, 15]
* **Data Structure**:
    ```json
    {
      "frame_name.jpg": [
        {
          "id": int,
          "corners": [[[x,y], [x,y], [x,y], [x,y]]],
          "rvec": [rx, ry, rz],
          "tvec": [tx, ty, tz]
        }
      ]
    }
    ```
* **Requirement**: Each frame entry is a **list** of dictionaries to support multiple markers[cite: 1, 15].

## 4. 3D Reconstruction (COLMAP)
* [cite_start]**Module**: `scripts/colmap_wrapper.py` [cite: 1, 15]
* **Required Outputs**: 
    * [cite_start]A sparse model folder with binary files [cite: 11]
    * [cite_start]Binary camera poses: `output/colmap/sparse/0/images.bin` [cite: 1, 15]
    * [cite_start]Binary point cloud: `output/colmap/sparse/0/points3D.bin` [cite: 1, 15]

## 5. Model Scaling
* [cite_start]**Module**: `scripts/model_scaler.py` [cite: 1, 15]
* [cite_start]**Input**: Requires valid paths to `aruco_data.json` and `images.bin` [cite: 1, 15]
* [cite_start]**Output**: Returns a `float` scale factor to transform units into real-world meters[cite: 1, 14, 15].