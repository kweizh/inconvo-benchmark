import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-api-task"
LOG_FILE = "/home/user/inconvo-api-task/output.log"

def test_output_log_exists():
    assert os.path.isfile(LOG_FILE), f"Output log file {LOG_FILE} does not exist."

def test_output_log_content():
    with open(LOG_FILE, "r") as f:
        content = f.read()
    
    assert "organisation_id" in content or "organisationId" in content, "Output should reflect context with organisation_id."
    # The SDK response usually contains a 'message' or 'table' object
    assert "message" in content.lower() or "table" in content.lower() or "chart" in content.lower(), \
        f"Output log does not seem to contain a structured Inconvo response: {content}"

def test_index_file_exists():
    # Check for index.ts or index.js
    ts_file = os.path.join(PROJECT_DIR, "index.ts")
    js_file = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(ts_file) or os.path.isfile(js_file), "Neither index.ts nor index.js found in project directory."

def test_package_json_dependencies():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), "package.json not found."
    with open(package_json_path, "r") as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@inconvoai/node" in deps, "@inconvoai/node dependency missing in package.json."

def test_inconvo_cli_initialized():
    # Check for .inconvo directory or inconvo.yaml
    inconvo_dir = os.path.join(PROJECT_DIR, ".inconvo")
    inconvo_yaml = os.path.join(PROJECT_DIR, "inconvo.yaml")
    # npx inconvo init creates a project structure
    assert os.path.isdir(inconvo_dir) or os.path.isfile(inconvo_yaml), "Inconvo project does not appear to be initialized."
