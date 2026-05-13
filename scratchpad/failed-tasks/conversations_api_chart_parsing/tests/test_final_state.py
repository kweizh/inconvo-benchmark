import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"

def test_script_execution():
    """Run the user's script and verify it returns a valid Vega-Lite chart schema."""
    script_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    
    # Run the script
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"
    
    output = result.stdout.strip()
    assert output, "Script produced no output."
    
    # Parse JSON
    try:
        chart_data = json.loads(output)
    except json.JSONDecodeError as e:
        pytest.fail(f"Output is not valid JSON. Error: {e}\nOutput: {output}")
        
    # Verify Vega-Lite schema
    schema = chart_data.get("$schema")
    assert schema == "https://vega.github.io/schema/vega-lite/v5.json", \
        f"Expected Vega-Lite schema, got: {schema}"
        
    # Verify data values
    data = chart_data.get("data", {})
    values = data.get("values")
    assert isinstance(values, list) and len(values) > 0, \
        "Expected chart data to contain a list of values."
