import os
import shutil
import subprocess
import pytest

def test_inconvo_binary_available():
    # Inconvo is installed via npm globally or available in PATH
    assert shutil.which("inconvo") is not None, "inconvo CLI binary not found in PATH."

def test_database_url_env_variable():
    # The task requires DATABASE_URL to be set
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."

def test_postgresql_available():
    # Verify psql is available to check database connectivity
    assert shutil.which("psql") is not None, "psql CLI binary not found in PATH."
