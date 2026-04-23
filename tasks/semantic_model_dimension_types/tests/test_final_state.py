import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_total_amount_is_measure():
    """Priority 3 fallback: basic file check for total_amount type."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "type: measure" in content, "Expected 'type: measure' for total_amount in inconvo.yaml."

def test_created_at_is_dimension():
    """Priority 3 fallback: basic file check for created_at type."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "type: dimension" in content, "Expected 'type: dimension' for created_at in inconvo.yaml."

def test_fields_state_is_on():
    """Priority 3 fallback: basic file check for state."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
        
    assert "state: On" in content, "Expected fields to have 'state: On' in inconvo.yaml."
