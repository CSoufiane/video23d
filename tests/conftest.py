import pytest
import os
from pathlib import Path

@pytest.fixture(scope="session")
def root_dir():
    """
    Finds the project root by looking for a 'Makefile' or '.git' directory.
    This is much safer than counting 'parent.parent'.
    """
    current_path = Path(__file__).resolve()
    # Climb up the tree until we find the Makefile
    for parent in current_path.parents:
        if (parent / "Makefile").exists() or (parent / ".git").exists():
            return parent
    # Fallback to the current working directory
    return Path(os.getcwd())