import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

def test_inconvo_yaml_initial_state():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "orders" in content, "Expected 'orders' table in initial inconvo.yaml"
    assert "users" in content, "Expected 'users' table in initial inconvo.yaml"
    assert "relations:" not in content, "Expected 'relations' to be absent in initial inconvo.yaml"

def test_package_json_exists():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json not found at {pkg_path}"
