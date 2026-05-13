import os
import shutil
import subprocess
import pytest

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_psql_available():
    assert shutil.which("psql") is not None, "psql binary not found in PATH."

def test_database_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL is not set."
    
    # Create tables
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        total_amount DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP NOT NULL,
        organisation_id INTEGER
    );
    
    -- Insert some dummy data for the revenue trend chart
    INSERT INTO customers (name) VALUES ('Test Customer') ON CONFLICT DO NOTHING;
    INSERT INTO orders (customer_id, total_amount, created_at, organisation_id) VALUES 
        (1, 1000.00, '2026-01-15 10:00:00', 1),
        (1, 1500.00, '2026-02-20 10:00:00', 1),
        (1, 2000.00, '2026-03-25 10:00:00', 1),
        (1, 2500.00, '2026-04-10 10:00:00', 1)
    ;
    """
    
    result = subprocess.run(
        ["psql", db_url, "-c", create_tables_sql],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to setup database: {result.stderr}"

def test_env_vars():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY is not set."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID is not set."
