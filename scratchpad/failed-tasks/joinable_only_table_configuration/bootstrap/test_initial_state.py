import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."

def test_database_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL environment variable is not set."
    
    assert shutil.which("psql") is not None, "psql binary not found in PATH."
    
    # Set up the tables
    setup_sql = """
    DROP TABLE IF EXISTS customer_addresses;
    DROP TABLE IF EXISTS customers;
    
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    
    CREATE TABLE customer_addresses (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        city VARCHAR(255) NOT NULL
    );
    
    INSERT INTO customers (name) VALUES ('Alice'), ('Bob');
    INSERT INTO customer_addresses (customer_id, city) VALUES (1, 'New York'), (2, 'San Francisco');
    """
    
    result = subprocess.run(
        ["psql", db_url, "-c", setup_sql],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to set up database tables: {result.stderr}"
