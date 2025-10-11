import pytest
from pathlib import Path

@pytest.fixture
def tests_dir() -> Path:
    """Fixture to provide tests directory path"""
    return Path(__file__).parent

