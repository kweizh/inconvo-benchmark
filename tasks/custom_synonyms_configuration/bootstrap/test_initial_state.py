import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml file {YAML_FILE} does not exist."

def test_initial_yaml_content():
    with open(YAML_FILE) as f:
        content = f.read()
    assert "orders:" in content, "Expected 'orders:' table in inconvo.yaml."
    assert "total_amount:" in content, "Expected 'total_amount:' field in inconvo.yaml."
    assert "synonyms:" not in content, "Expected no 'synonyms:' initially in inconvo.yaml."
    assert "revenue" not in content, "Expected no 'revenue' initially in inconvo.yaml."
    assert "income" not in content, "Expected no 'income' initially in inconvo.yaml."
