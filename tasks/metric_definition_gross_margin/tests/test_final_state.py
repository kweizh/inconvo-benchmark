import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"

def test_gross_margin_defined():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "gross_margin" in content, "Expected 'gross_margin' to be defined in inconvo.yaml."

def test_gross_margin_expression():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "revenue - cost" in content, "Expected 'revenue - cost' expression in inconvo.yaml."

def test_gross_margin_unit():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "USD" in content, "Expected 'USD' unit in inconvo.yaml."

def test_database_connection_and_sales_table():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        result = subprocess.run(
            ["psql", db_url, "-c", "SELECT count(*) FROM sales;"],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Failed to query 'sales' table: {result.stderr}"
