import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Semantic model {config_path} does not exist."

def test_env_vars_set():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY environment variable is not set."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID environment variable is not set."
    assert "INCONVO_POSTGRESQL_URL" in os.environ, "INCONVO_POSTGRESQL_URL environment variable is not set."

def test_database_table_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    if not db_url:
        pytest.fail("INCONVO_POSTGRESQL_URL is not set.")
    
    # Create the sales table
    sql = """
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        amount NUMERIC NOT NULL,
        created_at TIMESTAMP NOT NULL
    );
    INSERT INTO sales (amount, created_at) VALUES (100.0, '2026-01-15 10:00:00') ON CONFLICT DO NOTHING;
    INSERT INTO sales (amount, created_at) VALUES (150.0, '2026-02-20 11:00:00') ON CONFLICT DO NOTHING;
    """
    
    result = subprocess.run(
        ["psql", db_url, "-c", sql],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to set up database table: {result.stderr}"
