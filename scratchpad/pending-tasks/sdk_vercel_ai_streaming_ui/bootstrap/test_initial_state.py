import os
import shutil
import pytest
import json

PROJECT_DIR = "/home/user/app"

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json not found at {pkg_path}"
    
    with open(pkg_path, "r") as f:
        data = json.load(f)
        
    deps = data.get("dependencies", {})
    assert "@inconvoai/node" in deps, "@inconvoai/node is not installed in package.json"
    assert "@inconvoai/vercel-ai-sdk" in deps, "@inconvoai/vercel-ai-sdk is not installed in package.json"
    assert "ai" in deps, "ai package is not installed in package.json"
    assert "next" in deps, "next package is not installed in package.json"
    assert "react" in deps, "react package is not installed in package.json"
