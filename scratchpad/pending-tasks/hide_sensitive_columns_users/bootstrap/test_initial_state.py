import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_inconvo_cli_available():
    # Since it's installed via npm, npx inconvo should be available
    assert shutil.which("npx") is not None, "npx is not available in PATH"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml does not exist at {yaml_path}."

def test_environment_variables_set():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY is not set."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID is not set."
    assert "INCONVO_POSTGRESQL_URL" in os.environ, "INCONVO_POSTGRESQL_URL is not set."

def test_database_table_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    if db_url:
        # Create the users table if it doesn't exist
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            password_hash TEXT,
            ssn TEXT
        );
        """
        try:
            subprocess.run(
                ["psql", db_url, "-c", create_table_sql],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to set up database table: {e.stderr}")
