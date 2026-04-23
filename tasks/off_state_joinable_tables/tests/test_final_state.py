import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_yaml_file_exists():
    assert os.path.isfile(YAML_FILE), f"Config file {YAML_FILE} does not exist."

def test_table_states_updated():
    # Since inconvo doesn't have a specific CLI command to verify states,
    # we use python to parse the yaml file as Priority 3 fallback.
    # However, we can use a small python script with the standard library
    # to extract the state values. Wait, we can't use pyyaml easily unless we install it.
    # We will use simple string parsing or regex.
    
    with open(YAML_FILE, "r") as f:
        content = f.read()

    # Find the state for each table. This is a bit brittle but works for testing.
    # Let's extract the block for each table
    import re

    # Find customers block
    customers_match = re.search(r'customers:\s*\n\s*state:\s*([A-Za-z]+)', content)
    assert customers_match is not None, "Could not find 'state' for 'customers' table in inconvo.yaml"
    assert customers_match.group(1) == "Joinable", f"Expected customers state to be 'Joinable', got '{customers_match.group(1)}'"

    # Find internal_logs block
    logs_match = re.search(r'internal_logs:\s*\n\s*state:\s*([A-Za-z]+)', content)
    assert logs_match is not None, "Could not find 'state' for 'internal_logs' table in inconvo.yaml"
    assert logs_match.group(1) == "Off", f"Expected internal_logs state to be 'Off', got '{logs_match.group(1)}'"

    # Find orders block
    orders_match = re.search(r'orders:\s*\n\s*state:\s*([A-Za-z]+)', content)
    assert orders_match is not None, "Could not find 'state' for 'orders' table in inconvo.yaml"
    assert orders_match.group(1) == "Queryable", f"Expected orders state to be 'Queryable', got '{orders_match.group(1)}'"