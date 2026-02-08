import pytest
import subprocess
import sys
import os
from pathlib import Path
import importlib.metadata
from packaging.requirements import Requirement
from pytest_bdd import scenario, given, when, then, parsers

# --- Path Configuration ---
# Get the absolute path to the features directory
FEATURE_DIR = os.path.join(os.path.dirname(__file__), "../../features")

@scenario(os.path.join(FEATURE_DIR, 'environment_setup.feature'), 'US-01 - Project structure verification')
def test_project_structure():
    pass

@scenario(os.path.join(FEATURE_DIR, 'environment_setup.feature'), 'US-02 - Software dependencies verification')
def test_dependencies():
    pass


# --- Given Steps ---

@given('I am in the project root directory')
def i_am_in_root_dir(root_dir):
    """Confirms the root directory is accessible."""
    return root_dir

@given('the system is configured')
def system_configured():
    """Placeholder step to satisfy Gherkin context."""
    return True

# --- Then Steps (Structure) ---

@then(parsers.parse('the directory tree must contain "{folder1}", "{folder2}", and "{folder3}" folders'))
def check_folders(root_dir, folder1, folder2, folder3):
    for folder in [folder1, folder2, folder3]:
        path = root_dir / folder
        assert path.is_dir(), f"Directory missing: {folder}"

@then('a "README.md" file must be present and not empty')
def check_readme(root_dir):
    readme = root_dir / "README.md"
    assert readme.is_file(), "README.md is missing"
    assert readme.stat().st_size > 0, "README.md is empty"

# --- Then Steps (Dependencies) ---

@then('the Python version should be 3.11 or higher')
def check_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor
    assert (major == 3 and minor >= 11) or major > 3, f"Python 3.11+ required, found {major}.{minor}"

@then('the command "colmap -h" should execute without error')
def check_colmap():
    try:
        result = subprocess.run(["colmap", "-h"], capture_output=True, text=True)
        assert result.returncode == 0
    except FileNotFoundError:
        pytest.fail("COLMAP is not installed or not in your PATH.")

@then('the command "ffmpeg -version" should be recognized')
def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        assert result.returncode == 0
    except FileNotFoundError:
        pytest.fail("FFmpeg is not installed or not in your PATH.")

@then('the "cv2.aruco" module must be importable in Python')
def check_aruco_import():
    try:
        import cv2
        # Check if the aruco attribute exists (depends on opencv-contrib version)
        aruco_module = getattr(cv2, 'aruco', None)
        assert aruco_module is not None
    except ImportError:
        pytest.fail("OpenCV is not installed. Ensure 'opencv-contrib-python' is in requirements.txt.")

@then('all dependencies listed in "requirements.txt" must be installed')
def check_requirements(root_dir):
    requirements_path = root_dir / "requirements.txt"
    assert requirements_path.exists(), "requirements.txt file is missing"
    
    with open(requirements_path) as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith(('#', '-r')):
                continue
            
            req = Requirement(line)
            try:
                # Use importlib.metadata to check version
                installed_version = importlib.metadata.version(req.name)
                assert req.specifier.contains(installed_version, prereleases=True), \
                    f"Installed {req.name} ({installed_version}) does not match {req.specifier}"
            except importlib.metadata.PackageNotFoundError:
                pytest.fail(f"Dependency check failed: {req.name} is not installed.")