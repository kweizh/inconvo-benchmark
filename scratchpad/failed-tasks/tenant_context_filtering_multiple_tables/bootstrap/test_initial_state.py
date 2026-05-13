import os
import subprocess
import pytest

def test_setup_database():
    """Set up the required database tables and data for the test."""
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url, "INCONVO_POSTGRESQL_URL environment variable is not set."
    
    # Create users table
    create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        tenant_id INTEGER
    );
    TRUNCATE TABLE users;
    INSERT INTO users (name, tenant_id) VALUES ('User 1', 1), ('User 2', 1);
    INSERT INTO users (name, tenant_id) VALUES ('User 3', 2), ('User 4', 2), ('User 5', 2), ('User 6', 2), ('User 7', 2);
    """
    
    # Create orders table
    create_orders = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        amount DECIMAL,
        tenant_id INTEGER
    );
    TRUNCATE TABLE orders;
    INSERT INTO orders (amount, tenant_id) VALUES (10.0, 1), (20.0, 1), (30.0, 1);
    INSERT INTO orders (amount, tenant_id) VALUES (10.0, 2), (20.0, 2), (30.0, 2), (40.0, 2), (50.0, 2), (60.0, 2), (70.0, 2);
    """
    
    result_users = subprocess.run(["psql", db_url, "-c", create_users], capture_output=True, text=True)
    assert result_users.returncode == 0, f"Failed to setup users table: {result_users.stderr}"
    
    result_orders = subprocess.run(["psql", db_url, "-c", create_orders], capture_output=True, text=True)
    assert result_orders.returncode == 0, f"Failed to setup orders table: {result_orders.stderr}"
