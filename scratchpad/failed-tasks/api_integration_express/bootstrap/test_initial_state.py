import os
import psycopg2
import pytest

def test_database_connection():
    db_url = os.getenv("DATABASE_URL")
    assert db_url is not None, "DATABASE_URL environment variable is missing"
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    assert result[0] == 1
    cur.close()
    conn.close()

def test_schema_exists():
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Check if necessary tables exist (provided in setup)
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [row[0] for row in cur.fetchall()]
    assert "orders" in tables
    assert "products" in tables
    assert "stores" in tables
    
    cur.close()
    conn.close()

def test_inconvo_cli_installed():
    import subprocess
    result = subprocess.run(["npx", "inconvo@latest", "--version"], capture_output=True, text=True)
    assert result.returncode == 0 or "inconvo" in result.stdout.lower()
