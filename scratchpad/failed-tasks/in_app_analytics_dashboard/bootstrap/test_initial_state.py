import os
import shutil
import pytest
import subprocess

def test_node_and_npm_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_database_url_environment_variable_set():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."

def test_database_schema_initialized():
    db_url = os.environ.get("DATABASE_URL")
    assert db_url is not None, "DATABASE_URL environment variable is not set."
    
    # Initialize the schema
    sql = """
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        store_id INTEGER NOT NULL,
        revenue DECIMAL(10, 2) NOT NULL,
        cost DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    result = subprocess.run(
        ["psql", db_url, "-c", sql],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to initialize database schema: {result.stderr}"

def test_project_directory_exists():
    assert os.path.isdir("/home/user/myproject"), "/home/user/myproject directory does not exist."
