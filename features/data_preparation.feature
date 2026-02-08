Feature: Data Acquisition and Preparation
  As a user and developer
  I want to prepare the scene and extract data from the video
  In order to feed the photogrammetry algorithm

  @US-13
  Scenario: Extract usable frames from a video
    Given a valid input video file "input.mp4"
    And the FPS parameter is set to 2 frames per second
    When the extraction script is executed
    Then a frames directory is created
    And the images are named sequentially (e.g., frame_0001.jpg)
    And every extracted image is readable by the OpenCV library