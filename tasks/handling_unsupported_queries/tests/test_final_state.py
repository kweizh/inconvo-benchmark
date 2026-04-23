import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_password_hash_field_is_off():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "password_hash: { state: Off }" in content or "password_hash:\n        state: Off" in content or "password_hash: {state: Off}" in content or "password_hash:\n      state: Off" in content, "Expected state of password_hash to be 'Off' in inconvo.yaml."

def test_internal_logs_table_is_off():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "internal_logs:\n    state: Off" in content or "internal_logs: { state: Off }" in content or "internal_logs: {state: Off}" in content or "internal_logs:\n  state: Off" in content, "Expected state of internal_logs to be 'Off' in inconvo.yaml."
