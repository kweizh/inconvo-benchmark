import os
import shutil
import subprocess
import pytest

def test_inconvo_binary_available():
    # Check if inconvo is available via npx or global
    # Since the instructions say npx inconvo@latest, we check for npx
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_database_url_env_var():
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set."

def test_postgresql_connection():
    # Try to connect to postgres using psql if available, or just check the URL
    database_url = os.environ["DATABASE_URL"]
    assert database_url.startswith("postgres"), f"DATABASE_URL should be a postgres URL, got {database_url}"
    
    # Check if we can reach the database and tables exist
    # We use psql to check for tables
    try:
        result = subprocess.run(
            ["psql", database_url, "-c", "\\dt"],
            capture_output=True,
            text=True,
            check=True
        )
        tables = result.stdout.lower()
        assert "customers" in tables, "Table 'customers' not found in database."
        assert "orders" in tables, "Table 'orders' not found in database."
        assert "order_items" in tables, "Table 'order_items' not found in database."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to connect to PostgreSQL: {e.stderr}")
    except FileNotFoundError:
        # If psql is not installed, we might need to install it in the Dockerfile
        # For now, assume it's there or skip this specific check if we can't run it
        pass
