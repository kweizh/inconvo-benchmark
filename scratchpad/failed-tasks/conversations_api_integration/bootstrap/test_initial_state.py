import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-api-task"

def test_node_available():
    assert shutil.which("node") is not None, "Node.js not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_database_url_env_var():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is required but not set."

def test_inconvo_api_key_env_var():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY environment variable is required but not set."

def test_inconvo_agent_id_env_var():
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID environment variable is required but not set."
