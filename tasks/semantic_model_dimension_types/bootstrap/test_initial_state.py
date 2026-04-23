import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

def test_initial_yaml_content():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "orders:" in content, "Missing 'orders:' table in inconvo.yaml"
    assert "total_amount:" in content, "Missing 'total_amount:' field"
    assert "created_at:" in content, "Missing 'created_at:' field"
    assert "type: measure" not in content, "type: measure should not be in the initial file"
    assert "type: dimension" not in content, "type: dimension should not be in the initial file"
