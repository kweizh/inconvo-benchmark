import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."

def test_initial_passwords_state():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "passwords:" in content, "Expected 'passwords' table in inconvo.yaml."
    assert "users:" in content, "Expected 'users' table in inconvo.yaml."
    assert "state: Queryable" in content, "Expected 'state: Queryable' in inconvo.yaml."