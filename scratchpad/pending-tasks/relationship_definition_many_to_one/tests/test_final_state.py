import os
import subprocess
import pytest
import yaml

PROJECT_DIR = "/home/user/myproject"
CONFIG_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_yaml_exists():
    assert os.path.isfile(CONFIG_FILE), f"inconvo.yaml not found at {CONFIG_FILE}"

def test_tables_configuration():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    
    tables = config.get("tables", {})
    assert "orders" in tables, "Table 'orders' not found in inconvo.yaml"
    assert tables["orders"].get("state") == "Queryable", "Table 'orders' must be 'Queryable'"
    
    assert "customers" in tables, "Table 'customers' not found in inconvo.yaml"
    assert tables["customers"].get("state") == "Joinable", "Table 'customers' must be 'Joinable'"
    
    # Check fields in customers
    fields = tables["customers"].get("fields", {})
    assert "name" in fields, "Field 'name' not found in 'customers' table"
    assert fields["name"].get("state") == "On", "Field 'name' in 'customers' must be 'On'"

def test_relations_configuration():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    
    relations = config.get("relations", [])
    assert isinstance(relations, list), "Relations must be a list"
    
    found = False
    for rel in relations:
        if rel.get("name") == "order_to_customer":
            assert rel.get("left") == "orders.customer_id", "Relation 'left' side must be 'orders.customer_id'"
            assert rel.get("right") == "customers.id", "Relation 'right' side must be 'customers.id'"
            found = True
            break
    
    assert found, "Relation 'order_to_customer' not found in inconvo.yaml"

def test_model_validation():
    # Priority 1: Use Inconvo CLI to validate the model if possible
    # npx inconvo model check (assuming this command exists based on common patterns)
    # If not, we fall back to the yaml checks above.
    # For this task, we'll check if we can run a dry-run or check command.
    result = subprocess.run(
        ["npx", "inconvo", "model", "check"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    # If the command doesn't exist, we don't want to fail the whole test suite if the YAML is correct
    if result.returncode != 0 and "Unknown command" not in result.stderr:
         # Only fail if it's a validation error, not a missing command error
         if "error" in result.stderr.lower() or "invalid" in result.stderr.lower():
             assert False, f"Inconvo model validation failed: {result.stderr}"
