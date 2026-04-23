import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None or shutil.which("npx") is not None, "inconvo or npx binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_config_file_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

def test_initial_tables_exist():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    assert "users:" in content, "Expected 'users' table in inconvo.yaml."
    assert "profiles:" in content, "Expected 'profiles' table in inconvo.yaml."