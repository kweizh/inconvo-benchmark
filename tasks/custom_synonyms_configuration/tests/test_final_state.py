import os
import pytest
import re

PROJECT_DIR = "/home/user/myproject"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_synonyms_configured():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml file {YAML_FILE} does not exist."
    
    with open(YAML_FILE) as f:
        content = f.read()
    
    # Basic string checks
    assert "synonyms" in content, "Expected 'synonyms' property in inconvo.yaml."
    assert "revenue" in content, "Expected 'revenue' synonym in inconvo.yaml."
    assert "income" in content, "Expected 'income' synonym in inconvo.yaml."
    
    # Ensure they are added under total_amount
    # Using regex to find total_amount block and check for synonyms
    # This regex looks for total_amount followed by its configuration block
    match = re.search(r"total_amount:\s*\{([^}]*)\}", content)
    if match:
        block = match.group(1)
        assert "synonyms" in block, "Expected 'synonyms' inside total_amount configuration."
        assert "revenue" in block, "Expected 'revenue' inside total_amount synonyms."
        assert "income" in block, "Expected 'income' inside total_amount synonyms."
    else:
        # If not using inline object syntax, look for block syntax
        match_block = re.search(r"total_amount:(.*?)(?=\n\s*\w+:|\Z)", content, re.DOTALL)
        assert match_block is not None, "Could not find total_amount configuration block."
        block = match_block.group(1)
        assert "synonyms" in block, "Expected 'synonyms' under total_amount configuration."
        assert "revenue" in block, "Expected 'revenue' under total_amount synonyms."
        assert "income" in block, "Expected 'income' under total_amount synonyms."
