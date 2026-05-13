import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "chart_response.json")

def test_run_index_js():
    """Priority 1: Run the script to verify it works and generates the output."""
    # Ensure dependencies are installed just in case
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, capture_output=True)
    
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    # Write to output.log as required by the task
    with open(os.path.join(PROJECT_DIR, "output.log"), "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)
        
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"

def test_response_json_exists_and_valid():
    """Priority 3: Verify the output file exists and has valid chart data."""
    assert os.path.isfile(RESPONSE_FILE), f"chart_response.json not found at {RESPONSE_FILE}"

    with open(RESPONSE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("chart_response.json is not valid JSON")

    # Check if it contains some chart structure
    content_str = json.dumps(data).lower()
    assert "chart" in content_str or "data" in content_str or "type" in content_str or "bar" in content_str, \
        f"chart_response.json does not seem to contain chart data. Content: {data}"