import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INDEX_FILE = os.path.join(PROJECT_DIR, "index.js")
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

def test_index_js_exists():
    assert os.path.isfile(INDEX_FILE), f"index.js not found at {INDEX_FILE}"

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

    # Check if it contains some data structure.
    # The actual structure depends on the SDK, but we expect some kind of response.
    assert isinstance(data, dict) or isinstance(data, list) or isinstance(data, str), \
        f"response.json does not seem to contain valid response data. Content: {data}"
