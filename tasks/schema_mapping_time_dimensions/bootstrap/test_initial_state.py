import os
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "orders:" in content, "Expected 'orders' table definition in inconvo.yaml"

def test_index_js_exists():
    js_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(js_path), f"index.js not found at {js_path}"
