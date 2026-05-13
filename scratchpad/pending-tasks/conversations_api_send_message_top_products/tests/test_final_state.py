import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

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
    # Looking for some structure indicating a response from the API
    assert "data" in content_str or "table" in content_str or "text" in content_str or "id" in content_str, \
        f"response.json does not seem to contain expected API response data. Content: {data}"
