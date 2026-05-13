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
    
    # Create the yearly_metrics table
    sql = """
    CREATE TABLE IF NOT EXISTS yearly_metrics (
        id SERIAL PRIMARY KEY,
        year INTEGER NOT NULL,
        revenue_current NUMERIC NOT NULL,
        revenue_previous NUMERIC NOT NULL
    );
    INSERT INTO yearly_metrics (year, revenue_current, revenue_previous) VALUES (2025, 1200000.0, 1000000.0) ON CONFLICT DO NOTHING;
    INSERT INTO yearly_metrics (year, revenue_current, revenue_previous) VALUES (2026, 1500000.0, 1200000.0) ON CONFLICT DO NOTHING;
    """
    
    result = subprocess.run(
        ["psql", db_url, "-c", sql],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to set up database table: {result.stderr}"
