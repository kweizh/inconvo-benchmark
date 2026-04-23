import os
import psycopg2
import pytest

def test_database_connection():
    # Ensure DATABASE_URL is set
    db_url = os.environ.get("DATABASE_URL")
    assert db_url is not None, "DATABASE_URL environment variable is not set"
    
    # Test connection
    conn = psycopg2.connect(db_url)
    assert conn is not None
    conn.close()

def test_tables_exist():
    db_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Check if orders table exists
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'orders');")
    assert cur.fetchone()[0], "Table 'orders' does not exist"
    
    # Check if addresses table exists
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'addresses');")
    assert cur.fetchone()[0], "Table 'addresses' does not exist"
    
    # Check columns in orders
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'orders';")
    columns = [row[0] for row in cur.fetchall()]
    assert 'shipping_address_id' in columns, "Column 'shipping_address_id' missing in 'orders'"
    assert 'billing_address_id' in columns, "Column 'billing_address_id' missing in 'orders'"
    
    cur.close()
    conn.close()

def test_project_dir_exists():
    assert os.path.exists("/home/user"), "/home/user directory should exist"
