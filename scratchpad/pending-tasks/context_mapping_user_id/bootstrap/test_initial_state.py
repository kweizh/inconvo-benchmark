import os
import psycopg2
import pytest

def test_database_connection():
    db_url = os.getenv("DATABASE_URL")
    assert db_url is not None, "DATABASE_URL environment variable is required"
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Check if sales table exists
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sales');")
    assert cur.fetchone()[0], "Table 'sales' should exist"
    
    # Check if organisation_id column exists in sales table
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'sales' AND column_name = 'organisation_id';")
    assert cur.fetchone() is not None, "Column 'organisation_id' should exist in table 'sales'"
    
    cur.close()
    conn.close()

def test_inconvo_installed():
    import subprocess
    result = subprocess.run(["inconvo", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "inconvo CLI should be installed"

def test_initial_inconvo_yaml():
    assert os.path.exists("inconvo.yaml"), "inconvo.yaml should exist"
    with open("inconvo.yaml", "r") as f:
        content = f.read()
        assert "sales:" in content, "sales table should be defined in inconvo.yaml"
        assert "contextFilters:" not in content or "organisation_id" not in content, "contextFilters for organisation_id should not be set yet"
