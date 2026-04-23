import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

def test_inconvo_yaml_exists_and_contains_tables():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"
    
    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "orders" in content, "Expected 'orders' table definition in inconvo.yaml"
    assert "products" in content, "Expected 'products' table definition in inconvo.yaml"

def test_run_index_js():
    # Run the script that interacts with the SDK
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
    # The actual structure depends on the SDK, but we expect some kind of table/data response
    content_str = json.dumps(data).lower()
    assert "table" in content_str or "data" in content_str or "rows" in content_str, \
        f"response.json does not seem to contain table data. Content: {data}"
