Feature: Computer Vision Analysis
  As a developer
  I want to calibrate the camera and detect markers
  So that I can define the spatial reference frame

  @US-14
  Scenario: Load a valid camera calibration
    Given a camera calibration file "camera_calib.yaml"
    When the pipeline starts
    Then the camera matrix K is successfully loaded
    And the distortion coefficients D are available
    And no projection errors are raised during a test on a target image

  @US-15
  Scenario: Detect markers in an image
    Given a set of extracted frames
    When the ArUco detection algorithm is executed
    Then at least one marker ID is recognized per analyzed frame
    And the camera poses (rvec, tvec) are stored

  @US-16
  Scenario: Verify marker visibility over several frames
    Given a set of extracted frames
    When the ArUco detection algorithm is executed
    Then each reference marker is detected in at least 3 different frames