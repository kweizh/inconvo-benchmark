import os
import shutil
import pytest

PROJECT_DIR = "/home/user/project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."

def test_initial_yaml_content():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path) as f:
        content = f.read()
    assert "orders:" in content, "Expected 'orders' table definition in inconvo.yaml."
