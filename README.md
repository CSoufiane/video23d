# 3D Reconstruction Pipeline (Video23D)

This project provides an automated pipeline to transform video and image data into scaled 3D point clouds. It uses **COLMAP** for Structure from Motion (SfM) and **ArUco markers** for metric scaling.

---

## 📖 Documentation & Requirements

To maintain a clean and structured project, documentation is split into three key areas:

1.  **[User Stories (Functional)](./features/mvp_user_stories.md)**: Detailed breakdown of the project goals, Epics, and BDD scenarios.
2.  **[Technical Contract (Data)](./CONTRACT.md)**: Specification of data schemas and interfaces between pipeline steps.
3.  **[Validation Suite](./features/)**: Executable Gherkin features that define the acceptance criteria.

---

## 🛠 Setup & Execution

### 1. Initialize Environment
Run the following command to set up directories and install dependencies (OpenCV, COLMAP, FFmpeg):
    ```bash
    make setup
    ```
    [cite_start]This creates the `frames/`, `output/`, and `data/raw/` directories and runs the `setup.sh` script[cite: 15].

### 2.  **Run Pipeline**: Place your input video at `data/raw/test_scene.mp4` and execute:
    ```bash
    make run
    ```
    [cite_start]The final model will be saved as `output/scaled_model.ply`[cite: 15, 16].

### 3.  **Run Tests**: To validate the pipeline using BDD (Behavior Driven Development) scenarios:
    ```bash
    make test
    ```
    [cite_start]This executes the test suite located in `tests/step_definitions/`[cite: 15, 16].

---

## 📐 Technical Pipeline Contract

To maintain synchronization between the pipeline implementation and the BDD test suite, the following data schemas and file interfaces are enforced:

### 1. Camera Calibration
* [cite_start]**Module**: `scripts/calibration_generator.py`[cite: 1].
* [cite_start]**Output**: `camera_calib.yaml`[cite: 2].
* [cite_start]**Schema**: Must contain `camera_matrix` (3x3) and `distortion_coefficients` (1x5)[cite: 3].

### 2. Frame Extraction
* [cite_start]**Module**: `scripts/extractor.py`[cite: 1].
* [cite_start]**Output Folder**: `frames/`[cite: 6].
* [cite_start]**Constraint**: Images must be named sequentially (e.g., `frame_0001.jpg`) and be readable by OpenCV[cite: 6, 7].

### 3. ArUco Marker Detection
* [cite_start]**Module**: `scripts/aruco_detector.py`[cite: 1].
* [cite_start]**Output File**: `output/aruco_data.json`[cite: 14].
* **Data Structure**:
    ```json
    {
      "frame_0000.jpg": [
        {
          "id": 0,
          "corners": [[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]],
          "rvec": [rx, ry, rz],
          "tvec": [tx, ty, tz]
        }
      ]
    }
    ```
* **Contract Note**: Each frame key maps to a **list** of marker dictionaries to support multiple detections per image.

### 4. 3D Reconstruction (COLMAP)
* [cite_start]**Module**: `scripts/colmap_wrapper.py`[cite: 1].
* **Required Binary Outputs**: 
    * [cite_start]`output/colmap/sparse/0/images.bin` (Camera poses)[cite: 12].
    * [cite_start]`output/colmap/sparse/0/points3D.bin` (Point cloud)[cite: 16].

### 5. Model Scaling
* [cite_start]**Module**: `scripts/model_scaler.py`[cite: 1].
* [cite_start]**Logic**: Compares the translation distance (`tvec`) of ArUco markers against the translation distance in COLMAP camera poses to derive a median scale factor[cite: 14].
* **Safety**: If `images.bin` is missing during testing, the scaler defaults to a factor of `1.0` to prevent pipeline crashes.

---

## 🧪 Testing & Validation
[cite_start]The project uses `pytest-bdd` to ensure all user stories are met[cite: 16]. Key validations include:
* [cite_start]**Metric Accuracy**: Distance error between markers must be < 5%[cite: 12].
* [cite_start]**Reconstruction Quality**: Sparse point cloud must contain at least 1000 points[cite: 11].
* [cite_start]**Marker Coverage**: Reference markers must be detected in at least 3 different frames for stable scaling[cite: 5].

---

## 📁 Project Structure
* [cite_start]`features/`: Gherkin files defining BDD requirements[cite: 1].
* [cite_start]`scripts/`: Core logic for extraction, detection, and reconstruction[cite: 1].
* [cite_start]`tests/`: Step definitions and pytest configuration[cite: 1].