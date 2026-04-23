import os
import shutil
import pytest
import subprocess

PROJECT_DIR = "/home/user/inconvo-project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model {yaml_path} does not exist."

def test_initial_sales_table_has_revenue_cost():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "sales" in content, "Expected 'sales' table in initial inconvo.yaml."
    assert "revenue" in content, "Expected 'revenue' field in initial inconvo.yaml."
    assert "cost" in content, "Expected 'cost' field in initial inconvo.yaml."
    assert "gross_margin" not in content, "Expected 'gross_margin' to be absent initially."

def test_database_connection_and_sales_table():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        result = subprocess.run(
            ["psql", db_url, "-c", "SELECT count(*) FROM sales;"],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Failed to query 'sales' table: {result.stderr}"
