import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-project"
CONFIG_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_config_file_exists():
    assert os.path.isfile(CONFIG_FILE), f"Config file {CONFIG_FILE} does not exist."

def test_initial_config_content():
    with open(CONFIG_FILE) as f:
        content = f.read()
    assert "orders:" in content, "Expected 'orders' table in inconvo.yaml."
    assert "total_amount:" in content, "Expected 'total_amount' field in inconvo.yaml."
    assert "synonyms:" not in content, "Did not expect 'synonyms' to be already defined in inconvo.yaml."