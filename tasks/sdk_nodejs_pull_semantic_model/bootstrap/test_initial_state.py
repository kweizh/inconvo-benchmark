import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"

def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_npx_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_env_vars_available():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY environment variable is not set."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID environment variable is not set."
