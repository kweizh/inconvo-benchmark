import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_cli_available():
    # Verify npm is available which implies we can run npx inconvo
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."

def test_database_tables_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL environment variable is not set."
    
    assert shutil.which("psql") is not None, "psql binary not found in PATH."
    
    sql_commands = \"\"\"
        CREATE TABLE IF NOT EXISTS organizations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            organization_id INTEGER REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            total_amount DECIMAL(10, 2) NOT NULL,
            user_id INTEGER REFERENCES users(id)
        );
        TRUNCATE TABLE orders, users, organizations RESTART IDENTITY CASCADE;
        INSERT INTO organizations (name) VALUES ('Acme Corp'), ('Globex');
        INSERT INTO users (name, organization_id) VALUES ('Alice', 1), ('Bob', 2);
        INSERT INTO orders (total_amount, user_id) VALUES (100.00, 1), (250.00, 2), (150.00, 1);
    \"\"\"
    
    result = subprocess.run(
        ["psql", db_url, "-c", sql_commands],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to execute SQL commands: {result.stderr}"
    
    # Verify tables exist
    result = subprocess.run(
        ["psql", db_url, "-t", "-c", "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to query tables: {result.stderr}"
    
    output = result.stdout
    assert "organizations" in output, "Table 'organizations' was not created."
    assert "users" in output, "Table 'users' was not created."
    assert "orders" in output, "Table 'orders' was not created."
