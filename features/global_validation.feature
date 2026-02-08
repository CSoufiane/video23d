Feature: Global Pipeline Validation
  As an end user
  I want the pipeline to work from start to finish
  In order to validate the MVP success

  @US-22
  Scenario: End-to-End pipeline execution
    Given a test video located at "data/raw/test_scene.mp4"
    When I run the main command "python main.py"
    Then the pipeline executes without any critical errors
    And the final report indicates an average reconstruction error below 3%
    And a final scaled 3D model is available for visualization