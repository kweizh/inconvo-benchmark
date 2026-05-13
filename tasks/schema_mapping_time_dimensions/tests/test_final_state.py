import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

def test_inconvo_yaml_contains_time_dimension():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

    with open(yaml_path, "r") as f:
        content = f.read()

    # Priority 3 check for the file content
    assert "type: dimension" in content or "type: 'dimension'" in content or 'type: "dimension"' in content, \
        "Expected 'type: dimension' for created_at in inconvo.yaml"
    assert "state: On" in content or "state: 'On'" in content or 'state: "On"' in content, \
        "Expected 'state: On' for created_at in inconvo.yaml"

def test_run_index_js():
    # Priority 1: Run the script to verify the configuration
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"

def test_response_json_exists_and_valid():
    assert os.path.isfile(RESPONSE_FILE), f"response.json not found at {RESPONSE_FILE}"

    with open(RESPONSE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("response.json is not valid JSON")

    # Check if it contains some table structure
    content_str = json.dumps(data).lower()
    assert "table" in content_str or "data" in content_str or "rows" in content_str, \
        f"response.json does not seem to contain table data. Content: {data}"
