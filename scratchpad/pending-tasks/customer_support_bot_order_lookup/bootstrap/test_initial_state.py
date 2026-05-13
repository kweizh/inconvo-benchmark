import os
import shutil
import subprocess
import pytest

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_env_vars():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY not set"
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID not set"
    assert "INCONVO_POSTGRESQL_URL" in os.environ, "INCONVO_POSTGRESQL_URL not set"

def test_db_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL not set"
    assert shutil.which("psql") is not None, "psql binary not found in PATH."
    
    sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        status VARCHAR(50),
        customer_id INT
    );
    TRUNCATE TABLE orders;
    INSERT INTO orders (id, status, customer_id) VALUES (1, 'shipped', 1);
    """
    
    result = subprocess.run(["psql", db_url, "-c", sql], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to set up database: {result.stderr}"
