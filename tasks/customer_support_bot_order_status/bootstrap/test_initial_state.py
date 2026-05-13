import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-bot"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_env_file_exists():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f".env file not found at {env_path}"

def test_env_file_contains_variables():
    env_path = os.path.join(PROJECT_DIR, ".env")
    with open(env_path, "r") as f:
        content = f.read()
    
    assert "INCONVO_API_KEY" in content, "Expected INCONVO_API_KEY in .env file."
    assert "INCONVO_AGENT_ID" in content, "Expected INCONVO_AGENT_ID in .env file."
    assert "DATABASE_URL" in content, "Expected DATABASE_URL in .env file."

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."