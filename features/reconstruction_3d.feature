Feature: 3D Reconstruction
  As a developer
  I want to transform images into a 3D model
  In order to obtain an accurate spatial representation

  @US-17 @US-18
  Scenario: Generate sparse reconstruction and verify trajectory
    Given a directory of valid and calibrated images
    When COLMAP is executed with default parameters
    Then a sparse model (.db and binary folders) is generated
    And a sparse point cloud containing at least 1000 points is exported
    And the camera trajectory shows no jumps greater than 1 meter between two frames

  @US-19 @US-20
  Scenario: Scale alignment and metric precision validation
    Given camera poses from COLMAP
    And camera poses from ArUco markers (real-world scale)
    When the alignment algorithm using similarity transformation is executed
    Then a stable scale factor is calculated
    And the distance measured between two markers in the 3D model has an error < 5% compared to reality

  @US-21
  Scenario: Generate a dense point cloud (Optional)
    Given a valid sparse reconstruction
    When the dense reconstruction process is triggered
    Then a "model_dense.ply" file is generated in the output folder
    And the file follows the standard PLY format