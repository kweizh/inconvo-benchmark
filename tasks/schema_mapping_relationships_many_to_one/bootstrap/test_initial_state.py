import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Config file {yaml_path} does not exist."
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "line_items:" in content, "Expected 'line_items' table in inconvo.yaml."
    assert "products:" in content, "Expected 'products' table in inconvo.yaml."

def test_index_js_exists():
    index_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_path), f"Script {index_path} does not exist."
