Feature: Environment Setup
  As a developer
  I want to initialize the project and its dependencies
  So that I can ensure a stable reconstruction pipeline

  Scenario: US-01 - Project structure verification
    Given I am in the project root directory
    Then the directory tree must contain "frames", "scripts", and "output" folders
    And a "README.md" file must be present and not empty

  Scenario: US-02 - Software dependencies verification
    Given the system is configured
    Then the Python version should be 3.11 or higher
    And the command "colmap -h" should execute without error
    And the command "ffmpeg -version" should be recognized
    And the "cv2.aruco" module must be importable in Python
    And all dependencies listed in "requirements.txt" must be installed