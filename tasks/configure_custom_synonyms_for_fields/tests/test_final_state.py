import os
import pytest

PROJECT_DIR = "/home/user/myproject"
YAML_PATH = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_synonyms_configured():
    assert os.path.isfile(YAML_PATH), f"Semantic model file {YAML_PATH} does not exist."
    with open(YAML_PATH) as f:
        content = f.read()
    
    # Check if synonyms are configured for dob
    assert "synonyms" in content, "Synonyms not found in inconvo.yaml"
    assert "date of birth" in content, "'date of birth' synonym not found in inconvo.yaml"
    assert "birthday" in content, "'birthday' synonym not found in inconvo.yaml"
