import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
VERSION_FILE = os.path.join(PROJECT_DIR, "version.txt")

def test_version_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(VERSION_FILE), f"version.txt not found at {VERSION_FILE}"

def test_version_content_matches_cli():
    """Priority 1: Use CLI to get expected version and compare with file content."""
    result = subprocess.run(
        ["inconvo", "--version"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"'inconvo --version' failed: {result.stderr}"
    
    expected_version = result.stdout.strip()
    
    with open(VERSION_FILE, "r") as f:
        actual_content = f.read().strip()
        
    assert expected_version in actual_content or actual_content in expected_version, \
        f"Expected version '{expected_version}' to be in version.txt, but got '{actual_content}'"
