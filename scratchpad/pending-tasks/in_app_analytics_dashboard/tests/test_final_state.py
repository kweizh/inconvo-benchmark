import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
YAML_PATH = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_yaml_exists():
    assert os.path.isfile(YAML_PATH), f"inconvo.yaml not found at {YAML_PATH}"

def test_tables_defined():
    with open(YAML_PATH, "r") as f:
        content = f.read()
    assert "orders:" in content, "orders table is not defined in inconvo.yaml"
    assert "customers:" in content, "customers table is not defined in inconvo.yaml"
    assert "products:" in content, "products table is not defined in inconvo.yaml"

def test_relationship_defined():
    with open(YAML_PATH, "r") as f:
        content = f.read()
    assert "order_to_customer" in content, "order_to_customer relationship is not defined"
    assert "orders.customer_id" in content, "orders.customer_id is not in the relationship"
    assert "customers.id" in content, "customers.id is not in the relationship"

def test_gross_margin_measure_defined():
    with open(YAML_PATH, "r") as f:
        content = f.read()
    assert "gross_margin" in content, "gross_margin measure is not defined"

def test_context_filter_defined():
    with open(YAML_PATH, "r") as f:
        content = f.read()
    assert "store_id" in content, "store_id context filter is not defined"

def test_inconvo_validate_cli():
    result = subprocess.run(
        ["npx", "--yes", "inconvo@latest", "validate"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    # npx might prompt for installation, but since we used npx inconvo@latest init, it should be cached or we can bypass prompt with --yes
    # To be safe, we just check if it runs. If inconvo validate fails, it will have a non-zero exit code.
    # Note: If the database is not actually running with the correct schema, validate might fail.
    # The prompt says: "Make sure to use a real PostgreSQL database (not mocked) and require DATABASE_URL in the environment to setup the env and do the evaluations."
    # Since we don't have a real DB schema initialized in this test, we just check if the model is structurally valid, or if validate command exists.
    # Actually, if DATABASE_URL is required, we should assume the DB is running and has the schema.
    # If the user sets it up correctly, it should exit 0.
    assert result.returncode == 0, f"inconvo validate failed: {result.stderr}\n{result.stdout}"
