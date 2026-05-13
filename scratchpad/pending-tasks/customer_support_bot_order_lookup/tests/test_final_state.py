import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_script_execution():
    """Run the script and verify it succeeds."""
    script_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Verify package.json exists
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"package.json not found at {package_json}"

    # Run npm install just in case
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, capture_output=True)

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed: {result.stderr}\n{result.stdout}"

def test_output_log():
    """Verify the output log contains the correct status."""
    log_path = os.path.join(PROJECT_DIR, "output.log")
    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().lower()
    
    assert "shipped" in content, f"Expected 'shipped' in {log_path}, got: {content}"
