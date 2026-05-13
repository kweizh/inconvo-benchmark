import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

def test_initial_yaml_content():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "orders:" in content, "Expected 'orders' table in inconvo.yaml"
    assert "revenue:" in content, "Expected 'revenue' field in inconvo.yaml"
    assert "cost:" in content, "Expected 'cost' field in inconvo.yaml"
    assert "gross_margin:" not in content, "Expected 'gross_margin' to not exist initially in inconvo.yaml"
