import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_inconvo_sdk_installed():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"
    
    with open(package_json_path, "r") as f:
        content = f.read()
    
    assert "@inconvoai/node" in content, "Expected '@inconvoai/node' to be installed in package.json."
