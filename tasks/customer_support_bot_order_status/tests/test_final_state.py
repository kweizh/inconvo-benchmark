import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-bot"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

def test_inconvo_yaml_exists_and_contains_orders_table():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

    with open(yaml_path, "r") as f:
        content = f.read()

    assert "orders" in content, "Expected 'orders' table definition in inconvo.yaml"
    assert "status" in content, "Expected 'status' field in inconvo.yaml"
    assert "id" in content, "Expected 'id' field in inconvo.yaml"

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

    if isinstance(data, dict):
        assert data.get("error") is not True, f"output.json indicates an error: {data}"

    # Check if it contains some data structure
    content_str = json.dumps(data).lower()
    assert "table" in content_str or "data" in content_str or "rows" in content_str or "text" in content_str or "status" in content_str, \
        f"response.json does not seem to contain expected query results. Content: {data}"