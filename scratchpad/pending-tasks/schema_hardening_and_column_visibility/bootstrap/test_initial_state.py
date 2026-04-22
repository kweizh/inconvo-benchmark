import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = "/home/user/inconvo-project"
CONFIG_PATH = os.path.join(PROJECT_DIR, ".inconvo/inconvo.yaml")

def test_inconvo_binary_available():
    # Check if inconvo is available
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_config_file_exists():
    assert os.path.isfile(CONFIG_PATH), f"Config file {CONFIG_PATH} does not exist."

def test_database_url_env_var():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."

def test_initial_config_contains_sensitive_fields():
    # Verify that the initial config has the fields we want to hide
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    
    assert "users:" in content, "Table 'users' not found in inconvo.yaml"
    assert "password_hash:" in content, "Field 'password_hash' not found in users table"
    assert "secret_key:" in content, "Field 'secret_key' not found in users table"
    
    # Check that they are currently On or not set to Off
    # This is a bit loose but ensures the starting state is 'insecure'
    assert "state: Off" not in content or content.count("state: Off") < 2, \
        "Sensitive fields are already set to Off in the initial state."
