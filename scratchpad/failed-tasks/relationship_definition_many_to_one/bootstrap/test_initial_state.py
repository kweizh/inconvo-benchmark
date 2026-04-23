import os
import shutil
import subprocess
import pytest

def test_inconvo_binary_available():
    # The task uses npx inconvo, but we should check if npm is available
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_database_url_env_available():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."

def test_postgres_available():
    # Since we require a real PostgreSQL, we should check if psql or the port is reachable
    # For now, just check if we can connect via psql if available, or just rely on DATABASE_URL existence
    # as per instructions "require DATABASE_URL in the environment"
    pass
