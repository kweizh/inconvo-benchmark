import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"

def test_computed_column_in_semantic_model():
    """Priority 1: Use Inconvo CLI to verify the model state."""
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    assert agent_id, "INCONVO_AGENT_ID is not set."
    
    # Run model pull with JSON output
    result = subprocess.run(
        ["npx", "inconvo", "model", "pull", "--agent", agent_id, "--json"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'inconvo model pull' failed: {result.stderr}"
    
    try:
        model_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON output from model pull: {result.stdout}")
        
    # The output structure might vary, but typically it should contain tables -> orders -> computed (or fields)
    # Since we don't know the exact JSON structure of inconvo model pull, we can do a robust search
    # Or we can check if the file .inconvo/inconvo.yaml contains the computed column.
    
    # Let's also check the yaml file directly as a fallback if JSON parsing is tricky
    yaml_path = os.path.join(PROJECT_DIR, ".inconvo", "inconvo.yaml")
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            yaml_content = f.read()
            assert "average_order_value" in yaml_content, "Computed column 'average_order_value' not found in inconvo.yaml."
            assert "sum(total_amount)/count(id)" in yaml_content.replace(" ", ""), "Expression 'sum(total_amount)/count(id)' not found in inconvo.yaml."
    else:
        # Fallback to checking the JSON string dump
        json_str = json.dumps(model_data).replace(" ", "")
        assert "average_order_value" in json_str, "Computed column 'average_order_value' not found in the pulled model."
        assert "sum(total_amount)/count(id)" in json_str or "sum(total_amount) / count(id)".replace(" ", "") in json_str, "Expression 'sum(total_amount)/count(id)' not found in the pulled model."
