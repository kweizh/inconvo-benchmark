import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-project"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_yaml_file_exists():
    assert os.path.isfile(YAML_FILE), f"Config file {YAML_FILE} does not exist."

def test_initial_states():
    with open(YAML_FILE, "r") as f:
        content = f.read()
    
    assert "customers:" in content, "Expected 'customers' table in inconvo.yaml."
    assert "internal_logs:" in content, "Expected 'internal_logs' table in inconvo.yaml."
    assert "orders:" in content, "Expected 'orders' table in inconvo.yaml."
    
    # Simple check for initial state, ideally we'd parse YAML but this verifies the file was created correctly
    assert "state: Queryable" in content, "Expected initial states to be Queryable."