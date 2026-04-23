import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

def test_initial_orders_table_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    assert "orders:" in content, "Expected 'orders' table in inconvo.yaml."
    assert "revenue:" in content, "Expected 'revenue' field in inconvo.yaml."
    assert "cost:" in content, "Expected 'cost' field in inconvo.yaml."
    assert "gross_margin:" not in content, "The 'gross_margin' field should not exist initially."