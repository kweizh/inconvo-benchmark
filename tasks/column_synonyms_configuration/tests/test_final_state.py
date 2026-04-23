import os
import pytest

PROJECT_DIR = "/home/user/inconvo-project"
CONFIG_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_synonyms_added():
    with open(CONFIG_FILE) as f:
        content = f.read()
    
    assert "synonyms" in content, "Expected 'synonyms' property to be added to inconvo.yaml."
    assert "revenue" in content, "Expected 'revenue' to be in the synonyms list."
    assert "sales" in content, "Expected 'sales' to be in the synonyms list."
