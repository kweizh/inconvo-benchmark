import os
import subprocess
import json
import yaml
import pytest

PROJECT_DIR = "/home/user/ecommerce-analytics"
CONFIG_FILE = os.path.join(PROJECT_DIR, ".inconvo", "inconvo.yaml")

def test_config_file_exists():
    assert os.path.isfile(CONFIG_FILE), f"Inconvo configuration file not found at {CONFIG_FILE}"

def test_users_table_visibility():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    tables = config.get('tables', {})
    assert 'users' in tables, "Table 'users' not found in inconvo.yaml"
    
    users_config = tables['users']
    assert users_config.get('state') == 'Queryable', f"Expected 'users' table state to be 'Queryable', got {users_config.get('state')}"
    
    fields = users_config.get('fields', {})
    assert fields.get('password_hash', {}).get('state') == 'Off', "Field 'password_hash' in 'users' table should be 'Off'"
    assert fields.get('secret_key', {}).get('state') == 'Off', "Field 'secret_key' in 'users' table should be 'Off'"

def test_orders_table_types():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    tables = config.get('tables', {})
    assert 'orders' in tables, "Table 'orders' not found in inconvo.yaml"
    
    orders_config = tables['orders']
    fields = orders_config.get('fields', {})
    
    assert fields.get('total_amount', {}).get('type') == 'measure', "Field 'total_amount' should have type 'measure'"
    assert fields.get('created_at', {}).get('type') == 'dimension', "Field 'created_at' should have type 'dimension'"

def test_relationships_defined():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    relations = config.get('relations', [])
    assert len(relations) > 0, "No relationships defined in inconvo.yaml"
    
    # Check for a relationship between orders and users
    found = False
    for rel in relations:
        left = rel.get('left', '')
        right = rel.get('right', '')
        if ('orders' in left and 'users' in right) or ('users' in left and 'orders' in right):
            found = True
            break
    
    assert found, "Relationship between 'orders' and 'users' not found in inconvo.yaml"

def test_inconvo_validate():
    """Attempt to run inconvo validate if the CLI supports it."""
    # Based on plan.md, 'inconvo dev' starts a server, but there might be a validate command.
    # We use npx to run it.
    result = subprocess.run(
        ["npx", "inconvo@latest", "validate"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    # If the command doesn't exist, we don't necessarily fail the task, 
    # but if it does, it should pass.
    if result.returncode != 0 and "Unknown command" not in result.stderr:
         # Only fail if it's a validation error, not an 'unknown command' error
         if "error" in result.stderr.lower() or "fail" in result.stderr.lower():
             pytest.fail(f"inconvo validate failed: {result.stderr}")
