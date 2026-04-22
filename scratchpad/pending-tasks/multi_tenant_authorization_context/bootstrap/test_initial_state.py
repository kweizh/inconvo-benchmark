import os
import psycopg2
import subprocess
import json

def test_initial_state():
    # 1. Check DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    assert db_url is not None, "DATABASE_URL environment variable is required"
    
    # 2. Check if database is accessible and has products table
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'products');")
    assert cur.fetchone()[0], "Table 'products' should exist in the database"
    
    # 3. Check if products table has price and cost columns
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'products';")
    columns = [row[0] for row in cur.fetchall()]
    assert "price" in columns, "Column 'price' should exist in 'products' table"
    assert "cost" in columns, "Column 'cost' should exist in 'products' table"
    cur.close()
    conn.close()

    # 4. Check if inconvo CLI is installed
    result = subprocess.run(["npx", "inconvo", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "inconvo CLI should be available"

    # 5. Check if .inconvo directory exists (initialized)
    assert os.path.exists(".inconvo"), ".inconvo directory should exist (project initialized)"

if __name__ == "__main__":
    test_initial_state()
    print("Initial state verified successfully")
