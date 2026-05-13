import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_cli_available():
    assert shutil.which("npx") is not None, "npx is not available in PATH."

def test_database_schema_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL environment variable is not set."
    
    assert shutil.which("psql") is not None, "psql is not available in PATH."
    
    # Create tables
    setup_sql = \"\"\"
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            total_amount DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    \"\"\"
    
    result = subprocess.run(
        ["psql", db_url, "-c", setup_sql],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to set up database schema: {result.stderr}"
    
    # Verify tables exist
    check_sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    result = subprocess.run(
        ["psql", db_url, "-t", "-c", check_sql],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to check tables: {result.stderr}"
    
    tables = result.stdout.strip().split()
    assert "users" in tables, "Table 'users' does not exist."
    assert "orders" in tables, "Table 'orders' does not exist."
