import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_gross_margin_field_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    assert "gross_margin:" in content, "Expected 'gross_margin' field mapping in inconvo.yaml."

def test_gross_margin_state_and_type():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    # We expect 'gross_margin' to have state: On and type: measure
    assert "state: On" in content or "state: \"On\"" in content or "state: 'On'" in content, "Expected state: On for gross_margin."
    assert "type: measure" in content or "type: \"measure\"" in content or "type: 'measure'" in content, "Expected type: measure for gross_margin."

def test_gross_margin_calculation():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "revenue - cost" in content, "Expected the calculation 'revenue - cost' to be present for gross_margin."
