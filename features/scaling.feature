Feature: Model Scaling
  As a developer
  I want to scale the 3D model using ArUco references
  So that the measurements in the model reflect the real world

  @US-09
  Scenario: Calculate and apply scale factor
    Given a successful COLMAP reconstruction
    And a valid "aruco_data.json" with 3D poses
    When the scaling script is executed
    Then a scaling factor is calculated
    And the final point cloud is saved in meters