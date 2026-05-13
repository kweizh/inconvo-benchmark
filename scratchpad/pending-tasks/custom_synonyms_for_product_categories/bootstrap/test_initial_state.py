import os
import subprocess
import psycopg2
import pytest

def test_database_table_exists():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL environment variable is not set."
    
    # Create the products table if it doesn't exist
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            product_category VARCHAR(255) NOT NULL
        );
    """)
    
    # Verify the table exists
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'products' AND column_name = 'product_category';
    """)
    result = cursor.fetchone()
    assert result is not None, "products table with product_category column does not exist."
    
    cursor.close()
    conn.close()

def test_inconvo_cli_installed():
    assert subprocess.run(["npx", "inconvo", "--version"], capture_output=True).returncode == 0, "inconvo CLI is not installed or accessible via npx."
