import os
import subprocess
import pytest
import json

PROJECT_DIR = "/home/user/inconvo-app"

def test_inconvo_yaml_relations():
    """Priority 3 fallback: basic file check for yaml content."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"
    
    with open(yaml_path, "r") as f:
        content = f.read()
        
    # Check for order_to_buyer
    assert "order_to_buyer" in content, "Expected 'order_to_buyer' in inconvo.yaml"
    assert "orders.buyer_id" in content, "Expected 'orders.buyer_id' in inconvo.yaml"
    
    # Check for order_to_seller
    assert "order_to_seller" in content, "Expected 'order_to_seller' in inconvo.yaml"
    assert "orders.seller_id" in content, "Expected 'orders.seller_id' in inconvo.yaml"
    
    # Check for right side
    assert "users.id" in content, "Expected 'users.id' in inconvo.yaml"

def test_index_js_execution():
    """Priority 1: Run the script to verify it executes without error."""
    script_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(script_path), f"index.js not found at {script_path}"
    
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"
