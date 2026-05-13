import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_env_vars_set():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY is not set."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID is not set."
    assert "INCONVO_POSTGRESQL_URL" in os.environ, "INCONVO_POSTGRESQL_URL is not set."

def test_database_table_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    if not db_url:
        pytest.skip("INCONVO_POSTGRESQL_URL not set, skipping DB setup.")
    
    # Create the orders table if it doesn't exist
    sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        total_amount NUMERIC
    );
    """
    result = subprocess.run(
        ["psql", db_url, "-c", sql],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to set up database table: {result.stderr}"
