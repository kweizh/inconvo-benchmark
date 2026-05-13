import os
import subprocess
import pytest
import shutil

PROJECT_DIR = "/home/user/inconvo-project"

def test_computed_column_in_semantic_model():
    """Priority 1: Use Inconvo CLI to pull the model and verify the computed column."""
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    assert agent_id is not None, "INCONVO_AGENT_ID environment variable is not set."
    
    # Pull the latest model
    result = subprocess.run(
        ["npx", "inconvo", "model", "pull", "--agent", agent_id],
        cwd=PROJECT_DIR,
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"'inconvo model pull' failed: {result.stderr}"
    
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), "inconvo.yaml not found after pull."
    
    with open(yaml_path, 'r') as f:
        content = f.read()
        
    # Verify the computed column exists in the users table
    # We'll do a simple string matching since we can't use PyYAML
    assert "customer_lifetime_value:" in content, "Field 'customer_lifetime_value' not found in inconvo.yaml."
    
    # Check if the expression contains SUM and total_amount
    content_lower = content.lower()
    assert "sum" in content_lower and "total_amount" in content_lower, \
        "Expected expression to calculate sum of total_amount."
