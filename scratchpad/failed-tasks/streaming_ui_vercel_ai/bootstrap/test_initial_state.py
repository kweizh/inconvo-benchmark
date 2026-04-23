import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_node_installed():
    assert shutil.which("node") is not None, "Node.js not found in PATH."
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    assert result.stdout.startswith("v24"), f"Expected Node.js v24, got {result.stdout}"

def test_npm_installed():
    assert shutil.which("npm") is not None, "npm not found in PATH."

def test_postgresql_client_installed():
    assert shutil.which("psql") is not None, "psql client not found in PATH."

def test_database_url_env_set():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."
    assert os.environ["DATABASE_URL"].startswith("postgres://") or os.environ["DATABASE_URL"].startswith("postgresql://"), \
        "DATABASE_URL must be a valid PostgreSQL connection string."

def test_inconvo_keys_set():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY is not set."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID is not set."

def test_openai_key_set():
    assert "OPENAI_API_KEY" in os.environ, "OPENAI_API_KEY is not set (required for Vercel AI SDK)."
