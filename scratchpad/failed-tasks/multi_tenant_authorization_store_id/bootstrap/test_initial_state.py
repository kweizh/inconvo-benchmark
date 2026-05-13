import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_cli_available():
    assert shutil.which("inconvo") is not None or shutil.which("npx") is not None, "npx or inconvo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_database_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL environment variable is missing."

    # Setup the database table and insert data
    sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        store_id INTEGER NOT NULL,
        total_amount DECIMAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    TRUNCATE TABLE orders;
    INSERT INTO orders (store_id, total_amount) VALUES (1, 100.00);
    INSERT INTO orders (store_id, total_amount) VALUES (1, 150.00);
    INSERT INTO orders (store_id, total_amount) VALUES (1, 200.00);
    INSERT INTO orders (store_id, total_amount) VALUES (2, 50.00);
    INSERT INTO orders (store_id, total_amount) VALUES (2, 75.00);
    INSERT INTO orders (store_id, total_amount) VALUES (2, 125.00);
    INSERT INTO orders (store_id, total_amount) VALUES (2, 300.00);
    INSERT INTO orders (store_id, total_amount) VALUES (2, 400.00);
    """
    
    # Using psql to execute the SQL
    result = subprocess.run(
        ["psql", db_url, "-c", sql],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to setup database: {result.stderr}"
