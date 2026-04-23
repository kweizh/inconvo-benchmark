import os
import pytest

PROJECT_DIR = "/home/user/project"

def test_context_filters_in_orders_table():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."
    
    with open(yaml_path) as f:
        content = f.read()
    
    assert "store_id" in content, "Expected 'store_id' to be referenced in inconvo.yaml for the context filter."
    assert "region_id" in content, "Expected 'region_id' to be referenced in inconvo.yaml for the context filter."
    assert "context" in content, "Expected 'context' to be referenced in inconvo.yaml."
