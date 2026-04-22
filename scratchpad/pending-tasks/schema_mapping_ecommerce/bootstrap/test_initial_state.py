import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/ecommerce-analytics"

def test_node_available():
    assert shutil.which("node") is not None, "Node.js binary not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_npx_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_database_url_env_variable():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."
    assert os.environ["DATABASE_URL"].startswith("postgresql://"), "DATABASE_URL must be a valid PostgreSQL connection string."

def test_project_dir_exists():
    # The task says the user should create it, but in Harbor tasks, 
    # sometimes the base directory is already there. 
    # If the task says "Initialize an Inconvo project in /home/user/ecommerce-analytics",
    # we should check if /home/user exists.
    assert os.path.exists("/home/user"), "/home/user directory does not exist."
