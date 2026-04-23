import os
import pytest

PROJECT_DIR = "/home/user/my-agent"

def test_project_directory_exists():
    """Priority 3 fallback: basic directory existence check."""
    assert os.path.isdir(PROJECT_DIR), \
        f"Project directory not found at {PROJECT_DIR}"

def test_inconvo_yaml_exists():
    """Priority 3 fallback: basic file existence check."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), \
        f"inconvo.yaml not found at {yaml_path}"

def test_inconvo_yaml_content():
    """Priority 3 fallback: verify file content."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, 'r') as f:
        content = f.read()
    assert "tables: {}" in content, "Expected 'tables: {}' in inconvo.yaml"
    assert "relations: []" in content, "Expected 'relations: []' in inconvo.yaml"
