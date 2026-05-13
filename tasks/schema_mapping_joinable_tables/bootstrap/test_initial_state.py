import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Config file {yaml_path} does not exist."

def test_initial_state_is_queryable():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "state: Queryable" in content, "Expected initial state of customers to be 'Queryable' in inconvo.yaml."
