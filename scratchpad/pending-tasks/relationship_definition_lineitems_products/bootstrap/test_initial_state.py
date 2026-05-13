import os
import subprocess
import pytest

def test_database_url_env_var():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    assert db_url is not None, "INCONVO_POSTGRESQL_URL environment variable is not set."

def test_database_tables_setup():
    db_url = os.environ.get("INCONVO_POSTGRESQL_URL")
    
    # Setup tables
    setup_sql = """
    DROP TABLE IF EXISTS line_items;
    DROP TABLE IF EXISTS products;
    
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    
    CREATE TABLE line_items (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL
    );
    
    INSERT INTO products (id, name) VALUES 
        (1, 'Laptop'),
        (2, 'Mouse'),
        (3, 'Keyboard');
        
    INSERT INTO line_items (id, product_id, quantity) VALUES 
        (1, 1, 5),
        (2, 2, 20),
        (3, 3, 10),
        (4, 1, 2),
        (5, 2, 5);
    """
    
    try:
        subprocess.run(["psql", db_url, "-c", setup_sql], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to setup database tables: {e.stderr.decode()}")

    # Verify tables exist
    check_sql = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_name IN ('products', 'line_items');
    """
    
    try:
        result = subprocess.run(["psql", db_url, "-t", "-c", check_sql], check=True, capture_output=True, text=True)
        output = result.stdout
        assert "products" in output, "products table was not created."
        assert "line_items" in output, "line_items table was not created."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to verify database tables: {e.stderr.decode()}")
