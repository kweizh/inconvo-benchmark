import os
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_PATH = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    assert os.path.isfile(YAML_PATH), f"Config file {YAML_PATH} does not exist."

def test_initial_yaml_content():
    with open(YAML_PATH, "r") as f:
        content = f.read()
    
    # Check tables exist
    assert "users:" in content, "Expected 'users' table in inconvo.yaml"
    assert "products:" in content, "Expected 'products' table in inconvo.yaml"
    assert "orders:" in content, "Expected 'orders' table in inconvo.yaml"
    
    # Check fields exist
    assert "internal_id:" in content, "Expected 'internal_id' field in inconvo.yaml"
    assert "title:" in content, "Expected 'title' field in inconvo.yaml"
    assert "total_amount:" in content, "Expected 'total_amount' field in inconvo.yaml"
