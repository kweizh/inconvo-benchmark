import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_npx_binary_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."
