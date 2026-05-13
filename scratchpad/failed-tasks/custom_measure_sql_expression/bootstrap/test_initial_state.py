import os
import shutil
import pytest
import subprocess
import urllib.parse

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_database_url_provided():
    assert "INCONVO_POSTGRESQL_URL" in os.environ, "INCONVO_POSTGRESQL_URL environment variable is missing."

def test_setup_database_table():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    if not db_url:
        pytest.skip("INCONVO_POSTGRESQL_URL not set")
    
    try:
        import psycopg2
    except ImportError:
        pytest.skip("psycopg2 not installed")

    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()

    # Create the orders table and insert some test data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            status VARCHAR(50),
            amount NUMERIC
        );
        TRUNCATE TABLE orders;
        INSERT INTO orders (status, amount) VALUES ('completed', 100);
        INSERT INTO orders (status, amount) VALUES ('pending', 50);
        INSERT INTO orders (status, amount) VALUES ('completed', 200);
    """)
    cur.close()
    conn.close()
