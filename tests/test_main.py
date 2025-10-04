"""Test cases for main module"""
import pytest
from src.main import main


def test_main_runs():
    """Test that main function runs without errors"""
    try:
        main()
        assert True
    except Exception as e:
        pytest.fail(f"main() raised {e}")
