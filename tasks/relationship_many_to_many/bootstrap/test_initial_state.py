import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_cli_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_config_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

def test_initial_tables_defined():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    assert "orders:" in content, "Expected 'orders' table in inconvo.yaml."
    assert "products:" in content, "Expected 'products' table in inconvo.yaml."
    assert "line_items:" in content, "Expected 'line_items' table in inconvo.yaml."
    assert "relations:" in content, "Expected 'relations' section in inconvo.yaml."