import os
import pytest
import shutil

PROJECT_DIR = "/home/user/myproject"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."

def test_initial_yaml_state():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "password_hash: { state: On }" in content or "password_hash:\n        state: On" in content, "Expected initial state of password_hash to be 'On' in inconvo.yaml."
    assert "internal_logs:\n    state: Queryable" in content or "internal_logs: { state: Queryable }" in content, "Expected initial state of internal_logs to be 'Queryable' in inconvo.yaml."
