import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_context_filter_added():
    """Priority 3 fallback: basic file content check."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"
    
    with open(yaml_path) as f:
        content = f.read()
        
    assert "context_filter" in content, "Expected 'context_filter' in inconvo.yaml."
    assert "orders.store_id = userContext.store_id" in content, \
        "Expected context_filter to contain 'orders.store_id = userContext.store_id'."
