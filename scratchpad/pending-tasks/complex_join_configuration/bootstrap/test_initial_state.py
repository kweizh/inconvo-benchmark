import os
import shutil
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = "/home/user/inconvo-project"

def test_inconvo_cli_available():
    # The CLI is often used via npx, but we want to ensure it's installable or available
    # For Harbor, we'll likely have it installed globally or available via npx
    # We'll check if npx is available at least
    assert shutil.which("npx") is not None, "npx is not available in PATH"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist"

def test_database_url_env_var():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set"

def test_initial_database_connection():
    # Verify we can connect to the database
    # Since we're using PostgreSQL, we can use psql if available or just assume it's there if DATABASE_URL is set
    # But a better way is to check if we can run a simple query
    try:
        subprocess.run(["psql", os.environ["DATABASE_URL"], "-c", "SELECT 1"], check=True, capture_output=True)
    except Exception as e:
        pytest.fail(f"Could not connect to database using DATABASE_URL: {e}")

def test_required_tables_exist():
    # Check if employees and departments tables exist in the database
    db_url = os.environ["DATABASE_URL"]
    
    # Check employees table
    res = subprocess.run(["psql", db_url, "-t", "-c", "SELECT count(*) FROM information_schema.tables WHERE table_name = 'employees'"], capture_output=True, text=True)
    assert res.stdout.strip() == "1", "Table 'employees' does not exist in the database"
    
    # Check departments table
    res = subprocess.run(["psql", db_url, "-t", "-c", "SELECT count(*) FROM information_schema.tables WHERE table_name = 'departments'"], capture_output=True, text=True)
    assert res.stdout.strip() == "1", "Table 'departments' does not exist in the database"

def test_no_foreign_key_constraint():
    # The task specifically says NOT to add FK constraints to the DB
    # We should verify that it doesn't exist initially (or at least that we're testing the semantic layer)
    db_url = os.environ["DATABASE_URL"]
    query = """
    SELECT count(*)
    FROM information_schema.table_constraints 
    WHERE constraint_type = 'FOREIGN KEY' 
    AND table_name = 'employees' 
    AND constraint_name LIKE '%department%';
    """
    res = subprocess.run(["psql", db_url, "-t", "-c", query], capture_output=True, text=True)
    assert res.stdout.strip() == "0", "A foreign key constraint already exists on employees table, it should be handled in the semantic layer instead."
