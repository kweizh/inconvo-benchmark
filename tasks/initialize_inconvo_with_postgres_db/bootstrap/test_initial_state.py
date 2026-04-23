import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_absent():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert not os.path.isfile(config_path), f"Config file {config_path} should not exist yet."

def test_env_file_absent():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert not os.path.isfile(env_path), f".env file {env_path} should not exist yet."
