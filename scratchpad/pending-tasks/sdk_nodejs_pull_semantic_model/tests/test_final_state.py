import os
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
MODEL_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_yaml_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(MODEL_FILE), f"inconvo.yaml not found at {MODEL_FILE}"

def test_inconvo_yaml_contains_tables():
    """Priority 3 fallback: check file contents."""
    with open(MODEL_FILE, "r") as f:
        content = f.read()
    
    assert "tables:" in content, "Expected 'tables:' in inconvo.yaml to indicate a valid semantic model."
