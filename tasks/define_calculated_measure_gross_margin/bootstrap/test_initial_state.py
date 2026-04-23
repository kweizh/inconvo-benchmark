import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_cli_available():
    assert shutil.which("inconvo") is not None, "inconvo CLI not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_model_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."
    with open(config_path) as f:
        content = f.read()
    assert "products:" in content, "Expected 'products' table in inconvo.yaml."
