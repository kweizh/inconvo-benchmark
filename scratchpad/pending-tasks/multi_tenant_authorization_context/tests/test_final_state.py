import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_yaml_exists_and_contains_orders():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"

    with open(YAML_FILE, "r") as f:
        content = f.read()

    assert "orders" in content.lower(), "Expected 'orders' table definition in inconvo.yaml"

def test_run_index_js():
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

    content_str = json.dumps(data).lower()
    assert len(content_str) > 0, "response.json is empty"
