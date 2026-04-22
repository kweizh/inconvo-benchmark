import os
import subprocess
import json
import pytest
import yaml
from pathlib import Path

PROJECT_DIR = "/home/user/inconvo-project"

def test_relation_exists_in_config():
    """Priority 3: Check the semantic model configuration files."""
    inconvo_dir = Path(PROJECT_DIR) / ".inconvo"
    assert inconvo_dir.is_dir(), ".inconvo directory not found"
    
    # Inconvo typically stores relations in a relations.yaml or within table yamls
    # We'll search for 'employee_to_department' in all yaml files in .inconvo
    found_relation = False
    for yaml_file in inconvo_dir.rglob("*.yaml"):
        with open(yaml_file, 'r') as f:
            try:
                config = yaml.safe_load(f)
                if not config:
                    continue
                
                # Check if it's a relations list
                relations = []
                if isinstance(config, list):
                    relations = config
                elif isinstance(config, dict) and 'relations' in config:
                    relations = config['relations']
                
                for rel in relations:
                    if rel.get('name') == 'employee_to_department':
                        assert rel.get('left') in ['employees.department_id', 'departments.id'], f"Incorrect left side for relation: {rel.get('left')}"
                        assert rel.get('right') in ['employees.department_id', 'departments.id'], f"Incorrect right side for relation: {rel.get('right')}"
                        # Check type if specified, though Inconvo might infer it or use a specific key
                        # The prompt asked for many-to-one
                        if 'type' in rel:
                            assert rel['type'] in ['many-to-one', 'many_to_one'], f"Incorrect relation type: {rel['type']}"
                        found_relation = True
                        break
            except yaml.YAMLError:
                continue
        if found_relation:
            break
            
    assert found_relation, "Relation 'employee_to_department' not found in .inconvo configuration"

def test_table_states_configured():
    """Verify table states are set correctly."""
    inconvo_dir = Path(PROJECT_DIR) / ".inconvo"
    
    employees_queryable = False
    departments_joinable = False
    
    for yaml_file in inconvo_dir.rglob("*.yaml"):
        with open(yaml_file, 'r') as f:
            try:
                config = yaml.safe_load(f)
                if not isinstance(config, dict):
                    continue
                
                tables = config.get('tables', {})
                if 'employees' in tables:
                    if tables['employees'].get('state') == 'Queryable':
                        employees_queryable = True
                if 'departments' in tables:
                    if tables['departments'].get('state') in ['Joinable', 'Queryable']:
                        departments_joinable = True
            except yaml.YAMLError:
                continue
                
    assert employees_queryable, "Table 'employees' is not set to 'Queryable'"
    assert departments_joinable, "Table 'departments' is not set to 'Joinable' or 'Queryable'"

def test_cli_verification():
    """Priority 1: Use Inconvo CLI to verify the model if possible."""
    # Note: This requires the CLI to be able to run without a real backend in the test env,
    # or for the test env to have the mock backend running.
    # We'll try to run 'inconvo model pull --dry-run' to see if it validates the local config.
    result = subprocess.run(
        ["npx", "inconvo", "model", "pull", "--dry-run"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    # If the config is invalid, this might fail.
    assert result.returncode == 0, f"Inconvo CLI failed to validate the model: {result.stderr}"
