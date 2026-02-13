Feature: Camera Calibration Computation
  As a developer
  I want to compute the camera intrinsics from a set of calibration images
  In order to generate a valid camera_calib.yaml file for the reconstruction pipeline

  @US-06
  Scenario: Compute camera matrix and distortion coefficients
    Given a directory "data/calibration" containing checkerboard images
    And the checkerboard dimensions are 9x6
    When the calibration script is executed
    Then the re-projection error is calculated
    And the file "camera_calib.yaml" is generated in the root directory
    And the file contains "camera_matrix" and "distortion_coefficients"