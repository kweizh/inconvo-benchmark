import os
import shutil
import subprocess
import pytest
import psycopg2
from urllib.parse import urlparse

PROJECT_DIR = "/home/user/inconvo-project"

def setup_database():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    if not db_url:
        pytest.skip("INCONVO_POSTGRESQL_URL is not set")
    
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
        );
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT,
            amount DECIMAL
        );
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            order_id INT,
            user_id INT,
            amount DECIMAL
        );
    """)
    cursor.close()
    conn.close()

def test_setup_and_verify_database():
    setup_database()
    
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    if not db_url:
        return
        
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cursor.fetchall()]
    assert "users" in tables, "Table 'users' was not created."
    assert "orders" in tables, "Table 'orders' was not created."
    assert "payments" in tables, "Table 'payments' was not created."
    cursor.close()
    conn.close()

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_binary_available():
    assert shutil.which("inconvo") is not None, "inconvo binary not found in PATH."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."

def test_env_file_exists():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f"Environment file {env_path} does not exist."
